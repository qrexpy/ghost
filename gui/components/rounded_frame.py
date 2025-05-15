import ttkbootstrap as ttk

class RoundedFrame(ttk.Canvas):
    def __init__(self, parent, radius=(25, 25, 25, 25), **kwargs):
        canvas_kwargs = {}
        for key in kwargs:
            if key not in ["padx", "pady", "bootstyle", "style", "background", "parent_background"]:
                canvas_kwargs[key] = kwargs[key]
        super().__init__(parent, highlightthickness=0, bd=0, **canvas_kwargs)
        
        bootstyle = kwargs.get("bootstyle") or kwargs.get("style") or "primary.TButton"
        self.parent = parent
        self.radius = radius if not isinstance(radius, int) else (radius, radius, radius, radius)
        self.root = parent.winfo_toplevel()
        self.style = self.root.style
        self.frame_background = self.style.colors.get(bootstyle.split(".")[0]) if kwargs.get("background") is None else kwargs.get("background")
        self.parent_background = self._get_parent_background() if kwargs.get("parent_background") is None else kwargs.get("parent_background")
        
        self.configure(background=self.parent_background)
        self.inner_frame = ttk.Frame(self)
        self.create_window(0, 0, window=self.inner_frame, anchor="nw")

        self.bind("<Configure>", self.on_resize)

    def _get_parent_background(self):
        parent = self.parent
        
        if isinstance(parent, ttk.Frame):
            style = parent.cget("style")
            return self.style.lookup(style, "background")
        elif isinstance(parent, RoundedFrame):
            return parent.frame_background
        else:
            try:
                return parent.cget("background")
            except:
                return self.style.colors.get("dark")

    def on_resize(self, event=None):
        self.delete("all")

        width, height = self.winfo_width(), self.winfo_height()
        if width < 2 or height < 2:
            return

        width -= 1
        height -= 1

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
        self.create_polygon(points, smooth=True, fill=self.frame_background, outline=self.frame_background)

        try:
            self.itemconfig(self.inner_frame, width=width, height=height)
        except Exception as e:
            pass
        
    def set_corner_radius(self, radius):
        self.radius = radius
        self.on_resize()
        
    def set_background(self, background):
        self.frame_background = background
        self.on_resize()