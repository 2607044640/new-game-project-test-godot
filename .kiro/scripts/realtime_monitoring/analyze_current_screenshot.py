"""
Analyze Current Screenshot
Helper script to display the current screenshot and game state for Claude analysis.
"""

import json
import base64
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SCREENSHOT_FILE = PROJECT_ROOT / "current_screenshot.png"
GAMESTATE_FILE = PROJECT_ROOT / "screenshot_data.json"

def main():
    """Display current screenshot and game state."""
    print("=" * 60)
    print("Current Game State Analysis")
    print("=" * 60)
    
    # Check if files exist
    if not SCREENSHOT_FILE.exists():
        print("\n❌ No screenshot found at:", SCREENSHOT_FILE)
        print("Run realtime_screenshot_monitor.py first to capture screenshots.")
        return
    
    # Read and display screenshot info
    screenshot_size = SCREENSHOT_FILE.stat().st_size
    print(f"\n📸 Screenshot: {SCREENSHOT_FILE.name}")
    print(f"   Size: {screenshot_size / 1024:.1f} KB")
    
    # Read screenshot as base64
    with open(SCREENSHOT_FILE, 'rb') as f:
        screenshot_data = base64.b64encode(f.read()).decode('utf-8')
    
    print(f"   Base64 length: {len(screenshot_data)} characters")
    
    # Read and display game state
    if GAMESTATE_FILE.exists():
        print(f"\n📊 Game State: {GAMESTATE_FILE.name}")
        
        with open(GAMESTATE_FILE, 'r', encoding='utf-8') as f:
            game_state = json.load(f)
        
        # Display summary
        grid_state = game_state.get('gridState', {})
        icons = grid_state.get('icons', [])
        stats = game_state.get('statistics', {})
        
        print(f"\n   Grid Size: {grid_state.get('width', 0)} x {grid_state.get('height', 0)}")
        print(f"   Total Icons: {len(icons)}")
        
        # Count icon types
        icon_types = {}
        for icon in icons:
            icon_type = icon.get('iconType', 'Unknown')
            icon_types[icon_type] = icon_types.get(icon_type, 0) + 1
        
        print(f"\n   Icon Types:")
        for icon_type, count in sorted(icon_types.items()):
            print(f"     - {icon_type}: {count}")
        
        print(f"\n   Statistics:")
        print(f"     - Score: {stats.get('score', 0)}")
        print(f"     - Moves: {stats.get('moves', 0)}")
        print(f"     - Matches: {stats.get('matches', 0)}")
        
        # Display full JSON
        print(f"\n   Full Game State JSON:")
        print("   " + "-" * 56)
        print(json.dumps(game_state, indent=2))
    else:
        print(f"\n⚠️  No game state file found at: {GAMESTATE_FILE}")
    
    print("\n" + "=" * 60)
    print("✅ Analysis data ready")
    print("=" * 60)
    
    # Output for Claude to read
    print("\n📋 For Claude Analysis:")
    print(f"   Use: mcp_filesystem_read_media_file with path='new-game-project-test-godot/current_screenshot.png'")
    print(f"   Or read: {GAMESTATE_FILE}")

if __name__ == "__main__":
    main()
