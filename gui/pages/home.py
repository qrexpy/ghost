import webbrowser, discord, sys
import ttkbootstrap as ttk
import tkinter.font as tkFont
from ttkbootstrap.scrolled import ScrolledFrame
from gui.components import RoundedFrame, RoundedButton
from gui.helpers import Images
from utils.config import VERSION, CHANGELOG, MOTD, Config

class HomePage:
    def __init__(self, root, bot_controller, _restart_bot):
        self.root = root
        self.bot_controller = bot_controller
        self._restart_bot = _restart_bot
        self.width = root.winfo_width()
        self.height = root.winfo_height()
        self.restart = False
        self.avatar = None
        self.avatars = {}
        self.images = Images()
        self.cfg = Config()
                
        self.discord_logs_wrapper = None
        self.discord_logs_footer = None
        # self.discord_logs_textbox = None
        self.discord_logs_inner_wrapper = None
        self.discord_logs_max = False
        self.discord_logs_max_min_btn = None
        self.discord_logs_frame = None
        self.discord_logs = []
        
        self.details_wrapper = None
        self.friends_label = None
        self.guilds_label = None
        self.uptime_label = None
        self.latency_label = None
        
        self.restart_title = None
        self.restart_title_elipsis = "..."
        
        self.root.bind("<Configure>", self._update_wraplength)
        
    def _clear_everything(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def _update_restart_title(self):
        if self.restart:
            if len(self.restart_title_elipsis) == 3:
                self.restart_title_elipsis = "."
            else:
                self.restart_title_elipsis += "."
            self.restart_title.config(text=f"Ghost is restarting{self.restart_title_elipsis}")
        self.root.after(750, self._update_restart_title)
        
    def _update_account_details(self):
        try:
            if not self.restart:
                self.friends_label.config(text=f"Friends: {len(self.bot_controller.get_friends())}")
                self.guilds_label.config(text=f"Guilds: {len(self.bot_controller.get_guilds())}")
        except:
            pass
        self.root.after(1000, self._update_account_details)
        
    def _update_bot_details(self):
        try:
            if not self.restart:
                self.uptime_label.config(text=f"Uptime: {self.bot_controller.get_uptime()}")
                self.latency_label.config(text=f"Latency: {self.bot_controller.get_latency()}")
        except:
            pass
        self.root.after(1000, self._update_bot_details)
        
    def _draw_restart_button(self, parent, disabled=False):
        def _hover_enter(_):
            frame.set_background(background="#322bef")
            restart_label.configure(background="#322bef")
            
        def _hover_leave(_):
            frame.set_background(background=self.root.style.colors.get("primary"))
            restart_label.configure(background=self.root.style.colors.get("primary"))
        
        frame = RoundedFrame(parent, radius=(8, 8, 8, 8), bootstyle="primary.TButton" if not disabled else "disabled.TButton")
        
        restart_label = ttk.Label(frame, image=self.images.get("restart"), anchor="center")
        restart_label.configure(background=self.root.style.colors.get("primary") if not disabled else self.root.style.colors.get("disabled"))
        # restart_label.configure(background=self.root.style.colors.get("secondary"))
        restart_label.pack(anchor="center", fill=ttk.BOTH, expand=False, padx=25, pady=10)
        
        if not disabled:
            restart_label.bind("<Button-1>", lambda e: self._restart_bot())
            restart_label.bind("<Enter>", _hover_enter)
            restart_label.bind("<Leave>", _hover_leave)
            frame.bind("<Button-1>", lambda e: self._restart_bot())
            frame.bind("<Enter>", _hover_enter)
            frame.bind("<Leave>", _hover_leave)
        
        return frame
        
    def _draw_header(self, parent):
        wrapper = RoundedFrame(parent, radius=(15, 15, 15, 15), bootstyle="secondary.TFrame")
        wrapper.pack(fill=ttk.BOTH, expand=False)
        
        if self.avatar and not self.restart:
            avatar = ttk.Label(wrapper, image=self.avatar)
            avatar.configure(background=self.root.style.colors.get("secondary"))
            avatar.grid(row=0, column=0, sticky=ttk.W, padx=(15, 10), pady=15, rowspan=2)
            
        if not self.restart:
            display_name = ttk.Label(wrapper, text=self.bot_controller.get_user().display_name, font=("Host Grotesk", 16 if sys.platform != "darwin" else 20, "bold"))
            display_name.configure(background=self.root.style.colors.get("secondary"))
            display_name.grid(row=0, column=1, sticky=ttk.W, pady=(15, 0))

            username = ttk.Label(wrapper, text=self.bot_controller.get_user().name, font=("Host Grotesk", 12 if sys.platform != "darwin" else 14, "italic"))
            username.configure(background=self.root.style.colors.get("secondary"), foreground="lightgrey")
            username.grid(row=1, column=1, sticky=ttk.W, pady=(0, 15))
            
            # restart_btn = self._draw_restart_button(wrapper)
            # restart_btn.grid(row=0, column=3, rowspan=2, sticky=ttk.EW, padx=(10, 16), pady=(10, 10))
            restart_btn = RoundedButton(wrapper, radius=8, bootstyle="primary.TButton", command=lambda _: self._restart_bot(), image=self.images.get("restart"), padx=15, pady=6)
            restart_btn.grid(row=0, column=3, rowspan=2, sticky=ttk.EW, padx=(10, 16), pady=(10, 10))
            
            wrapper.grid_columnconfigure(2, weight=1)
        else:
            self.restart_title = ttk.Label(wrapper, text="Ghost is restarting...", font=("Host Grotesk", 14 if sys.platform != "darwin" else 20, "bold"), anchor="center")
            self.restart_title.configure(background=self.root.style.colors.get("secondary"))
            self.restart_title.grid(row=0, column=0, sticky=ttk.NSEW, pady=26, padx=15, columnspan=2)
            wrapper.grid_columnconfigure(0, weight=1)
            self.root.after(750, self._update_restart_title)
    
    def _draw_details_wrapper(self, parent):
        wrapper = ttk.Frame(parent, width=self.width)
        wrapper.configure(style="default.TLabel")
        wrapper.pack(fill=ttk.BOTH, expand=False, pady=(10, 0))
        
        wrapper.grid_rowconfigure(0, weight=1)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_columnconfigure(1, weight=1)
        
        return wrapper
    
    def _draw_account_details(self, parent):
        wrapper = RoundedFrame(parent, radius=(15, 15, 15, 15), bootstyle="dark.TFrame")
        wrapper.grid(row=0, column=0, sticky=ttk.NSEW, padx=(0, 5), pady=(0, 5))
        
        if self.restart:
            return
        
        title = ttk.Label(wrapper, text="Discord", font=("Host Grotesk", 14 if sys.platform != "darwin" else 20, "bold"))
        title.configure(background=self.root.style.colors.get("dark"))
        title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=(10, 0))
        
        ttk.Separator(wrapper, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="we", padx=(10, 10), pady=5)
        wrapper.grid_columnconfigure(1, weight=1)
        
        self.friends_label = ttk.Label(wrapper, text=f"Friends: {len(self.bot_controller.get_friends())}", font=("Host Grotesk", 12 if sys.platform != "darwin" else 14))
        self.friends_label.configure(background=self.root.style.colors.get("dark"), foreground="white" if not self.restart else "lightgrey")
        self.friends_label.grid(row=2, column=0, sticky=ttk.W, padx=10, pady=(5, 0))
        
        self.guilds_label = ttk.Label(wrapper, text=f"Guilds: {len(self.bot_controller.get_guilds())}", font=("Host Grotesk", 12 if sys.platform != "darwin" else 14))
        self.guilds_label.configure(background=self.root.style.colors.get("dark"), foreground="white" if not self.restart else "lightgrey")
        self.guilds_label.grid(row=3, column=0, sticky=ttk.W, padx=10, pady=(0, 10))
        
    def _draw_bot_details(self, parent):
        wrapper = RoundedFrame(parent, radius=(15, 15, 15, 15), bootstyle="dark.TFrame")
        wrapper.grid(row=0, column=1, sticky=ttk.NSEW, padx=(5, 0), pady=(0, 5))
        
        if self.restart:
            return
        
        title = ttk.Label(wrapper, text="Ghost", font=("Host Grotesk", 14 if sys.platform != "darwin" else 16, "bold"))
        title.configure(background=self.root.style.colors.get("dark"))
        title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=(10, 0))
        
        ttk.Separator(wrapper, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="we", padx=(10, 10), pady=5)
        wrapper.grid_columnconfigure(1, weight=1)
        
        version = ttk.Label(wrapper, text=f"Version: {VERSION}", font=("Host Grotesk", 12 if sys.platform != "darwin" else 14))
        version.configure(background=self.root.style.colors.get("dark"))
        version.grid(row=2, column=0, sticky=ttk.W, padx=(10, 0), pady=(5, 0))    
        
        self.uptime_label = ttk.Label(wrapper, text=f"Uptime: {self.bot_controller.get_uptime()}", font=("Host Grotesk", 12 if sys.platform != "darwin" else 14))
        self.uptime_label.configure(background=self.root.style.colors.get("dark"), foreground="white" if not self.restart else "lightgrey")
        self.uptime_label.grid(row=3, column=0, sticky=ttk.W, padx=(10, 0))
        
        self.latency_label = ttk.Label(wrapper, text=f"Latency: {self.bot_controller.get_latency()}", font=("Host Grotesk", 12 if sys.platform != "darwin" else 14))
        self.latency_label.configure(background=self.root.style.colors.get("dark"), foreground="white" if not self.restart else "lightgrey")
        self.latency_label.grid(row=4, column=0, sticky=ttk.W, padx=(10, 0), pady=(0, 10))
        
    def _update_wraplength(self, event=None):
        if self.discord_logs_frame:
            try:
                new_width = self.discord_logs_frame.winfo_width() - 30  # Adjust for padding
                for widget in self.discord_logs_frame.winfo_children():
                    if isinstance(widget, ttk.Label):
                        widget.configure(wraplength=max(new_width, 100))
            except:
                pass
            
    def _display_log(self, log_entry):
        author, message, delete_time = log_entry
        try:
            
            frame = RoundedFrame(self.discord_logs_frame, radius=(8, 8, 8, 8), bootstyle="secondary.TFrame", parent_background=self.root.style.colors.get("dark"))
            frame.pack(fill=ttk.X, pady=(0, 5), padx=(0, 15))
            
            try:
                if author.id not in self.avatars:
                    self.avatars[author.id] = self.bot_controller.get_avatar_from_url(author.avatar.url, size=50, radius=5)
                    
                avatar_image = self.avatars.get(author.id)
            except:
                url = "https://ia600305.us.archive.org/31/items/discordprofilepictures/discordblue.png"
                avatar_image = self.bot_controller.get_avatar_from_url(url, size=50, radius=5)
            
            avatar = ttk.Label(frame, image=avatar_image)
            avatar.configure(background=self.root.style.colors.get("secondary"))
            avatar.grid(row=0, column=0, sticky=ttk.NW, padx=(5, 5), rowspan=3, pady=5)
            
            author_label = ttk.Label(frame, text=author.display_name, font=("Host Grotesk", 12 if sys.platform != "darwin" else 14, "bold"))
            author_label.configure(background=self.root.style.colors.get("secondary"))
            author_label.grid(row=0, column=1, sticky=ttk.NW, padx=(0, 10), pady=(5, 0))
            
            message_content = message.content[:250] + "..." if len(message.content) > 250 else message.content
            
            message_label = ttk.Label(frame, text=message_content, font=("Host Grotesk", 10 if sys.platform != "darwin" else 12), wraplength=350)
            message_label.configure(background=self.root.style.colors.get("secondary"))
            message_label.grid(row=1, column=1, sticky=ttk.NW, padx=(0, 10))
            
            channel_label_text = f"Deleted in DMs" if isinstance(message.channel, discord.DMChannel) else f"Deleted in {message.guild.name} > #{message.channel.name}"
            channel_label = ttk.Label(frame, text=channel_label_text, font=("Host Grotesk", 8 if sys.platform != "darwin" else 10, "italic"))
            channel_label.configure(background=self.root.style.colors.get("secondary"), foreground="lightgrey")
            channel_label.grid(row=2, column=1, sticky=ttk.NW, padx=(0, 10), pady=(0, 5))
            
            ttk.Label(frame, text="", background=self.root.style.colors.get("secondary")).grid(row=2, column=2, sticky=ttk.E)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
            
            # # Function to update wraplength
            # def update_wraplength(event):
            #     new_width = frame.winfo_width() - 60  # Adjusting for padding and avatar width
            #     message_label.configure(wraplength=new_width if new_width > 100 else 100)

            # # Bind window resize event
            # self.root.bind("<Configure>", update_wraplength)

            self.discord_logs_canvas.yview_moveto(1)
        except:
            pass
        
    def add_discord_log(self, author, message, delete_time):
        log_entry = (author, message, delete_time)
        self.discord_logs.append(log_entry)
        self._display_log(log_entry)
        
    def _load_discord_logs(self):
        for log_entry in self.discord_logs:
            self._display_log(log_entry)
            
        try:
            self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_wrapper)
            self.discord_logs_canvas.yview_moveto(1)
        except:
            pass
        
    def _clear_discord_logs(self):
        for widget in self.discord_logs_frame.winfo_children():
            widget.destroy()
        
        self.discord_logs = []
        self.avatars = {}
        
        # Clear the canvas
        self.discord_logs_canvas.delete("all")
        
        # Reset the scroll region
        self.discord_logs_canvas.configure(scrollregion=self.discord_logs_canvas.bbox("all"))
        
        # Update the canvas width
        self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_wrapper)
        
    def _max_discord_logs(self):
        self.root.update_idletasks()
        self.discord_logs_max = True
        self.discord_logs_max_min_btn.configure(image=self.images.get("min"))
        self.discord_logs_max_min_btn.bind("<Button-1>", lambda e: self._min_discord_logs())
        # self.discord_logs_textbox.configure(height=18)
        
        # self.discord_logs_wrapper.pack_forget()
        # self.discord_logs_footer.pack_forget()
        self.details_wrapper.pack_forget()
        
        self.discord_logs_wrapper.pack(fill=ttk.BOTH, expand=True, pady=(10, 0))
        # self.discord_logs_footer.pack(fill=ttk.BOTH, expand=False)
        self.root.update_idletasks()
        
    def _min_discord_logs(self):
        self.root.update_idletasks()
        self.discord_logs_max = False
        self.discord_logs_max_min_btn.configure(image=self.images.get("max"))
        self.discord_logs_max_min_btn.bind("<Button-1>", lambda e: self._max_discord_logs())
        # self.discord_logs_textbox.configure(height=10)
    
        self.discord_logs_wrapper.pack_forget()
        # self.discord_logs_footer.pack_forget()
        self.details_wrapper.pack(fill=ttk.BOTH, expand=False, pady=(10, 0))
        self.discord_logs_wrapper.pack(fill=ttk.BOTH, expand=True, pady=(5, 0))
        # self.discord_logs_footer.pack(fill=ttk.BOTH, expand=False)
        self.root.update_idletasks()
        
    def _update_canvas_width(self, canvas, logs_wrapper):
        canvas.itemconfig(self.canvas_window, width=logs_wrapper.winfo_width() - 24)

    def _draw_discord_logs(self, parent):
        if self.restart:
            wrapper = RoundedFrame(parent, radius=(15, 15, 15, 15), bootstyle="dark.TFrame")
            wrapper.pack(fill=ttk.BOTH, expand=True, pady=(5, 0))
            
            return wrapper
        
        wrapper = ttk.Frame(parent)
        wrapper.pack(fill=ttk.BOTH, expand=True, pady=(5, 0))
        
        header_wrapper = RoundedFrame(wrapper, radius=(15, 15, 0, 0), style="secondary.TFrame")
        header_wrapper.pack(fill=ttk.BOTH, expand=False)
        
        title = ttk.Label(header_wrapper, text="Deleted Messages", font=("Host Grotesk", 14 if sys.platform != "darwin" else 16, "bold"))
        title.configure(background=self.root.style.colors.get("secondary"))
        title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=10)
        header_wrapper.columnconfigure(1, weight=1)
        
        clear_btn = ttk.Label(header_wrapper, image=self.images.get("trash"), font=("Host Grotesk", 12 if sys.platform != "darwin" else 14, "bold"))
        clear_btn.configure(background=self.root.style.colors.get("secondary"), foreground="white")
        clear_btn.bind("<Button-1>", lambda e: self._clear_discord_logs())
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(foreground="lightgrey"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(foreground="white"))
        clear_btn.grid(row=0, column=2, sticky=ttk.E, pady=10)
        
        self.discord_logs_max_min_btn = ttk.Label(header_wrapper, image=self.images.get("max") if not self.discord_logs_max else self.images.get("min"), anchor="center")
        self.discord_logs_max_min_btn.configure(background=self.root.style.colors.get("secondary"))
        self.discord_logs_max_min_btn.bind("<Button-1>", lambda e: self._max_discord_logs() if not self.discord_logs_max else lambda e: self._min_discord_logs())
        self.discord_logs_max_min_btn.grid(row=0, column=3, sticky=ttk.E, padx=(10, 13), pady=8)
        
        logs_wrapper = RoundedFrame(wrapper, radius=(0, 0, 15, 15), style="dark.TFrame")
        logs_wrapper.pack(fill=ttk.BOTH, expand=True)
        
        self.discord_logs_inner_wrapper = ttk.Frame(logs_wrapper)
        self.discord_logs_inner_wrapper.pack(fill=ttk.BOTH, expand=True, padx=10, pady=10)

        canvas = ttk.Canvas(self.discord_logs_inner_wrapper)
        scrollbar = ttk.Scrollbar(self.discord_logs_inner_wrapper, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas, style="dark.TFrame")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, background=self.root.style.colors.get("dark"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.discord_logs_frame = scroll_frame  # Store this for adding logs later
        self.discord_logs_canvas = canvas  # Store this for updating the width later

        # Schedule the update of canvas width after the UI has been rendered
        canvas.after(100, lambda: self._update_canvas_width(canvas, logs_wrapper))

        return wrapper
        
    def draw(self, parent, restart=False):
        self.restart = restart
        self.avatar = self.bot_controller.get_avatar()
        self._draw_header(parent)
        
        self.details_wrapper = self._draw_details_wrapper(parent)
        self._draw_account_details(self.details_wrapper)
        self._draw_bot_details(self.details_wrapper)
        self.discord_logs_wrapper = self._draw_discord_logs(parent)
        
        self._load_discord_logs()
        
        if self.discord_logs_max:
            self._max_discord_logs()
            
        try:
            self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_wrapper)
            self.discord_logs_canvas.yview_moveto(1)
        except:
            pass
        
        self._update_bot_details()
        self._update_account_details()