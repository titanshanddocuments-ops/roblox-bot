"""
UI Demo - Test the UI without running the full bot
Shows what the UI looks like with sample data
"""
import time
import random
import threading
from ui.app import TradingBotUI
from stats.events import EventEmitter
from stats.stats_manager import StatsManager


def simulate_bot_activity(ui_app):
    """
    Simulate bot activity for demo purposes
    """
    events = EventEmitter()
    stats = StatsManager()

    # Start session
    stats.start_session()

    # Demo log messages
    demo_logs = [
        ("Initializing bot systems...", "info"),
        ("Loading account configuration", "info"),
        ("Connecting to Roblox API", "info"),
        ("Authentication successful", "success"),
        ("Loading rolimons data", "info"),
        ("Starting trader queue", "info"),
        ("Scanning for active traders", "info"),
        ("Found 25 potential traders", "success"),
        ("Fetching inventory for user 123456", "info"),
        ("Inventory scan complete - 47 items found", "success"),
        ("Generating trade combinations", "info"),
        ("Found 3 valid trades", "success"),
        ("Selecting best trade", "info"),
        ("Trade sent to user 123456", "success"),
        ("Rate limit detected, waiting 10 seconds", "warning"),
        ("Scanning for traders", "info"),
        ("User 789012 has no tradeable items", "warning"),
        ("Checking outbound trades", "info"),
        ("Cancelled 1 losing outbound trade", "warning"),
        ("Checking completed trades", "info"),
        ("Trade accepted! Profit: +450 RAP", "success"),
        ("Continuing scan", "info"),
    ]

    statuses = [
        "INITIALIZING",
        "SCANNING FOR TRADERS",
        "FETCHING INVENTORY",
        "GENERATING TRADES",
        "SENDING TRADE",
        "WAITING - RATE LIMITED",
        "CHECKING OUTBOUNDS",
        "IDLE",
    ]

    # Simulate activity
    for i in range(50):
        if i < len(demo_logs):
            message, severity = demo_logs[i]
            events.emit_log(message, severity)

        # Change status periodically
        if i % 4 == 0 and statuses:
            status = statuses[i % len(statuses)]
            events.emit_status(status)

        # Simulate stats updates
        if i % 5 == 0:
            stats.increment('trades_sent')

        if i % 8 == 0:
            stats.increment('trades_accepted')
            stats.add_profit(rap_gain=random.randint(100, 800),
                           value_gain=random.randint(0, 500),
                           overall_gain=random.randint(200, 900))

        if i % 12 == 0:
            stats.increment('trades_declined')

        if i % 15 == 0:
            stats.increment('trades_countered')

        time.sleep(2)

    events.emit_log("Demo completed!", "success")
    events.emit_status("DEMO COMPLETE - IDLE")


def main():
    """
    Run the UI demo
    """
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              DOGGO TRADER - UI DEMO                      ║")
    print("║                                                          ║")
    print("║  This demo shows the UI with simulated bot activity     ║")
    print("║  No actual trading will occur                           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("Launching UI demo...")
    print()

    # Create UI
    ui_app = TradingBotUI()

    # Start simulated activity in background
    demo_thread = threading.Thread(target=simulate_bot_activity, args=(ui_app,), daemon=True)
    demo_thread.start()

    # Run UI
    ui_app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo stopped.")
