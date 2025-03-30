"""
Configuration settings for the Scavenger Hunt Announcer.
"""

# Default settings
DEFAULT_PDF_PATH = "scav_lists/2024.pdf"
ANNOUNCEMENT_INTERVAL_HOURS = 2
MAX_PREVIEW_ITEMS = 5
MAX_ITEM_PREVIEW_LENGTH = 100

# Text-to-speech settings
TTS_VOICE = "Samantha"  # A clear, natural-sounding voice
TTS_RATE = 150  # Speech rate (50-300)
TTS_VOLUME = 1.0  # Volume level (0.0 to 1.0)
TTS_PITCH = 1.0  # Pitch level (0.5 to 2.0)
TTS_PAUSE_BETWEEN_ITEMS = 1.0  # Pause between items in seconds

# Logging settings
LOG_FILE = "scav_announcer.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# Menu options
MENU_OPTIONS = {
    "1": "Select items by page numbers",
    "2": "Select items by item numbers",
    "3": "Select random items",
    "4": "Start announcements",
    "5": "Preview current selection",
    "6": "Exit"
} 