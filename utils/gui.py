# anyone reading this, i sincerely apologize for the mess you're about to witness
# tkinter sucks and i hate it

import os
import sys
import discord
import requests
import threading
import ttkbootstrap as ttk

from utils import console
from utils import config
from utils import files

from pathlib import Path
from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText
from PIL import Image, ImageTk, ImageOps

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
        self.height = 500
        self.bot_started = False
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

        icon_size = (20, 20)
        home_icon = files.resource_path("data/icons/house-solid.png")
        settings_icon = files.resource_path("data/icons/gear-solid.png")
        theming_icon = files.resource_path("data/icons/paint-roller-solid.png")
        snipers_icon = files.resource_path("data/icons/crosshairs-solid.png")
        rich_presence_icon = files.resource_path("data/icons/discord-brands-solid.png")
        logout_icon = files.resource_path("data/icons/power-off-solid.png")
        apis_icon = files.resource_path("data/icons/cloud-solid.png")
        session_spoofing_icon = files.resource_path("data/icons/shuffle-solid.png")
        submit_icon = files.resource_path("data/icons/arrow-right-solid.png")

        self.home_icon = ImageTk.PhotoImage(Image.open(home_icon).resize(icon_size))
        self.settings_icon = ImageTk.PhotoImage(Image.open(settings_icon).resize(icon_size))
        self.theming_icon = ImageTk.PhotoImage(Image.open(theming_icon).resize(icon_size))
        self.snipers_icon = ImageTk.PhotoImage(Image.open(snipers_icon).resize(icon_size))
        self.rich_presence_icon = ImageTk.PhotoImage(Image.open(rich_presence_icon).resize(icon_size))
        self.logout_icon = ImageTk.PhotoImage(Image.open(logout_icon).resize(icon_size))
        self.apis_icon = ImageTk.PhotoImage(Image.open(apis_icon).resize(icon_size))
        self.session_spoofing_icon = ImageTk.PhotoImage(Image.open(session_spoofing_icon).resize(icon_size))
        self.submit_icon = ImageTk.PhotoImage(Image.open(submit_icon).resize((10, 10)))

        # self.root.style.configure("primary.TButton", background="#254bff")
        # self.root.style.configure("secondary.TButton", background="#383838")
        # self.root.style.configure("success.TButton", background="#00db7c")
        # self.root.style.configure("danger.TButton", background="#e7230f")
        # self.root.style.configure("warning.TButton", background="#f39500")

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

        close_button = ttk.Label(titlebar, text="x")
        close_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        close_button.bind("<Button-1>", lambda e: self.quit())

        title.pack(side=ttk.LEFT, padx=10)
        minimise_button.pack(side=ttk.RIGHT, padx=10)
        close_button.pack(side=ttk.RIGHT, padx=10)

    def draw_sidebar(self):
        # self.draw_titlebar()

        width = self.width // (self.width // 65)
        self.sidebar = ttk.Frame(self.root, width=width, height=self.height)
        self.sidebar.pack(fill=ttk.BOTH, side=ttk.LEFT)
        self.sidebar.configure(style="dark.TFrame")
        self.sidebar.grid_propagate(False)

        home_button = ttk.Label(self.sidebar, image=self.home_icon)
        home_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        home_button.bind("<Button-1>", lambda e: self.draw_home())

        settings_button = ttk.Label(self.sidebar, image=self.settings_icon)
        settings_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        settings_button.bind("<Button-1>", lambda e: self.draw_settings())

        theming_button = ttk.Label(self.sidebar, image=self.theming_icon)
        theming_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        theming_button.bind("<Button-1>", lambda e: self.draw_theming())

        snipers_button = ttk.Label(self.sidebar, image=self.snipers_icon)
        snipers_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        snipers_button.bind("<Button-1>", lambda e: self.draw_snipers())

        rich_presence_button = ttk.Label(self.sidebar, image=self.rich_presence_icon)
        rich_presence_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        rich_presence_button.bind("<Button-1>", lambda e: self.draw_rich_presence())

        logout_button = ttk.Label(self.sidebar, image=self.logout_icon)
        logout_button.configure(background=self.root.style.colors.get("dark"), anchor="center")
        logout_button.bind("<Button-1>", lambda e: self.quit())

        home_button.grid(row=0, column=0, sticky=ttk.NSEW, pady=(10, 2), padx=10, ipady=12)
        settings_button.grid(row=1, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=12)
        theming_button.grid(row=2, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=12)
        snipers_button.grid(row=3, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=12)
        rich_presence_button.grid(row=4, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=12)
        logout_button.grid(row=6, column=0, sticky=ttk.NSEW, pady=(2, 10), padx=10, ipady=12)

        self.sidebar.grid_rowconfigure(5, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

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

    def add_console(self, prefix, text):
        time = console.get_formatted_time()
        self.console.append((time, prefix, text))

    def update_console(self):
        self.visible_console_lines = self.console[-20:]

        try:
            self.console_inner_wrapper.delete(1.0, "end")
            for index, (time, prefix, text) in enumerate(self.console):
                self.console_inner_wrapper.insert("end", f"[{time}] [{prefix}] {text}\n")
                self.console_inner_wrapper.see("end")

        except Exception as e:
            pass

        self.root.after(500, self.update_console)

    def draw_home(self):
        self.clear_main()
        main = self.draw_main()
        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35

        # header_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        # header_frame.pack(fill=ttk.BOTH)

        header_frame = RoundedFrame(
            main, 
            radius=(15, 15, 0, 0), 
            bootstyle="secondary.TFrame", 
            background=self.root.style.colors.get("secondary")
            )
        header_frame.pack(fill=ttk.BOTH)

        title = ttk.Label(header_frame, text=f"Ghost v{config.VERSION}", font="-weight bold -size 20")
        title.configure(background=self.root.style.colors.get("secondary"))
        subtitle = ttk.Label(header_frame, text=config.MOTD, font="-slant italic -size 14")
        subtitle.configure(background=self.root.style.colors.get("secondary"))

        title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=(15, 0))
        subtitle.grid(row=1, column=0, columnspan=2, sticky=ttk.NSEW, padx=15, pady=(0, 15))

        # title.pack(fill=ttk.BOTH, padx=15, pady=(15, 0))
        # subtitle.pack(fill=ttk.BOTH, padx=15, pady=(0, 15))

        # console_textarea = ttk.Frame(main, width=width)
        # console_textarea.configure(style="dark.TFrame")
        console_textarea = RoundedFrame(
            main,
            radius=(0, 0, 15, 15),
            bootstyle="dark.TFrame",
            background=self.root.style.colors.get("dark")
            )
        console_textarea.pack(fill="both", expand=True)

        self.console_inner_wrapper = ttk.Text(console_textarea, wrap="word", height=20, font=("Menlo", 12))
        self.console_inner_wrapper.config(
            border=0, 
            background=self.root.style.colors.get("dark"), 
            foreground="lightgrey", 
            highlightcolor=self.root.style.colors.get("dark"), 
            highlightbackground=self.root.style.colors.get("dark")
            )
        self.console_inner_wrapper.pack(fill="both", expand=True, padx=5, pady=10)

        self.root.after(500, self.update_console)

        main.grid_columnconfigure(0, weight=1)

    def draw_snipers(self):
        self.clear_main()
        main = self.draw_main()
        cfg = config.Config()

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

        # title = ttk.Label(main, text="Snipers", font="-weight bold -size 20")
        # title.grid(row=0, column=0, sticky=ttk.NSEW)

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
            cfg.set("gui", config_tk_entries["gui"].instate(["selected"]), save=False)

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
        if cfg.get("gui"):
            gui_checkbox.invoke()
        else:
            for _ in range(2):
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

        if cfg.get("session_spoofing"):
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

    def run_without_bot(self):
        self.draw_sidebar()
        self.draw_home()
        self.root.mainloop()

    def run(self):
        cfg = config.Config()

        if cfg.get("gui"):
            if cfg.get("token") == "":
                self.draw_onboarding()
            else:
                bot_start_btn = ttk.Button(self.root, text="Start Ghost", command=self.start_bot_thread)
                bot_start_btn.pack(fill=ttk.BOTH, side=ttk.BOTTOM, pady=10)

                bot_start_btn.invoke()
                bot_start_btn.destroy()

                while not self.bot_started:
                    pass
                
                self.center_window()
                self.draw_sidebar()
                self.draw_home()

                self.root.after(500, self.update_console)
            self.root.mainloop()
        else:
            self.start_bot()

    def start_bot(self):
        cfg = config.Config()

        try:
            console.print_info("Starting Ghost...")
            self.bot.run(cfg.get("token"), log_handler=console.handler)
        except discord.errors.LoginFailure:
            console.print_error("Failed to login, reset token and showing onboarding again...")
            cfg.set("token", "")
            cfg.save()
            os.execl(sys.executable, sys.executable, *sys.argv)

    def start_bot_thread(self):
        self.thread = threading.Thread(target=self.start_bot)
        self.thread.start()

if __name__ == "__main__":
    gui = GhostGUI()
    gui.run_without_bot()