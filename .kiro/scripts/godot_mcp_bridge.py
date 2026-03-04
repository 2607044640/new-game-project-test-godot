#!/usr/bin/env python3
"""
Godot MCP Bridge
Connects Kiro to the Godot game via MCP protocol
"""

import json
import sys
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict

# Try to import requests, but make it optional for basic functionality
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

GODOT_MCP_URL = "http://localhost:8765/"
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Load config
CONFIG_FILE = Path(__file__).parent / "godot_config.json"
if CONFIG_FILE.exists():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        GODOT_EXECUTABLE = config.get("godot_executable", "godot")
        PROJECT_ROOT = Path(config.get("project_root", PROJECT_ROOT))
else:
    GODOT_EXECUTABLE = os.environ.get("GODOT_EXECUTABLE", "godot")

def call_godot_mcp(tool: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
    """Call Godot MCP Server"""
    if not HAS_REQUESTS:
        # Fallback to urllib if requests not available
        import urllib.request
        import urllib.error
        
        payload = {
            "tool": tool,
            "arguments": arguments or {}
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(GODOT_MCP_URL, data=data, 
                                        headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError:
            return {
                "success": False,
                "error": "Cannot connect to Godot. Make sure the game is running."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    payload = {
        "tool": tool,
        "arguments": arguments or {}
    }
    
    try:
        response = requests.post(GODOT_MCP_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to Godot. Make sure the game is running."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def start_game() -> Dict[str, Any]:
    """Start Godot game"""
    try:
        # Build first
        build_result = build_project()
        if not build_result.get("success"):
            return build_result
        
        # Start Godot in headless mode or with display
        cmd = [GODOT_EXECUTABLE, "--path", str(PROJECT_ROOT)]
        
        # Start process in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(PROJECT_ROOT)
        )
        
        # Wait a bit for server to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            return {
                "success": False,
                "error": f"Godot failed to start: {stderr.decode('utf-8', errors='ignore')}"
            }
        
        return {
            "success": True,
            "message": f"Godot game started (PID: {process.pid})",
            "pid": process.pid
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"Godot executable not found: {GODOT_EXECUTABLE}. Set GODOT_EXECUTABLE env variable."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to start game: {str(e)}"
        }

def build_project() -> Dict[str, Any]:
    """Build C# project"""
    try:
        sln_file = PROJECT_ROOT / "New Game Project Test Godot.sln"
        
        if not sln_file.exists():
            return {
                "success": False,
                "error": f"Solution file not found: {sln_file}"
            }
        
        result = subprocess.run(
            ["dotnet", "build", str(sln_file)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "Build succeeded",
                "output": result.stdout
            }
        else:
            return {
                "success": False,
                "error": "Build failed",
                "output": result.stdout + "\n" + result.stderr
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Build timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Build error: {str(e)}"
        }

def get_logs(lines: int = 50) -> Dict[str, Any]:
    """Get Godot logs"""
    try:
        # Try to read log file directly
        appdata = os.environ.get("APPDATA")
        if not appdata:
            return {
                "success": False,
                "error": "APPDATA environment variable not found"
            }
        
        log_path = Path(appdata) / "Godot" / "app_userdata" / "New Game Project Test Godot" / "logs" / "godot.log"
        
        if not log_path.exists():
            return {
                "success": False,
                "error": f"Log file not found: {log_path}"
            }
        
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            return {
                "success": True,
                "logs": [line.rstrip() for line in recent_lines],
                "total_lines": len(all_lines)
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to read logs: {str(e)}"
        }

def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request from Kiro"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "tools/list":
        # Return available tools
        return {
            "tools": [
                {
                    "name": "start_game",
                    "description": "Start the Godot game (builds first, then launches)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "build_project",
                    "description": "Build the C# project using dotnet build",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "get_logs",
                    "description": "Get recent Godot log entries",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "lines": {
                                "type": "number",
                                "description": "Number of recent log lines to retrieve (default: 50)",
                                "default": 50
                            }
                        },
                        "required": []
                    }
                },
                {
                    "name": "get_scene_tree",
                    "description": "Get the current Godot scene tree structure (requires game running)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "simulate_click",
                    "description": "Simulate a mouse click at specified coordinates (requires game running)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {
                                "type": "number",
                                "description": "X coordinate"
                            },
                            "y": {
                                "type": "number",
                                "description": "Y coordinate"
                            }
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "get_screenshot",
                    "description": "Get a screenshot of the game viewport as Base64 PNG (requires game running)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        # Call a tool
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        # Handle local tools (don't need game running)
        if tool_name == "start_game":
            result = start_game()
        elif tool_name == "build_project":
            result = build_project()
        elif tool_name == "get_logs":
            lines = tool_args.get("lines", 50)
            result = get_logs(lines)
        # Handle game tools (need game running)
        elif tool_name in ["get_scene_tree", "simulate_click", "get_screenshot"]:
            result = call_godot_mcp(tool_name, tool_args)
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {tool_name}"
                    }
                ],
                "isError": True
            }
        
        if result.get("success"):
            # Format output based on tool
            if tool_name == "get_logs":
                text = "\n".join(result.get("logs", []))
            elif tool_name in ["build_project", "start_game"]:
                text = result.get("message", "") + "\n" + result.get("output", "")
            else:
                text = json.dumps(result.get("data"), indent=2)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {result.get('error')}\n{result.get('output', '')}"
                    }
                ],
                "isError": True
            }
    
    return {"error": "Unknown method"}

def main():
    """Main MCP server loop"""
    print("Godot MCP Bridge started", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_mcp_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {
                "error": str(e)
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
