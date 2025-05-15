import os
import ttkbootstrap as ttk

from utils.files import get_application_support
from gui.helpers.images import Images
from gui.components.rounded_frame import RoundedFrame

class ScriptPage:
    def __init__(self, root, script):
        self.gui = root
        self.root = root.root
        self.script = script
        self.images = Images()
        self.editor = None
        self.linenumbers = None
        self.text_scrollbar = None
        
    def _go_back(self):
        self._save_script()
        self.gui.draw_scripts()
        
    def _get_script_content(self):
        with open(get_application_support() + f"/scripts/{self.script}", "r") as file:
            return file.read()
        
    def _save_script(self):
        with open(get_application_support() + f"/scripts/{self.script}", "w") as file:
            file.write(self.editor.get("1.0", ttk.END))

    def _draw_header(self, parent):
        wrapper = ttk.Frame(parent)
        
        back_button = ttk.Label(wrapper, image=self.images.get("left-chevron"))
        back_button.grid(row=0, column=0, sticky=ttk.W, padx=(0, 10))
        back_button.bind("<Button-1>", lambda e: self._go_back())
            
        script_name = ttk.Label(wrapper, text=self.script, font=("Host Grotesk", 16, "bold"))
        script_name.grid(row=0, column=1, sticky=ttk.W)
        
        return wrapper

    def _update_line_numbers(self, event=None):
        """Update line numbers in the left sidebar."""
        line_numbers = ""
        for i in range(1, int(self.editor.index('end-1c').split('.')[0]) + 1):
            line_numbers += f"{i}\n"
        self.linenumbers.config(state="normal")
        self.linenumbers.delete('1.0', 'end')
        self.linenumbers.insert('1.0', line_numbers)
        self.linenumbers.config(state="disabled")

    def move_cursor_to_line(self, line_number):
        """Move the cursor to a specific line and set focus."""
        self.editor.mark_set("insert", f"{line_number}.0")  # line_number.0 represents the start of the line
        self.editor.see(f"{line_number}.0")  # Scroll to the line if it's out of view
        self.editor.focus_set()  # Ensure focus is set after moving the cursor

    def _sync_scroll(self, *args):
        """Sync the scrolling of line numbers and editor."""
        if args[0] == "moveto" or args[0] == "scroll":
            # Sync both editor and line numbers
            self.linenumbers.yview(*args)
            self.editor.yview(*args)

    def draw(self, parent):
        header = self._draw_header(parent)
        header.pack(fill=ttk.X, pady=(0, 20))
        
        editor_wrapper = RoundedFrame(parent, radius=(15, 15, 15, 15), bootstyle="dark.TFrame")
        editor_wrapper.pack(fill=ttk.BOTH, expand=True)
        
        # Create a frame to hold both the line numbers and editor
        text_container = ttk.Frame(editor_wrapper)
        text_container.pack(fill=ttk.BOTH, expand=True)

        # Line number widget (disabled to prevent editing)
        self.linenumbers = ttk.Text(text_container, width=4, font=("JetBrainsMono NF Regular", 12), state="disabled")
        self.linenumbers.pack(side=ttk.LEFT, fill=ttk.Y)

        # Main text editor
        self.editor = ttk.Text(text_container, wrap="word", font=("JetBrainsMono NF Regular", 12))
        self.editor.pack(fill=ttk.BOTH, expand=True)

        # Insert script content
        self.editor.insert(ttk.END, self._get_script_content())

        # Ensure the editor is editable
        self.editor.configure(state="normal")
        self.editor.config(tabs=("4c",))

        # Create a scrollbar and link it to the editor and line numbers
        self.text_scrollbar = ttk.Scrollbar(editor_wrapper, orient="vertical", command=self._sync_scroll)
        self.text_scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

        # Set the scrollbars for both widgets
        self.editor.config(yscrollcommand=self.text_scrollbar.set)
        self.linenumbers.config(yscrollcommand=self.text_scrollbar.set)

        # Focus handling
        def set_focus(event):
            # Set focus when clicking inside the editor
            self.editor.focus_set()

        # Focus handling
        self.editor.bind("<Button-1>", set_focus)  # Set focus on click
        self.editor.bind("<Enter>", lambda e: self.editor.focus_set())  # Set focus when mouse enters
        self.editor.bind("<FocusIn>", lambda e: self.editor.focus_set())  # Set focus when it gains focus

        # Attach events to sync line numbers
        self.editor.bind("<KeyRelease>", self._update_line_numbers)
        self.editor.bind("<MouseWheel>", self._update_line_numbers)

        # Initialize line numbers
        self._update_line_numbers()

        # Example usage: Move cursor to a specific line (for instance, line 5)
        self.move_cursor_to_line(5)
