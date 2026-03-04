"""
Real-time Screenshot Monitor for Godot Game
Continuously captures screenshots and game state from the running game.
"""

import socket
import json
import base64
import time
import os
from datetime import datetime
from pathlib import Path

# Configuration
MCP_HOST = "127.0.0.1"
MCP_PORT = 8765
CAPTURE_INTERVAL = 3  # seconds between captures
SCREENSHOT_DIR = Path(__file__).parent.parent / "screenshots"
PROJECT_ROOT = Path(__file__).parent.parent.parent

def send_mcp_request(tool_name, arguments=None):
    """Send a request to the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((MCP_HOST, MCP_PORT))
            
            request_json = json.dumps(request) + "\n"
            sock.sendall(request_json.encode('utf-8'))
            
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b"\n" in response_data:
                    break
            
            response = json.loads(response_data.decode('utf-8'))
            return response
    except Exception as e:
        print(f"Error communicating with MCP server: {e}")
        return None

def save_screenshot(base64_data, filename):
    """Save base64 screenshot data to file."""
    try:
        image_data = base64.b64decode(base64_data)
        with open(filename, 'wb') as f:
            f.write(image_data)
        return True
    except Exception as e:
        print(f"Error saving screenshot: {e}")
        return False

def capture_and_save():
    """Capture game state and save screenshot."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Capturing game state...")
    
    response = send_mcp_request("get_game_state")
    
    if not response or "error" in response:
        print(f"  ❌ Failed to capture: {response.get('error', 'Unknown error') if response else 'No response'}")
        return False
    
    result = response.get("result", {})
    content = result.get("content", [])
    
    # Extract screenshot and game state
    screenshot_base64 = None
    game_state_text = None
    
    for item in content:
        if item.get("type") == "image":
            screenshot_base64 = item.get("data")
        elif item.get("type") == "text":
            game_state_text = item.get("text")
    
    if not screenshot_base64:
        print("  ❌ No screenshot in response")
        return False
    
    # Save current screenshot (overwrite)
    current_screenshot = PROJECT_ROOT / "current_screenshot.png"
    if save_screenshot(screenshot_base64, current_screenshot):
        print(f"  ✅ Updated: current_screenshot.png")
    
    # Save timestamped copy
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_screenshot = SCREENSHOT_DIR / f"screenshot_{timestamp}.png"
    if save_screenshot(screenshot_base64, timestamped_screenshot):
        print(f"  ✅ Saved: {timestamped_screenshot.name}")
    
    # Save game state JSON
    if game_state_text:
        json_file = PROJECT_ROOT / "screenshot_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(game_state_text)
        print(f"  ✅ Updated: screenshot_data.json")
        
        # Also save timestamped JSON
        timestamped_json = SCREENSHOT_DIR / f"gamestate_{timestamp}.json"
        with open(timestamped_json, 'w', encoding='utf-8') as f:
            f.write(game_state_text)
    
    return True

def main():
    """Main monitoring loop."""
    print("=" * 60)
    print("Real-time Screenshot Monitor")
    print("=" * 60)
    print(f"MCP Server: {MCP_HOST}:{MCP_PORT}")
    print(f"Capture Interval: {CAPTURE_INTERVAL} seconds")
    print(f"Screenshot Directory: {SCREENSHOT_DIR}")
    print(f"Current Screenshot: {PROJECT_ROOT / 'current_screenshot.png'}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop monitoring\n")
    
    # Create screenshot directory if it doesn't exist
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    
    capture_count = 0
    error_count = 0
    
    try:
        while True:
            if capture_and_save():
                capture_count += 1
                print(f"  📊 Total captures: {capture_count} | Errors: {error_count}\n")
            else:
                error_count += 1
                print(f"  📊 Total captures: {capture_count} | Errors: {error_count}\n")
            
            time.sleep(CAPTURE_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Monitoring stopped")
        print(f"Total captures: {capture_count}")
        print(f"Total errors: {error_count}")
        print("=" * 60)

if __name__ == "__main__":
    main()
