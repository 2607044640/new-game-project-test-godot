# Real-time Screenshot Monitoring System

## Overview

This system allows Claude to view and analyze screenshots from your running Godot game in real-time. It consists of three Python scripts that work together to capture, monitor, and present game screenshots.

## Components

### 1. `realtime_screenshot_monitor.py` - Main Capture Tool

Continuously captures screenshots from the running game via MCP server.

**Features:**
- Captures every 3 seconds (configurable)
- Updates `current_screenshot.png` (always latest)
- Saves timestamped copies to `.kiro/screenshots/`
- Saves game state JSON with each capture
- Shows capture statistics

**Usage:**
```cmd
cd new-game-project-test-godot\.kiro\scripts
python realtime_screenshot_monitor.py
```

**Requirements:**
- Game must be running with MCP server active (port 8765)
- Press Ctrl+C to stop

### 2. `watch_screenshot_folder.py` - Folder Monitor

Watches the screenshots folder and notifies when new files appear.

**Features:**
- Real-time file system monitoring
- Displays file size and timestamp
- Tracks total screenshot count

**Usage:**
```cmd
cd new-game-project-test-godot\.kiro\scripts
python watch_screenshot_folder.py
```

**Requirements:**
- Install watchdog: `pip install watchdog`
- Press Ctrl+C to stop

### 3. `analyze_current_screenshot.py` - Analysis Helper

Displays the current screenshot and game state data for Claude to analyze.

**Features:**
- Shows screenshot file info
- Displays game state summary
- Lists icon types and counts
- Shows full JSON data

**Usage:**
```cmd
cd new-game-project-test-godot\.kiro\scripts
python analyze_current_screenshot.py
```

## Workflow for Real-time Analysis

### Setup (One-time)

1. Install required library:
```cmd
pip install watchdog
```

2. Start your Godot game (F5)

### During Development

1. **Start the monitor** (in one terminal):
```cmd
cd new-game-project-test-godot\.kiro\scripts
python realtime_screenshot_monitor.py
```

2. **Optional: Start the watcher** (in another terminal):
```cmd
cd new-game-project-test-godot\.kiro\scripts
python watch_screenshot_folder.py
```

3. **Ask Claude to analyze**:
   - "Analyze the current screenshot"
   - "What do you see in the game right now?"
   - "Count the icons in the current state"

4. **Claude will**:
   - Read `current_screenshot.png` using `mcp_filesystem_read_media_file`
   - Read `screenshot_data.json` for structured data
   - Provide analysis based on both visual and structured data

## File Locations

```
new-game-project-test-godot/
├── current_screenshot.png          # Always the latest screenshot
├── screenshot_data.json            # Latest game state data
└── .kiro/
    └── screenshots/                # Timestamped history
        ├── screenshot_20250104_143022.png
        ├── gamestate_20250104_143022.json
        ├── screenshot_20250104_143025.png
        └── gamestate_20250104_143025.json
```

## How Claude Analyzes Screenshots

When you ask Claude to analyze, it will:

1. **Read the image file**:
```python
# Claude uses this internally
mcp_filesystem_read_media_file(path="new-game-project-test-godot/current_screenshot.png")
```

2. **Read the game state**:
```python
# Claude reads the JSON
with open("screenshot_data.json") as f:
    game_state = json.load(f)
```

3. **Combine both sources**:
   - Visual context from the screenshot
   - Accurate data from the JSON (icon positions, types, counts)
   - No reliance on vision model counting (which is unreliable)

## Configuration

### Change Capture Interval

Edit `realtime_screenshot_monitor.py`:
```python
CAPTURE_INTERVAL = 3  # Change to desired seconds
```

### Change Screenshot Directory

Edit `realtime_screenshot_monitor.py`:
```python
SCREENSHOT_DIR = Path(__file__).parent.parent / "screenshots"  # Change path
```

## Troubleshooting

### "Error communicating with MCP server"
- Make sure the game is running (F5)
- Check that MCP server is active on port 8765
- Verify no firewall blocking localhost:8765

### "No screenshot found"
- Run `realtime_screenshot_monitor.py` first
- Wait for at least one capture cycle (3 seconds)
- Check that `current_screenshot.png` exists in project root

### "watchdog library not installed"
- Install it: `pip install watchdog`

## Example Session

```
User: Start monitoring the game
[Runs realtime_screenshot_monitor.py]

User: What do you see in the game right now?
Claude: [Reads current_screenshot.png and screenshot_data.json]
        I can see a 6x6 grid with 6 icons:
        - Icon: 1
        - Icon2: 1
        - Icon3: 1
        - Icon7: 1
        - Icon8: 1
        - Icon9: 1
        
        The icons are positioned at...
        [Provides detailed analysis]

User: Click on the Icon3
Claude: [Uses simulate_click with coordinates from game state]
        Clicked at position (x, y)

User: What changed?
Claude: [Reads updated screenshot]
        The Icon3 has moved to...
        [Analyzes the change]
```

## Benefits

1. **No Vision Model Limitations**: Uses structured data for accurate counting
2. **Real-time Feedback**: See game state as it changes
3. **Historical Record**: All screenshots saved with timestamps
4. **Dual Analysis**: Visual + structured data for complete understanding
5. **Automated**: No manual screenshot taking needed

## Next Steps

- Integrate with game events (capture on specific actions)
- Add automatic analysis triggers
- Create comparison tools (before/after screenshots)
- Add annotation capabilities
