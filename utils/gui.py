# anyone reading this, i sincerely apologize for the mess you're about to witness
# tkinter sucks and i hate it

import os
import sys
import time
import psutil
import discord
import asyncio
import requests
import threading
import webbrowser
import concurrent
import ttkbootstrap as ttk

from utils import console
from utils import config
from utils import files
from utils import cmdhelper

from pathlib import Path
from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText
from PIL import Image, ImageTk

PATH = Path(__file__).parent

class RoundedFrame(ttk.Canvas):
    def __init__(self, parent, radius=(25, 25, 25, 25), bootstyle="dark.TFrame", background="black", **kwargs):
        super().__init__(parent, background=background, highlightthickness=0, bd=0, **kwargs)
        self.radius = radius
        self.background = background

        self.inner_frame = ttk.Frame(self, style=bootstyle)
        self.create_window(0, 0, window=self.inner_frame, anchor="nw")

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """ Redraw the rounded rectangle and adjust inner frame """
        self.delete("all")

        width, height = self.winfo_width(), self.winfo_height()
        if width < 2 or height < 2:
            return

        radius_tl, radius_tr, radius_br, radius_bl = self.radius

        points = [
            radius_tl, 0,
            width - radius_tr, 0,
            width, 0,
            width, radius_tr,
            width, height - radius_br,
            width, height,
            width - radius_br, height,
            radius_bl, height,
            0, height,
            0, height - radius_bl,
            0, radius_tl,
            0, 0
        ]
        self.create_polygon(points, smooth=True, fill=self.background, outline=self.background)

        try:
            self.itemconfig(self.inner_frame, width=width, height=height)
        except Exception as e:
            pass

class GhostGUI:
    def __init__(self, bot=None):
        self.bot = bot
        self.width = 600
        self.height = 520
        self.bot_started = False
        self.bot_thread = None
        self.console = []
        self.visible_console_lines = []

        self.root = ttk.tk.Tk()
        self.root.title("Ghost")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.minsize(self.width, self.height)
        # self.root.resizable(False, False)
        # self.root.overrideredirect(True)
        self.root.style = ttk.Style()
        self.root.style.theme_use("darkly")
        self.root.style.configure("TEntry", background=self.root.style.colors.get("dark"), fieldbackground=self.root.style.colors.get("secondary"))
        self.root.style.configure("TCheckbutton", background=self.root.style.colors.get("dark"))

        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.user_avatar_path = files.resource_path("data/cache/avatar.png")
        self.current_page = "home"

        # self.root.style.configure("primary.TButton", background="#254bff")
        # self.root.style.configure("secondary.TButton", background="#383838")
        # self.root.style.configure("success.TButton", background="#00db7c")
        # self.root.style.configure("danger.TButton", background="#e7230f")
        # self.root.style.configure("warning.TButton", background="#f39500")

        self.start_button = ttk.Button(self.root, text="Start Ghost", command=self.start_bot_thread)
        self.start_button.pack(fill=ttk.BOTH, side=ttk.BOTTOM, pady=10)

    def load_images(self):
        icon_size = (20, 20)
        small_size = (15, 15)
        tiny_size = (10, 10)

        icons = {
            "home": "data/icons/house-solid.png",
            "home_hover": "data/icons/hover/house-solid.png",
            "settings": "data/icons/gear-solid.png",
            "settings_hover": "data/icons/hover/gear-solid.png",
            "theming": "data/icons/paint-roller-solid.png",
            "theming_hover": "data/icons/hover/paint-roller-solid.png",
            "snipers": "data/icons/crosshairs-solid.png",
            "snipers_hover": "data/icons/hover/crosshairs-solid.png",
            "rich_presence": "data/icons/discord-brands-solid.png",
            "rich_presence_hover": "data/icons/hover/discord-brands-solid.png",
            "console": "data/icons/terminal-solid.png",
            "console_hover": "data/icons/hover/terminal-solid.png",
            "logout": "data/icons/power-off-solid.png",
            "logout_hover": "data/icons/hover/power-off-solid.png",
            "apis": "data/icons/cloud-solid.png",
            "session_spoofing": "data/icons/shuffle-solid.png",
            "submit": "data/icons/arrow-right-solid.png",
            "trash": "data/icons/trash-solid.png",
            "github": "data/icons/github-brands-solid.png",
            "restart": "data/icons/rotate-right-solid.png",
        }

        self.images = {}  # Dictionary to hold images

        for key, path in icons.items():
            size = small_size if key in ["trash", "github"] else tiny_size if key == "submit" else icon_size
            image_path = files.resource_path(path)
            self.images[key] = ImageTk.PhotoImage(Image.open(image_path).resize(size))

        # Optional: Assign commonly used images as attributes
        self.home_icon = self.images["home"]
        self.home_icon_hover = self.images["home_hover"]
        self.settings_icon = self.images["settings"]
        self.settings_icon_hover = self.images["settings_hover"]
        self.theming_icon = self.images["theming"]
        self.theming_icon_hover = self.images["theming_hover"]
        self.snipers_icon = self.images["snipers"]
        self.snipers_icon_hover = self.images["snipers_hover"]
        self.rich_presence_icon = self.images["rich_presence"]
        self.rich_presence_icon_hover = self.images["rich_presence_hover"]
        self.console_icon = self.images["console"]
        self.console_icon_hover = self.images["console_hover"]
        self.logout_icon = self.images["logout"]
        self.logout_icon_hover = self.images["logout_hover"]

        self.apis_icon = self.images["apis"]
        self.session_spoofing_icon = self.images["session_spoofing"]
        self.submit_icon = self.images["submit"]
        self.github_icon = self.images["github"]
        self.trash_icon_small = self.images["trash"]
        self.restart_icon = self.images["restart"]

    def save_avatar(self):
        response = requests.get(self.bot.user.avatar.url)
        with open(files.resource_path("data/cache/avatar.png"), "wb") as file:
            file.write(response.content)

    def center_window(self, width=None, height=None):
        if height is not None:
            self.height = height
        if width is not None:
            self.width = width

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.focus_force()

    def quit(self):
        console.print_info("Quitting Ghost...")

        if os.name == "nt":
            os.kill(os.getpid(), 9)
        else:
            os._exit(0)

    def draw_titlebar(self):
        def start_move(event):
            """ Store the mouse position when the drag starts. """
            self._offset_x = event.x
            self._offset_y = event.y

        def move_window(event):
            """ Move the window based on the initial offset. """
            x = event.x_root - self._offset_x
            y = event.y_root - self._offset_y
            self.root.geometry(f"+{x}+{y}")

        titlebar = ttk.Frame(self.root)
        titlebar.configure(style="dark.TFrame")

        # Bind events
        titlebar.bind("<Button-1>", start_move)  # Capture the starting position
        titlebar.bind("<B1-Motion>", move_window)  # Move the window

        titlebar.pack(fill=ttk.BOTH, side=ttk.TOP)

        title = ttk.Label(titlebar, text="Ghost", font="-size 12")
        title.configure(background=self.root.style.colors.get("dark"))

        minimise_button = ttk.Label(titlebar, text="—")
        minimise_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        minimise_button.bind("<Button-1>", lambda e: self.root.iconify())

        close_button = ttk.Label(titlebar, text="×", font="-size 14")
        close_button.configure(background=self.root.style.colors.get("dark"), anchor="n")
        close_button.bind("<Button-1>", lambda e: self.quit())

        title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=10)
        minimise_button.grid(row=0, column=2, sticky=ttk.E, padx=5, pady=10)
        close_button.grid(row=0, column=3, sticky=ttk.E, padx=(0, 10), pady=10)

        titlebar.grid_columnconfigure(1, weight=1)

    def draw_sidebar(self):
        # self.draw_titlebar()

        def _create_sidebar_button(image, hover_image, page_name, command, row, special_bg=False):
            """Helper function to create sidebar buttons with hover and selection effects."""
            is_selected = self.current_page == page_name
            bg_color = self.root.style.colors.get("secondary") if is_selected else self.root.style.colors.get("dark")

            button = ttk.Label(self.sidebar, image=image, background=bg_color, anchor="center")
            button.bind("<Button-1>", lambda e: self._update_page(command, page_name))
            button.bind("<Enter>", lambda e: button.configure(image=hover_image))
            button.bind("<Leave>", lambda e: button.configure(image=image))
            button.grid(row=row, column=0, sticky=ttk.NSEW, pady=(10, 2) if row == 0 else 2, ipady=12)
            
            return button

        # Create sidebar
        width = self.width // (self.width // 65)
        self.sidebar = ttk.Frame(self.root, width=width, height=self.height, style="dark.TFrame")
        self.sidebar.pack(fill=ttk.BOTH, side=ttk.LEFT)
        self.sidebar.grid_propagate(False)

        # Sidebar buttons
        self.buttons = {
            "home": _create_sidebar_button(self.home_icon, self.home_icon_hover, "home", self.draw_home, 0),
            "console": _create_sidebar_button(self.console_icon, self.console_icon_hover, "console", self.draw_console, 1),
            "settings": _create_sidebar_button(self.settings_icon, self.settings_icon_hover, "settings", self.draw_settings, 2),
            "theming": _create_sidebar_button(self.theming_icon, self.theming_icon_hover, "theming", self.draw_theming, 3),
            "snipers": _create_sidebar_button(self.snipers_icon, self.snipers_icon_hover, "snipers", self.draw_snipers, 4),
            "rpc": _create_sidebar_button(self.rich_presence_icon, self.rich_presence_icon_hover, "rpc", self.draw_rich_presence, 5),
        }

        # Logout button (doesn't need page tracking)
        logout_button = ttk.Label(self.sidebar, image=self.logout_icon, background=self.root.style.colors.get("dark"), anchor="center")
        logout_button.bind("<Button-1>", lambda e: self.quit())
        logout_button.bind("<Enter>", lambda e: logout_button.configure(image=self.logout_icon_hover))
        logout_button.bind("<Leave>", lambda e: logout_button.configure(image=self.logout_icon))
        logout_button.grid(row=7, column=0, sticky=ttk.NSEW, pady=(2, 10), ipady=12)

        # Configure grid
        self.sidebar.grid_rowconfigure(6, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

    def _update_page(self, command, page_name):
        """Updates the current page and refreshes the sidebar to highlight the selected page."""
        self.current_page = page_name
        self.draw_sidebar()  # Redraw sidebar to update button backgrounds
        command()

    def draw_main(self, scrollable=False):
        width = self.width - (self.width // 100)
        main = ScrolledFrame(self.root, width=width, height=self.height) if scrollable else ttk.Frame(self.root, width=width, height=self.height)
        if isinstance(main, ScrolledFrame):
            main.hide_scrollbars()
            main.enable_scrolling()
        main.pack(fill=ttk.BOTH, expand=True, padx=23 if scrollable else 25, pady=23 if scrollable else 25)

        return main

    def clear_main(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()

        self.draw_sidebar()

    def clear_console(self):
        self.console = []
        self.update_console()

    def add_console(self, prefix, text):
        time = console.get_formatted_time()
        self.console.append((time, prefix, text))
        self.update_console()

    def update_console(self):
        self.visible_console_lines = self.console[-20:]

        try:
            self.console_inner_wrapper.config(state="normal")
            self.console_inner_wrapper.delete(1.0, "end")
            for index, (time, prefix, text) in enumerate(self.console):
                if "sniper_arg" in prefix.lower():
                    self.console_inner_wrapper.insert("end", f"{' '*10} {text}\n")
                else:
                    self.console_inner_wrapper.insert("end", f"[{time}] [{prefix}] {text}\n")
                self.console_inner_wrapper.see("end")

            self.console_inner_wrapper.config(state="disabled")

        except Exception as e:
            pass

        # self.root.after(500, self.update_console)

    def update_bot_details(self):
        try:
            latency = self.bot.latency
            latency_ms = round(latency * 1000) if latency != float("inf") else 0  # Fallback to 0ms

            self.uptime_label.config(text=f"Uptime: {cmdhelper.format_time(time.time() - self.bot.start_time, short_form=True)}")
            self.latency_label.config(text=f"Latency: {latency_ms}ms")
        except Exception as e:
            pass

        self.root.after(1000, self.update_bot_details)

    def update_discord_details(self):
        try:
            self.friends_label.config(text=f"Friends: {len(self.bot.friends)}")
            self.guilds_label.config(text=f"Guilds: {len(self.bot.guilds)}")
        except Exception as e:
            pass

        self.root.after(5000, self.update_discord_details)

    def draw_home(self):
        self.clear_main()
        main = self.draw_main()
        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35

        self.current_page = "home"

        header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 15, 15), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        header_frame.pack(fill=ttk.BOTH)

        self.avatar_image_large = ImageTk.PhotoImage(Image.open(self.user_avatar_path).resize((50, 50)))
        avatar_label = ttk.Label(header_frame, image=self.avatar_image_large)
        avatar_label.configure(background=self.root.style.colors.get("secondary"))

        username_label = ttk.Label(header_frame, text=f"{self.bot.user.display_name}", font="-weight bold -size 20")
        username_label.configure(background=self.root.style.colors.get("secondary"))

        subtitle = ttk.Label(header_frame, text=f"{self.bot.user.name}", font="-slant italic -size 14")
        subtitle.configure(background=self.root.style.colors.get("secondary"), foreground="lightgrey")

        restart_label = ttk.Label(header_frame, image=self.restart_icon)
        restart_label.configure(background=self.root.style.colors.get("secondary"))
        restart_label.bind("<Button-1>", lambda e: self.restart_bot())

        avatar_label.grid(row=0, column=0, sticky=ttk.W, padx=(15, 10), pady=15, rowspan=2)
        restart_label.grid(row=0, column=3, sticky=ttk.E, padx=(0, 30), pady=15, rowspan=2)
        username_label.grid(row=0, column=1, sticky=ttk.W, pady=(15, 0))
        subtitle.grid(row=1, column=1, sticky=ttk.W, pady=(0, 15))

        header_frame.grid_columnconfigure(2, weight=1)

        details_wrapper_frame = ttk.Frame(main, width=width)
        details_wrapper_frame.configure(style="default.TLabel")
        details_wrapper_frame.pack(fill=ttk.BOTH, expand=False, pady=(10, 0))

        # --------------------------------------------

        account_details_frame = RoundedFrame(
            details_wrapper_frame,
            radius=(15, 15, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        
        account_details_frame.grid(row=0, column=0, sticky=ttk.NSEW, padx=(0, 5), pady=(0, 5))
        details_wrapper_frame.grid_columnconfigure(0, weight=1)
        details_wrapper_frame.grid_rowconfigure(0, weight=1)

        account_details_title = ttk.Label(account_details_frame, text="Discord", font="-weight bold -size 16")
        account_details_title.configure(background=self.root.style.colors.get("dark"))
        account_details_title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=(10, 0))

        ttk.Separator(account_details_frame, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="we", padx=(10, 10), pady=5)
        account_details_frame.grid_columnconfigure(1, weight=1)

        self.friends_label = ttk.Label(account_details_frame, text=f"Friends: {len(self.bot.friends)}", font="-size 14")
        self.friends_label.configure(background=self.root.style.colors.get("dark"))

        self.guilds_label = ttk.Label(account_details_frame, text=f"Guilds: {len(self.bot.guilds)}", font="-size 14")
        self.guilds_label.configure(background=self.root.style.colors.get("dark"))

        self.friends_label.grid(row=2, column=0, sticky=ttk.W, padx=10, pady=(5, 0))
        self.guilds_label.grid(row=3, column=0, sticky=ttk.W, padx=(10, 40), pady=(0, 10))

        # --------------------------------------------

        bot_details_frame = RoundedFrame(
            details_wrapper_frame,
            radius=(15, 15, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        
        bot_details_frame.grid(row=0, column=1, sticky=ttk.NSEW, padx=(5, 0), pady=(0, 5))
        details_wrapper_frame.grid_columnconfigure(1, weight=1)

        bot_details_title = ttk.Label(bot_details_frame, text="Ghost", font="-weight bold -size 16")
        bot_details_title.configure(background=self.root.style.colors.get("dark"))
        bot_details_title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=(10, 0))

        ttk.Separator(bot_details_frame, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="we", padx=(10, 10), pady=5)
        bot_details_frame.grid_columnconfigure(1, weight=1)

        self.uptime_label = ttk.Label(bot_details_frame, text=f"Uptime: {cmdhelper.format_time(time.time() - self.bot.start_time, short_form=True)}", font="-size 14")
        self.uptime_label.configure(background=self.root.style.colors.get("dark"))

        latency = self.bot.latency
        latency_ms = round(latency * 1000) if latency != float("inf") else 0  # Fallback to 0ms

        self.latency_label = ttk.Label(bot_details_frame, text=f"Latency: {latency_ms}ms", font="-size 14")
        self.latency_label.configure(background=self.root.style.colors.get("dark"))

        version_label = ttk.Label(bot_details_frame, text=f"Version: {config.VERSION}", font="-size 14")
        version_label.configure(background=self.root.style.colors.get("dark"))

        self.uptime_label.grid(row=2, column=0, sticky=ttk.W, padx=(10, 0), pady=(5, 0))
        self.latency_label.grid(row=3, column=0, sticky=ttk.W, padx=(10, 0))
        version_label.grid(row=4, column=0, sticky=ttk.W, padx=(10, 0), pady=(0, 10))

        # --------------------------------------------

        changelog_frame = RoundedFrame(
            main,
            radius=(15, 15, 0, 0),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        
        changelog_frame.pack(fill=ttk.BOTH, expand=True, pady=(5, 0))

        changelog_title = ttk.Label(changelog_frame, text="Latest Changelog", font="-weight bold -size 16")
        changelog_title.configure(background=self.root.style.colors.get("dark"))
        changelog_title.pack(fill=ttk.BOTH, padx=10, pady=(10, 0))

        changelog_textbox = ttk.Text(changelog_frame, wrap="word", height=10, font=("JetBrainsMono NF Regular", 12))
        changelog_textbox.config(
            border=0,
            background=self.root.style.colors.get("dark"),
            foreground="lightgrey",
            highlightcolor=self.root.style.colors.get("dark"),
            highlightbackground=self.root.style.colors.get("dark"),
            )
        
        changelog_textbox.pack(fill=ttk.BOTH, expand=True, padx=10, pady=5)
        changelog_textbox.insert("end", config.CHANGELOG)
        changelog_textbox.config(state="disabled")

        changelog_footer_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="secondary.TFrame",
            background=self.root.style.colors.get("secondary")
            )
        
        changelog_footer_frame.pack(fill=ttk.BOTH, expand=False)

        changelog_footer_label = ttk.Label(changelog_footer_frame, text="Star Ghost on GitHub! (please 🙏)", font="-slant italic -size 12")
        changelog_footer_label.configure(background=self.root.style.colors.get("secondary"))

        github_label = ttk.Label(changelog_footer_frame, image=self.github_icon)
        github_label.configure(background=self.root.style.colors.get("secondary"))
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/ghostselfbot/ghost"))

        changelog_footer_label.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=5)
        github_label.grid(row=0, column=2, sticky=ttk.E, padx=10, pady=5)
        changelog_footer_frame.grid_columnconfigure(1, weight=1)

        # --------------------------------------------

        self.root.after(1000, self.update_bot_details)
        self.root.after(5000, self.update_discord_details)

    def draw_console(self):
        self.clear_main()
        main = self.draw_main()

        self.current_page = "console"

        console_textarea = RoundedFrame(
            main,
            radius=(15, 15, 0, 0),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        console_textarea.pack(fill="both", expand=True)

        self.console_inner_wrapper = ttk.Text(console_textarea, wrap="word", height=20, font=("JetBrainsMono NF Regular", 12))
        self.console_inner_wrapper.config(
            border=0, 
            background=self.root.style.colors.get("dark"), 
            foreground="lightgrey", 
            highlightcolor=self.root.style.colors.get("dark"), 
            highlightbackground=self.root.style.colors.get("dark"),
            state="disabled"
            )
        self.console_inner_wrapper.pack(fill="both", expand=True, padx=5, pady=5)

        self.update_console()

        footer_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="secondary.TFrame",
            background=self.root.style.colors.get("secondary")
            )

        footer_frame.pack(fill="both", expand=False)

        self.avatar_image_small = ImageTk.PhotoImage(Image.open(self.user_avatar_path).resize((15, 15)))
        avatar_label = ttk.Label(footer_frame, image=self.avatar_image_small)
        avatar_label.configure(background=self.root.style.colors.get("secondary"))

        username_label = ttk.Label(footer_frame, text=f"Logged in as {self.bot.user.name}", font="-slant italic -size 12")
        username_label.configure(background=self.root.style.colors.get("secondary"))

        clear_console_label = ttk.Label(footer_frame, image=self.trash_icon_small)
        clear_console_label.configure(background=self.root.style.colors.get("secondary"))
        clear_console_label.bind("<Button-1>", lambda e: self.clear_console())

        avatar_label.grid(row=0, column=0, sticky=ttk.W, padx=(10, 5), pady=5)
        username_label.grid(row=0, column=1, sticky=ttk.W, pady=5)
        clear_console_label.grid(row=0, column=3, sticky=ttk.E, padx=(5, 10), pady=5)

        footer_frame.grid_columnconfigure(2, weight=1)

        main.grid_columnconfigure(0, weight=1)

    def draw_snipers(self):
        self.clear_main()
        main = self.draw_main()
        cfg = config.Config()

        self.current_page = "snipers"

        placeholder = "Paste your webhook here..."
        snipers = cfg.get_snipers()
        snipers_tk_entries = {}

        def save_sniper(sniper_name):
            sniper: config.Sniper = cfg.get_sniper(sniper_name)

            for key, entry in snipers_tk_entries[sniper_name].items():
                if key == "webhook":
                    if entry.get() != placeholder:
                        sniper.set_webhook(entry.get())
                elif key == "enabled":
                    if entry.instate(["selected"]):
                        sniper.enable()
                    else:
                        sniper.disable()
                else:
                    sniper.set(key, entry.instate(["selected"]))

            sniper.save()

        header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 15, 15), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        header_frame.grid(row=0, column=0, sticky=ttk.NSEW, pady=(0, 2))

        title = ttk.Label(header_frame, text=f"Snipers", font="-weight bold -size 20")
        title.configure(background=self.root.style.colors.get("secondary"))
        icon = ttk.Label(header_frame, image=self.snipers_icon)
        icon.configure(background=self.root.style.colors.get("secondary"))

        title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=15)
        icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)

        header_frame.grid_columnconfigure(1, weight=1)

        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35 // 2

        snipers_wrapper_frame = ttk.Frame(main, width=width)
        snipers_wrapper_frame.configure(style="default.TLabel")
        snipers_wrapper_frame.grid(row=1, column=0, sticky=ttk.NSEW, pady=13)
        main.grid_columnconfigure(0, weight=1)

        for index, sniper in enumerate(snipers):
            column = index % 2
            row = 1 + (index // 2)
            padding = (5, 2)

            snipers_tk_entries[sniper.name] = {}

            if column == 0:
                padding = (0, 2)
            elif column == 1:
                padding = ((5, 0), 2)

            # sniper_frame = ttk.Frame(snipers_wrapper_frame, width=width, style="secondary.TFrame")
            sniper_frame = RoundedFrame(
                snipers_wrapper_frame,
                radius=(15, 15, 15, 15),
                bootstyle="dark.TFrame",
                background=self.root.style.colors.get("dark")
                )
            sniper_frame.grid(row=row, column=column, sticky=ttk.NSEW, padx=padding[0], pady=padding[1])

            snipers_wrapper_frame.grid_columnconfigure(column, weight=1)

            sniper_title = ttk.Label(sniper_frame, text=f"{sniper.name.capitalize()} Sniper", font=("Arial", 16, "bold"))
            sniper_title.configure(background=self.root.style.colors.get("dark"))
            sniper_title.grid(row=0, column=0, sticky=ttk.NSEW, pady=(10, 0), padx=10)

            for index, (key, value) in enumerate(sniper.to_dict().items()):
                if isinstance(value, bool):
                    checkbox = ttk.Checkbutton(sniper_frame, text=" ".join(word.capitalize() for word in str(key).split("_")), style="success.TCheckbutton")
                    checkbox.grid(row=index + 1, column=0, sticky=ttk.W, pady=(5, 0), padx=13)

                    if value:
                        checkbox.invoke()
                    else:
                        for _ in range(2):
                            checkbox.invoke()

                    snipers_tk_entries[sniper.name][key] = checkbox
                else:
                    label = ttk.Label(sniper_frame, text=f"{key.capitalize()}")
                    label.configure(background=self.root.style.colors.get("dark"))

                    entry = ttk.Entry(sniper_frame, bootstyle="secondary")
                    if value != "":
                        entry.insert(0, value)
                    else:
                        entry.insert(0, placeholder)

                    label.grid(row=index + 1, column=0, sticky=ttk.W, pady=(8, 0), padx=10)
                    entry.grid(row=index + 2, column=0, sticky=ttk.EW, padx=10, columnspan=2)

                    sniper_frame.grid_columnconfigure(1, weight=1)

                    snipers_tk_entries[sniper.name][key] = entry

            row = len(sniper.to_dict()) + 2

            save_button = ttk.Button(sniper_frame, text="Save", style="success.TButton", command=lambda sniper_name=sniper.name: save_sniper(sniper_name))
            save_button.grid(row=row, column=0, sticky=ttk.EW, pady=(5, 10), padx=10, columnspan=2, ipady=5)

    def draw_theming(self):
        self.clear_main()
        main = self.draw_main()
        cfg = config.Config()

        self.current_page = "theming"

        themes = cfg.get_themes()
        theme_dict = cfg.theme.to_dict()
        theme_tk_entries = []

        def save_theme():
            for index, (key, value) in enumerate(theme_dict.items()):
                cfg.theme.set(key, theme_tk_entries[index].get())

            cfg.theme.save()

            # get the message style entry
            message_style = message_style_entry.cget("text")
            cfg.set("message_settings.style", message_style)

        def set_theme(theme):
            select_theme_menu.configure(text=theme)
            cfg.set_theme(theme)
            self.draw_theming()

        def delete_theme():
            double_check = ttk.Toplevel(self.root)

            double_check.title("Are you sure?")
            double_check.resizable(False, False)

            label = ttk.Label(double_check, text="Are you sure you want to delete this theme?")
            delete_button = ttk.Button(double_check, text="Yes", style="danger.TButton", command=lambda: delete(double_check))

            label.grid(row=0, column=0, sticky=ttk.NSEW, padx=10, pady=10)
            delete_button.grid(row=1, column=0, sticky=ttk.NSEW, padx=10, pady=10)

        def delete(toplevel):
            toplevel.destroy()

            if cfg.theme.name.lower() == "ghost":
                console.print_error("Cannot delete the default theme.")
                return

            cfg.delete_theme(cfg.theme.name)
            self.draw_theming()

        def create_theme(theme_name):
            if theme_name is None or theme_name == "":
                console.print_error("Please enter a theme name.")
                return

            success = cfg.create_theme(theme_name)

            if isinstance(success, bool) and not success:
                console.print_error("Theme already exists.")
                return

            cfg.set_theme(success.name)
            cfg.save()
            self.draw_theming()


        header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 0, 0), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        header_frame.grid(row=0, column=0, sticky=ttk.NSEW)

        title = ttk.Label(header_frame, text=f"Theming", font="-weight bold -size 20")
        title.configure(background=self.root.style.colors.get("secondary"))
        icon = ttk.Label(header_frame, image=self.theming_icon)
        icon.configure(background=self.root.style.colors.get("secondary"))

        title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=15)
        icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)

        header_frame.grid_columnconfigure(1, weight=1)

        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35

        # theme_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        theme_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        theme_frame.grid(row=1, column=0, sticky=ttk.NSEW)

        main.grid_columnconfigure(0, weight=1)

        create_theme_label = ttk.Label(theme_frame, text="Create a new theme")
        create_theme_label.configure(background=self.root.style.colors.get("dark"))

        create_theme_entry = ttk.Entry(theme_frame)
        create_theme_entry.config(style="secondary.TEntry")
        create_theme_button = ttk.Button(theme_frame, text="Create", style="success.TButton", command=lambda: create_theme(create_theme_entry.get()))

        create_theme_label.grid(row=0, column=0, sticky=ttk.W, padx=(10, 0), pady=(10, 0))
        create_theme_entry.grid(row=0, column=1, sticky="we", padx=(10, 10), pady=(10, 0))
        create_theme_button.grid(row=0, column=2, sticky=ttk.E, padx=(0, 11), pady=(10, 0))

        select_theme_label = ttk.Label(theme_frame, text="Select a theme")
        select_theme_label.configure(background=self.root.style.colors.get("dark"))

        select_theme_menu = ttk.Menubutton(theme_frame, text=cfg.theme.name, bootstyle="secondary")
        select_theme_menu.menu = ttk.Menu(select_theme_menu, tearoff=0)
        select_theme_menu["menu"] = select_theme_menu.menu

        for theme in themes:
            select_theme_menu.menu.add_command(label=str(theme), command=lambda theme=theme.name: set_theme(theme))

        message_style_label = ttk.Label(theme_frame, text="Global message style")
        message_style_label.configure(background=self.root.style.colors.get("dark"))

        message_style_entry = ttk.Menubutton(theme_frame, text=cfg.config["message_settings"]["style"], bootstyle="secondary")
        message_style_entry.menu = ttk.Menu(message_style_entry, tearoff=0)
        message_style_entry["menu"] = message_style_entry.menu

        for style in ["codeblock", "image", "embed"]:
            message_style_entry.menu.add_command(label=style, command=lambda style=style: message_style_entry.configure(text=style))

        select_theme_label.grid(row=1, column=0, sticky=ttk.W, padx=(10, 0), pady=(10, 0))
        select_theme_menu.grid(row=1, column=1, columnspan=2, sticky="we", padx=(10, 10), pady=(10, 0))

        message_style_label.grid(row=2, column=0, sticky=ttk.W, padx=(10, 0), pady=(10, 0))
        message_style_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=(10, 10), pady=(10, 0))

        # draw a horizontal line
        ttk.Separator(theme_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="we", padx=(10, 10), pady=(15, 5))

        for index, (key, value) in enumerate(theme_dict.items()):
            padding = (10, 2)
            entry = ttk.Entry(theme_frame, bootstyle="secondary")
            entry.insert(0, value)

            if index == 0:
                padding = (padding[0], (10, 2))
            elif index == len(theme_dict) - 1:
                padding = (padding[0], (2, 10))

            label = ttk.Label(theme_frame, text=key.capitalize())
            label.configure(background=self.root.style.colors.get("dark"))

            label.grid(row=index + 4, column=0, sticky=ttk.W, padx=padding[0], pady=padding[1])
            entry.grid(row=index + 4, column=1, columnspan=2, sticky="we", padx=padding[0], pady=padding[1])

            theme_frame.grid_columnconfigure(1, weight=1)
            theme_tk_entries.append(entry)

        ttk.Separator(theme_frame, orient="horizontal").grid(row=len(theme_dict) + 5, column=0, columnspan=3, sticky="we", padx=(10, 10), pady=(5, 15))

        save_theme_label = ttk.Label(theme_frame, text="Remember to save your changes!", font="-slant italic -size 14")
        save_theme_label.configure(background=self.root.style.colors.get("dark"))
        save_theme_button = ttk.Button(theme_frame, text="Save", style="success.TButton", command=save_theme)
        delete_theme_button = ttk.Button(theme_frame, text="Delete", style="danger.TButton", command=delete_theme)

        save_theme_label.grid(row=len(theme_dict) + 6, column=0, columnspan=2, sticky=ttk.W, padx=(10, 0), pady=(0, 10))
        save_theme_button.grid(row=len(theme_dict) + 6, column=1, sticky=ttk.E, padx=(0, 5), pady=(0, 10))
        delete_theme_button.grid(row=len(theme_dict) + 6, column=2, sticky=ttk.E, padx=(0, 11), pady=(0, 10))

    def draw_settings(self):
        self.clear_main()
        main = self.draw_main(scrollable=True)
        cfg = config.Config()
        
        self.current_page = "settings"

        config_tk_entries = {}
        config_entries = {
            "token": "Token",
            "prefix": "Prefix",
            "theme": "Theme",
            "rich_presence": "Enable rich presence",
            "gui": "Enable GUI",
            "rich_embed_webhook": "Rich embed webhook",
            "message_settings.auto_delete_delay": "Auto delete delay",
        }

        def save_cfg():
            for index, (key, value) in enumerate(config_entries.items()):
                tkinter_entry = config_tk_entries[key]

                if key == "rich_presence" or key == "theme" or key == "gui":
                    continue

                if key == "prefix":
                    self.bot.command_prefix = tkinter_entry.get()

                if "message_settings" in key:
                    if tkinter_entry.get().isdigit():
                        cfg.set(key, int(tkinter_entry.get()), save=False)
                    else:
                        console.print_error("Auto delete delay must be an integer.")
                        continue

                cfg.set(key, tkinter_entry.get())

            cfg.set("rich_presence.enabled", config_tk_entries["rich_presence"].instate(["selected"]), save=False)
            # cfg.set("gui", config_tk_entries["gui"].instate(["selected"]), save=False)

            cfg.save()
            cfg.check()

        # width = self.width - self.sidebar.winfo_reqwidth() + 50

        header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 0, 0), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        # header_frame.grid(row=0, column=0, sticky=ttk.NSEW)
        header_frame.pack(fill=ttk.BOTH, expand=True)
        title = ttk.Label(header_frame, text=f"Settings", font="-weight bold -size 20")
        title.configure(background=self.root.style.colors.get("secondary"))
        icon = ttk.Label(header_frame, image=self.settings_icon)
        icon.configure(background=self.root.style.colors.get("secondary"))

        title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=15)
        icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)

        header_frame.grid_columnconfigure(1, weight=1)

        # config_frame = ttk.Frame(main, style="secondary.TFrame")
        config_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        # config_frame.grid(row=1, column=0, sticky=ttk.EW, pady=(0, 15))
        config_frame.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        main.grid_columnconfigure(0, weight=1)

        for index, (key, value) in enumerate(config_entries.items()):
            if key == "rich_presence" or key == "gui":
                continue

            padding = (10, 2)
            cfg_value = cfg.get(key)
            entry = ttk.Entry(config_frame, bootstyle="secondary") if key != "token" else ttk.Entry(config_frame, bootstyle="secondary", show="*")
            if key == "theme":
                entry.insert(0, "Use theming page to edit your theme.")
                entry.configure(state="readonly")
            else:
                entry.insert(0, cfg_value)

            if index == 0:
                padding = (padding[0], (10, 2))
            elif index == len(config_entries) - 1:
                padding = (padding[0], (2, 5))

            label = ttk.Label(config_frame, text=value)
            label.configure(background=self.root.style.colors.get("dark"))

            label.grid(row=index + 1, column=0, sticky=ttk.W, padx=padding[0], pady=padding[1])
            entry.grid(row=index + 1, column=1, sticky="we", padx=padding[0], pady=padding[1], columnspan=3)

            config_frame.grid_columnconfigure(1, weight=1)
            config_tk_entries[key] = entry

        rpc_checkbox = ttk.Checkbutton(config_frame, text="Enable rich presence", style="success.TCheckbutton")
        rpc_checkbox.grid(row=len(config_entries) + 1, column=0, columnspan=2, sticky=ttk.W, padx=(13, 0), pady=(10, 0))
        if cfg.get("rich_presence")["enabled"]:
            rpc_checkbox.invoke()
        else:
            for _ in range(2):
                rpc_checkbox.invoke()

        gui_checkbox = ttk.Checkbutton(config_frame, text="Enable GUI", style="success.TCheckbutton")
        gui_checkbox.configure(state="disabled")
        gui_checkbox.grid(row=len(config_entries) + 2, column=0, columnspan=2, sticky=ttk.W, padx=(13, 0), pady=(10, 0))
        gui_checkbox.invoke()

        config_tk_entries["rich_presence"] = rpc_checkbox
        config_tk_entries["gui"] = gui_checkbox

        restart_required_label = ttk.Label(config_frame, text="A restart is required to apply changes!", font="-slant italic -size 14")
        restart_required_label.configure(background=self.root.style.colors.get("dark"))

        restart_required_label.grid(row=len(config_entries) + 3, column=0, columnspan=2, sticky=ttk.W, padx=(10, 0), pady=10)
        save_cfg_button = ttk.Button(config_frame, text="Save", style="success.TButton", command=save_cfg)
        save_cfg_button.grid(row=len(config_entries) + 3, column=3, sticky=ttk.E, padx=(0, 11), pady=10)

        # ------------------------------------------------------------------------------------------------------

        apis_header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 0, 0), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        # apis_header_frame.grid(row=2, column=0, sticky=ttk.NSEW)
        apis_header_frame.pack(fill=ttk.BOTH, expand=True)

        apis_title = ttk.Label(apis_header_frame, text=f"APIs", font="-weight bold -size 20")
        apis_title.configure(background=self.root.style.colors.get("secondary"))
        apis_icon = ttk.Label(apis_header_frame, image=self.apis_icon)
        apis_icon.configure(background=self.root.style.colors.get("secondary"))

        apis_title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=15)
        apis_icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)

        apis_header_frame.grid_columnconfigure(1, weight=1)

        # apis_frame = ttk.Frame(main, style="secondary.TFrame")
        apis_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        # apis_frame.grid(row=3, column=0, sticky=ttk.EW, pady=(0, 15))
        apis_frame.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        api_keys_tk_entries = {}
        api_keys_entries = {
            "serpapi": "SerpAPI",
        }

        def save_api_keys():
            for index, (key, value) in enumerate(api_keys_entries.items()):
                tkinter_entry = api_keys_tk_entries[key]
                cfg.set(f"apis.{key}", tkinter_entry.get())

            cfg.save()

        for index, (key, value) in enumerate(api_keys_entries.items()):
            padding = (10, 0)
            cfg_value = cfg.get(f"apis.{key}")
            entry = ttk.Entry(apis_frame, bootstyle="secondary", show="*")
            entry.insert(0, cfg_value)

            if index == 0:
                padding = (padding[0], (10, 0))
            elif index == len(api_keys_entries) - 1:
                padding = (padding[0], (0, 5))

            label = ttk.Label(apis_frame, text=value)
            label.configure(background=self.root.style.colors.get("dark"))

            label.grid(row=index + 1, column=0, sticky=ttk.W, padx=(10, 5), pady=padding[1])
            entry.grid(row=index + 1, column=1, sticky="we", padx=(0, 10), pady=padding[1], columnspan=2)

            apis_frame.grid_columnconfigure(1, weight=1)
            api_keys_tk_entries[key] = entry

        save_api_keys_button = ttk.Button(apis_frame, text="Save", style="success.TButton", command=save_api_keys)
        save_api_keys_button.grid(row=len(api_keys_entries) + 1, column=2, sticky=ttk.E, padx=(0, 11), pady=10)

        # ------------------------------------------------------------------------------------------------------

        session_spoofing_header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 0, 0), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        # session_spoofing_header_frame.grid(row=4, column=0, sticky=ttk.NSEW)
        session_spoofing_header_frame.pack(fill=ttk.BOTH, expand=True)

        session_spoofing_title = ttk.Label(session_spoofing_header_frame, text=f"Session Spoofing", font="-weight bold -size 20")
        session_spoofing_title.configure(background=self.root.style.colors.get("secondary"))
        session_spoofing_icon = ttk.Label(session_spoofing_header_frame, image=self.session_spoofing_icon)
        session_spoofing_icon.configure(background=self.root.style.colors.get("secondary"))

        session_spoofing_title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=15)
        session_spoofing_icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)

        session_spoofing_header_frame.grid_columnconfigure(1, weight=1)

        # session_spoofing_frame = ttk.Frame(main, style="secondary.TFrame")
        session_spoofing_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        # session_spoofing_frame.grid(row=5, column=0, sticky=ttk.EW)
        session_spoofing_frame.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))

        session_spoofing_checkbox = ttk.Checkbutton(session_spoofing_frame, text="Enable session spoofing", style="success.TCheckbutton")
        session_spoofing_checkbox.grid(row=0, column=0, columnspan=2, sticky=ttk.W, padx=(13, 0), pady=(10, 0))

        if cfg.get("session_spoofing")["enabled"]:
            session_spoofing_checkbox.invoke()
        else:
            for _ in range(2):
                session_spoofing_checkbox.invoke()

        session_spoofing_device_label = ttk.Label(session_spoofing_frame, text="Session spoofing device")
        session_spoofing_device_label.configure(background=self.root.style.colors.get("dark"))

        session_spoofing_device_entry = ttk.Menubutton(session_spoofing_frame, text=cfg.get("session_spoofing.device"), bootstyle="secondary")
        session_spoofing_device_entry.menu = ttk.Menu(session_spoofing_device_entry, tearoff=0)
        session_spoofing_device_entry["menu"] = session_spoofing_device_entry.menu

        for device in ["mobile", "desktop", "web", "embedded"]:
            session_spoofing_device_entry.menu.add_command(label=device, command=lambda device=device: session_spoofing_device_entry.configure(text=device))

        session_spoofing_device_label.grid(row=1, column=0, sticky=ttk.W, padx=(10, 0), pady=(5, 0))
        session_spoofing_device_entry.grid(row=1, column=1, sticky="we", padx=(10, 10), pady=(5, 0))

        def save_session_spoofing():
            cfg.set("session_spoofing.enabled", session_spoofing_checkbox.instate(["selected"]))
            cfg.set("session_spoofing.device", session_spoofing_device_entry.cget("text"))
            cfg.save()

        save_session_spoofing_button = ttk.Button(session_spoofing_frame, text="Save", style="success.TButton", command=save_session_spoofing)
        save_session_spoofing_button.grid(row=2, column=1, sticky=ttk.E, padx=(0, 11), pady=10)

        restart_required_label = ttk.Label(session_spoofing_frame, text="A restart is required to apply changes!", font="-slant italic -size 14")
        restart_required_label.configure(background=self.root.style.colors.get("dark"))

        restart_required_label.grid(row=2, column=0, sticky=ttk.W, padx=(10, 0), pady=10)

        session_spoofing_frame.grid_columnconfigure(1, weight=1)

    def draw_rich_presence(self):
        cfg = config.Config()
        rpc = cfg.get_rich_presence()
        
        self.clear_main()
        main = self.draw_main()
        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35
        
        self.current_page = "rpc"

        header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 0, 0), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        header_frame.grid(row=0, column=0, sticky=ttk.NSEW)

        title = ttk.Label(header_frame, text=f"Rich Presence", font="-weight bold -size 20")
        title.configure(background=self.root.style.colors.get("secondary"))
        icon = ttk.Label(header_frame, image=self.rich_presence_icon)
        icon.configure(background=self.root.style.colors.get("secondary"))

        title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=15)
        icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)

        header_frame.grid_columnconfigure(1, weight=1)
        
        # rpc_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        rpc_frame = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        rpc_frame.grid(row=1, column=0, sticky=ttk.EW)
        
        main.grid_columnconfigure(0, weight=1)
                
        rpc_entries = {
            "client_id": "Client ID",
            "details": "Details",
            "state": "State",
            "large_image": "Large Image Key",
            "large_text": "Large Text",
            "small_image": "Small Image Key",
            "small_text": "Small Text",
        }
        
        rpc_tk_entries = {}
        
        def save_rpc():
            for index, (key, value) in enumerate(rpc_entries.items()):
                tkinter_entry = rpc_tk_entries[key]
                rpc.set(key, tkinter_entry.get())
                
            rpc.save()
            
        for index, (key, value) in enumerate(rpc_entries.items()):
            padding = (10, 2)
            rpc_value = rpc.get(key)
            entry = ttk.Entry(rpc_frame, bootstyle="secondary")
            entry.insert(0, rpc_value)
            
            if index == 0:
                padding = (padding[0], (10, 2))
            elif index == len(rpc_entries) - 1:
                padding = (padding[0], (5, 2))
                
            label = ttk.Label(rpc_frame, text=value)
            label.configure(background=self.root.style.colors.get("dark"))
            
            label.grid(row=index + 1, column=0, sticky=ttk.W, padx=padding[0], pady=padding[1])
            entry.grid(row=index + 1, column=1, sticky="we", padx=padding[0], pady=padding[1], columnspan=3)
            
            rpc_frame.grid_columnconfigure(1, weight=1)
            rpc_tk_entries[key] = entry
            
        def reset_rpc():
            rpc.reset_defaults()
            self.draw_rich_presence()
        
        save_label = ttk.Label(rpc_frame, text="A restart is required to apply changes!", font="-slant italic -size 14")
        save_label.configure(background=self.root.style.colors.get("dark"))
        save_label.grid(row=len(rpc_entries) + 1, column=0, columnspan=2, sticky=ttk.W, padx=(10, 0), pady=10)
        
        save_rpc_button = ttk.Button(rpc_frame, text="Save", style="success.TButton", command=save_rpc)
        save_rpc_button.grid(row=len(rpc_entries) + 1, column=2, sticky=ttk.E, pady=10)
        
        reset_rpc_button = ttk.Button(rpc_frame, text="Reset", style="danger.TButton", command=reset_rpc)
        reset_rpc_button.grid(row=len(rpc_entries) + 1, column=3, sticky=ttk.E, padx=(5, 11), pady=10)

    def draw_onboarding(self):
        # resize the window
        self.root.minsize(450, 115)
        self.root.geometry("450x115")
        self.root.overrideredirect(False)

        self.center_window(450, 115)

        entry_frame = RoundedFrame(
            self.root, 
            radius=(15, 15, 15, 15), 
            bootstyle="dark.TFrame", 
            background=self.root.style.colors.get("dark")
            )
        
        entry_frame.pack(fill=ttk.BOTH, padx=30, pady=30)

        submit_button = ttk.Label(entry_frame, image=self.submit_icon)
        submit_button.configure(background=self.root.style.colors.get("dark"))
        submit_button.bind("<Button-1>", lambda event: submit_token())
        submit_button.bind("<Enter>", lambda event: submit_button.configure(cursor="hand2"))
        submit_button.bind("<Leave>", lambda event: submit_button.configure(cursor="arrow"))

        def submit_token():
            entry_text = entry.get()
            if entry_text == "Paste your token here...":
                console.print_error("Please paste your token.")
                return

            cfg = config.Config()
            cfg.set("token", entry_text)
            cfg.save()

            os.execl(sys.executable, sys.executable, *sys.argv)

        def focus_in(event):
            entry.delete(0, "end")
            entry.configure(foreground="white", show="*")

        def focus_out(event):
            entry.insert(0, "Paste your token here...")
            entry.configure(foreground="grey", show="")

        entry = ttk.Entry(entry_frame, bootstyle="dark")
        entry.insert(0, "Paste your token here...")
        entry.configure(foreground="grey")
        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)
        
        entry.grid(row=0, column=0, sticky=ttk.EW, padx=(10, 0), pady=10, columnspan=2)
        submit_button.grid(row=0, column=2, sticky=ttk.E, padx=(0, 20), pady=10)
        entry_frame.grid_columnconfigure(1, weight=1)

    def draw_loading(self, type="start"):
        self.root.minsize(400, 90)
        self.root.geometry("400x90")
        self.root.overrideredirect(False)

        self.center_window(400, 90)

        loading_label = ttk.Label(self.root, text="Ghost is starting..." if type == "start" else "Ghost is restarting...", font="-weight bold -size 20", anchor="center")
        loading_label.pack(fill=ttk.BOTH, padx=30, pady=30, anchor="center")
        self.root.pack_propagate(False)

    def run_without_bot(self):
        self.draw_sidebar()
        self.draw_home()
        self.root.mainloop()

    def run(self):
        cfg = config.Config()

        if cfg.get("gui"):
            if cfg.get("token") == "":
                self.start_button.destroy()
                self.load_images()
                self.draw_onboarding()
            else:
                self.start_button.invoke()
                self.start_button.destroy()

                self.center_window()
                self.draw_loading()

            self.root.mainloop()
        else:
            self.start_bot_thread()

    def check_bot_started(self):
        if self.bot.is_ready():
            self.bot_started = True
            self.root.after(0, self.on_bot_ready)
        else:
            self.root.after(500, self.check_bot_started)

    def on_bot_ready(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.minsize(600, 520)
        self.root.geometry(f"{600}x{520}")
        self.center_window(600, 520)
        self.load_images()

        self.root.after(0, self.save_avatar)
        self.root.after(0, self.draw_sidebar)
        self.root.after(0, self.draw_home)

        self.root.after(500, self.update_console)

    def start_bot_thread(self):
        if not self.bot_started:
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            self.root.after(0, self.check_bot_started)

    def run_bot(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.bot_start())

    async def bot_start(self):
        cfg = config.Config()
        self.bot_started = True
        try:
            console.print_info("Starting Ghost...")
            await self.bot.start(cfg.get("token"), reconnect=True)
        except discord.errors.LoginFailure:
            console.print_error("Failed to login, reset token and showing onboarding again...")
            cfg.set("token", "")
            cfg.save()
            os.execl(sys.executable, sys.executable, *sys.argv)

    def hide_all_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    async def stop_bot(self):
        self.bot_started = False
        console.print_info("Stopping Ghost...")
        await self.bot.close()
        console.print_success("Ghost stopped!")

        # Cancel all remaining tasks in the event loop
        console.print_info("Cancelling all remaining tasks...")
        loop = self.bot.loop
        tasks = [task for task in asyncio.all_tasks(loop) if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
            console.print_success(f"Cancelled task: {task}")
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Properly stop the event loop
        console.print_info("Stopping the event loop...")
        loop.stop()
        console.print_success("Event loop stopped!")

    async def _restart_bot(self):
        cfg = config.Config()
        # console.print_info("Calling stop_bot()...")
        # await self.stop_bot()
        # console.print_info("Bot stopped!")

        # Create a fresh bot instance

        await self.bot.close()

        console.print_info("Creating a new bot instance...")
        from ghost import ghost
        self.bot = ghost(command_prefix=config.Config().get("prefix"), self_bot=True, help_command=None)
        console.print_info("New bot instance created!")

        # Start the bot
        console.print_info("Starting the bot...")
        self.bot_started = True
        await self.bot.start(cfg.get("token"), reconnect=True)
        console.print_success("Bot started!")

    def restart_bot(self):
        """Handles the bot restart from the main thread."""
        if self.bot_started:
            self.hide_all_ui()

            loop = self.bot.loop
            loop.create_task(self.stop_bot())
            
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            new_loop.run_until_complete(self._restart_bot())

if __name__ == "__main__":
    gui = GhostGUI()
    gui.run_without_bot()