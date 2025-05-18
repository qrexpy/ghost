import sys
import ttkbootstrap as ttk

class LoadingPage:
    def __init__(self, root):
        self.root = root
        self.width = 400
        self.height = 90
        
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def draw(self, type="start"):
        loading_label = ttk.Label(self.root, text="Ghost is starting..." if type == "start" else "Ghost is restarting...", font=("Host Grotesk", 14 if sys.platform != "darwin" else 20, "bold"), anchor="center")
        loading_label.pack(fill=ttk.BOTH, padx=30, pady=30, anchor="center")
        self.root.pack_propagate(False)
        
        return loading_label