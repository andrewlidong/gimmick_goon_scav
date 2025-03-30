import PyPDF2
import schedule
import time
import os
import subprocess
import random
import logging
import json
from datetime import datetime
from config import *

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class ScavAnnouncer:
    def __init__(self):
        self.pdf_path = DEFAULT_PDF_PATH
        self.items = []
        self.selected_items = []
        self.current_index = 0
        self.announcement_history = []
        self._read_pdf()
        self._load_history()

    def _read_pdf(self):
        """Read items from the PDF file."""
        try:
            if not os.path.exists(self.pdf_path):
                raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    # Split by newlines and filter out empty lines
                    items = [item.strip() for item in text.split('\n') if item.strip()]
                    # Store items with their page numbers and indices
                    self.items.extend([(item, page_num, idx + 1) for idx, item in enumerate(items)])
                
                logging.info(f"Successfully loaded {len(self.items)} items from {self.pdf_path}")
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")
            raise

    def _load_history(self):
        """Load announcement history from file."""
        try:
            if os.path.exists('announcement_history.json'):
                with open('announcement_history.json', 'r') as f:
                    self.announcement_history = json.load(f)
                logging.info("Loaded announcement history")
        except Exception as e:
            logging.error(f"Error loading history: {e}")

    def _save_history(self):
        """Save announcement history to file."""
        try:
            with open('announcement_history.json', 'w') as f:
                json.dump(self.announcement_history, f)
            logging.info("Saved announcement history")
        except Exception as e:
            logging.error(f"Error saving history: {e}")

    def select_by_pages(self, pages):
        """Select items from specific pages."""
        try:
            self.selected_items = [item for item in self.items if item[1] in pages]
            logging.info(f"Selected {len(self.selected_items)} items from pages {pages}")
            self._preview_selection()
        except Exception as e:
            logging.error(f"Error selecting by pages: {e}")
            raise

    def select_by_item_numbers(self, start, end):
        """Select items by their item numbers."""
        try:
            if start < 1 or end > len(self.items):
                raise ValueError(f"Invalid range: {start}-{end}. Valid range is 1-{len(self.items)}")
            
            self.selected_items = [item for item in self.items if start <= item[2] <= end]
            logging.info(f"Selected {len(self.selected_items)} items from numbers {start} to {end}")
            self._preview_selection()
        except Exception as e:
            logging.error(f"Error selecting by item numbers: {e}")
            raise

    def select_random(self, count):
        """Select a random set of items."""
        try:
            if count > len(self.items):
                count = len(self.items)
                logging.warning(f"Requested count exceeds total items. Using {count} instead.")
            
            self.selected_items = random.sample(self.items, count)
            logging.info(f"Randomly selected {count} items")
            self._preview_selection()
        except Exception as e:
            logging.error(f"Error selecting random items: {e}")
            raise

    def _preview_selection(self):
        """Show a preview of selected items."""
        if not self.selected_items:
            logging.warning("No items selected!")
            return

        print("\nPreview of selected items:")
        for i, (item, page, num) in enumerate(self.selected_items[:MAX_PREVIEW_ITEMS], 1):
            print(f"{i}. (Page {page}, #{num}) {item[:MAX_ITEM_PREVIEW_LENGTH]}...")
        if len(self.selected_items) > MAX_PREVIEW_ITEMS:
            print(f"... and {len(self.selected_items) - MAX_PREVIEW_ITEMS} more items")

    def announce_next_item(self):
        """Announce the next item in the selected list."""
        if not self.selected_items:
            logging.warning("No items selected! Please select items first.")
            return

        if self.current_index >= len(self.selected_items):
            logging.info("All items have been announced! Starting over...")
            self.current_index = 0

        current_time = datetime.now().strftime("%H:%M")
        item, page, num = self.selected_items[self.current_index]
        
        announcement = f"Time to work on item number {num} from page {page}: {item}"
        logging.info(f"Announcing: {announcement}")
        print(f"\n{announcement}")
        
        try:
            # Use say command with voice and rate options
            cmd = ['say', '-v', TTS_VOICE, '-r', str(TTS_RATE), announcement]
            subprocess.run(cmd)
            
            # Record announcement in history
            self.announcement_history.append({
                'timestamp': datetime.now().isoformat(),
                'item': item,
                'page': page,
                'number': num
            })
            self._save_history()
        except Exception as e:
            logging.error(f"Error with text-to-speech: {e}")
            print(f"Error with text-to-speech: {e}")
        
        self.current_index += 1

    def show_history(self):
        """Display announcement history."""
        if not self.announcement_history:
            print("\nNo announcement history available.")
            return

        print("\nAnnouncement History:")
        for entry in self.announcement_history[-10:]:  # Show last 10 announcements
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            print(f"{timestamp} - Page {entry['page']}, #{entry['number']}: {entry['item'][:100]}...")

def print_menu():
    print("\nScavenger Hunt Announcer Menu:")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")
    print("7. View announcement history")

def main():
    try:
        announcer = ScavAnnouncer()
        
        if not announcer.items:
            logging.error("No items were found in the PDF!")
            return

        logging.info("Starting Scavenger Hunt Announcer")
        
        while True:
            print_menu()
            choice = input("\nEnter your choice (1-7): ")
            
            try:
                if choice == '1':
                    pages = input("Enter page numbers (comma-separated, e.g., 1,2,3): ")
                    try:
                        page_list = [int(p.strip()) for p in pages.split(',')]
                        announcer.select_by_pages(page_list)
                    except ValueError:
                        logging.error("Invalid page numbers input")
                        print("Invalid input! Please enter numbers separated by commas.")
                
                elif choice == '2':
                    try:
                        start = int(input("Enter starting item number: "))
                        end = int(input("Enter ending item number: "))
                        announcer.select_by_item_numbers(start, end)
                    except ValueError:
                        logging.error("Invalid item numbers input")
                        print("Invalid input! Please enter valid numbers.")
                
                elif choice == '3':
                    try:
                        count = int(input("How many random items do you want? "))
                        announcer.select_random(count)
                    except ValueError:
                        logging.error("Invalid random count input")
                        print("Invalid input! Please enter a valid number.")
                
                elif choice == '4':
                    if not announcer.selected_items:
                        logging.warning("Attempted to start announcements without selection")
                        print("Please select items first!")
                        continue
                        
                    print(f"\nStarting announcements every {ANNOUNCEMENT_INTERVAL_HOURS} hours...")
                    print("(Press Ctrl+C to stop)")
                    
                    # Schedule announcements
                    schedule.every(ANNOUNCEMENT_INTERVAL_HOURS).hours.do(announcer.announce_next_item)
                    
                    # Run the first announcement immediately
                    announcer.announce_next_item()
                    
                    try:
                        while True:
                            schedule.run_pending()
                            time.sleep(60)
                    except KeyboardInterrupt:
                        logging.info("Stopping announcements...")
                        print("\nStopping announcements...")
                        schedule.clear()
                
                elif choice == '5':
                    if announcer.selected_items:
                        announcer._preview_selection()
                    else:
                        print("No items currently selected!")
                
                elif choice == '6':
                    logging.info("Exiting program")
                    print("Goodbye!")
                    break
                
                elif choice == '7':
                    announcer.show_history()
                
                else:
                    logging.warning(f"Invalid menu choice: {choice}")
                    print("Invalid choice! Please try again.")
            
            except Exception as e:
                logging.error(f"Error processing menu choice: {e}")
                print(f"An error occurred: {e}")
                print("Please try again.")

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
        return

if __name__ == "__main__":
    main() 