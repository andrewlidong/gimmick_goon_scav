# Scav Hunt Announcer

A Python application for managing and announcing items from the University of Chicago Scavenger Hunt list. Available in both GUI and command-line interfaces.

## Features

### GUI Version
- Modern, user-friendly interface with intuitive controls
- Real-time preview of selected items
- Advanced voice control settings:
  - Voice selection from system voices
  - Speech rate adjustment (50-300)
  - Volume control (0-100%)
  - Voice testing capability
- Multiple item selection methods:
  - By page numbers
  - By item numbers
  - Random selection
- Announcement history tracking
- Scheduled announcements with configurable intervals
- Visual feedback and status updates

### Command-Line Version
- Interactive menu-driven interface
- Multiple selection methods
- Text-to-speech announcements
- Configurable announcement intervals
- History tracking

## Requirements

- Python 3.6 or higher
- macOS (for text-to-speech functionality)
- Required Python packages:
  - PyQt5 (for GUI version)
  - PyPDF2
  - schedule

## Installation

1. Clone the repository:
```bash
git clone https://github.com/andrewlidong/scav-hunt-announcer.git
cd scav-hunt-announcer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Version

1. Start the GUI application:
```bash
python scav_announcer_gui.py
```

2. Using the GUI:
   - **Select Items**:
     - Enter page numbers (e.g., "1,2,3") and click "Select by Pages"
     - Use the item number range selector
     - Choose number of random items and click "Select Random"
   
   - **Voice Settings**:
     - Choose a voice from the dropdown
     - Adjust speech rate (50-300)
     - Control volume using the slider
     - Test settings with "Test Voice" button
   
   - **Announcements**:
     - Click "Announce Now" for immediate announcement
     - Use "Start Announcements" for scheduled announcements
     - "Stop Announcements" to end scheduled announcements
   
   - **Monitor**:
     - View selected items in the preview section
     - Check announcement history in the bottom section
     - See next scheduled announcement time

### Command-Line Version

1. Run the command-line interface:
```bash
python scav_announcer.py
```

2. Follow the menu options to:
   - Select items by page numbers
   - Select items by item numbers
   - Select random items
   - Start/stop announcements
   - Preview current selection

## Configuration

Settings can be customized in `config.py`:

```python
# Default settings
DEFAULT_PDF_PATH = "scav_lists/2024.pdf"
ANNOUNCEMENT_INTERVAL_HOURS = 2
MAX_PREVIEW_ITEMS = 5
MAX_ITEM_PREVIEW_LENGTH = 100

# Text-to-speech settings
TTS_VOICE = "Samantha"  # Default voice
TTS_RATE = 150  # Speech rate (50-300)
TTS_VOLUME = 1.0  # Volume level (0.0 to 1.0)
```

## PDF Format

Place your scavenger hunt list PDF in the `scav_lists` directory. The PDF should have:
- One item per line
- Clear page numbers
- Consistent formatting

A sample PDF (`scav_lists/sample.pdf`) is provided for reference.

## Troubleshooting

1. **Voice Issues**:
   - Ensure macOS text-to-speech is enabled
   - Try different voices from the system
   - Adjust rate if speech is unclear

2. **PDF Reading Issues**:
   - Verify PDF format matches requirements
   - Check file permissions
   - Ensure PDF is not password-protected

3. **GUI Issues**:
   - Verify PyQt5 installation
   - Check system requirements
   - Try reinstalling dependencies