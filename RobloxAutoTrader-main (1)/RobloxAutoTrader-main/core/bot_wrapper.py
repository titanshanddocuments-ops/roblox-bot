"""
Bot Wrapper with UI Integration
Wraps key bot methods to emit statistics and status updates
"""
from stats.events import EventEmitter
from stats.stats_manager import StatsManager


class BotWrapper:
    """
    Wrapper that adds UI event emissions to bot operations
    """

    def __init__(self, doggo_instance):
        self.doggo = doggo_instance
        self.events = EventEmitter()
        self.stats = StatsManager()
        self._wrap_methods()

    def _wrap_methods(self):
        """Wrap key methods to emit events"""

        # Wrap trade sending
        if hasattr(self.doggo, 'start_trader'):
            original_start = self.doggo.start_trader

            def wrapped_start():
                self.events.emit_status("SCANNING FOR TRADERS")
                return original_start()

            self.doggo.start_trader = wrapped_start

    def track_trade_sent(self, result, trade_data=None):
        """Track when a trade is sent"""
        if result:
            self.stats.increment('trades_sent')
            self.events.emit_log("Trade sent successfully", "success")

            if trade_data:
                # Calculate and track profit
                rap_gain = trade_data.get('their_rap', 0) - trade_data.get('self_rap', 0)
                value_gain = trade_data.get('their_value', 0) - trade_data.get('self_value', 0)
                overall_gain = trade_data.get('their_overall_value', 0) - trade_data.get('self_overall_value', 0)

                self.stats.add_profit(
                    rap_gain=int(rap_gain),
                    value_gain=int(value_gain),
                    overall_gain=int(overall_gain)
                )
        else:
            self.events.emit_log("Trade send failed", "warning")

    def track_trade_accepted(self):
        """Track when a trade is accepted"""
        self.stats.increment('trades_accepted')
        self.events.emit_log("Trade accepted!", "success")

    def track_trade_declined(self):
        """Track when a trade is declined"""
        self.stats.increment('trades_declined')
        self.events.emit_log("Trade declined", "info")

    def track_trade_countered(self):
        """Track when a trade is countered"""
        self.stats.increment('trades_countered')
        self.events.emit_log("Trade countered", "info")

    def track_trade_cancelled(self):
        """Track when a trade is cancelled"""
        self.stats.increment('trades_cancelled')
        self.events.emit_log("Trade cancelled", "warning")

    def track_error(self, error_msg):
        """Track when an error occurs"""
        self.stats.increment('errors')
        self.events.emit_log(f"Error: {error_msg}", "error")

    def set_status(self, status):
        """Update bot status"""
        self.events.emit_status(status)
