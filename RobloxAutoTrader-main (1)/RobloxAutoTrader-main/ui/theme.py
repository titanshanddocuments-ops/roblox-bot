"""
8-bit / Retro Terminal Theme
Deep Purple / Neon Purple with Magenta highlights
"""

# Color Palette
COLORS = {
    # Background colors
    'bg_primary': '#1a0a2e',        # Deep purple background
    'bg_secondary': '#16213e',      # Slightly lighter purple
    'bg_panel': '#0f0726',          # Darker panel background

    # Text colors
    'text_primary': '#e94cff',      # Neon purple
    'text_secondary': '#b968ff',    # Lighter purple
    'text_dim': '#7d5ba6',          # Dimmed purple
    'text_white': '#f0e6ff',        # Off-white with purple tint

    # Accent colors
    'accent_magenta': '#ff00ff',    # Bright magenta
    'accent_cyan': '#00ffff',       # Cyan for info
    'accent_success': '#39ff14',    # Neon green for success
    'accent_warning': '#ffaa00',    # Orange for warnings
    'accent_error': '#ff0055',      # Pink-red for errors

    # Border colors
    'border_main': '#7d3fff',       # Purple border
    'border_active': '#ff00ff',     # Magenta for active elements

    # Status colors
    'status_idle': '#7d5ba6',       # Dim purple
    'status_active': '#39ff14',     # Neon green
    'status_error': '#ff0055',      # Pink-red
    'status_warning': '#ffaa00',    # Orange
}

# Font settings
FONTS = {
    'mono_regular': ('Consolas', 10),
    'mono_bold': ('Consolas', 10, 'bold'),
    'mono_large': ('Consolas', 12, 'bold'),
    'mono_small': ('Consolas', 8),
    'title': ('Consolas', 16, 'bold'),
}

# UI Settings
UI_CONFIG = {
    'window_width': 1000,
    'window_height': 700,
    'padding': 10,
    'border_width': 2,
    'corner_radius': 0,  # Sharp corners for 8-bit look
}

# ASCII Art for the header
ASCII_HEADER = """
╔══════════════════════════════════════════════════════════════════════╗
║  ██████╗  ██████╗  ██████╗  ██████╗  ██████╗     ████████╗██████╗   ║
║  ██╔══██╗██╔═══██╗██╔════╝ ██╔════╝ ██╔═══██╗    ╚══██╔══╝██╔══██╗  ║
║  ██║  ██║██║   ██║██║  ███╗██║  ███╗██║   ██║       ██║   ██████╔╝  ║
║  ██║  ██║██║   ██║██║   ██║██║   ██║██║   ██║       ██║   ██╔══██╗  ║
║  ██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝       ██║   ██║  ██║  ║
║  ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝        ╚═╝   ╚═╝  ╚═╝  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

# Status indicators
STATUS_ICONS = {
    'idle': '○',
    'active': '●',
    'scanning': '◐',
    'sending': '►',
    'error': '✗',
    'success': '✓',
    'waiting': '◌',
}

# Log severity colors
LOG_COLORS = {
    'info': COLORS['text_secondary'],
    'success': COLORS['accent_success'],
    'warning': COLORS['accent_warning'],
    'error': COLORS['accent_error'],
    'debug': COLORS['text_dim'],
}

def get_log_tag_color(severity: str):
    """Get color for log severity tag"""
    return LOG_COLORS.get(severity.lower(), COLORS['text_primary'])
