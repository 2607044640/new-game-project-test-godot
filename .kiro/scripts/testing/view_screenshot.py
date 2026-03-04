#!/usr/bin/env python3
"""
Fetch and display screenshot with base64 output for Kiro to view.
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
    
    json_body = json.dumps(request)
    http_request = (
        f"POST / HTTP/1.1\r\n"
        f"Host: localhost:8765\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(json_body)}\r\n"
        f"\r\n"
        f"{json_body}"
    )
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    try:
        sock.connect(("localhost", 8765))
        sock.sendall(http_request.encode())
        
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            
            if b"\r\n\r\n" in response:
                headers_end = response.find(b"\r\n\r\n")
                headers = response[:headers_end].decode()
                body_start = headers_end + 4
                
                for line in headers.split("\r\n"):
                    if line.startswith("Content-Length:"):
                        content_length = int(line.split(":")[1].strip())
                        if len(response) >= body_start + content_length:
                            break
        
        headers_end = response.find(b"\r\n\r\n")
        body = response[headers_end + 4:].decode()
        
        return json.loads(body)
        
    finally:
        sock.close()

def main():
    print("📸 Fetching screenshot from Godot game...")
    print()
    
    try:
        response = send_mcp_request("get_game_state")
        
        if response.get("isError"):
            print("❌ Error:", response["content"][0]["text"])
            return False
        
        content = response.get("content", [])
        
        screenshot_data = None
        game_state_json = None
        
        for item in content:
            if item["type"] == "image":
                screenshot_data = item["data"]
            elif item["type"] == "text":
                game_state_json = item["text"]
        
        if not screenshot_data:
            print("❌ No screenshot found")
            return False
        
        # Save to file
        output_path = Path(__file__).parent.parent.parent / "current_screenshot.png"
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(screenshot_data))
        
        print(f"✅ Screenshot saved: {output_path}")
        print()
        
        # Show game state
        if game_state_json:
            game_state = json.loads(game_state_json)
            print("📊 Game State:")
            print(f"  Grid: {game_state['game_state']['rows']}x{game_state['game_state']['columns']}")
            print(f"  Total cells: {len(game_state['game_state']['cells'])}")
            print()
            
            icon_counts = {}
            for cell in game_state['game_state']['cells']:
                icon_type = cell['iconType']
                icon_counts[icon_type] = icon_counts.get(icon_type, 0) + 1
            
            print("🎮 Icons detected:")
            for icon_type, count in sorted(icon_counts.items()):
                print(f"  • {icon_type}: {count}")
            print()
        
        # Output base64 for Kiro (first 100 chars as preview)
        print("=" * 70)
        print("📷 Screenshot captured successfully!")
        print(f"   Size: {len(screenshot_data)} bytes (base64)")
        print(f"   Preview: {screenshot_data[:100]}...")
        print("=" * 70)
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Game not running on port 8765")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
