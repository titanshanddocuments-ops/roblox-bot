"""
UI Logger Adapter
Wraps the existing log function to also emit events to the UI
"""
from stats.events import EventEmitter


class UILoggerAdapter:
    """
    Adapter that wraps the existing logging system to emit UI events
    """

    def __init__(self, original_log_func):
        self.original_log = original_log_func
        self.events = EventEmitter()
        self.enabled = True

    def log(self, msg, dontPrint=False, severityNum=0):
        """
        Intercept log calls and emit to UI
        """
        # Call original log function
        self.original_log(msg, dontPrint, severityNum)

        # Only emit to UI if enabled
        if self.enabled:
            # Map severity numbers to severity names
            severity_map = {
                0: "info",
                1: "warning",
                2: "warning",
                3: "error",
                4: "error",
                5: "debug"
            }

            severity = severity_map.get(severityNum, "info")

            # Emit to UI
            if not dontPrint:
                self.events.emit_log(str(msg), severity)
