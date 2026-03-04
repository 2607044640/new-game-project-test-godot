#!/usr/bin/env python3
"""
Test Godot MCP Server connection
"""

import requests
import json
import sys

MCP_URL = "http://localhost:8765/"

def test_connection():
    """Test if Godot MCP Server is running"""
    print("Testing Godot MCP Server connection...")
    print(f"URL: {MCP_URL}")
    print("-" * 50)
    
    try:
        # Test 1: Get Scene Tree
        print("\n1. Testing get_scene_tree...")
        response = requests.post(MCP_URL, json={
            "tool": "get_scene_tree",
            "arguments": {}
        }, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Scene tree retrieved successfully!")
                print(json.dumps(result["data"], indent=2))
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Godot MCP Server")
        print("\nPlease make sure:")
        print("1. Godot game is running (press F5 in Godot Editor)")
        print("2. MCPServer node is added to the scene")
        print("3. Game has been compiled (click Build button)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    try:
        # Test 2: Get Screenshot
        print("\n2. Testing get_screenshot...")
        response = requests.post(MCP_URL, json={
            "tool": "get_screenshot",
            "arguments": {}
        }, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                screenshot_data = result["data"]["screenshot"]
                print(f"✅ Screenshot captured! Size: {len(screenshot_data)} bytes")
                
                # Save screenshot
                import base64
                from pathlib import Path
                
                img_data = base64.b64decode(screenshot_data)
                output_path = Path(".kiro/TempFolder/godot_screenshot.png")
                output_path.write_bytes(img_data)
                print(f"📸 Screenshot saved to: {output_path}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    try:
        # Test 3: Simulate Click
        print("\n3. Testing simulate_click...")
        response = requests.post(MCP_URL, json={
            "tool": "simulate_click",
            "arguments": {"x": 320, "y": 240}
        }, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ Click simulated at (320, 240)")
                print(json.dumps(result["data"], indent=2))
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
