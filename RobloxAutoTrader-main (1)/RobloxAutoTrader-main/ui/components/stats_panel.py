import tkinter as tk
from ui.theme import COLORS, FONTS


class StatsPanel(tk.Frame):
    """
    Statistics panel showing lifetime and session stats
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_panel'])

        # Header
        header = tk.Label(
            self,
            text="▼ LIFETIME STATISTICS",
            font=FONTS['mono_bold'],
            bg=COLORS['bg_panel'],
            fg=COLORS['text_primary'],
            anchor='w'
        )
        header.pack(fill=tk.X, padx=5, pady=(5, 10))

        # Stats container
        stats_container = tk.Frame(self, bg=COLORS['bg_primary'])
        stats_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # Create stat labels
        self.stat_labels = {}

        self._create_section(stats_container, "TRADES", [
            ("trades_sent", "Sent:"),
            ("trades_accepted", "Accepted:"),
            ("trades_declined", "Declined:"),
            ("trades_countered", "Countered:"),
            ("trades_cancelled", "Cancelled:"),
        ])

        self._add_separator(stats_container)

        self._create_section(stats_container, "PROFIT", [
            ("profit_overall", "Overall:"),
            ("profit_rap", "RAP:"),
            ("profit_value", "Value:"),
        ])

        self._add_separator(stats_container)

        self._create_section(stats_container, "SYSTEM", [
            ("errors", "Errors:"),
            ("uptime", "Uptime:"),
            ("sessions", "Sessions:"),
        ])

    def _create_section(self, parent, title, stats):
        """Create a section of statistics"""
        # Section title
        section_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        section_frame.pack(fill=tk.X, padx=10, pady=5)

        title_label = tk.Label(
            section_frame,
            text=f"┌─ {title} ─",
            font=FONTS['mono_small'],
            bg=COLORS['bg_primary'],
            fg=COLORS['accent_magenta'],
            anchor='w'
        )
        title_label.pack(fill=tk.X)

        # Stats rows
        for key, label_text in stats:
            row = tk.Frame(section_frame, bg=COLORS['bg_primary'])
            row.pack(fill=tk.X, pady=2)

            label = tk.Label(
                row,
                text=f"  │ {label_text}",
                font=FONTS['mono_regular'],
                bg=COLORS['bg_primary'],
                fg=COLORS['text_dim'],
                anchor='w',
                width=15
            )
            label.pack(side=tk.LEFT)

            value = tk.Label(
                row,
                text="0",
                font=FONTS['mono_bold'],
                bg=COLORS['bg_primary'],
                fg=COLORS['accent_success'],
                anchor='e'
            )
            value.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 10))

            self.stat_labels[key] = value

    def _add_separator(self, parent):
        """Add a visual separator"""
        separator = tk.Frame(parent, bg=COLORS['border_main'], height=1)
        separator.pack(fill=tk.X, padx=10, pady=10)

    def update_stat(self, stat_name: str, value):
        """Update a specific statistic"""
        if stat_name in self.stat_labels:
            if isinstance(value, float):
                formatted_value = f"{value:,.2f}"
            elif isinstance(value, int):
                formatted_value = f"{value:,}"
            else:
                formatted_value = str(value)

            self.stat_labels[stat_name].config(text=formatted_value)

    def update_all_stats(self, stats: dict):
        """Update all statistics at once"""
        lifetime = stats.get('lifetime', {})

        # Map stats to UI labels
        stat_mapping = {
            'trades_sent': lifetime.get('trades_sent', 0),
            'trades_accepted': lifetime.get('trades_accepted', 0),
            'trades_declined': lifetime.get('trades_declined', 0),
            'trades_countered': lifetime.get('trades_countered', 0),
            'trades_cancelled': lifetime.get('trades_cancelled', 0),
            'profit_overall': lifetime.get('total_profit_overall', 0),
            'profit_rap': lifetime.get('total_profit_rap', 0),
            'profit_value': lifetime.get('total_profit_value', 0),
            'errors': lifetime.get('errors', 0),
            'sessions': lifetime.get('sessions', 0),
        }

        # Format uptime
        uptime_seconds = stats.get('lifetime_uptime', 0)
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        stat_mapping['uptime'] = f"{hours}h {minutes}m"

        for key, value in stat_mapping.items():
            self.update_stat(key, value)
