#!/usr/bin/env python3
"""
Display screenshot from game state in Kiro conversation.
This script fetches the screenshot and displays it directly.
"""

import socket
import json
import base64
import sys
from pathlib import Path

def send_mcp_request(tool, arguments=None):
    """Send an MCP request to the Godot server."""
    if arguments is None:
        arguments = {}
    
    request = {
        "tool": tool,
        "arguments": arguments
    }
    
    # Create HTTP POST request
    json_body = json.dumps(request)
    http_request = (
        f"POST / HTTP/1.1\r\n"
        f"Host: localhost:8765\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(json_body)}\r\n"
        f"\r\n"
        f"{json_body}"
    )
    
    # Connect and send
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    try:
        sock.connect(("localhost", 8765))
        sock.sendall(http_request.encode())
        
        # Receive response
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            
            # Check if we have the complete response
            if b"\r\n\r\n" in response:
                # Parse headers to get content length
                headers_end = response.find(b"\r\n\r\n")
                headers = response[:headers_end].decode()
                body_start = headers_end + 4
                
                # Find Content-Length
                for line in headers.split("\r\n"):
                    if line.startswith("Content-Length:"):
                        content_length = int(line.split(":")[1].strip())
                        # Check if we have the full body
                        if len(response) >= body_start + content_length:
                            break
        
        # Parse response
        headers_end = response.find(b"\r\n\r\n")
        body = response[headers_end + 4:].decode()
        
        return json.loads(body)
        
    finally:
        sock.close()

def get_screenshot():
    """Get screenshot from game and display it."""
    print("📸 Fetching screenshot from game...")
    print()
    
    try:
        response = send_mcp_request("get_game_state")
        
        if response.get("isError"):
            print("❌ Error:", response["content"][0]["text"])
            return False
        
        # Parse the response
        content = response.get("content", [])
        
        # Find screenshot data
        screenshot_data = None
        game_state_json = None
        
        for item in content:
            if item["type"] == "image":
                screenshot_data = item["data"]
            elif item["type"] == "text":
                game_state_json = item["text"]
        
        if not screenshot_data:
            print("❌ No screenshot data found")
            return False
        
        # Save screenshot to file
        output_path = Path(__file__).parent / "current_screenshot.png"
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(screenshot_data))
        
        print(f"✅ Screenshot saved to: {output_path}")
        print()
        
        # Parse game state for context
        if game_state_json:
            game_state = json.loads(game_state_json)
            print("📊 Game State:")
            print(f"  Grid: {game_state['game_state']['rows']}x{game_state['game_state']['columns']}")
            print(f"  Cells: {len(game_state['game_state']['cells'])}")
            print()
            
            # Count icons
            icon_counts = {}
            for cell in game_state['game_state']['cells']:
                icon_type = cell['iconType']
                icon_counts[icon_type] = icon_counts.get(icon_type, 0) + 1
            
            print("🎮 Icon Counts:")
            for icon_type, count in sorted(icon_counts.items()):
                print(f"  {icon_type}: {count}")
            print()
        
        # Output the image path for Kiro to display
        print("=" * 60)
        print("SCREENSHOT PATH FOR KIRO:")
        print(str(output_path.absolute()))
        print("=" * 60)
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Connection refused. Is the game running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = get_screenshot()
    sys.exit(0 if success else 1)
