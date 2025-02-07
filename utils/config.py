import json
import os
import time
import requests

from . import console
from . import webhook as webhook_client

MOTD = "A cockroach can live for weeks without its head".lower()
PRODUCTION = False
VERSION = "3.5.2"
VERSION += "-dev" if not PRODUCTION else ""
DEFAULT_RPC = {
        "enabled": False,
        "client_id": "1018195507560063039",
        "state": "ghost aint dead",
        "details": "",
        "large_image": "ghost",
        "large_text": "",
        "small_image": "",
        "small_text": "",
        "name": "Ghost"
    }
DEFAULT_CONFIG = {
    "token": "",
    "prefix": ".",
    "rich_presence": DEFAULT_RPC,
    "theme": "ghost",
    "gui": True,
    "rich_embed_webhook": "",
    "message_settings": {
        "auto_delete_delay": 15,
        "style": "image"
    },
    "session_spoofing": {
        "enabled": False,
        "device": "desktop"
    },
    "snipers": {
        "nitro": {
            "enabled": True,
            "ignore_invalid": False,
            "webhook": ""
        },
        "privnote": {
            "enabled": True,
            "ignore_invalid": False,
            "webhook": ""
        }
    },
    "apis": {
        "serpapi": ""
    }
}
DEFAULT_THEME = {
    "title": "ghost selfbot",
    "emoji": "\ud83d\udc7b",
    "image": "https://ghost.benny.fun/assets/ghost.png",
    "colour": "#575757",
    "footer": "ghost aint dead"
}
CHANGELOG = """New:
  - Added checks for no desktop interface and will run headless if so
  - Added rich embed mode! Nope this isn't using web embeds.
  - Added rich embed webhook to GUI
  - Add spam command
  - Add proper uptime
  - Add mutual server members command!
  - Add clearcache command
  - Add massping command
  - Add embed message style option in gui
  - Added aura and gyatt commands (proper brainrot)
  - Added challenge and achievement commands using api.alexflipnote.dev
  - Added rainbow reaction and rainbow codeblock using ascii colours
  - Added ascii colours to codeblock for future changes to codeblock mode
  - Add dm channel check for clear command
  - Add yoinkrpc command and more customisable rich presence
  - Add no_response option to restart, useful for executing the command within another command
  - Add command history command
  - Add custom pypresence git to requirements for custom names in RPC
  - Add rich presence customisation in gui

Fix:
  - Fix codeblock styling for footers
  - Fix RPS description not showing
  - Fix dox command
  - Fix search command
  - Fix hyperlink
  - Fixed soundboard and playsound command.

Change:
  - Rename config to config.example.json and add default config to gitingore so config isnt overwritten when merging changes.
  - Edit RPC error log
  - Update NSFW commands to use nekobot
  - Improve generate help commands and add custom emojis to titles
  - Improve config command
  - Adding short and long formatting for uptime
  - Improved specs command
  - Allowed delete_after to be disabled
  - Improve send_message
  - Adjust headerless check to check for ttkbootstrap not tkinter
  - Improve banner printing
  - Search now searches through command aliases
  - Make print_banner get terminal width for correct dash size"""

MAKE_CONFIG = lambda: json.dump(DEFAULT_CONFIG, open("config.json", "w"), indent=4) if not os.path.exists("config.json") else None

class RichPresence:
    def __init__(self, config, **kwargs):
        self.enabled = kwargs.get("enabled", False)
        self.client_id = kwargs.get("client_id", None)
        self.state = kwargs.get("state", None)
        self.details = kwargs.get("details", None)
        self.large_image = kwargs.get("large_image", None)
        self.large_text = kwargs.get("large_text", None)
        self.small_image = kwargs.get("small_image", None)
        self.small_text = kwargs.get("small_text", None)
        self.name = kwargs.get("name", None)
        self.config = config
        
    def set(self, key, value):
        setattr(self, key, value)
        
    def get(self, key):
        return getattr(self, key)
        
    def save(self):
        self.config.config["rich_presence"] = {
            "enabled": self.enabled,
            "client_id": self.client_id,
            "state": self.state,
            "details": self.details,
            "large_image": self.large_image,
            "large_text": self.large_text,
            "small_image": self.small_image,
            "small_text": self.small_text,
            "name": self.name
        }
        self.config.save()

    def reset_defaults(self):
        self.config.config["rich_presence"] = DEFAULT_RPC
        self.config.config["rich_presence"]["enabled"] = self.enabled
        self.config.save()
            
    def to_dict(self):
        rpc_dict = {}
        
        if self.state: rpc_dict["state"] = self.state
        if self.details: rpc_dict["details"] = self.details
        if self.large_image: rpc_dict["large_image"] = self.large_image
        if self.large_text: rpc_dict["large_text"] = self.large_text
        if self.small_image: rpc_dict["small_image"] = self.small_image
        if self.small_text: rpc_dict["small_text"] = self.small_text
        if self.name: rpc_dict["name"] = self.name
        rpc_dict["start"] = time.time()
        
        return rpc_dict

class Theme:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.title = kwargs.get("title")
        self.emoji = kwargs.get("emoji")
        self.image = kwargs.get("image")
        self.colour = kwargs.get("colour")
        self.footer = kwargs.get("footer")

    def set(self, key, value):
        setattr(self, key, value)

    def save(self):
        with open(f"themes/{self.name}.json", "w") as f:
            json.dump({
                "title": self.title,
                "emoji": self.emoji,
                "image": self.image,
                "colour": self.colour,
                "footer": self.footer
            }, f, indent=4)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "title": self.title,
            "emoji": self.emoji,
            "image": self.image,
            "colour": self.colour,
            "footer": self.footer
        }

class Sniper:
    def __init__(self, config, **kwargs):
        self.name = kwargs.get("name")
        self.enabled = kwargs.get("enabled")
        self.ignore_invalid = kwargs.get("ignore_invalid")
        self.webhook = kwargs.get("webhook")
        self.config = config

    def save(self):
        self.config.config["snipers"][self.name] = {
            "enabled": self.enabled,
            "ignore_invalid": self.ignore_invalid,
            "webhook": self.webhook
        }
        self.config.save()

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "ignore_invalid": self.ignore_invalid,
            "webhook": self.webhook
        }

    def set(self, key, value):
        setattr(self, key, value)

    def get_webhook(self):
        return webhook_client.Webhook.from_url(self.webhook)

    def set_webhook(self, webhook):
        try:
            self.webhook = webhook.url
        except:
            self.webhook = webhook
        self.save()

    def enable(self):
        self.enabled = True
        self.save()

    def disable(self):
        self.enabled = False
        self.save()

    def toggle(self):
        self.enabled = not self.enabled
        self.save()

    def ignore_invalid(self):
        self.ignore_invalid = True
        self.save()

    def toggle_ignore_invalid(self):
        self.ignore_invalid = not self.ignore_invalid
        self.save()

class Config:
    def __init__(self) -> None:
        global CHANGELOG
        # self.check()
        self.config = json.load(open("config.json"))
        self.theme = self.get_theme(self.config["theme"])

    def check(self):
        if not os.path.exists("backups/"):
            os.mkdir("backups/")
            console.print_info("Created backups folder")
        if not os.path.exists("scripts/"):
            os.mkdir("scripts/")
            console.print_info("Created scripts folder")
        if not os.path.exists("data/"):
            os.mkdir("data/")
            console.print_info("Created data folder")
        if not os.path.exists("data/cache/"):
            os.mkdir("data/cache/")
            console.print_info("Created cache folder")
        if not os.path.exists("data/sniped_codes.txt"):
            open("data/sniped_codes.txt", "w").close()
            console.print_info("Created sniped codes file")
        if not os.path.exists("data/privnote_saves.json"):
            json.dump({}, open("data/privnote_saves.json", "w"), indent=4)
            console.print_info("Created privnote saves file")
        if not os.path.exists("config.json"):
            with open("config.json", "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            console.print_info("Created config file")
        if not os.path.exists("themes/"):
            os.makedirs("themes/")
            console.print_info("Created themes folder")
        if not os.path.exists("themes/ghost.json"):
            json.dump(DEFAULT_THEME, open("themes/ghost.json", "w"), indent=4)
            console.print_info("Created default theme file")

        if os.path.exists("data/cache/command_history.txt"):
            os.remove("data/cache/command_history.txt")
            console.print_info("Removed old command history file")

        if os.path.exists("config.json"):
            self.config = json.load(open("config.json"))

            for key in DEFAULT_CONFIG:
                if key == "theme":
                    if isinstance(self.config[key], dict):
                        self.config[key] = "ghost"

                if key == "snipers":
                    for sniper in DEFAULT_CONFIG[key]:
                        if sniper not in self.config[key]:
                            self.config[key][sniper] = DEFAULT_CONFIG[key][sniper]

                        if isinstance(self.config[key][sniper], bool):
                            sniper_enabled = self.config[key][sniper]
                            self.config[key][sniper] = DEFAULT_CONFIG[key][sniper]
                            self.config[key][sniper]["enabled"] = sniper_enabled

                        self.config[key][sniper] = {**DEFAULT_CONFIG[key][sniper], **self.config[key][sniper]}

                if key == "rich_presence":
                    if isinstance(self.config[key], bool):
                        self.config[key] = DEFAULT_CONFIG[key]
                    else:
                        self.config[key] = {**DEFAULT_CONFIG[key], **self.config[key]}

                if key not in self.config:
                    self.config[key] = DEFAULT_CONFIG[key]

            for key in self.config:
                if key == "message_settings":
                    auto_delete_delay = self.config[key]["auto_delete_delay"]

                    if not isinstance(auto_delete_delay, int):
                        self.config[key]["auto_delete_delay"] = int(auto_delete_delay) if auto_delete_delay.isdigit() else DEFAULT_CONFIG[key]["auto_delete_delay"]

            json.dump(self.config, open("config.json", "w"), indent=4)

        # if self.get("token") == "":
        #     console.print_error("No token found, please set it below.")
        #     new_token = input("> ")

        #     self.set("token", new_token)

        # if self.get("prefix") == "":
        #     console.print_error("No prefix found, please set it below.")
        #     new_prefix = input("> ")

        #     self.set("prefix", new_prefix)

    def save(self) -> None:
        if isinstance(self.config["theme"], dict):
            self.save_theme_file(self.config["theme_name"], self.config["theme"])
            self.config["theme"] = self.config["theme_name"]
            self.config.pop("theme_name")

        json.dump(self.config, open("config.json", "w"), indent=4)

    def get(self, key) -> str:
        subkey = None

        if "." in key:
            key, subkey = key.split(".")

        if subkey:
            return self.config[key][subkey]

        return self.config[key]

    def set(self, key, value, save=True) -> None:
        if "." in key:
            key, subkey = key.split(".")
            self.config[key][subkey] = value
        elif isinstance(value, dict):
            self.config[key] = {**self.config[key], **value}
        else:
            self.config[key] = value

        if save:
            self.save()

    def get_theme_file(self, theme):
        return json.load(open(f"themes/{theme}.json")) if os.path.exists(f"themes/{theme}.json") else None

    def save_theme_file(self, theme_name, new_obj) -> None:
        json.dump(new_obj, open(f"themes/{theme_name}.json", "w"), indent=4)

    def get_theme(self, theme_name):
        if not os.path.exists(f"themes/{theme_name}.json"):
            return Theme(**DEFAULT_THEME)

        theme_obj = self.get_theme_file(theme_name)
        theme_obj["name"] = theme_name
        return Theme(**theme_obj)

    def set_theme(self, theme_name):
        self.config["theme"] = theme_name
        self.save()
        self.theme = self.get_theme(theme_name)

    def delete_theme(self, theme_name):
        if self.theme.name == theme_name:
            self.set_theme("ghost")

        os.remove(f"themes/{theme_name}.json")
        self.save()

    def get_themes(self):
        themes = []
        for theme in os.listdir("themes/"):
            if theme.endswith(".json"):
                theme = theme.replace(".json", "")
                themes.append(Theme(name=theme, **self.get_theme_file(theme)))

        return themes

    def get_sniper(self, sniper):
        if sniper not in self.config["snipers"]:
            return None

        obj = self.config["snipers"].get(sniper)
        obj["name"] = sniper
        return Sniper(config=self, **obj)

    def get_snipers(self):
        snipers = []
        for sniper in self.config["snipers"]:
            obj = self.config["snipers"][sniper]
            obj["name"] = sniper
            snipers.append(Sniper(config=self, **obj))

        return snipers

    def get_session_spoofing(self):
        return self.config["session_spoofing"]["enabled"], self.config["session_spoofing"]["device"]

    def set_session_spoofing(self, enabled, device):
        self.config["session_spoofing"]["enabled"] = enabled
        self.config["session_spoofing"]["device"] = device
        self.save()
        
    def get_rich_presence(self):
        return RichPresence(config=self, **self.config["rich_presence"])

    def create_theme(self, theme_name):
        if os.path.exists(f"themes/{theme_name}.json"):
            return False

        theme_name = theme_name.replace(" ", "_")

        json.dump(DEFAULT_THEME, open(f"themes/{theme_name}.json", "w"), indent=4)
        theme = Theme(name=theme_name, **DEFAULT_THEME)
        return theme

    def add_command_history(self, command_string):
        if not os.path.exists("data/cache/command_history.txt"):
            open("data/cache/command_history.txt", "w")

        with open("data/cache/command_history.txt", "a") as f:
            f.write(f"{console.get_formatted_time()}|{command_string}\n")

    def get_command_history(self):
        if not os.path.exists("data/cache/command_history.txt"):
            open("data/cache/command_history.txt", "w")

        with open("data/cache/command_history.txt", "r") as f:
            lines = f.readlines()
            commands = []

            for line in lines:
                formatted = line.strip()
                time, command_string = (formatted.split("|")[0], formatted.split("|")[1])
                commands.append((time, command_string))

            return commands

    @staticmethod
    def get_python_path():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def quit():
        exit()
