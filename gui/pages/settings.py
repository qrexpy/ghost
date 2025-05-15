import ttkbootstrap as ttk
from gui.components.settings import GeneralPanel, ThemingPanel, APIsPanel, SessionSpoofingPanel, RichPresencePanel, SnipersPanel
from gui.helpers import Images
from utils.config import Config

class SettingsPage:
    def __init__(self, root, bot_controller):
        self.root = root
        self.bot_controller = bot_controller
        self.width = root.winfo_width()
        self.height = root.winfo_height()
        self.parent = None
        self.images = Images()
        self.cfg = Config()
        self.cfg.subscribe(self)
        
    def refresh_config(self):
        if not self.parent:
            return
        
        try:
            for widget in self.parent.winfo_children():
                widget.destroy()
                
            if self.parent: self.parent.update_idletasks()
            self.draw(self.parent)
        except:
            pass
          
    def draw(self, parent):
        self.parent = parent
        
        general = GeneralPanel(self.root, parent, self.bot_controller, self.images, self.cfg).draw()
        general.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        
        theming = ThemingPanel(self.root, parent, self.images, self.cfg).draw()
        theming.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        
        apis = APIsPanel(self.root, parent, self.images, self.cfg).draw()
        apis.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        
        session_spoofing = SessionSpoofingPanel(self.root, parent, self.images, self.cfg).draw()
        session_spoofing.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        
        rpc = RichPresencePanel(self.root, parent, self.images, self.cfg).draw()
        rpc.pack(fill=ttk.BOTH, expand=True, pady=(0, 15))
        
        snipers = SnipersPanel(self.root, parent, self.images, self.cfg).draw()
        snipers.pack(fill=ttk.BOTH, expand=True)