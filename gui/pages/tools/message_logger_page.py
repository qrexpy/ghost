import sys, discord, time
import ttkbootstrap as ttk
from gui.components import RoundedFrame, ToolPage

class MessageLoggerPage(ToolPage):
    def __init__(self, toolspage, root, bot_controller, images, layout):
        super().__init__(toolspage, root, bot_controller, images, layout, title="Message Logger")
        
        # Message logger specific attributes
        self.discord_logs = []
        self.avatars = {}
        self.discord_logs_frame = None
        self.discord_logs_canvas = None
        self.canvas_window = None
        self.discord_logs_inner_wrapper = None
        
        # Bind window resize event for wraplength updates
        self.root.bind("<Configure>", self._update_wraplength)
    
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
            self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_inner_wrapper.master)
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
        self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_inner_wrapper.master)
    
    def _update_canvas_width(self, canvas, logs_wrapper):
        canvas.itemconfig(self.canvas_window, width=logs_wrapper.winfo_width() - 24)

    def draw_content(self, wrapper):
        # Header with title and clear button
        header_wrapper = ttk.Frame(wrapper)
        header_wrapper.pack(fill=ttk.X, pady=(10, 10))
        
        title = ttk.Label(header_wrapper, text="Deleted Messages", font=("Host Grotesk", 14 if sys.platform != "darwin" else 16, "bold"))
        title.configure(background=self.root.style.colors.get("dark"))
        title.grid(row=0, column=0, sticky=ttk.W, padx=10, pady=0)
        header_wrapper.columnconfigure(1, weight=1)
        
        clear_btn = ttk.Label(header_wrapper, image=self.images.get("trash"), font=("Host Grotesk", 12 if sys.platform != "darwin" else 14, "bold"))
        clear_btn.configure(background=self.root.style.colors.get("dark"), foreground="white")
        clear_btn.bind("<Button-1>", lambda e: self._clear_discord_logs())
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(foreground="lightgrey"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(foreground="white"))
        clear_btn.grid(row=0, column=2, sticky=ttk.E, pady=0, padx=10)
        
        # Main logs area
        self.discord_logs_inner_wrapper = ttk.Frame(wrapper)
        self.discord_logs_inner_wrapper.pack(fill=ttk.BOTH, expand=True, padx=10, pady=(0, 10))

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
        canvas.after(100, lambda: self._update_canvas_width(canvas, self.discord_logs_inner_wrapper))
        
        # Load existing logs
        self._load_discord_logs()