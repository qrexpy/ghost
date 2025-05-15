import os
import shutil
import sys
import ctypes
import subprocess

from utils.files import resource_path

# FONTS = [
#     resource_path("data/fonts/Roboto-Regular.ttf"),
#     resource_path("data/fonts/Roboto-Bold.ttf"),
#     resource_path("data/fonts/Roboto-LightItalic.ttf")
# ]

FONTS = [resource_path(f"data/fonts/{path}") for path in os.listdir(resource_path("data/fonts")) if path.endswith(".ttf")
         and not path.startswith(".")
         and not path.startswith("_")
         and not path.startswith("~")
         and not path.startswith("#")
         and not path.startswith("._")]

SYSTEM_FONT_DIR = {
    "darwin": os.path.expanduser("~/Library/Fonts"),
    "win32": os.path.expandvars("%WINDIR%\\Fonts"),
    "linux": "/usr/share/fonts",
}

def get_fonts():
    font_files = [os.path.basename(font) for font in FONTS]
    
    # sort them by first letter
    font_files.sort()
    
    return font_files

def already_installed(font_path):
    """
    Checks if the font is already installed on the system.
    """
    font_name = os.path.basename(font_path)
    system_platform = sys.platform

    # Check if the font exists in the system font directories
    if system_platform == "darwin":
        font_dir = os.path.expanduser("~/Library/Fonts")
    elif system_platform == "win32":
        font_dir = os.path.expandvars("%WINDIR%\\Fonts")
    elif system_platform == "linux":
        font_dir = "/usr/share/fonts"
    else:
        return False  # Unsupported platform
    
    # Check if the font file is present in the system font directory
    font_installed = os.path.join(font_dir, font_name)
    return os.path.exists(font_installed)

def check_fonts():
    installed = []
    
    for font in FONTS:
        if already_installed(font):
            installed.append(font)
            
    return len(installed) == len(FONTS)

def load_custom_font(font_path):
    """
    Load the font into the system if not already installed.
    """
    if already_installed(font_path):
        print(f"Font already installed: {font_path}")
        return
    
    font_name = os.path.basename(font_path)
    system_platform = sys.platform

    # Define where to install the font based on the platform
    if system_platform == "darwin":
        install_dir = os.path.expanduser("~/Library/Fonts")
    elif system_platform == "win32":
        install_dir = os.path.expandvars("%WINDIR%\\Fonts")
        shutil.copy(font_path, os.path.join(install_dir, font_name))
        ctypes.windll.gdi32.AddFontResourceEx(os.path.join(install_dir, font_name), 0, 0)
        print(f"Font installed: {font_path}")
        return
    elif system_platform == "linux":
        install_dir = "/usr/share/fonts"
    else:
        print(f"Unsupported platform: {system_platform}")
        return
    
    # Install the font by copying it to the system directory
    shutil.copy(font_path, os.path.join(install_dir, font_name))
    print(f"Font installed: {font_path}")

def load_fonts():
    """
    Loads all fonts into the system.
    """
    for font in FONTS:
        if not os.path.exists(font):
            print(f"Warning: Font file '{font}' not found.")
            continue
        
        try:
            load_custom_font(font)
        except Exception as e:
            print(f"Failed to load font '{font}': {e}")

def uninstall_fonts():
    """
    Removes all fonts from the system after app is finished.
    """
    for font in FONTS:
        font_name = os.path.basename(font)
        system_platform = sys.platform

        # Uninstall fonts based on platform
        if system_platform == "darwin":
            font_dir = os.path.expanduser("~/Library/Fonts")
            font_path = os.path.join(font_dir, font_name)
            if os.path.exists(font_path):
                os.remove(font_path)
                print(f"Uninstalled font: {font_name}")
                # Run the AppleScript to remove the font from Font Book (macOS)
                uninstall_mac_font(font_name)
        elif system_platform == "win32":
            font_dir = os.path.expandvars("%WINDIR%\\Fonts")
            font_path = os.path.join(font_dir, font_name)
            if os.path.exists(font_path):
                os.remove(font_path)
                print(f"Uninstalled font: {font_name}")
        elif system_platform == "linux":
            font_dir = "/usr/share/fonts"
            font_path = os.path.join(font_dir, font_name)
            if os.path.exists(font_path):
                os.remove(font_path)
                print(f"Uninstalled font: {font_name}")
        else:
            print(f"Unsupported platform: {system_platform}")

def uninstall_mac_font(font_name):
    """
    Uses AppleScript to remove the font from Font Book on macOS.
    """
    script = f'''
    tell application "Font Book"
        set theFont to (first font whose name is "{font_name}")
        remove theFont
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        print(f"Font '{font_name}' removed from Font Book.")
    except subprocess.CalledProcessError:
        print(f"Failed to remove font '{font_name}' from Font Book.")
