import threading
import certifi
import os
import sys

os.environ["SSL_CERT_FILE"] = certifi.where()

HEADLESS = "DISPLAY" not in os.environ and sys.platform == "linux"

from bot.controller import BotController
from utils import startup_check, check_fonts, console
from utils.files import get_application_support
from utils.config import Config

if not HEADLESS:
    from gui.main import GhostGUI
    from gui.font_check import FontCheckGUI

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

def run():
    cfg = Config()
    controller = BotController()
    
    if cfg.get("token") == "":
        print("No token found. Running in GUI mode.")
        # gui_only()
    else:
        startup_check.check()
        threading.Thread(target=controller.start, daemon=True).start()
    
    GhostGUI(controller).run()
    
def gui_only():
    GhostGUI(None).run()
    
def no_gui():
    startup_check.check()
    cfg = Config()
    
    if cfg.get("token") == "":
        console.error("No token found. Please enter one below.")
        token = input("> ")
        cfg.set("token", token)
        cfg.save()
    else:
        console.info("Token found. Starting bot.")
    
    console.info("Starting bot.")
    
    controller = BotController()
    controller.start()
    
    while True:
        pass

def main():
    get_application_support()
    startup_check.check()
    cfg = Config()
    cfg.check()
    
    if HEADLESS:    
        print("Running in headless mode.")
        no_gui()
    else:
        print("Running in GUI mode. Checking fonts...")
        if cfg.get_skip_fonts():
            print("Skipping font check.")
            cfg.set_skip_fonts(False)
            run()
        elif check_fonts():
            print("Fonts are good.")
            run()
        else:
            print("Fonts are bad.")
            FontCheckGUI().run()
            run()

if __name__ == "__main__":
    main()
    # no_gui()
