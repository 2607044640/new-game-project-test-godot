#!/usr/bin/env python3
"""Start game and take screenshot"""
import subprocess
import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

def call_mcp_tool(tool_name, arguments=None):
    """Call MCP tool via stdin/stdout"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    bridge_path = PROJECT_ROOT / ".kiro" / "scripts" / "godot_mcp_bridge.py"
    
    proc = subprocess.Popen(
        ["python", str(bridge_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = proc.communicate(json.dumps(request) + "\n")
    
    try:
        return json.loads(stdout)
    except:
        return {"error": f"Failed to parse: {stdout}\nStderr: {stderr}"}

# Start game
print("Starting Godot game...")
result = call_mcp_tool("start_game")
print(f"Start result: {result}")

print("\nWaiting 5 seconds for MCP Server to initialize...")
time.sleep(5)

# Take screenshot
print("\nTaking screenshot...")
result = call_mcp_tool("get_screenshot")

if "content" in result:
    print("✓ Screenshot captured successfully!")
    print(f"Response type: {result['content'][0].get('type')}")
    if result['content'][0].get('type') == 'image':
        data_len = len(result['content'][0].get('data', ''))
        print(f"Image data length: {data_len} characters")
else:
    print(f"Error: {result}")
