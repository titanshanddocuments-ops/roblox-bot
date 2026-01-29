import tkinter as tk
from ui.theme import COLORS, FONTS, STATUS_ICONS


class StatusBar(tk.Frame):
    """
    Status bar showing current bot activity
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_secondary'], height=40)
        self.pack_propagate(False)

        # Status indicator
        self.status_icon = tk.Label(
            self,
            text=STATUS_ICONS['idle'],
            font=FONTS['mono_large'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['status_idle'],
            width=3
        )
        self.status_icon.pack(side=tk.LEFT, padx=10)

        # Status text
        self.status_text = tk.Label(
            self,
            text="IDLE",
            font=FONTS['mono_bold'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['status_idle'],
            anchor='w'
        )
        self.status_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Session info
        self.session_info = tk.Label(
            self,
            text="Session: 0h 0m",
            font=FONTS['mono_regular'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_dim'],
            anchor='e'
        )
        self.session_info.pack(side=tk.RIGHT, padx=10)

    def set_status(self, status: str, icon_key: str = None):
        """Update the status display"""
        status_upper = status.upper()

        # Determine color based on status
        if 'error' in status.lower():
            color = COLORS['status_error']
            icon = STATUS_ICONS['error']
        elif 'scanning' in status.lower():
            color = COLORS['status_active']
            icon = STATUS_ICONS['scanning']
        elif 'sending' in status.lower() or 'trading' in status.lower():
            color = COLORS['status_active']
            icon = STATUS_ICONS['sending']
        elif 'waiting' in status.lower():
            color = COLORS['status_warning']
            icon = STATUS_ICONS['waiting']
        elif 'idle' in status.lower():
            color = COLORS['status_idle']
            icon = STATUS_ICONS['idle']
        else:
            color = COLORS['status_active']
            icon = STATUS_ICONS['active']

        # Override icon if specified
        if icon_key and icon_key in STATUS_ICONS:
            icon = STATUS_ICONS[icon_key]

        self.status_icon.config(text=icon, fg=color)
        self.status_text.config(text=status_upper, fg=color)

    def update_session_time(self, uptime_seconds: int):
        """Update session uptime display"""
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        self.session_info.config(text=f"Session: {hours}h {minutes}m")
