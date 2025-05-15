from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os
import threading
from utils.files import resource_path

def resize_and_sharpen(image, size):
    resized_image = image.resize(size, Image.LANCZOS)
    sharpened_image = ImageEnhance.Sharpness(resized_image).enhance(2.0)
    return sharpened_image

class Images:
    _instance = None
    _lock = threading.Lock()  # Thread-safe singleton lock

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check locking
                    cls._instance = super(Images, cls).__new__(cls)
                    cls._instance._init_images()  # Initialize images
        return cls._instance

    def _init_images(self):
        self.images = {}
        self.original_images = {}
        self._load_images()
        self._load_webhooks_template()

    def _load_webhooks_template(self):
        path = resource_path("data/icons/ghost-webhooks.png")
        new_height = 180

        if os.path.exists(path):
            img = Image.open(path)
            width, height = img.size
            ratio = width / height
            new_width = int(new_height * ratio)
            self.images["ghost_webhooks"] = ImageTk.PhotoImage(resize_and_sharpen(img, (new_width, new_height)))
            print(self.images["ghost_webhooks"])
        else:
            print(f"Warning: Image file '{path}' not found.")

    def _load_images(self):
        SIZES = {
            "bigger": (23, 23),
            "icon": (20, 20),
            "small": (15, 15),
            "smaller": (12, 12),
            "tiny": (10, 10),
            "logo": (50, 50),
        }

        ICON_CONFIG = {
            "bigger": ["scripts"],
            "small": ["trash", "github", "restart", "checkmark", "left-chevron", "file-signature", "trash-white"],
            "tiny": ["submit", "max", "min", "search"],
            "smaller": ["folder-open", "plus"],
            "logo": ["ghost-logo"],
        }

        ICON_PATHS = {
            "home": "data/icons/house-solid.png",
            "settings": "data/icons/gear-solid.png",
            "theming": "data/icons/paint-roller-solid.png",
            "snipers": "data/icons/crosshairs-solid.png",
            "rich_presence": "data/icons/discord-brands-solid.png",
            "console": "data/icons/terminal-solid.png",
            "logout": "data/icons/power-off-solid.png",
            "scripts": "data/icons/script-solid.png",
            "apis": "data/icons/cloud-solid.png",
            "session_spoofing": "data/icons/shuffle-solid.png",
            "submit": "data/icons/arrow-right-solid.png",
            "trash": "data/icons/trash-solid.png",
            "trash-white": "data/icons/trash-solid-white.png",
            "github": "data/icons/github-brands-solid.png",
            "restart": "data/icons/rotate-right-solid.png",
            "ghost-logo": "data/icons/ghost-logo.png",
            "min": "data/icons/min-solid.png",
            "max": "data/icons/max-solid.png",
            "checkmark": "data/icons/check-solid.png",
            "search": "data/icons/magnifying-glass-solid.png",
            "plus": "data/icons/plus-solid.png",
            "folder-open": "data/icons/folder-open-solid.png",
            "file-signature": "data/icons/file-signature-solid.png",
            "left-chevron": "data/icons/chevron-left-solid.png",
            "tools": "data/icons/screwdriver-wrench-solid.png",
        }

        for key, path in ICON_PATHS.items():
            size = SIZES["icon"]  # Default size
            for size_name, keys in ICON_CONFIG.items():
                if key in keys:
                    size = SIZES[size_name]
                    break

            image_path = resource_path(path)
            if os.path.exists(image_path):
                original_image = Image.open(image_path)
                original_image.info["dpi"] = (300, 300)
                sharpened_image = resize_and_sharpen(original_image, size)
                self.images[key] = ImageTk.PhotoImage(sharpened_image)
                self.original_images[key] = sharpened_image
            else:
                print(f"Warning: Image file '{image_path}' not found.")

    def hex_to_rgb(self, hex_colour):
        hex_colour = hex_colour.lstrip('#')
        return tuple(int(hex_colour[i:i+2], 16) for i in (0, 2, 4))

    def change_image_colour(self, image, hex_colour):
        rgb_colour = self.hex_to_rgb(hex_colour)
        image = image.convert("RGBA")
        data = image.getdata()

        new_data = [
            (rgb_colour[0], rgb_colour[1], rgb_colour[2], item[3])
            if item[0] in range(200, 256) and item[1] in range(200, 256) and item[2] in range(200, 256)
            else item
            for item in data
        ]

        image.putdata(new_data)
        return image

    def get(self, key, hover_colour=None):
        if key not in self.original_images:
            return None

        if hover_colour:
            image = self.change_image_colour(self.original_images[key], hover_colour)
            return ImageTk.PhotoImage(image)

        return self.images.get(key)
