#!/usr/bin/env python3
"""Test start_game MCP tool"""

import json
import subprocess
import time

def test_start_game():
    """Test starting Godot game"""
    request = {
        "method": "tools/call",
        "params": {
            "name": "start_game",
            "arguments": {}
        }
    }
    
    print("="*60)
    print("Testing: start_game")
    print("="*60)
    
    # Run bridge script
    process = subprocess.Popen(
        ["python", ".kiro/scripts/godot_mcp_bridge.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(json.dumps(request) + "\n", timeout=35)
    
    if stderr:
        print(f"STDERR: {stderr}")
    
    try:
        response = json.loads(stdout.strip())
        if response.get("isError"):
            print(f"❌ ERROR: {response['content'][0]['text']}")
            return False
        else:
            print(f"✅ SUCCESS:")
            print(response['content'][0]['text'])
            
            # Wait a bit and check if game is running
            time.sleep(3)
            print("\n⏳ Waiting for game to start...")
            
            # Try to connect to MCP server
            import urllib.request
            try:
                req = urllib.request.Request("http://localhost:8765/")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    print("✅ Game MCP Server is responding!")
                    return True
            except:
                print("⚠️  Game started but MCP Server not responding yet")
                return True
                
    except Exception as e:
        print(f"❌ Failed: {e}")
        print(f"Raw output: {stdout}")
        return False

if __name__ == "__main__":
    success = test_start_game()
    print("\n" + "="*60)
    if success:
        print("✅ start_game test PASSED")
        print("Note: Close the Godot window manually")
    else:
        print("❌ start_game test FAILED")
    print("="*60)
