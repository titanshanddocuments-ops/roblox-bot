"""
Main entry point for the trading bot with UI
Launches the bot in a background thread and shows the UI
"""
import sys
import threading
import time
from ui.app import TradingBotUI
from stats.events import EventEmitter
from stats.stats_manager import StatsManager
from core.ui_logger import UILoggerAdapter

# Import original logging
from handler.handle_logs import log as original_log

# Create global UI logger
ui_logger = UILoggerAdapter(original_log)

# Monkey-patch the log function in all modules
import handler.handle_logs
handler.handle_logs.log = ui_logger.log


def run_bot_in_background(ui_app):
    """
    Run the original Doggo bot in a background thread
    """
    try:
        from main import Doggo

        events = EventEmitter()
        stats = StatsManager()

        # Start a new session
        stats.start_session()
        events.emit_log("Starting trading bot...", "info")
        events.emit_status("STARTING")

        # Create and run bot
        doggo = Doggo()

        # Hook into bot methods to track statistics
        original_send_trade = None
        for account in doggo.load_roblox_accounts():
            if hasattr(account, 'send_trade'):
                original_send_trade = account.send_trade

                def wrapped_send_trade(*args, **kwargs):
                    result = original_send_trade(*args, **kwargs)
                    if result:
                        stats.increment('trades_sent')
                        events.emit_log(f"Trade sent successfully", "success")
                    return result

                account.send_trade = wrapped_send_trade

        events.emit_status("SCANNING FOR TRADERS")

        # Run the main bot loop
        doggo.start_trader()

    except KeyboardInterrupt:
        events.emit_log("Bot stopped by user", "warning")
        events.emit_status("STOPPED")
    except Exception as e:
        events = EventEmitter()
        stats = StatsManager()
        stats.increment('errors')
        events.emit_log(f"Bot error: {str(e)}", "error")
        events.emit_status("ERROR")
        import traceback
        events.emit_log(traceback.format_exc(), "debug")


def main():
    """
    Main entry point - launches UI and bot
    """
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         DOGGO TRADER - ROBLOX TRADING BOT                ║")
    print("║                    UI MODE v1.0                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("Launching UI...")

    # Create UI
    ui_app = TradingBotUI()

    # Check if user wants to run bot automatically
    ui_app.events.emit_log("UI Ready. Type 'start' in console or close window to run bot.", "info")

    # Subscribe to shutdown event
    def on_shutdown(data):
        print("\nShutdown requested from UI. Stopping bot...")
        sys.exit(0)

    ui_app.events.on("app_shutdown", on_shutdown)

    # Start bot in background thread with a slight delay
    bot_thread = threading.Thread(target=run_bot_in_background, args=(ui_app,), daemon=True)
    bot_thread.start()

    # Run UI (blocking)
    ui_app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
