import os
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from gui.helpers import Images

class Sidebar:
    def __init__(self, root):
        self.root = root
        self.images = Images()
        self.current_page = None
        self.button_cmds = {}
        self.tk_buttons = []
        self.sidebar = None
        
        root_width = 600
        self.width = root_width // (root_width // 65)
        
    def add_button(self, page_name, command):
        self.button_cmds[page_name] = command
        
    def set_current_page(self, page_name):
        self.current_page = page_name
    
    def _hover_enter(self, button, page_name):
        background = "#242424" if self.current_page != page_name else self.root.style.colors.get("secondary")
        button.configure(background=background)
        
    def _hover_leave(self, button, page_name):
        background = self.root.style.colors.get("dark") if self.current_page != page_name else self.root.style.colors.get("secondary")
        button.configure(background=background)
    
    def _create_button(self, image, page_name, command, row):
        is_selected = self.current_page == page_name
        bg_color = self.root.style.colors.get("secondary") if is_selected else self.root.style.colors.get("dark")
        
        button = ttk.Label(self.sidebar, image=image, background=bg_color, anchor="center")
        button.bind("<Button-1>", lambda e: self._update_page(command, page_name))
        button.bind("<Enter>", lambda e: self._hover_enter(button, page_name))
        button.bind("<Leave>", lambda e: self._hover_leave(button, page_name))
        button.grid(row=row, column=0, sticky=ttk.NSEW, pady=(10, 2) if row == 0 else 2, ipady=12)
        
        self.tk_buttons.append(button)
        
    def set_button_command(self, page_name, command):
        if page_name in self.button_cmds:
            self.button_cmds[page_name] = command
        else:
            raise ValueError(f"Button '{page_name}' not found in sidebar.")
        
    def _quit(self):
        if str(Messagebox.yesno("Are you sure you want to quit?", title="Ghost")).lower() == "yes":
            if os.name == "nt":
                os.kill(os.getpid(), 9)
            else:
                os._exit(0)
                
    def disable(self):
        allowed = ["home", "console"]
        
        for button in self.tk_buttons:
            if str(button) in self.root.tk.call("winfo", "children", self.sidebar):  
                if button.cget("image") not in [self.images.get("home"), self.images.get("console")]:
                    button.unbind("<Button-1>")
                    button.unbind("<Enter>")
                    button.unbind("<Leave>")
        
    def draw(self):
        self.sidebar = ttk.Frame(self.root, width=self.width, height=self.root.winfo_height(), style="dark.TFrame")
        # self.sidebar.pack(side=ttk.LEFT, fill=ttk.BOTH)
        self.sidebar.grid_propagate(False)
    
        self.buttons = {
            "home": self._create_button(self.images.get("home"), "home", self.button_cmds["home"], 0),
            "console": self._create_button(self.images.get("console"), "console", self.button_cmds["console"], 1),
            "settings": self._create_button(self.images.get("settings"), "settings", self.button_cmds["settings"], 2),
            "scripts": self._create_button(self.images.get("scripts"), "scripts", self.button_cmds["scripts"], 3),
            "tools": self._create_button(self.images.get("tools"), "tools", self.button_cmds["tools"], 4),
        }
            
        logout_btn = ttk.Label(self.sidebar, image=self.images.get("logout"), background=self.root.style.colors.get("dark"), anchor="center")
        logout_btn.bind("<Button-1>", lambda e: self._quit())
        logout_btn.bind("<Enter>", lambda e: self._hover_enter(logout_btn, "logout"))
        logout_btn.bind("<Leave>", lambda e: self._hover_leave(logout_btn, "logout"))
        logout_btn.grid(row=len(self.buttons) + 2, column=0, sticky=ttk.NSEW, pady=10, ipady=12)
        
        self.sidebar.grid_rowconfigure(len(self.buttons) + 1, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        return self.sidebar
        
    def _update_page(self, command, page_name):
        if self.current_page == page_name:
            return
        
        self.current_page = page_name
        command()