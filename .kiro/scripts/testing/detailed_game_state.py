#!/usr/bin/env python3
"""
Show detailed game state with all icon information.
"""

import socket
import json
import base64
import sys
from pathlib import Path

def send_mcp_request(tool, arguments=None):
    if arguments is None:
        arguments = {}
    
    request = {"tool": tool, "arguments": arguments}
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
    print("=" * 70)
    print("🎮 DETAILED GAME STATE ANALYSIS")
    print("=" * 70)
    print()
    
    try:
        response = send_mcp_request("get_game_state")
        
        if response.get("isError"):
            print("❌ Error:", response["content"][0]["text"])
            return False
        
        content = response.get("content", [])
        game_state_json = None
        screenshot_data = None
        
        for item in content:
            if item["type"] == "text":
                game_state_json = item["text"]
            elif item["type"] == "image":
                screenshot_data = item["data"]
        
        if not game_state_json:
            print("❌ No game state data")
            return False
        
        game_state = json.loads(game_state_json)
        
        print("📊 GRID INFORMATION:")
        print(f"   Rows: {game_state['game_state']['rows']}")
        print(f"   Columns: {game_state['game_state']['columns']}")
        print(f"   Total cells detected: {len(game_state['game_state']['cells'])}")
        print()
        
        print("🎯 DETAILED CELL INFORMATION:")
        print("-" * 70)
        for i, cell in enumerate(game_state['game_state']['cells'], 1):
            print(f"Cell #{i}:")
            print(f"  Position: Row {cell['row']}, Column {cell['column']}")
            print(f"  Icon Type: {cell['iconType']}")
            print(f"  Screen Position: ({cell['screenPosition']['x']:.1f}, {cell['screenPosition']['y']:.1f})")
            print()
        
        print("=" * 70)
        print("📈 ICON COUNT SUMMARY:")
        icon_counts = {}
        for cell in game_state['game_state']['cells']:
            icon_type = cell['iconType']
            icon_counts[icon_type] = icon_counts.get(icon_type, 0) + 1
        
        for icon_type, count in sorted(icon_counts.items()):
            print(f"   {icon_type}: {count}")
        print("=" * 70)
        
        if screenshot_data:
            output_path = Path(__file__).parent.parent.parent / "current_screenshot.png"
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(screenshot_data))
            print(f"\n📸 Screenshot saved: {output_path}")
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Game not running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
