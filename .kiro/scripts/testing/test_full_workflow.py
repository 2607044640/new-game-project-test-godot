import socket
import json
import base64
import time

def send_mcp_request(tool_name, arguments=None):
    """Send MCP request to godot_mcp_bridge.py"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 3000))
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    message = json.dumps(request) + "\n"
    sock.sendall(message.encode('utf-8'))
    
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
        if b'\n' in response:
            break
    
    sock.close()
    return json.loads(response.decode('utf-8'))

# Step 1: Start game
print("Starting game...")
result = send_mcp_request("start_game")
print(f"Start game result: {result}")
time.sleep(3)  # Wait for game to initialize

# Step 2: Get screenshot
print("\nGetting screenshot...")
result = send_mcp_request("get_screenshot")
if result.get("result"):
    base64_data = result["result"]["content"][0]["text"]
    
    # Save to file
    image_data = base64.b64decode(base64_data)
    with open("current_screenshot.png", "wb") as f:
        f.write(image_data)
    print(f"Screenshot saved! Size: {len(image_data)} bytes")
else:
    print(f"Error: {result}")
