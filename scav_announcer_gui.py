import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QSpinBox, 
                           QLineEdit, QTextEdit, QMessageBox, QComboBox,
                           QGroupBox, QScrollArea, QSlider, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import schedule
import time
import subprocess
from datetime import datetime
from scav_announcer import ScavAnnouncer
from config import *

def get_available_voices():
    """Get list of available voices from macOS."""
    try:
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        voices = []
        for line in result.stdout.split('\n'):
            if line.strip():
                voice_name = line.split()[0]
                if not any(char.isdigit() for char in voice_name):  # Filter out numbered variants
                    voices.append(voice_name)
        return voices
    except Exception as e:
        print(f"Error getting voices: {e}")
        return ["Samantha"]  # Default fallback

class ScavAnnouncerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.announcer = ScavAnnouncer()
        self.schedule_timer = QTimer()
        self.schedule_timer.timeout.connect(self.check_schedule)
        self.available_voices = get_available_voices()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Scavenger Hunt Announcer')
        self.setGeometry(100, 100, 1000, 800)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        self.status_label = QLabel(f"Loaded {len(self.announcer.items)} items from {DEFAULT_PDF_PATH}")
        self.next_announcement_label = QLabel("Next announcement: Not scheduled")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.next_announcement_label)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        # Selection section
        selection_group = QGroupBox("Select Items")
        selection_layout = QVBoxLayout()

        # Page selection
        page_layout = QHBoxLayout()
        page_layout.addWidget(QLabel("Page numbers:"))
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("e.g., 1,2,3")
        page_layout.addWidget(self.page_input)
        select_pages_btn = QPushButton("Select by Pages")
        select_pages_btn.clicked.connect(self.select_by_pages)
        page_layout.addWidget(select_pages_btn)
        selection_layout.addLayout(page_layout)

        # Item number selection
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel("Item numbers:"))
        self.start_item = QSpinBox()
        self.start_item.setRange(1, len(self.announcer.items))
        self.end_item = QSpinBox()
        self.end_item.setRange(1, len(self.announcer.items))
        self.end_item.setValue(len(self.announcer.items))
        item_layout.addWidget(self.start_item)
        item_layout.addWidget(QLabel("to"))
        item_layout.addWidget(self.end_item)
        select_items_btn = QPushButton("Select by Items")
        select_items_btn.clicked.connect(self.select_by_item_numbers)
        item_layout.addWidget(select_items_btn)
        selection_layout.addLayout(item_layout)

        # Random selection
        random_layout = QHBoxLayout()
        random_layout.addWidget(QLabel("Random items:"))
        self.random_count = QSpinBox()
        self.random_count.setRange(1, len(self.announcer.items))
        self.random_count.setValue(5)
        random_layout.addWidget(self.random_count)
        select_random_btn = QPushButton("Select Random")
        select_random_btn.clicked.connect(self.select_random)
        random_layout.addWidget(select_random_btn)
        selection_layout.addLayout(random_layout)

        selection_group.setLayout(selection_layout)
        main_layout.addWidget(selection_group)

        # Preview section
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)

        # Voice settings section
        voice_group = QGroupBox("Voice Settings")
        voice_layout = QVBoxLayout()

        # Voice selection
        voice_select_layout = QHBoxLayout()
        voice_select_layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(self.available_voices)
        current_voice_index = self.available_voices.index(TTS_VOICE) if TTS_VOICE in self.available_voices else 0
        self.voice_combo.setCurrentIndex(current_voice_index)
        voice_select_layout.addWidget(self.voice_combo)
        voice_layout.addLayout(voice_select_layout)

        # Rate control
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Rate:"))
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(50, 300)
        self.rate_spin.setValue(TTS_RATE)
        rate_layout.addWidget(self.rate_spin)
        voice_layout.addLayout(rate_layout)

        # Pitch control
        pitch_layout = QHBoxLayout()
        pitch_layout.addWidget(QLabel("Pitch:"))
        self.pitch_spin = QDoubleSpinBox()
        self.pitch_spin.setRange(0.5, 2.0)
        self.pitch_spin.setSingleStep(0.1)
        self.pitch_spin.setValue(TTS_PITCH)
        pitch_layout.addWidget(self.pitch_spin)
        voice_layout.addLayout(pitch_layout)

        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(TTS_VOLUME * 100))
        volume_layout.addWidget(self.volume_slider)
        self.volume_label = QLabel(f"{int(TTS_VOLUME * 100)}%")
        volume_layout.addWidget(self.volume_label)
        voice_layout.addLayout(volume_layout)

        # Test voice button
        test_voice_btn = QPushButton("Test Voice")
        test_voice_btn.clicked.connect(self.test_voice)
        voice_layout.addWidget(test_voice_btn)

        voice_group.setLayout(voice_layout)
        main_layout.addWidget(voice_group)

        # Announcement section
        announcement_group = QGroupBox("Announcements")
        announcement_layout = QVBoxLayout()

        # Control buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Announcements")
        self.start_btn.clicked.connect(self.start_announcements)
        self.stop_btn = QPushButton("Stop Announcements")
        self.stop_btn.clicked.connect(self.stop_announcements)
        self.stop_btn.setEnabled(False)
        self.announce_now_btn = QPushButton("Announce Now")
        self.announce_now_btn.clicked.connect(self.announce_now)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.announce_now_btn)
        announcement_layout.addLayout(button_layout)

        announcement_group.setLayout(announcement_layout)
        main_layout.addWidget(announcement_group)

        # History section
        history_group = QGroupBox("Announcement History")
        history_layout = QVBoxLayout()
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        history_layout.addWidget(self.history_text)
        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)

        # Connect volume slider to label update
        self.volume_slider.valueChanged.connect(self.update_volume_label)

        # Update history display
        self.update_history_display()

    def update_volume_label(self, value):
        self.volume_label.setText(f"{value}%")

    def test_voice(self):
        """Test the current voice settings with a sample announcement."""
        test_text = "Testing voice settings. This is a sample announcement."
        try:
            subprocess.run([
                'say',
                '-v', self.voice_combo.currentText(),
                '-r', str(self.rate_spin.value()),
                test_text
            ])
        except Exception as e:
            QMessageBox.warning(self, "Voice Test Error", f"Error testing voice: {e}")

    def select_by_pages(self):
        try:
            pages = [int(p.strip()) for p in self.page_input.text().split(',')]
            self.announcer.select_by_pages(pages)
            self.update_preview()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid page numbers separated by commas.")

    def select_by_item_numbers(self):
        try:
            self.announcer.select_by_item_numbers(self.start_item.value(), self.end_item.value())
            self.update_preview()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Range", str(e))

    def select_random(self):
        try:
            self.announcer.select_random(self.random_count.value())
            self.update_preview()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Count", str(e))

    def update_preview(self):
        if not self.announcer.selected_items:
            self.preview_text.setText("No items selected")
            return

        preview_text = "Selected Items:\n\n"
        for i, (item, page, num) in enumerate(self.announcer.selected_items[:MAX_PREVIEW_ITEMS], 1):
            preview_text += f"{i}. (Page {page}, #{num}) {item[:MAX_ITEM_PREVIEW_LENGTH]}...\n"
        if len(self.announcer.selected_items) > MAX_PREVIEW_ITEMS:
            preview_text += f"\n... and {len(self.announcer.selected_items) - MAX_PREVIEW_ITEMS} more items"
        
        self.preview_text.setText(preview_text)

    def start_announcements(self):
        if not self.announcer.selected_items:
            QMessageBox.warning(self, "No Selection", "Please select items first!")
            return

        schedule.every(ANNOUNCEMENT_INTERVAL_HOURS).hours.do(self.announce_now)
        self.schedule_timer.start(60000)  # Check every minute
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.update_next_announcement()
        self.announce_now()

    def stop_announcements(self):
        schedule.clear()
        self.schedule_timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.next_announcement_label.setText("Next announcement: Not scheduled")

    def announce_now(self):
        if not self.announcer.selected_items:
            QMessageBox.warning(self, "No Selection", "Please select items first!")
            return

        if self.announcer.current_index >= len(self.announcer.selected_items):
            self.announcer.current_index = 0

        item, page, num = self.announcer.selected_items[self.announcer.current_index]
        announcement = f"Time to work on item number {num} from page {page}: {item}"
        
        try:
            subprocess.run([
                'say',
                '-v', self.voice_combo.currentText(),
                '-r', str(self.rate_spin.value()),
                announcement
            ])
            
            # Record announcement in history
            self.announcer.announcement_history.append({
                'timestamp': datetime.now().isoformat(),
                'item': item,
                'page': page,
                'number': num
            })
            self.announcer._save_history()
            
            self.announcer.current_index += 1
            self.update_history_display()
            self.update_next_announcement()
            
        except Exception as e:
            QMessageBox.warning(self, "Announcement Error", f"Error making announcement: {e}")

    def update_next_announcement(self):
        if schedule.get_jobs():
            next_job = schedule.next_run()
            if next_job:
                self.next_announcement_label.setText(
                    f"Next announcement: {next_job.strftime('%Y-%m-%d %H:%M:%S')}"
                )

    def update_history_display(self):
        if not self.announcer.announcement_history:
            self.history_text.setText("No announcement history available.")
            return

        history_text = "Announcement History:\n\n"
        for entry in self.announcer.announcement_history[-10:]:
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            history_text += f"{timestamp} - Page {entry['page']}, #{entry['number']}: {entry['item'][:100]}...\n"
        
        self.history_text.setText(history_text)

    def check_schedule(self):
        schedule.run_pending()

    def closeEvent(self, event):
        self.stop_announcements()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = ScavAnnouncerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 