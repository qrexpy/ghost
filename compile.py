import os
import sys
import platform
import subprocess

def build():
    system = platform.system()
    
    name = "Ghost"
    entry_script = "ghost.py"
    icon = "data/icon.png"

    common_args = [
        "pyinstaller",
        "--name=" + name,
        "--onefile",
        "--windowed",
        "--noconsole",
        f"--icon={icon}",
        "--hidden-import=discord",
        "--hidden-import=discord.ext.commands",
        "--collect-submodules=discord",
        entry_script
    ]

    # Add paths to site-packages if needed
    if system == "Windows":
        site_packages = ".venv\\Lib\\site-packages"
        add_data = [
            "--add-data=data\\*;data",
            "--add-data=data\\fonts\\*;data/fonts",
            "--add-data=data\\icons\\*;data/icons"
        ]
    else:
        site_packages = ".venv/lib/python3.10/site-packages"
        add_data = [
            "--add-data=data/*:data",
            "--add-data=data/fonts/*:data/fonts",
            "--add-data=data/icons/*:data/icons"
        ]
    
    common_args.append(f"--paths={site_packages}")
    common_args += add_data

    # macOS-specific option
    if system == "Darwin":
        common_args.append("--osx-bundle-identifier=fun.benny.ghost")

    # Run the command
    print(f"Building for {system}...")
    subprocess.run(common_args)

if __name__ == "__main__":
    build()
