# Scavenger Hunt Announcer

This application reads a PDF file containing a scavenger hunt list and announces each item every 2 hours using text-to-speech.

## Requirements

- Python 3.6 or higher
- A PDF file containing your scavenger hunt list (one item per line)

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python scav_announcer.py
   ```
2. When prompted, enter the full path to your PDF file
3. The application will:
   - Read all items from the PDF
   - Announce the first item immediately
   - Continue announcing items every 2 hours
   - Loop back to the beginning when all items have been announced

## Features

- Reads PDF files and extracts text
- Announces items using text-to-speech
- Runs continuously, announcing items every 2 hours
- Shows current time with each announcement
- Automatically loops through the list
- Prints announcements to console as well as speaking them

## Notes

- Make sure your PDF file is readable and contains text (not scanned images)
- Each item should be on a separate line in the PDF
- The application will keep running until you stop it (Ctrl+C) 