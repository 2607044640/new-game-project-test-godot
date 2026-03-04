# Real-time Screenshot Monitoring - Quick Start Guide

## What This Does

Allows Claude to see your Godot game in real-time by continuously capturing screenshots and game state data.

## Quick Start (3 Steps)

### 1. Start Your Game
Press `F5` in Godot to run the game with MCP server active.

### 2. Start the Monitor
Open a terminal and run:
```cmd
cd C:\Godot\new-game-project-test-godot\.kiro\scripts
python realtime_screenshot_monitor.py
```

You'll see output like:
```
============================================================
Real-time Screenshot Monitor
============================================================
MCP Server: 127.0.0.1:8765
Capture Interval: 3 seconds
Screenshot Directory: C:\Godot\new-game-project-test-godot\.kiro\screenshots
Current Screenshot: C:\Godot\new-game-project-test-godot\current_screenshot.png
============================================================

Press Ctrl+C to stop monitoring

[14:30:22] Capturing game state...
  ✅ Updated: current_screenshot.png
  ✅ Saved: screenshot_20250104_143022.png
  ✅ Updated: screenshot_data.json
  📊 Total captures: 1 | Errors: 0
```

### 3. Ask Claude to Analyze
In your Kiro chat, simply say:
- "What do you see in the game right now?"
- "Analyze the current screenshot"
- "How many icons are on the screen?"

Claude will automatically read the latest screenshot and game state data.

## What Gets Captured

Every 3 seconds, the monitor captures:

1. **Screenshot** (`current_screenshot.png`)
   - Visual representation of the game
   - Always overwritten with latest capture
   - PNG format, ~25-50 KB

2. **Game State JSON** (`screenshot_data.json`)
   - Structured data about the game
   - Icon positions, types, and counts
   - Game statistics (score, moves, matches)
   - Grid dimensions

3. **Timestamped History** (`.kiro/screenshots/`)
   - `screenshot_YYYYMMDD_HHMMSS.png`
   - `gamestate_YYYYMMDD_HHMMSS.json`
   - Keeps a record of all captures

## Example Analysis Session

```
You: Start the monitor
[Terminal shows captures happening every 3 seconds]

You: What's on the screen right now?

Claude: Looking at the current game state, I can see:
        - Grid: 6x6
        - Total Icons: 6
        - Icon Types:
          * Icon: 1
          * Icon2: 1
          * Icon3: 1
          * Icon7: 1
          * Icon8: 1
          * Icon9: 1
        - Score: 0
        - Moves: 0

You: Click on Icon3

Claude: [Uses simulate_click with coordinates from game state]
        Done! Clicked at position (x, y)

You: What changed?

Claude: [Reads updated screenshot]
        The Icon3 has moved to a new position...
```

## Optional: Watch for New Screenshots

In a second terminal, run:
```cmd
cd C:\Godot\new-game-project-test-godot\.kiro\scripts
python watch_screenshot_folder.py
```

This will notify you whenever a new screenshot is saved:
```
============================================================
🖼️  NEW SCREENSHOT DETECTED
============================================================
Time: 14:30:25
File: screenshot_20250104_143025.png
Size: 26.3 KB
Total screenshots: 2
============================================================
```

**Note:** Requires `pip install watchdog`

## Stopping the Monitor

Press `Ctrl+C` in the terminal running the monitor:
```
============================================================
Monitoring stopped
Total captures: 42
Total errors: 0
============================================================
```

## Troubleshooting

### "Error communicating with MCP server"
**Solution:** Make sure the game is running (F5 in Godot)

### "No screenshot found"
**Solution:** Wait 3 seconds for the first capture, or run the monitor script

### Monitor not capturing
**Solution:** 
1. Check game is running
2. Check MCP server is on port 8765
3. Try restarting the game

## Files Created

```
new-game-project-test-godot/
├── current_screenshot.png          ← Latest screenshot (always updated)
├── screenshot_data.json            ← Latest game state (always updated)
└── .kiro/
    ├── screenshots/                ← History folder
    │   ├── screenshot_20250104_143022.png
    │   ├── gamestate_20250104_143022.json
    │   ├── screenshot_20250104_143025.png
    │   └── gamestate_20250104_143025.json
    └── scripts/
        ├── realtime_screenshot_monitor.py      ← Main tool
        ├── watch_screenshot_folder.py          ← Optional watcher
        └── analyze_current_screenshot.py       ← Analysis helper
```

## Advanced Usage

### Change Capture Speed

Edit `realtime_screenshot_monitor.py`, line 13:
```python
CAPTURE_INTERVAL = 3  # Change to 1 for faster, 5 for slower
```

### Manual Analysis

Run the analysis helper anytime:
```cmd
python analyze_current_screenshot.py
```

This shows a summary of the current game state without Claude.

## Why This Works Better Than Pure Vision

Traditional approach (unreliable):
- AI looks at screenshot
- Tries to count icons visually
- Gets wrong answers (5, 2, 15 instead of 6)
- Vision models struggle with repetitive objects

Our approach (reliable):
- Screenshot provides visual context
- JSON provides exact data (positions, types, counts)
- Claude reads both sources
- 100% accurate counting and analysis

## Next Steps

Once monitoring is working, you can:
1. Ask Claude to analyze game states
2. Request specific actions (clicks, moves)
3. Compare before/after screenshots
4. Track game progression over time
5. Debug visual issues

For more details, see: `.kiro/docs/RealtimeScreenshotMonitoring.md`
