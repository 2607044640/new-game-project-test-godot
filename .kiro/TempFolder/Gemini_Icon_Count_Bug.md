# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows

## Problem
GameStateCapture system reports 6 icons in the scene, but user only sees 3 icons in the actual game. The system is detecting all Sprite2D nodes with "Icon" in their name, but some may be invisible, off-screen, or duplicates.

## What I Tried
1. **First attempt**: Implemented basic icon detection using `FindIconsRecursive()` that searches for all Sprite2D nodes containing "Icon" in name
   - Result: Reports 6 icons (Icon, Icon2, Icon3, Icon7, Icon8, Icon9) but user sees only 3
   
2. **Second attempt**: Created detailed analysis script to show all icon positions
   - Result: Confirmed 6 nodes detected with positions:
     - Icon at (192.0, 312.0)
     - Icon7 at (597.0, 516.0)
     - Icon8 at (196.0, 97.0)
     - Icon9 at (1017.0, 88.0)
     - Icon3 at (978.0, 298.0)
     - Icon2 at (606.0, 118.0)
   
3. **Third attempt**: Verified screenshot capture works correctly (43,172 bytes PNG saved)
   - Result: Screenshot saves successfully but discrepancy between detected nodes and visible icons remains

## Current Code

### GameStateCapture.cs - Icon Detection Method
```csharp
/// <summary>
/// Captures the current grid/board state with all cell data.
/// Returns structured data for programmatic analysis.
/// </summary>
private GridStateData CaptureGridState()
{
    var gridState = new GridStateData
    {
        Rows = 0,
        Columns = 0,
        Cells = new List<CellData>(),
        Statistics = CaptureStatistics()
    };

    // Find all Sprite2D nodes (icons) in the scene
    var root = GetTree().Root;
    var icons = FindIconsRecursive(root);

    // For now, treat each icon as a cell
    // This is a simple implementation - can be extended for actual grid structure
    int index = 0;
    foreach (var icon in icons)
    {
        var cell = new CellData
        {
            Row = index / 8,  // Assume 8 columns for now
            Column = index % 8,
            IconType = icon.Name,  // Use node name as icon type
            ScreenPosition = new Vector2Data(icon.GlobalPosition)
        };
        gridState.Cells.Add(cell);
        index++;
    }

    gridState.Rows = (gridState.Cells.Count + 7) / 8;  // Calculate rows
    gridState.Columns = Math.Min(gridState.Cells.Count, 8);

    return gridState;
}

/// <summary>
/// Finds all Sprite2D nodes (icons) recursively in the scene tree.
/// </summary>
private List<Sprite2D> FindIconsRecursive(Node node)
{
    var icons = new List<Sprite2D>();

    if (node is Sprite2D sprite && node.Name.ToString().Contains("Icon"))
    {
        icons.Add(sprite);
    }

    foreach (Node child in node.GetChildren())
    {
        icons.AddRange(FindIconsRecursive(child));
    }

    return icons;
}
```

## Test Output
```
📊 GRID INFORMATION:
   Rows: 1
   Columns: 6
   Total cells detected: 6

🎯 DETAILED CELL INFORMATION:
Cell #1: Row 0, Column 0, Icon Type: Icon, Screen Position: (192.0, 312.0)
Cell #2: Row 0, Column 1, Icon Type: Icon7, Screen Position: (597.0, 516.0)
Cell #3: Row 0, Column 2, Icon Type: Icon8, Screen Position: (196.0, 97.0)
Cell #4: Row 0, Column 3, Icon Type: Icon9, Screen Position: (1017.0, 88.0)
Cell #5: Row 0, Column 4, Icon Type: Icon3, Screen Position: (978.0, 298.0)
Cell #6: Row 0, Column 5, Icon Type: Icon2, Screen Position: (606.0, 118.0)

📈 ICON COUNT SUMMARY:
   Icon: 1, Icon2: 1, Icon3: 1, Icon7: 1, Icon8: 1, Icon9: 1
```

## Expected Behavior
The system should only detect and report the 3 icons that are actually visible in the game.

## Actual Behavior
The system detects 6 Sprite2D nodes with "Icon" in their names, even though only 3 are visible to the user.

## Possible Causes
1. Some icons might be invisible (Visible property set to false)
2. Some icons might be off-screen or outside the viewport
3. Some icons might be in different layers or z-index
4. There might be duplicate or template nodes in the scene tree
5. Some nodes might be in the editor but not active in the running game

## Questions for Gemini

1. **How should I filter the icon detection to only include visible icons?**
   - Should I check the `Visible` property?
   - Should I check if the icon is within the viewport bounds?
   - Should I check the `Modulate.A` (alpha) value?

2. **What's the best way to determine if a Sprite2D is actually rendered in the game?**
   - Is there a method to check if a node is in the active scene vs editor-only?
   - Should I check parent node visibility recursively?

3. **How can I verify which icons are actually visible to the player?**
   - Should I use `GetViewportRect()` to check if position is within bounds?
   - Should I check `IsVisibleInTree()` method?

4. **What's the recommended approach for game state capture in Godot?**
   - Should I use a different method than recursive scene tree traversal?
   - Should I maintain a separate list of active game objects?

## Additional Context
- This is part of an MCP (Model Context Protocol) server for AI game analysis
- The goal is to provide accurate game state data without relying on vision models
- Screenshot capture works correctly (43KB PNG)
- The system is based on godot-runtime-bridge architecture
- User has modified the game scene multiple times during testing

## Request
Please provide:
1. Code fix for the `FindIconsRecursive()` method to only detect visible icons
2. Explanation of why 6 nodes are detected when only 3 are visible
3. Best practices for game state detection in Godot C#
