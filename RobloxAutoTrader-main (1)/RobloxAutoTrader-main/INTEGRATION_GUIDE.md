# UI Integration Guide

## Overview

This guide explains how to integrate the new 8-bit purple UI with your existing Roblox trading bot.

## What Was Added

### New Modules

1. **stats/** - Statistics tracking and persistence
   - `events.py` - Event emitter for UI updates
   - `stats_manager.py` - Tracks lifetime and session statistics

2. **ui/** - Retro terminal UI components
   - `app.py` - Main UI window
   - `theme.py` - 8-bit purple color scheme
   - `components/` - Reusable UI components
     - `log_viewer.py` - Live log viewer
     - `stats_panel.py` - Statistics display
     - `status_bar.py` - Bot status indicator

3. **core/** - Integration layer
   - `ui_logger.py` - Wraps existing logger to emit UI events
   - `bot_wrapper.py` - Wraps bot methods to track statistics

4. **main_ui.py** - New entry point that launches bot with UI

## How It Works

### Architecture

```
┌─────────────────┐
│   UI (Tkinter)  │ ← Shows logs, stats, status
└────────┬────────┘
         │
         │ subscribes to
         ↓
┌─────────────────┐
│  Event Emitter  │ ← Thread-safe event system
└────────┬────────┘
         ↑
         │ emits events
┌────────┴────────┐
│  Stats Manager  │ ← Tracks statistics
│  & UI Logger    │
└────────┬────────┘
         ↑
         │ calls
┌────────┴────────┐
│  Original Bot   │ ← Your existing logic (unchanged)
│     (Doggo)     │
└─────────────────┘
```

### Key Design Decisions

1. **No Core Logic Changes** - Your existing bot code is completely untouched
2. **Event-Driven** - UI subscribes to events, never blocks bot operations
3. **Thread-Safe** - All UI updates happen via thread-safe queue
4. **Persistent Stats** - Statistics saved to JSON file between sessions

## Running the UI

### Option 1: Quick Start (Recommended)

```bash
python main_ui.py
```

This will:
1. Launch the purple retro UI window
2. Start the trading bot in a background thread
3. Stream all activity to the UI in real-time

### Option 2: Test UI Only

```python
from ui.app import TradingBotUI

ui = TradingBotUI()
ui.add_log("Test message", "success")
ui.set_status("TESTING")
ui.run()
```

### Option 3: Integrate Into Existing Code

Add these lines to your existing `main.py`:

```python
from stats.events import EventEmitter
from stats.stats_manager import StatsManager

# At the start of your script
events = EventEmitter()
stats = StatsManager()
stats.start_session()

# Throughout your code, emit events:
events.emit_status("SCANNING")
events.emit_log("Trade sent to user 12345", "success")
stats.increment('trades_sent')
stats.add_profit(rap_gain=500, value_gain=100, overall_gain=600)
```

## Adding Statistics Tracking

### Manual Integration Points

To track statistics in your existing code, add these calls:

#### 1. When Sending a Trade

In `roblox_api.py` → `send_trade()`:

```python
# Add at the top
from stats.stats_manager import StatsManager
from stats.events import EventEmitter

# In the send_trade method, after successful send:
if Response.status_code == 200:
    StatsManager().increment('trades_sent')
    EventEmitter().emit_log(f"Trade sent to {trader_id}", "success")
    return trade_response.json()['id']
```

#### 2. When Checking Completeds

In `roblox_api.py` → `check_completeds()`:

```python
# When a trade is found as accepted:
StatsManager().increment('trades_accepted')

# Extract profit from formatted_trade
rap_gain = formatted_trade['their_rap'] - formatted_trade['self_rap']
value_gain = formatted_trade['their_value'] - formatted_trade['self_value']
overall_gain = formatted_trade['their_overall_value'] - formatted_trade['self_overall_value']

StatsManager().add_profit(
    rap_gain=int(rap_gain),
    value_gain=int(value_gain),
    overall_gain=int(overall_gain)
)
EventEmitter().emit_log(f"Trade completed! +{overall_gain} profit", "success")
```

#### 3. When Countering Trades

In `roblox_api.py` → `counter_trades()`:

```python
# After successful counter
if send_trade_response:
    StatsManager().increment('trades_countered')
    EventEmitter().emit_log("Counter trade sent", "info")
```

#### 4. When Cancelling Outbounds

In `roblox_api.py` → `outbound_api_checker()`:

```python
# After cancelling
if cancel_request.status_code == 200:
    StatsManager().increment('trades_cancelled')
    EventEmitter().emit_log("Cancelled losing outbound", "warning")
```

#### 5. Status Updates

In `main.py` → Various places:

```python
from stats.events import EventEmitter

events = EventEmitter()

# When scanning
events.emit_status("SCANNING FOR TRADERS")

# When generating trades
events.emit_status("GENERATING TRADES")

# When waiting
events.emit_status("WAITING - RATE LIMITED")

# When idle
events.emit_status("IDLE")

# When error
events.emit_status("ERROR - CHECK LOGS")
```

## UI Features

### Live Log Viewer
- Color-coded by severity (info, success, warning, error, debug)
- Auto-scrolls to latest message
- Timestamps on every log
- Maximum 1000 lines (auto-trims old logs)

### Statistics Panel
Shows lifetime totals:
- Trades sent/accepted/declined/countered/cancelled
- Profit (RAP, Value, Overall)
- Total uptime
- Total sessions
- Error count

### Status Bar
- Visual indicator (colored circle)
- Current activity text
- Session uptime counter

### Keyboard Shortcuts
- Clear logs button clears the log viewer
- Window close prompts to stop bot

## Customizing the Theme

Edit `ui/theme.py`:

```python
COLORS = {
    'bg_primary': '#1a0a2e',      # Change background
    'text_primary': '#e94cff',     # Change text color
    'accent_success': '#39ff14',   # Change success color
    # ... etc
}
```

## Troubleshooting

### Issue: UI window freezes
**Cause:** Bot code is running in UI thread
**Fix:** Ensure bot runs in background thread (see `main_ui.py`)

### Issue: Logs not showing
**Cause:** Logger not emitting events
**Fix:** Make sure you're using `EventEmitter().emit_log()`

### Issue: Stats not updating
**Cause:** Stats not being incremented
**Fix:** Add `StatsManager().increment('stat_name')` calls

### Issue: UI doesn't close properly
**Cause:** Bot thread not daemon
**Fix:** Set `daemon=True` when creating bot thread

## File Structure Summary

```
RobloxAutoTrader-main/
├── main.py                  # Original entry point (unchanged)
├── main_ui.py              # NEW: UI entry point
├── stats/                  # NEW: Statistics module
│   ├── __init__.py
│   ├── events.py          # Event emitter
│   └── stats_manager.py   # Stats tracking
├── ui/                    # NEW: UI module
│   ├── __init__.py
│   ├── app.py            # Main UI window
│   ├── theme.py          # Color scheme
│   └── components/
│       ├── __init__.py
│       ├── log_viewer.py
│       ├── stats_panel.py
│       └── status_bar.py
├── core/                 # NEW: Integration layer
│   ├── __init__.py
│   ├── ui_logger.py     # Logger adapter
│   └── bot_wrapper.py   # Bot wrapper
└── [all your existing files remain unchanged]
```

## Next Steps

1. **Run the UI**: `python main_ui.py`
2. **Test it out**: Watch logs appear in real-time
3. **Add tracking**: Add statistics calls to your bot code
4. **Customize**: Adjust colors, fonts, layout in `theme.py`

## Example: Full Integration

Here's a complete example of integrating stats into one method:

```python
# In roblox_api.py
def send_trade(self, trader_id, trade_send, trade_recieve, self_robux=None,
                counter_trade=False, counter_id=None):
    # Import at top of file
    from stats.events import EventEmitter
    from stats.stats_manager import StatsManager

    events = EventEmitter()
    stats = StatsManager()

    # ... existing code ...

    if trade_response.status_code == 200:
        log("Trade sent!")

        # ADD THESE LINES:
        stats.increment('trades_sent')
        events.emit_log(f"Trade sent to user {trader_id}", "success")
        events.emit_status("TRADE SENT - SCANNING")

        return trade_response.json()['id']

    # ... rest of existing code ...
```

That's it! The UI will automatically update with the new statistics.

## Support

If you encounter issues:
1. Check console for error messages
2. Verify all new files are in correct directories
3. Ensure no syntax errors in integration code
4. Check that bot thread is running with `daemon=True`

Happy trading!
