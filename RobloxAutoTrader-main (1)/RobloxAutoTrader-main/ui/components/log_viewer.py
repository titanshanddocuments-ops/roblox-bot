import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from ui.theme import COLORS, FONTS, get_log_tag_color


class LogViewer(tk.Frame):
    """
    Live log viewer component with color-coded severity levels
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_panel'])

        self.max_lines = 1000  # Limit log lines to prevent memory issues

        # Header
        header = tk.Label(
            self,
            text="▼ LIVE ACTIVITY LOG",
            font=FONTS['mono_bold'],
            bg=COLORS['bg_panel'],
            fg=COLORS['text_primary'],
            anchor='w'
        )
        header.pack(fill=tk.X, padx=5, pady=(5, 0))

        # Log text widget
        self.log_text = scrolledtext.ScrolledText(
            self,
            font=FONTS['mono_regular'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            insertbackground=COLORS['accent_magenta'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure tags for different severity levels
        self.log_text.tag_config('info', foreground=COLORS['text_secondary'])
        self.log_text.tag_config('success', foreground=COLORS['accent_success'])
        self.log_text.tag_config('warning', foreground=COLORS['accent_warning'])
        self.log_text.tag_config('error', foreground=COLORS['accent_error'])
        self.log_text.tag_config('debug', foreground=COLORS['text_dim'])
        self.log_text.tag_config('timestamp', foreground=COLORS['text_dim'])
        self.log_text.tag_config('tag', foreground=COLORS['accent_magenta'])

    def add_log(self, message: str, severity: str = "info"):
        """Add a log message to the viewer"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        severity_upper = severity.upper().ljust(7)

        self.log_text.config(state=tk.NORMAL)

        # Add timestamp
        self.log_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')

        # Add severity tag
        self.log_text.insert(tk.END, f"[{severity_upper}] ", severity.lower())

        # Add message
        self.log_text.insert(tk.END, f"{message}\n", severity.lower())

        # Limit the number of lines
        line_count = int(self.log_text.index('end-1c').split('.')[0])
        if line_count > self.max_lines:
            self.log_text.delete('1.0', '2.0')

        # Auto-scroll to bottom
        self.log_text.see(tk.END)

        self.log_text.config(state=tk.DISABLED)

    def clear_logs(self):
        """Clear all logs"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
