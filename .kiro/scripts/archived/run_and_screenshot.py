#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import json
import base64

# Start Godot
print("Starting Godot...")
godot_path = r"C:\Godot\Godot_v4.6.1-stable_mono_win64\Godot_v4.6.1-stable_mono_win64.exe"
project_path = r"C:\Godot\new-game-project-test-godot"

process = subprocess.Popen(
    [godot_path, "--path", project_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print(f"Godot started (PID: {process.pid})")
print("Waiting 8 seconds for MCP server to initialize...")
time.sleep(8)

# Take screenshot
print("\nCalling get_screenshot...")
try:
    data = json.dumps({"tool": "get_screenshot", "arguments": {}}).encode('utf-8')
    req = urllib.request.Request("http://localhost:8765/", data=data, 
                                headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))
    
    print("Response received!")
    
    if result.get("content"):
        for item in result["content"]:
            if item.get("type") == "image":
                print(f"\n✓ Screenshot captured!")
                print(f"  MIME: {item['mimeType']}")
                print(f"  Data size: {len(item['data'])} chars")
                
                # Save to file
                img_data = base64.b64decode(item['data'])
                with open("current_screenshot.png", "wb") as f:
                    f.write(img_data)
                print(f"  Saved to: current_screenshot.png ({len(img_data)} bytes)")
            elif item.get("type") == "text":
                print(f"\nText response: {item.get('text')}")
    else:
        print(f"\nUnexpected response: {json.dumps(result, indent=2)}")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone! Check current_screenshot.png")
