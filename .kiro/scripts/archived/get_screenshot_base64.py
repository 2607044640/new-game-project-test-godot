#!/usr/bin/env python3
"""Get screenshot as Base64 and output for display"""

import urllib.request
import json
import sys

def get_screenshot():
    """Get screenshot from Godot MCP Server"""
    try:
        payload = {
            "tool": "get_screenshot",
            "arguments": {}
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            'http://localhost:8765/',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get("success"):
                screenshot_b64 = result["data"]["screenshot"]
                print(f"Screenshot captured: {len(screenshot_b64)} bytes (Base64)")
                print("\n" + "="*60)
                print("BASE64_IMAGE_START")
                print(screenshot_b64)
                print("BASE64_IMAGE_END")
                print("="*60)
                return screenshot_b64
            else:
                print(f"Error: {result.get('error')}")
                return None
                
    except Exception as e:
        print(f"Failed to get screenshot: {e}")
        return None

if __name__ == "__main__":
    get_screenshot()
