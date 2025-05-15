import os
import json
from utils.defaults import DEFAULT_CONFIG, DEFAULT_THEME
from utils import files

BASE_PATH = files.get_application_support() + "/"

REQUIRED_DIRS = [
    "backups",
    "data/sensitive",
    "data/cache",
    "data",
    "scripts",
    "themes"
]

REQUIRED_FILES = {
    "data/sniped_codes.txt": "",
    "data/privnote_saves.json": {},
    "data/sensitive/tokens.json": [],
    "themes/ghost.json": DEFAULT_THEME,
    "config.json": DEFAULT_CONFIG,
    # "ghost.log": ""
}

def create_directories():
    for directory in REQUIRED_DIRS:
        os.makedirs(BASE_PATH + directory, exist_ok=True)

def create_files():
    for path, content in REQUIRED_FILES.items():
        if not os.path.exists(BASE_PATH + path):
            with open(BASE_PATH + path, "w") as f:
                if isinstance(content, str):
                    f.write(content)
                else:
                    json.dump(content, f, indent=4)
            print(f"Created missing file: {path}")

def clear_cache():
    for file in os.listdir(BASE_PATH + "data/cache"):
        if file not in ["CREATE_WEBHOOKS"]:
            os.remove(BASE_PATH + f"data/cache/{file}")
    print("Cleared cache.")

def check():
    create_directories()
    create_files()
    clear_cache()
    print("Startup checks complete.")
    
if __name__ == "__main__":
    check()