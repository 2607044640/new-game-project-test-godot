---
inclusion: always
---

<instructions>
# Godot C# Development Rules

## Session Start
Read `.kiro/steering/docLastConversationState.md` to restore context.

## Execution Protocol
- Call `mcp_sequential_thinking_sequentialthinking` on EVERY request
- Execute immediately - never reply with just "Understood"
- Implement incrementally, verify each step

## C# Compilation
After editing `.cs` file:
```cmd
dotnet build "New Game Project Test Godot.sln"
```

Verify in Godot Editor: Click "Build" button (top-right)

## Testing Game State
Test game state capture:
```cmd
python .kiro/scripts/testing/detailed_game_state.py
```

View comprehensive test results:
```cmd
python .kiro/scripts/testing/comprehensive_test.py
```

## Logging
Read logs:
```powershell
Get-Content "$env:APPDATA\Godot\app_userdata\New Game Project Test Godot\logs\godot.log" -Tail 50
```

In code:
```csharp
GD.Print("message");        // Normal
GD.PrintErr("error");       // Red
GD.PushWarning("warning");  // Yellow
```

## Scene System
- Save node tree as `.tscn` - instantly reusable
- Instance: `Ctrl+Shift+A` > "Instance Child Scene"
- Inherit: Right-click scene > "Change Type" > Load parent

## TempFolder
Location: `.kiro/TempFolder/`

Use for: Task checklists, analysis notes, bug tracking
Format: `FeatureName_Purpose.md` with `[ ]`/`[x]` checkboxes
Delete when complete.

Never use for: Permanent docs, steering files, specs
</instructions>

<mcp_tools>
# Godot MCP Tools

## Build & Run
```
build_project    - Compile C# project
start_game       - Build + launch Godot
get_logs         - Read recent log lines (default: 50)
```

## Game Control (requires game running)
```
get_scene_tree   - Get scene structure
simulate_click   - Click at (x, y)
get_game_state   - Capture screenshot + structured data
```

## Usage
```
"Compile"              → build_project
"Last 20 log lines"    → get_logs with lines=20
"Click at 320, 240"    → simulate_click with x=320, y=240
"Capture game state"   → get_game_state
```

## Key Feature
`get_game_state` returns:
- Screenshot (PNG base64)
- Structured data (icon types, positions, counts)
- Solves vision model counting issues

## Configuration
Edit `.kiro/scripts/godot_config.json` for Godot executable path.
</mcp_tools>

<context>
**Project:** 消消乐+扫雷混合游戏 (Match-3 + Minesweeper hybrid)
**Engine:** Godot 4.6.1 stable mono
**Language:** C# only

**Key Files:**
- Main Scene: `My2DMap.tscn`
- MCP Server: `Scripts/MCP/MCPServer.cs` (port 8765)
- Game State: `Scripts/MCP/GameStateCapture.cs`
- Test Scripts: `.kiro/scripts/testing/`
</context>

