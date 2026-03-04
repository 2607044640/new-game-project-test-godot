#!/usr/bin/env python3
import urllib.request
import json

try:
    data = json.dumps({"tool": "get_screenshot", "arguments": {}}).encode('utf-8')
    req = urllib.request.Request("http://localhost:8765/", data=data, 
                                headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))
    
    if result.get("content"):
        # MCP Image format
        for item in result["content"]:
            if item.get("type") == "image":
                print(f"Screenshot captured! Size: {len(item['data'])} bytes")
                print(f"MIME: {item['mimeType']}")
                # Save to file for verification
                import base64
                with open("screenshot_test.png", "wb") as f:
                    f.write(base64.b64decode(item['data']))
                print("Saved to screenshot_test.png")
    else:
        print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
