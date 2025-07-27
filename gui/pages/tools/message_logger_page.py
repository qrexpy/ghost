import ttkbootstrap as ttk
import tkinter.font as tkFont
import discord
import time
import sys
from ttkbootstrap.scrolled import ScrolledFrame
from gui.components import RoundedFrame, ToolPage, RoundedButton
from utils.config import Config

class MessageLoggerPage(ToolPage):
    def __init__(self, toolspage, root, bot_controller, images, layout):
        super().__init__(toolspage, root, bot_controller, images, layout, title="Message Logger", frame=False)
        self.cfg = Config()
        
        # Message logging state
        self.discord_logs = []
        self.avatars = {}
        
        # UI components
        self.discord_logs_wrapper = None
        self.discord_logs_frame = None
        self.discord_logs_canvas = None
        self.canvas_window = None
        
        # Blacklist UI components
        self.blacklist_frame = None
        self.server_checkboxes = {}
        self.server_vars = {}
        self.select_all_var = None
        self.blacklist_visible = False
        
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

    def add_discord_log(self, author, message, delete_time):
        """Add a deleted message to the logger."""
        # Check if server is blacklisted
        if hasattr(message, 'guild') and message.guild:
            if self.cfg.is_server_blacklisted_for_message_logger(str(message.guild.id)):
                return  # Don't log messages from blacklisted servers
        
        log_entry = (author, message, delete_time)
        self.discord_logs.append(log_entry)
        
        if self.discord_logs_frame:
            self._display_log(log_entry)

    def _display_log(self, log_entry):
        """Display a single deleted message log entry."""
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

            if self.discord_logs_canvas:
                self.discord_logs_canvas.yview_moveto(1)
        except Exception as e:
            print(f"Error displaying log: {e}")

    def _clear_discord_logs(self):
        """Clear all displayed logs."""
        if self.discord_logs_frame:
            for widget in self.discord_logs_frame.winfo_children():
                widget.destroy()
        
        self.discord_logs = []
        self.avatars = {}
        
        if self.discord_logs_canvas:
            # Clear the canvas
            self.discord_logs_canvas.delete("all")
            
            # Reset the scroll region
            self.discord_logs_canvas.configure(scrollregion=self.discord_logs_canvas.bbox("all"))
            
            # Update the canvas width
            self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_wrapper)

    def _update_canvas_width(self, canvas, logs_wrapper):
        if canvas and logs_wrapper and self.canvas_window:
            try:
                canvas.itemconfig(self.canvas_window, width=logs_wrapper.winfo_width() - 24)
            except:
                pass

    def _toggle_blacklist(self):
        """Toggle the blacklist configuration panel."""
        self.blacklist_visible = not self.blacklist_visible
        
        if self.blacklist_visible:
            self._show_blacklist()
        else:
            self._hide_blacklist()

    def _show_blacklist(self):
        """Show the blacklist configuration panel."""
        if self.blacklist_frame:
            self.blacklist_frame.pack(fill=ttk.BOTH, expand=True, pady=(10, 0))

    def _hide_blacklist(self):
        """Hide the blacklist configuration panel."""
        if self.blacklist_frame:
            self.blacklist_frame.pack_forget()

    def _on_select_all_toggle(self):
        """Handle select all/deselect all checkbox."""
        select_all = self.select_all_var.get()
        for var in self.server_vars.values():
            var.set(select_all)
        self._update_blacklist()

    def _on_server_toggle(self):
        """Handle individual server checkbox toggle."""
        # Update select all checkbox based on individual selections
        all_selected = all(var.get() for var in self.server_vars.values())
        none_selected = not any(var.get() for var in self.server_vars.values())
        
        if all_selected:
            self.select_all_var.set(True)
        elif none_selected:
            self.select_all_var.set(False)
        else:
            # Some selected, some not - set to intermediate state if supported
            self.select_all_var.set(False)
        
        self._update_blacklist()

    def _update_blacklist(self):
        """Update the configuration with current blacklist selections."""
        blacklisted_servers = []
        for guild_id, var in self.server_vars.items():
            if var.get():
                blacklisted_servers.append(guild_id)
        
        self.cfg.set_message_logger_blacklist(blacklisted_servers)

    def _draw_blacklist_panel(self, parent):
        """Draw the server blacklist configuration panel."""
        wrapper = RoundedFrame(parent, radius=(15, 15, 15, 15), bootstyle="dark.TFrame")
        
        # Header
        header = ttk.Frame(wrapper)
        header.pack(fill=ttk.X, padx=15, pady=(15, 10))
        
        title = ttk.Label(header, text="Server Blacklist", font=("Host Grotesk", 14 if sys.platform != "darwin" else 16, "bold"))
        title.configure(background=self.root.style.colors.get("dark"))
        title.pack(side=ttk.LEFT)
        
        # Select All checkbox
        self.select_all_var = ttk.BooleanVar()
        select_all_cb = ttk.Checkbutton(header, text="Select All", variable=self.select_all_var, command=self._on_select_all_toggle)
        select_all_cb.configure(background=self.root.style.colors.get("dark"))
        select_all_cb.pack(side=ttk.RIGHT)
        
        # Separator
        ttk.Separator(wrapper, orient="horizontal").pack(fill=ttk.X, padx=15, pady=(0, 10))
        
        # Scrollable server list
        scroll_frame = ScrolledFrame(wrapper, bootstyle="dark")
        scroll_frame.pack(fill=ttk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Get current blacklist
        current_blacklist = self.cfg.get_message_logger_blacklist()
        
        # Add server checkboxes
        if self.bot_controller and self.bot_controller.bot:
            guilds = self.bot_controller.get_guilds()
            if guilds:
                for guild in guilds:
                    guild_id = str(guild.id)
                    var = ttk.BooleanVar()
                    var.set(guild_id in current_blacklist)
                    
                    cb = ttk.Checkbutton(scroll_frame, text=f"{guild.name} ({guild.member_count} members)", 
                                       variable=var, command=self._on_server_toggle)
                    cb.configure(background=self.root.style.colors.get("dark"))
                    cb.pack(fill=ttk.X, pady=2, padx=5)
                    
                    self.server_vars[guild_id] = var
            else:
                no_servers_label = ttk.Label(scroll_frame, text="No servers found. Make sure the bot is connected.", 
                                           font=("Host Grotesk", 10 if sys.platform != "darwin" else 12))
                no_servers_label.configure(background=self.root.style.colors.get("dark"), foreground="lightgrey")
                no_servers_label.pack(pady=20)
        
        # Update select all state
        if self.server_vars:
            all_selected = all(var.get() for var in self.server_vars.values())
            self.select_all_var.set(all_selected)
        
        return wrapper

    def draw_content(self, wrapper):
        # Main container
        main_container = ttk.Frame(wrapper)
        main_container.pack(fill=ttk.BOTH, expand=True)
        
        # Header with controls
        header_wrapper = RoundedFrame(main_container, radius=(15, 15, 0, 0), style="secondary.TFrame")
        header_wrapper.pack(fill=ttk.X)
        
        title = ttk.Label(header_wrapper, text="Deleted Messages", font=("Host Grotesk", 14 if sys.platform != "darwin" else 16, "bold"))
        title.configure(background=self.root.style.colors.get("secondary"))
        title.grid(row=0, column=0, sticky=ttk.W, padx=15, pady=15)
        header_wrapper.columnconfigure(1, weight=1)
        
        # Controls
        controls_frame = ttk.Frame(header_wrapper)
        controls_frame.configure(style="secondary.TFrame")
        controls_frame.grid(row=0, column=2, sticky=ttk.E, padx=15, pady=15)
        
        # Blacklist toggle button
        blacklist_btn = RoundedButton(controls_frame, radius=8, bootstyle="primary.TButton", 
                                    command=self._toggle_blacklist, text="Blacklist", padx=10, pady=4)
        blacklist_btn.pack(side=ttk.RIGHT, padx=(10, 0))
        
        # Clear button
        clear_btn = ttk.Label(controls_frame, image=self.images.get("trash"), font=("Host Grotesk", 12 if sys.platform != "darwin" else 14, "bold"))
        clear_btn.configure(background=self.root.style.colors.get("secondary"), foreground="white")
        clear_btn.bind("<Button-1>", lambda e: self._clear_discord_logs())
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(foreground="lightgrey"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(foreground="white"))
        clear_btn.pack(side=ttk.RIGHT, padx=(0, 10))
        
        # Message logs container
        logs_container = ttk.Frame(main_container)
        logs_container.pack(fill=ttk.BOTH, expand=True)
        
        # Logs wrapper
        logs_wrapper = RoundedFrame(logs_container, radius=(0, 0, 15, 15), style="dark.TFrame")
        logs_wrapper.pack(fill=ttk.BOTH, expand=True)
        
        self.discord_logs_wrapper = logs_wrapper
        
        # Inner wrapper for the scrollable content
        logs_inner_wrapper = ttk.Frame(logs_wrapper)
        logs_inner_wrapper.pack(fill=ttk.BOTH, expand=True, padx=10, pady=10)

        # Canvas and scrollbar
        canvas = ttk.Canvas(logs_inner_wrapper)
        scrollbar = ttk.Scrollbar(logs_inner_wrapper, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas, style="dark.TFrame")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, background=self.root.style.colors.get("dark"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.discord_logs_frame = scroll_frame
        self.discord_logs_canvas = canvas

        # Schedule the update of canvas width after the UI has been rendered
        canvas.after(100, lambda: self._update_canvas_width(canvas, logs_wrapper))
        
        # Blacklist panel (initially hidden)
        self.blacklist_frame = self._draw_blacklist_panel(main_container)
        self.blacklist_frame.pack_forget()  # Hide initially
        
        # Load existing logs
        self._load_discord_logs()

    def _load_discord_logs(self):
        """Load and display existing logs."""
        for log_entry in self.discord_logs:
            self._display_log(log_entry)
            
        if self.discord_logs_canvas and self.discord_logs_wrapper:
            try:
                self._update_canvas_width(self.discord_logs_canvas, self.discord_logs_wrapper)
                self.discord_logs_canvas.yview_moveto(1)
            except:
                pass