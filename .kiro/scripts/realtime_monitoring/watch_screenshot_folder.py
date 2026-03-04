"""
Screenshot Folder Watcher
Monitors the screenshots folder for new files and notifies when they appear.
Requires: pip install watchdog
"""

import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog library not installed")
    print("Install it with: pip install watchdog")
    sys.exit(1)

SCREENSHOT_DIR = Path(__file__).parent.parent / "screenshots"

class ScreenshotHandler(FileSystemEventHandler):
    """Handles file system events for screenshots."""
    
    def __init__(self):
        self.screenshot_count = 0
    
    def on_created(self, event):
        """Called when a file is created."""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        # Only process PNG files
        if filepath.suffix.lower() == '.png':
            self.screenshot_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            print(f"\n{'='*60}")
            print(f"🖼️  NEW SCREENSHOT DETECTED")
            print(f"{'='*60}")
            print(f"Time: {timestamp}")
            print(f"File: {filepath.name}")
            print(f"Size: {filepath.stat().st_size / 1024:.1f} KB")
            print(f"Total screenshots: {self.screenshot_count}")
            print(f"{'='*60}\n")
    
    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        # Notify about JSON updates
        if filepath.suffix.lower() == '.json':
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] 📝 Game state updated: {filepath.name}")

def main():
    """Main watcher loop."""
    print("=" * 60)
    print("Screenshot Folder Watcher")
    print("=" * 60)
    print(f"Monitoring: {SCREENSHOT_DIR}")
    print("=" * 60)
    print("\nWaiting for new screenshots...")
    print("Press Ctrl+C to stop\n")
    
    # Create directory if it doesn't exist
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Set up the observer
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SCREENSHOT_DIR), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n" + "=" * 60)
        print("Watcher stopped")
        print(f"Total screenshots detected: {event_handler.screenshot_count}")
        print("=" * 60)
    
    observer.join()

if __name__ == "__main__":
    main()
