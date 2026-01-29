import tkinter as tk
from tkinter import messagebox
import threading
from ui.theme import COLORS, FONTS, ASCII_HEADER
from ui.components import LogViewer, StatsPanel, StatusBar
from stats.events import EventEmitter
from stats.stats_manager import StatsManager


class TradingBotUI:
    """
    Main UI window for the trading bot
    8-bit retro terminal aesthetic with purple theme
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Doggo Trader - Roblox Trading Bot")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg_primary'])
        self.root.resizable(True, True)

        # Event system
        self.events = EventEmitter()
        self.stats_manager = StatsManager()

        # Subscribe to events
        self.events.on("log", self._on_log)
        self.events.on("status", self._on_status)
        self.events.on("stat", self._on_stat_update)
        self.events.on("profit_update", self._on_profit_update)

        # Build UI
        self._build_ui()

        # Start update loop
        self._start_update_loop()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        """Build the UI layout"""
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # ASCII Header
        header_text = tk.Text(
            main_container,
            font=FONTS['mono_small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['accent_magenta'],
            height=9,
            relief=tk.FLAT,
            borderwidth=0
        )
        header_text.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_text.insert('1.0', ASCII_HEADER)
        header_text.config(state=tk.DISABLED)

        # Status bar
        self.status_bar = StatusBar(main_container)
        self.status_bar.pack(fill=tk.X, padx=10, pady=5)

        # Content area - split into two panels
        content_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left panel - Statistics (30%)
        left_panel = tk.Frame(content_frame, bg=COLORS['bg_panel'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        left_panel.pack_propagate(False)

        self.stats_panel = StatsPanel(left_panel)
        self.stats_panel.pack(fill=tk.BOTH, expand=True)

        # Right panel - Logs (70%)
        right_panel = tk.Frame(content_frame, bg=COLORS['bg_panel'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.log_viewer = LogViewer(right_panel)
        self.log_viewer.pack(fill=tk.BOTH, expand=True)

        # Bottom controls
        controls_frame = tk.Frame(main_container, bg=COLORS['bg_secondary'], height=40)
        controls_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        controls_frame.pack_propagate(False)

        # Clear logs button
        clear_btn = tk.Button(
            controls_frame,
            text="[ CLEAR LOGS ]",
            font=FONTS['mono_regular'],
            bg=COLORS['bg_panel'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['border_active'],
            activeforeground=COLORS['text_white'],
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            command=self._clear_logs
        )
        clear_btn.pack(side=tk.LEFT, padx=10, pady=5)

        # Version/info label
        info_label = tk.Label(
            controls_frame,
            text="v1.0 BETA | by shibahex",
            font=FONTS['mono_small'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_dim'],
            anchor='e'
        )
        info_label.pack(side=tk.RIGHT, padx=10)

        # Load initial stats
        self._load_stats()

    def _start_update_loop(self):
        """Start the periodic update loop"""
        self._update_ui()

    def _update_ui(self):
        """Periodic UI update"""
        # Update session uptime
        uptime = self.stats_manager.get_session_uptime()
        self.status_bar.update_session_time(uptime)

        # Check for new log messages
        while not self.events.log_queue.empty():
            log_data = self.events.log_queue.get()
            self.log_viewer.add_log(log_data['message'], log_data['severity'])

        # Schedule next update
        self.root.after(1000, self._update_ui)

    def _load_stats(self):
        """Load and display statistics"""
        stats = self.stats_manager.get_stats()
        self.stats_panel.update_all_stats(stats)

    def _clear_logs(self):
        """Clear the log viewer"""
        self.log_viewer.clear_logs()
        self.events.emit_log("Logs cleared by user", "info")

    def _on_log(self, data):
        """Handle log events"""
        # Logs are handled by the update loop via the queue
        pass

    def _on_status(self, status):
        """Handle status change events"""
        self.status_bar.set_status(status)

    def _on_stat_update(self, data):
        """Handle statistic update events"""
        stat_name = data.get('name')
        value = data.get('value')
        self.stats_panel.update_stat(stat_name, value)

    def _on_profit_update(self, data):
        """Handle profit update events"""
        self.stats_panel.update_stat('profit_rap', data.get('rap', 0))
        self.stats_panel.update_stat('profit_value', data.get('value', 0))
        self.stats_panel.update_stat('profit_overall', data.get('overall', 0))

    def _on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Stop the trading bot and exit?"):
            self.stats_manager.end_session()
            self.events.emit("app_shutdown", None)
            self.root.destroy()

    def run(self):
        """Start the UI main loop"""
        self.events.emit_log("Trading bot UI started", "success")
        self.events.emit_status("INITIALIZING")
        self.root.mainloop()

    def add_log(self, message: str, severity: str = "info"):
        """Public method to add logs from external sources"""
        self.events.emit_log(message, severity)

    def set_status(self, status: str):
        """Public method to set status from external sources"""
        self.events.emit_status(status)
