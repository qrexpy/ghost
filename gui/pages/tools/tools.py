import os, sys
import ttkbootstrap as ttk

from gui.components import RoundedFrame
from gui.pages.tools.spypet_page import SpyPetPage
from gui.pages.tools.message_logger_page import MessageLoggerPage
from gui.pages.tools.user_lookup_page import UserLookupPage

class ToolsPage:
    def __init__(self, root, bot_controller, images, layout):
        self.root = root
        self.bot_controller = bot_controller
        self.images = images
        self.layout = layout
        
        self.spypet_page = SpyPetPage(self, root, bot_controller, images, layout)
        self.message_logger_page = MessageLoggerPage(self, root, bot_controller, images, layout)
        self.user_lookup_page = UserLookupPage(self, root, bot_controller, images, layout)
        
        self.pages = [
            {
                "name": "ghetto spy.pet",
                "description": "A tool to look up every message sent by a user you share mutual servers with.",
                "page": self.spypet_page,
                "command": self.draw_spypet
            },
            {
                "name": "Message Logger",
                "description": "A tool to log deleted messages from every server you're in.",
                "page": self.message_logger_page,
                "command": self.draw_message_logger
            },
            {
                "name": "User Lookup",
                "description": "A tool to look up a user's information.",
                "page": self.user_lookup_page,
                "command": self.draw_user_lookup
            }
        ]
        
    def draw_spypet(self):
        self.layout.sidebar.set_current_page("tools")
        self.layout.clear()
        main = self.layout.main()
        self.spypet_page.draw(main)
        # 🔧 FIX: re-fetch main each time
        self.layout.sidebar.set_button_command("tools", self.draw_spypet)
        
    def draw_message_logger(self):
        self.layout.sidebar.set_current_page("tools")
        self.layout.clear()
        main = self.layout.main()
        self.message_logger_page.draw(main)
        # 🔧 FIX: re-fetch main each time
        self.layout.sidebar.set_button_command("tools", self.draw_message_logger)
        
    def draw_user_lookup(self):
        self.layout.sidebar.set_current_page("tools")
        self.layout.clear()
        main = self.layout.main()
        self.user_lookup_page.draw(main)
        # 🔧 FIX: re-fetch main each time
        self.layout.sidebar.set_button_command("tools", self.draw_user_lookup)
        
    def draw(self, parent):
        
        
        for page in self.pages:
            page_wrapper = RoundedFrame(parent, radius=10, bootstyle="dark.TFrame")
            page_wrapper.pack(fill="x", expand=True, pady=(0, 10))
            page_wrapper.bind("<Button-1>", lambda e, cmd=page["command"]: cmd())

            page_title = ttk.Label(page_wrapper, text=page["name"], font=("Host Grotesk", 14 if sys.platform != "darwin" else 20, "bold"))
            page_title.configure(background=self.root.style.colors.get("dark"))
            page_title.grid(row=0, column=0, sticky=ttk.NSEW, padx=15, pady=(15, 5))
            page_title.bind("<Button-1>", lambda e, cmd=page["command"]: cmd())

            page_description = ttk.Label(page_wrapper, text=page["description"], font=("Host Grotesk", 12 if sys.platform != "darwin" else 16), wraplength=450)
            page_description.configure(background=self.root.style.colors.get("dark"))
            page_description.grid(row=1, column=0, sticky=ttk.NSEW, padx=15, pady=(0, 15))
            page_description.bind("<Button-1>", lambda e, cmd=page["command"]: cmd())
            
            # page_icon = ttk.Label(self.header, image=self.header_icon)
            # page_icon.configure(background=self.root.style.colors.get("secondary"))
            # page_icon.grid(row=0, column=2, sticky=ttk.E, padx=(0, 15), pady=15)