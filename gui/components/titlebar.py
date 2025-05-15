import ttkbootstrap as ttk

class Titlebar:
    def __init__(self, root):
        self.root = root
        self._offset_x = 0
        self._offset_y = 0

    def _on_press(self, event):
        self._offset_x = event.x_root - self.root.winfo_x()
        self._offset_y = event.y_root - self.root.winfo_y()
        
        event.widget.grab_set()
        
        self.root.bind("<Motion>", self._move_window)
        self.root.bind("<ButtonRelease-1>", self._on_release)

    def _move_window(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        self.root.geometry(f"+{x}+{y}")

    def _on_release(self, event):
        self.root.unbind("<Motion>")
        self.root.unbind("<ButtonRelease-1>")
        self.root.grab_release()
        
    def draw(self):
        titlebar = ttk.Frame(self.root, style="dark.TFrame")
        inner_wrapper = ttk.Frame(titlebar, style="dark.TFrame")
        inner_wrapper.pack(fill=ttk.BOTH, expand=True, pady=5, padx=10)
        
        titlebar.bind("<Button-1>", self._on_press)
        inner_wrapper.bind("<Button-1>", self._on_press)
        
        title = ttk.Label(inner_wrapper, text="Ghost")
        title.configure(background=self.root.style.colors.get("dark"))
        title.pack(side=ttk.LEFT)
        
        return titlebar