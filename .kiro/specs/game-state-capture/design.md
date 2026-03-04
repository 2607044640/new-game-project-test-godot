# Design Document: Game State Capture System

## Overview

The Game State Capture System provides a reliable way for AI agents to analyze game state without depending on vision model capabilities. Instead of relying on AI to "see" and count objects in screenshots, the system provides structured data (grid state, statistics, positions) alongside screenshots for visual context.

This design addresses the fundamental limitation of Vision-Language Models (VLMs) in counting repeated objects - a problem known as "attention collapse." By providing structured data, we enable accurate programmatic analysis while maintaining visual feedback for human developers.

### Key Design Principles

1. **Structured Data First**: Prioritize machine-readable data over visual analysis
2. **Visual Context Secondary**: Screenshots supplement structured data for human review
3. **Extensibility**: Easy to add new game state properties
4. **Performance**: Non-blocking capture that doesn't disrupt gameplay
5. **Accuracy**: Captured state exactly matches actual game state

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         AI Agent                             │
│                    (External MCP Client)                     │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Request: get_game_state
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      MCPServer.cs                            │
│  - Handles MCP protocol                                      │
│  - Routes tool requests                                      │
│  - Serializes responses                                      │
└────────────────────────┬────────────────────────────────────┘
                         │ Call capture
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  GameStateCapture.cs                         │
│  - Orchestrates state capture                                │
│  - Calls specialized capture methods                         │
│  - Combines results                                          │
└─────┬──────────────────┬──────────────────┬─────────────────┘
      │                  │                  │
      ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐      ┌──────────┐
│Screenshot│      │Grid State│      │Statistics│
│ Capture  │      │ Capture  │      │ Capture  │
└──────────┘      └──────────┘      └──────────┘
      │                  │                  │
      └──────────────────┴──────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  GameStateData.cs   │
              │  - Data structures  │
              │  - JSON serialization│
              └─────────────────────┘
```

### Component Responsibilities

**MCPServer.cs** (Modified)
- Add handler for "get_game_state" tool
- Invoke GameStateCapture
- Serialize response to JSON
- Handle errors and return MCP-formatted responses

**GameStateCapture.cs** (New)
- Main orchestrator for state capture
- Calls screenshot capture method
- Calls grid state extraction method
- Calls statistics extraction method
- Combines results into GameStateData
- Handles async operations on main thread

**GameStateData.cs** (New)
- Data structures for all captured state
- JSON serialization attributes
- Validation methods

## Components and Interfaces

### GameStateData.cs

```csharp
public class GameStateData
{
    public ScreenshotData Screenshot { get; set; }
    public GridStateData GameState { get; set; }
}

public class ScreenshotData
{
    public string Base64 { get; set; }
    public int Width { get; set; }
    public int Height { get; set; }
    public string MimeType { get; set; } = "image/png";
}

public class GridStateData
{
    public int Rows { get; set; }
    public int Columns { get; set; }
    public List<CellData> Cells { get; set; }
    public GameStatistics Statistics { get; set; }
}

public class CellData
{
    public int Row { get; set; }
    public int Column { get; set; }
    public string IconType { get; set; }  // e.g., "red", "blue", "bomb", "empty"
    public Vector2 ScreenPosition { get; set; }
}

public class GameStatistics
{
    public int Score { get; set; }
    public int RemainingMoves { get; set; }
    public string GamePhase { get; set; }  // e.g., "playing", "game_over", "paused"
    public Dictionary<string, object> CustomData { get; set; }  // Extensibility
}
```

### GameStateCapture.cs Interface

```csharp
public class GameStateCapture : Node
{
    // Main capture method
    public async Task<GameStateData> CaptureStateAsync()
    
    // Individual capture methods
    private async Task<ScreenshotData> CaptureScreenshotAsync()
    private GridStateData CaptureGridState()
    private GameStatistics CaptureStatistics()
    
    // Helper methods
    private Node FindGameBoard()
    private List<CellData> ExtractCellsFromBoard(Node board)
}
```

### MCPServer.cs Integration

```csharp
// Add to tool handlers
private string HandleGetGameState(Dictionary<string, object> arguments)
{
    try
    {
        // Queue capture on main thread
        var tcs = new TaskCompletionSource<GameStateData>();
        _mainThreadQueue.Enqueue(() => {
            var capture = GetNode<GameStateCapture>("/root/GameStateCapture");
            var result = await capture.CaptureStateAsync();
            tcs.SetResult(result);
        });
        
        var gameState = await tcs.Task;
        return SerializeGameState(gameState);
    }
    catch (Exception ex)
    {
        return CreateErrorResponse($"Failed to capture game state: {ex.Message}");
    }
}
```

## Data Models

### MCP Response Format

The response follows MCP protocol standards with both text and image content:

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"game_state\": {...}, \"screenshot\": {...}}"
    },
    {
      "type": "image",
      "data": "base64_encoded_png_data",
      "mimeType": "image/png"
    }
  ]
}
```

### Game State JSON Structure

```json
{
  "screenshot": {
    "base64": "iVBORw0KGgoAAAANS...",
    "width": 1920,
    "height": 1080,
    "mimeType": "image/png"
  },
  "game_state": {
    "rows": 8,
    "columns": 8,
    "cells": [
      {
        "row": 0,
        "column": 0,
        "iconType": "red",
        "screenPosition": {"x": 100, "y": 150}
      },
      {
        "row": 0,
        "column": 1,
        "iconType": "blue",
        "screenPosition": {"x": 180, "y": 150}
      }
    ],
    "statistics": {
      "score": 1250,
      "remainingMoves": 15,
      "gamePhase": "playing",
      "customData": {
        "minesRevealed": 3,
        "comboCount": 2
      }
    }
  }
}
```

### Grid State Extraction Strategy

The system needs to query the game scene to extract grid state. For the Match-3 + Minesweeper hybrid:

1. **Find the game board node** - Query scene tree for the board container
2. **Iterate through cells** - Get all child nodes representing cells
3. **Extract icon type** - Read node properties or texture names to determine icon type
4. **Record positions** - Get global position of each cell
5. **Build cell list** - Create CellData objects for each cell

This approach is game-specific and should be implemented in a way that's easy to modify for different game types.



## Error Handling

### Error Categories

**Screenshot Capture Errors**
- Viewport not found
- Image encoding failure
- Memory allocation failure
- Async operation timeout

**Grid State Extraction Errors**
- Game board node not found
- Invalid cell structure
- Missing icon type information
- Position calculation failure

**Serialization Errors**
- JSON serialization failure
- Invalid data structure
- Circular reference detection
- Encoding errors

### Error Response Format

All errors follow MCP error response format:

```json
{
  "error": {
    "code": "CAPTURE_FAILED",
    "message": "Failed to capture game state: Grid board node not found",
    "details": {
      "component": "GameStateCapture",
      "method": "CaptureGridState",
      "timestamp": "2025-01-15T10:30:00Z"
    }
  }
}
```

### Error Handling Strategy

1. **Graceful Degradation**: If screenshot fails, still return grid state if available
2. **Detailed Logging**: Log all errors with stack traces for debugging
3. **Retry Logic**: For transient errors (e.g., async timeouts), implement retry with exponential backoff
4. **Validation**: Validate data structures before serialization to catch errors early
5. **User-Friendly Messages**: Provide actionable error messages for AI agents

### Error Recovery

```csharp
public async Task<GameStateData> CaptureStateAsync()
{
    var result = new GameStateData();
    
    try
    {
        result.Screenshot = await CaptureScreenshotAsync();
    }
    catch (Exception ex)
    {
        GD.PushWarning($"Screenshot capture failed: {ex.Message}");
        // Continue with null screenshot - grid state is more important
    }
    
    try
    {
        result.GameState = CaptureGridState();
    }
    catch (Exception ex)
    {
        GD.PrintErr($"Grid state capture failed: {ex.Message}");
        throw; // Grid state is critical - fail if unavailable
    }
    
    return result;
}
```

## Testing Strategy

### Dual Testing Approach

This system requires both unit tests and property-based tests for comprehensive coverage:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Test screenshot capture with known viewport
- Test grid state extraction with mock game board
- Test JSON serialization with sample data
- Test error handling with simulated failures
- Test MCP response formatting

**Property-Based Tests**: Verify universal properties across all inputs
- Test serialization round-trips for all valid game states
- Test grid state accuracy for randomly generated boards
- Test data structure invariants
- Test performance characteristics

Both approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing Configuration

We'll use **NUnit** with **FsCheck** for property-based testing in C#:

```csharp
[Test, Property(Iterations = 100)]
public void PropertyTest_Example(/* generated parameters */)
{
    // Test implementation
}
```

Each property test will:
- Run minimum 100 iterations (due to randomization)
- Be tagged with a comment referencing the design property
- Reference the specific requirements it validates

Tag format: `// Feature: game-state-capture, Property {number}: {property_text}`

### Test Organization

```
Tests/
├── Unit/
│   ├── GameStateDataTests.cs
│   ├── GameStateCaptureTests.cs
│   └── MCPServerIntegrationTests.cs
└── Properties/
    ├── SerializationPropertyTests.cs
    ├── GridStatePropertyTests.cs
    └── AccuracyPropertyTests.cs
```

### Integration Testing

Integration tests will verify the complete flow:

1. Start MCP Server
2. Send "get_game_state" request
3. Verify response format
4. Validate screenshot data
5. Validate grid state data
6. Verify data accuracy against actual game state

### Performance Testing

Performance tests will verify:
- Capture completes within 100ms
- Memory usage stays within acceptable bounds
- No memory leaks over repeated captures
- Concurrent captures don't degrade performance



## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system - essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

The following properties define the correctness criteria for the game state capture system. Each property is universally quantified and references the requirements it validates.

### Property 1: Grid State Accuracy

*For any* game board state, the captured grid data SHALL exactly match the actual game board, including all cell icon types, positions, and grid dimensions.

**Validates: Requirements 1.1, 4.1, 4.2, 4.3, 10.1, 10.3**

**Rationale**: This is the core accuracy property. The entire purpose of structured data is to provide accurate, programmatic access to game state. If the captured grid doesn't match reality, the system fails its primary purpose.

**Test Approach**: Create game boards with known states, capture them, and verify every cell's icon type and position matches the actual board.

### Property 2: Icon Counting Accuracy (KEY PROPERTY)

*For any* game board state and any icon type, counting icons from the structured data SHALL produce the exact count of that icon type in the actual game board.

**Validates: Requirements 4.5**

**Rationale**: This is THE KEY PROPERTY that solves the original problem. Vision models cannot accurately count repeated icons due to attention collapse. By providing structured data, we enable perfect counting without visual analysis. This property must ALWAYS hold.

**Test Approach**: Generate random game boards with known icon counts, capture state, count icons from structured data, and verify counts match exactly.

### Property 3: Statistics Completeness and Accuracy

*For any* game state capture, the statistics SHALL include score, remaining moves, and game phase fields, and these values SHALL exactly match the actual game state at capture time.

**Validates: Requirements 1.2, 5.1, 5.2, 5.3, 5.5, 10.2**

**Rationale**: Statistics provide context for AI decision-making. Incomplete or inaccurate statistics lead to poor decisions.

**Test Approach**: Set game to known state (specific score, moves, phase), capture state, and verify all statistics fields are present and accurate.

### Property 4: Screenshot Validity (Round-Trip)

*For any* captured screenshot, decoding the base64 data SHALL produce a valid PNG image, and the image dimensions SHALL match the reported width and height.

**Validates: Requirements 2.1, 2.2, 2.5**

**Rationale**: This is a round-trip property. If we can encode and decode the screenshot successfully, it's valid. This ensures the screenshot is usable for human review.

**Test Approach**: Capture screenshot, decode base64, verify PNG validity, check dimensions match.

### Property 5: Screenshot Dimensions Validity

*For any* captured screenshot, the width and height SHALL be positive integers greater than zero.

**Validates: Requirements 2.3**

**Rationale**: Invalid dimensions (zero, negative) indicate a capture failure. This is a basic invariant.

**Test Approach**: Capture screenshot and verify width > 0 and height > 0.

### Property 6: Combined Response Completeness

*For any* game state capture request, the response SHALL include both a non-null screenshot field and a non-null game_state field.

**Validates: Requirements 3.1**

**Rationale**: The system promises both visual and structured data. Missing either field breaks the contract.

**Test Approach**: Capture state and verify both fields are present and non-null.

### Property 7: JSON Serialization Round-Trip

*For any* valid game state data, serializing to JSON and then deserializing SHALL produce an equivalent data structure with all fields preserved.

**Validates: Requirements 1.3, 3.3**

**Rationale**: This is a classic round-trip property. If serialization loses data, the system is broken. This ensures data integrity through the MCP protocol.

**Test Approach**: Create game state data, serialize to JSON, deserialize, and verify all fields match original.

### Property 8: Empty Cell Representation

*For any* game board containing empty cells, the captured grid state SHALL represent empty cells with a distinct icon type (e.g., "empty" or null) that differs from all occupied cell icon types.

**Validates: Requirements 4.4**

**Rationale**: Empty cells must be distinguishable from occupied cells for accurate game state analysis. This is an edge case that's important to handle correctly.

**Test Approach**: Create board with empty cells, capture state, verify empty cells have distinct representation.

### Property 9: Custom Data Preservation

*For any* game state with custom data fields in the statistics, serializing and deserializing SHALL preserve all custom fields and their values.

**Validates: Requirements 5.4, 7.3**

**Rationale**: Extensibility requires that custom data survives serialization. This ensures the system can grow without breaking.

**Test Approach**: Add custom fields to statistics, serialize, deserialize, verify custom fields are preserved.

### Property 10: Backward Compatibility

*For any* game state data structure, adding new optional fields SHALL NOT break deserialization of data that lacks those fields.

**Validates: Requirements 7.5**

**Rationale**: As the system evolves, old data must still be readable. This ensures we don't break existing consumers.

**Test Approach**: Deserialize old-format JSON (missing new fields), verify it succeeds and uses default values.

### Property 11: Performance Bound

*For any* game state capture, the operation SHALL complete within 100 milliseconds.

**Validates: Requirements 8.1**

**Rationale**: Slow captures disrupt gameplay. This is a performance invariant that must hold.

**Test Approach**: Measure capture time across multiple captures, verify all complete within threshold.

### Property 12: Concurrent Performance

*For any* sequence of N concurrent capture requests (N ≤ 10), the average capture time SHALL NOT exceed 150 milliseconds.

**Validates: Requirements 8.5**

**Rationale**: Multiple AI agents might request state simultaneously. The system should handle this gracefully.

**Test Approach**: Issue multiple concurrent capture requests, measure average time, verify within threshold.

### Property 13: Data Freshness

*For any* two sequential captures with a game state change between them, the second capture SHALL reflect the changed state and SHALL NOT return the same data as the first capture.

**Validates: Requirements 10.4, 10.5**

**Rationale**: Stale data leads to incorrect AI decisions. Each capture must reflect current reality.

**Test Approach**: Capture state, modify game state, capture again, verify data differs and reflects changes.

### Summary of Properties

The properties above cover:
- **Accuracy** (Properties 1, 2, 3, 13): Data matches reality
- **Validity** (Properties 4, 5, 6, 7): Data structures are well-formed
- **Robustness** (Properties 8, 9, 10): Edge cases and extensibility
- **Performance** (Properties 11, 12): System responsiveness

Property 2 (Icon Counting Accuracy) is the most critical - it directly solves the vision model limitation that motivated this entire system.
