#!/usr/bin/env python3
"""Complete screenshot capture and save workflow"""
import subprocess
import json
import time
import base64
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

print("=" * 60)
print("COMPLETE SCREENSHOT TEST")
print("=" * 60)

# Step 1: Start game
print("\n[1/3] Starting Godot game...")
result = call_mcp_tool("start_game")
if "error" in result or result.get("isError"):
    print(f"ERROR: {result}")
    exit(1)

print("✓ Game started successfully")
print("Waiting 5 seconds for initialization...")
time.sleep(5)

# Step 2: Get screenshot
print("\n[2/3] Capturing screenshot...")
result = call_mcp_tool("get_screenshot")

if "error" in result or result.get("isError"):
    print(f"ERROR: {result}")
    exit(1)

# Step 3: Extract and save Base64 data
print("\n[3/3] Processing screenshot data...")
try:
    text_content = result["content"][0]["text"]
    data = json.loads(text_content)
    
    if not data.get("success"):
        print(f"ERROR: {data}")
        exit(1)
    
    base64_data = data["data"]
    
    # Decode and save
    image_bytes = base64.b64decode(base64_data)
    output_path = PROJECT_ROOT / "current_screenshot.png"
    
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    
    print(f"✓ Screenshot saved: {output_path}")
    print(f"  File size: {len(image_bytes):,} bytes")
    print(f"  Base64 length: {len(base64_data):,} characters")
    
    print("\n" + "=" * 60)
    print("SUCCESS! Screenshot captured and saved.")
    print("=" * 60)
    
except Exception as e:
    print(f"ERROR processing data: {e}")
    print(f"Raw response: {result}")
    exit(1)
