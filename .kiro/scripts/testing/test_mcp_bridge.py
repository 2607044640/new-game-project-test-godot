#!/usr/bin/env python3
"""Test MCP Bridge tools"""

import json
import subprocess
import sys

def test_tool(tool_name, arguments=None):
    """Test a single MCP tool"""
    request = {
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: {tool_name}")
    print(f"{'='*60}")
    
    # Run bridge script
    process = subprocess.Popen(
        ["python", ".kiro/scripts/godot_mcp_bridge.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(json.dumps(request) + "\n")
    
    if stderr:
        print(f"STDERR: {stderr}")
    
    try:
        response = json.loads(stdout.strip())
        if response.get("isError"):
            print(f"❌ ERROR: {response['content'][0]['text']}")
        else:
            print(f"✅ SUCCESS:")
            print(response['content'][0]['text'][:500])
    except Exception as e:
        print(f"❌ Failed to parse response: {e}")
        print(f"Raw output: {stdout}")

if __name__ == "__main__":
    # Test build
    test_tool("build_project")
    
    # Test logs
    test_tool("get_logs", {"lines": 10})
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)
