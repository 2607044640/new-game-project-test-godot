#!/usr/bin/env python3
"""
Simple Godot MCP Server test (no external dependencies)
Uses only Python standard library
"""

import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

MCP_URL = "http://localhost:8765/"

def call_mcp(tool, arguments=None):
    """Call Godot MCP Server using urllib"""
    payload = {
        "tool": tool,
        "arguments": arguments or {}
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = Request(MCP_URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except URLError as e:
        return {"success": False, "error": f"Connection error: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("=" * 60)
    print("Godot MCP Server Test (Simple Version)")
    print("=" * 60)
    
    # Test 1: Get Scene Tree
    print("\n[1/3] Testing get_scene_tree...")
    result = call_mcp("get_scene_tree")
    
    if result.get("success"):
        print("✅ SUCCESS: Scene tree retrieved!")
        print(json.dumps(result["data"], indent=2)[:500] + "...")
    else:
        print(f"❌ FAILED: {result.get('error')}")
        print("\n⚠️  Make sure:")
        print("  1. Godot game is running (press F5)")
        print("  2. MCPServer node is in the scene")
        print("  3. Output shows: 'MCP Server started on port 8765'")
        return False
    
    # Test 2: Simulate Click
    print("\n[2/3] Testing simulate_click...")
    result = call_mcp("simulate_click", {"x": 320, "y": 240})
    
    if result.get("success"):
        print(f"✅ SUCCESS: Click simulated at (320, 240)")
    else:
        print(f"❌ FAILED: {result.get('error')}")
    
    # Test 3: Get Screenshot
    print("\n[3/3] Testing get_screenshot...")
    result = call_mcp("get_screenshot")
    
    if result.get("success"):
        screenshot_b64 = result["data"]["screenshot"]
        print(f"✅ SUCCESS: Screenshot captured!")
        print(f"   Size: {len(screenshot_b64)} bytes (Base64)")
        
        # Save screenshot
        try:
            import base64
            img_data = base64.b64decode(screenshot_b64)
            
            with open(".kiro/TempFolder/godot_screenshot.png", "wb") as f:
                f.write(img_data)
            
            print(f"   📸 Saved to: .kiro/TempFolder/godot_screenshot.png")
        except Exception as e:
            print(f"   ⚠️  Could not save screenshot: {e}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
