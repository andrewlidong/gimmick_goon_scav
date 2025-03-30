import PyPDF2
import schedule
import time
import os
import subprocess
import random
from datetime import datetime

class ScavAnnouncer:
    def __init__(self):
        self.pdf_path = "scav_lists/2024.pdf"
        self.items = []
        self.selected_items = []
        self.current_index = 0
        self._read_pdf()

    def _read_pdf(self):
        """Read items from the PDF file."""
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    # Split by newlines and filter out empty lines
                    items = [item.strip() for item in text.split('\n') if item.strip()]
                    # Store items with their page numbers and indices
                    self.items.extend([(item, page_num, idx + 1) for idx, item in enumerate(items)])
        except Exception as e:
            print(f"Error reading PDF: {e}")

    def select_by_pages(self, pages):
        """Select items from specific pages."""
        self.selected_items = [item for item in self.items if item[1] in pages]
        print(f"\nSelected {len(self.selected_items)} items from pages {pages}")
        self._preview_selection()

    def select_by_item_numbers(self, start, end):
        """Select items by their item numbers."""
        self.selected_items = [item for item in self.items if start <= item[2] <= end]
        print(f"\nSelected {len(self.selected_items)} items from numbers {start} to {end}")
        self._preview_selection()

    def select_random(self, count):
        """Select a random set of items."""
        if count > len(self.items):
            count = len(self.items)
        self.selected_items = random.sample(self.items, count)
        print(f"\nRandomly selected {count} items")
        self._preview_selection()

    def _preview_selection(self):
        """Show a preview of selected items."""
        print("\nPreview of selected items:")
        for i, (item, page, num) in enumerate(self.selected_items[:5], 1):
            print(f"{i}. (Page {page}, #{num}) {item[:100]}...")
        if len(self.selected_items) > 5:
            print(f"... and {len(self.selected_items) - 5} more items")

    def announce_next_item(self):
        """Announce the next item in the selected list."""
        if not self.selected_items:
            print("No items selected! Please select items first.")
            return

        if self.current_index >= len(self.selected_items):
            print("All items have been announced!")
            self.current_index = 0  # Reset to start over

        current_time = datetime.now().strftime("%H:%M")
        item, page, num = self.selected_items[self.current_index]
        
        announcement = f"Time to work on item number {num} from page {page}: {item}"
        print(f"\n{announcement}")
        
        try:
            subprocess.run(['say', announcement])
        except Exception as e:
            print(f"Error with text-to-speech: {e}")
        
        self.current_index += 1

def print_menu():
    print("\nScavenger Hunt Announcer Menu:")
    print("1. Select items by page numbers")
    print("2. Select items by item numbers")
    print("3. Select random items")
    print("4. Start announcements (2-hour intervals)")
    print("5. Preview current selection")
    print("6. Exit")

def main():
    announcer = ScavAnnouncer()
    
    if not announcer.items:
        print("Error: Could not read the scavenger hunt list!")
        return

    print(f"Successfully loaded {len(announcer.items)} items from the scavenger hunt list!")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            pages = input("Enter page numbers (comma-separated, e.g., 1,2,3): ")
            try:
                page_list = [int(p.strip()) for p in pages.split(',')]
                announcer.select_by_pages(page_list)
            except ValueError:
                print("Invalid input! Please enter numbers separated by commas.")
        
        elif choice == '2':
            try:
                start = int(input("Enter starting item number: "))
                end = int(input("Enter ending item number: "))
                announcer.select_by_item_numbers(start, end)
            except ValueError:
                print("Invalid input! Please enter valid numbers.")
        
        elif choice == '3':
            try:
                count = int(input("How many random items do you want? "))
                announcer.select_random(count)
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        
        elif choice == '4':
            if not announcer.selected_items:
                print("Please select items first!")
                continue
                
            print("\nStarting announcements every 2 hours...")
            print("(Press Ctrl+C to stop)")
            
            # Schedule announcements every 2 hours
            schedule.every(2).hours.do(announcer.announce_next_item)
            
            # Run the first announcement immediately
            announcer.announce_next_item()
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nStopping announcements...")
                schedule.clear()
        
        elif choice == '5':
            if announcer.selected_items:
                announcer._preview_selection()
            else:
                print("No items currently selected!")
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main() 