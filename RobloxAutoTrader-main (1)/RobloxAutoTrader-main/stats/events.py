import threading
from typing import Callable, Dict, List
from queue import Queue


class EventEmitter:
    """
    Thread-safe event emitter for UI updates.
    Allows the core logic to emit events that the UI can subscribe to.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.listeners: Dict[str, List[Callable]] = {}
        self.log_queue = Queue()
        self._lock = threading.Lock()

    def on(self, event: str, callback: Callable):
        """Subscribe to an event"""
        with self._lock:
            if event not in self.listeners:
                self.listeners[event] = []
            self.listeners[event].append(callback)

    def off(self, event: str, callback: Callable):
        """Unsubscribe from an event"""
        with self._lock:
            if event in self.listeners:
                self.listeners[event].remove(callback)

    def emit(self, event: str, data=None):
        """Emit an event to all subscribers"""
        with self._lock:
            if event in self.listeners:
                for callback in self.listeners[event]:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"Error in event handler: {e}")

    def emit_log(self, message: str, severity: str = "info"):
        """Emit a log message"""
        self.log_queue.put({"message": message, "severity": severity})
        self.emit("log", {"message": message, "severity": severity})

    def emit_status(self, status: str):
        """Emit status change"""
        self.emit("status", status)

    def emit_stat(self, stat_name: str, value):
        """Emit statistics update"""
        self.emit("stat", {"name": stat_name, "value": value})
