#!/usr/bin/env python3
"""
Test script for the get_game_state MCP tool.
Tests the new game state capture system with screenshot and structured data.
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

def test_get_game_state():
    """Test the get_game_state tool."""
    print("=" * 60)
    print("Testing get_game_state tool")
    print("=" * 60)
    
    try:
        response = send_mcp_request("get_game_state")
        
        if response.get("isError"):
            print("❌ Error:", response["content"][0]["text"])
            return False
        
        print("✅ get_game_state succeeded!")
        print()
        
        # Parse the response
        content = response.get("content", [])
        
        # Find text content (game state JSON)
        game_state_json = None
        screenshot_data = None
        
        for item in content:
            if item["type"] == "text":
                game_state_json = item["text"]
            elif item["type"] == "image":
                screenshot_data = item["data"]
        
        if game_state_json:
            game_state = json.loads(game_state_json)
            print("📊 Game State Data:")
            print(f"  Grid: {game_state['game_state']['rows']}x{game_state['game_state']['columns']}")
            print(f"  Cells: {len(game_state['game_state']['cells'])}")
            print(f"  Score: {game_state['game_state']['statistics']['score']}")
            print(f"  Phase: {game_state['game_state']['statistics']['gamePhase']}")
            print()
            
            # Show cell details
            print("🎮 Cells:")
            for cell in game_state['game_state']['cells'][:10]:  # Show first 10
                print(f"  [{cell['row']},{cell['column']}] {cell['iconType']} at ({cell['screenPosition']['x']:.1f}, {cell['screenPosition']['y']:.1f})")
            if len(game_state['game_state']['cells']) > 10:
                print(f"  ... and {len(game_state['game_state']['cells']) - 10} more cells")
            print()
        
        if screenshot_data:
            screenshot_size = len(screenshot_data)
            print(f"📸 Screenshot: {screenshot_size} bytes (base64)")
            
            # Save screenshot to file
            output_path = Path(__file__).parent / "test_game_state_screenshot.png"
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(screenshot_data))
            print(f"   Saved to: {output_path}")
            print()
        
        # Count icons by type
        if game_state_json:
            icon_counts = {}
            for cell in game_state['game_state']['cells']:
                icon_type = cell['iconType']
                icon_counts[icon_type] = icon_counts.get(icon_type, 0) + 1
            
            print("📈 Icon Counts (THE KEY TEST - no vision model needed!):")
            for icon_type, count in sorted(icon_counts.items()):
                print(f"  {icon_type}: {count}")
            print()
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Connection refused. Is the game running with MCP Server?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print()
    print("🎮 Godot MCP Game State Test")
    print()
    print("Make sure the game is running before running this test!")
    print()
    
    success = test_get_game_state()
    
    print()
    print("=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Tests failed")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
