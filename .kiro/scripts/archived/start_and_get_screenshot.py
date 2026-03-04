#!/usr/bin/env python3
"""Start Godot game and capture screenshot"""
import sys
import json
import time

# Import the MCP bridge tools
sys.path.insert(0, r'C:\Godot\new-game-project-test-godot\.kiro\scripts')
from godot_mcp_bridge import start_game, call_godot_mcp

def main():
    print("Starting Godot game...")
    result = start_game()
    print(f"Start game result: {result}")
    
    # Wait for game to initialize MCP server
    print("Waiting 5 seconds for MCP server to start...")
    time.sleep(5)
    
    print("Capturing screenshot...")
    screenshot_result = call_godot_mcp("get_screenshot")
    
    # Output the result as JSON for Kiro to parse
    print("\n=== SCREENSHOT RESULT ===")
    print(json.dumps(screenshot_result, indent=2))
    
    return screenshot_result

if __name__ == "__main__":
    main()
