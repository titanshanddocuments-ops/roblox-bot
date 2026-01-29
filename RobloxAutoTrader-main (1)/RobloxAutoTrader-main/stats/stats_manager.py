import os
from datetime import datetime
import time
from handler.handle_json import JsonHandler
from stats.events import EventEmitter


class StatsManager:
    """
    Manages lifetime statistics for the trading bot.
    Persists data locally and optionally syncs to Supabase.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.stats_file = JsonHandler('stats_lifetime.json')
        self.events = EventEmitter()
        self.session_start = time.time()

        # Initialize stats structure
        self.stats = self._load_stats()

    def _load_stats(self):
        """Load stats from file or create default structure"""
        try:
            data = self.stats_file.read_data()
            if not data:
                data = self._default_stats()
                self.stats_file.write_data(data)
            return data
        except:
            data = self._default_stats()
            self.stats_file.write_data(data)
            return data

    def _default_stats(self):
        """Default statistics structure"""
        return {
            "lifetime": {
                "trades_sent": 0,
                "trades_accepted": 0,
                "trades_declined": 0,
                "trades_countered": 0,
                "trades_cancelled": 0,
                "errors": 0,
                "total_profit_rap": 0,
                "total_profit_value": 0,
                "total_profit_overall": 0,
                "uptime_seconds": 0,
                "sessions": 0,
                "last_session": None
            },
            "session": {
                "trades_sent": 0,
                "trades_accepted": 0,
                "trades_declined": 0,
                "trades_countered": 0,
                "trades_cancelled": 0,
                "errors": 0,
                "profit_rap": 0,
                "profit_value": 0,
                "profit_overall": 0,
                "start_time": datetime.now().isoformat()
            }
        }

    def increment(self, stat_name: str, amount: int = 1):
        """Increment a statistic"""
        # Update session stats
        if stat_name in self.stats["session"]:
            self.stats["session"][stat_name] += amount

        # Update lifetime stats
        if stat_name in self.stats["lifetime"]:
            self.stats["lifetime"][stat_name] += amount

        self._save_stats()
        self.events.emit_stat(stat_name, self.stats["lifetime"].get(stat_name, 0))

    def add_profit(self, rap_gain: int = 0, value_gain: int = 0, overall_gain: int = 0):
        """Add profit to statistics"""
        self.stats["session"]["profit_rap"] += rap_gain
        self.stats["session"]["profit_value"] += value_gain
        self.stats["session"]["profit_overall"] += overall_gain

        self.stats["lifetime"]["total_profit_rap"] += rap_gain
        self.stats["lifetime"]["total_profit_value"] += value_gain
        self.stats["lifetime"]["total_profit_overall"] += overall_gain

        self._save_stats()
        self.events.emit("profit_update", {
            "rap": self.stats["lifetime"]["total_profit_rap"],
            "value": self.stats["lifetime"]["total_profit_value"],
            "overall": self.stats["lifetime"]["total_profit_overall"]
        })

    def get_session_uptime(self):
        """Get current session uptime in seconds"""
        return int(time.time() - self.session_start)

    def get_lifetime_uptime(self):
        """Get total lifetime uptime in seconds"""
        return self.stats["lifetime"]["uptime_seconds"] + self.get_session_uptime()

    def start_session(self):
        """Start a new session"""
        self.stats["lifetime"]["sessions"] += 1
        self.stats["lifetime"]["last_session"] = datetime.now().isoformat()
        self.session_start = time.time()

        # Reset session stats
        self.stats["session"] = {
            "trades_sent": 0,
            "trades_accepted": 0,
            "trades_declined": 0,
            "trades_countered": 0,
            "trades_cancelled": 0,
            "errors": 0,
            "profit_rap": 0,
            "profit_value": 0,
            "profit_overall": 0,
            "start_time": datetime.now().isoformat()
        }

        self._save_stats()

    def end_session(self):
        """End current session and save uptime"""
        session_time = self.get_session_uptime()
        self.stats["lifetime"]["uptime_seconds"] += session_time
        self._save_stats()

    def _save_stats(self):
        """Save statistics to file"""
        try:
            self.stats_file.write_data(self.stats)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def get_stats(self):
        """Get current statistics"""
        return {
            "lifetime": self.stats["lifetime"].copy(),
            "session": self.stats["session"].copy(),
            "session_uptime": self.get_session_uptime(),
            "lifetime_uptime": self.get_lifetime_uptime()
        }
