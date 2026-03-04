# Implementation Plan: Game State Capture System

## Overview

This implementation plan breaks down the game state capture system into discrete, testable steps. The system provides structured game state data alongside screenshots, enabling AI agents to reliably analyze game state without depending on vision model capabilities.

The implementation follows an incremental approach: data structures → capture logic → MCP integration → testing. Each step builds on previous work and validates functionality early.

## Tasks

- [ ] 1. Create data structure classes
  - [x] 1.1 Create GameStateData.cs with all data structures
    - Define GameStateData, ScreenshotData, GridStateData, CellData, GameStatistics classes
    - Add JSON serialization attributes
    - Include XML documentation comments
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1_
  
  - [x] 1.2 Write property test for JSON serialization round-trip
    - **Property 7: JSON Serialization Round-Trip**
    - **Validates: Requirements 1.3, 3.3**
    - Generate random GameStateData instances, serialize to JSON, deserialize, verify equality
    - _Requirements: 1.3, 3.3_
  
  - [ ] 1.3 Write unit tests for data structure validation
    - Test empty cell representation
    - Test custom data fields
    - Test dimension validation
    - _Requirements: 4.4, 5.4, 2.3_

- [ ] 2. Implement GameStateCapture class
  - [x] 2.1 Create GameStateCapture.cs with basic structure
    - Create class inheriting from Node
    - Add method stubs for CaptureStateAsync, CaptureScreenshotAsync, CaptureGridState, CaptureStatistics
    - Add error handling framework
    - _Requirements: 1.1, 2.1, 5.1_
  
  - [x] 2.2 Implement screenshot capture method
    - Use get_tree().root.get_viewport().get_texture().get_image()
    - Encode as PNG with save_png_to_buffer()
    - Convert to base64
    - Include dimensions
    - Reference backup file: `.kiro/TempFolder/MCPServer_Backup_WithScreenshot.cs`
    - _Requirements: 2.1, 2.2, 2.3, 2.5_
  
  - [ ] 2.3 Write property test for screenshot validity
    - **Property 4: Screenshot Validity (Round-Trip)**
    - **Validates: Requirements 2.1, 2.2, 2.5**
    - Capture screenshot, decode base64, verify PNG validity, check dimensions
    - _Requirements: 2.1, 2.2, 2.5_
  
  - [ ] 2.4 Write property test for screenshot dimensions
    - **Property 5: Screenshot Dimensions Validity**
    - **Validates: Requirements 2.3**
    - Verify width > 0 and height > 0 for all captures
    - _Requirements: 2.3_

- [x] 3. Checkpoint - Verify screenshot capture works
  - Ensure screenshot tests pass, ask the user if questions arise about game scene structure

- [ ] 4. Implement grid state extraction
  - [x] 4.1 Implement CaptureGridState method
    - Find game board node in scene tree (query My2DMap.tscn structure)
    - Iterate through cell nodes
    - Extract icon type from node properties or texture names
    - Record cell positions (row, column, screen position)
    - Build CellData list
    - _Requirements: 1.1, 4.1, 4.2, 4.3, 4.4_
  
  - [ ] 4.2 Write property test for grid state accuracy
    - **Property 1: Grid State Accuracy**
    - **Validates: Requirements 1.1, 4.1, 4.2, 4.3, 10.1, 10.3**
    - Create game boards with known states, capture, verify all cells match
    - _Requirements: 1.1, 4.1, 4.2, 4.3, 10.1, 10.3_
  
  - [ ] 4.3 Write property test for icon counting accuracy (KEY TEST)
    - **Property 2: Icon Counting Accuracy**
    - **Validates: Requirements 4.5**
    - Generate random boards with known icon counts, capture, count from structured data, verify exact match
    - This is THE KEY PROPERTY that solves the vision model problem
    - _Requirements: 4.5_
  
  - [ ] 4.4 Write unit test for empty cell representation
    - **Property 8: Empty Cell Representation**
    - **Validates: Requirements 4.4**
    - Create board with empty cells, verify distinct representation
    - _Requirements: 4.4_

- [ ] 5. Implement statistics capture
  - [ ] 5.1 Implement CaptureStatistics method
    - Query game manager for score
    - Query game manager for remaining moves
    - Query game manager for game phase
    - Support custom data fields via Dictionary
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [ ] 5.2 Write property test for statistics completeness and accuracy
    - **Property 3: Statistics Completeness and Accuracy**
    - **Validates: Requirements 1.2, 5.1, 5.2, 5.3, 5.5, 10.2**
    - Set game to known state, capture, verify all statistics fields present and accurate
    - _Requirements: 1.2, 5.1, 5.2, 5.3, 5.5, 10.2_
  
  - [ ] 5.3 Write property test for custom data preservation
    - **Property 9: Custom Data Preservation**
    - **Validates: Requirements 5.4, 7.3**
    - Add custom fields, serialize, deserialize, verify preservation
    - _Requirements: 5.4, 7.3_

- [ ] 6. Implement main capture orchestration
  - [x] 6.1 Implement CaptureStateAsync method
    - Call CaptureScreenshotAsync (with error handling)
    - Call CaptureGridState (with error handling)
    - Call CaptureStatistics (with error handling)
    - Combine results into GameStateData
    - Implement graceful degradation (continue if screenshot fails)
    - _Requirements: 3.1, 9.1, 9.2_
  
  - [ ] 6.2 Write property test for combined response completeness
    - **Property 6: Combined Response Completeness**
    - **Validates: Requirements 3.1**
    - Capture state, verify both screenshot and game_state fields are non-null
    - _Requirements: 3.1_
  
  - [ ] 6.3 Write property test for data freshness
    - **Property 13: Data Freshness**
    - **Validates: Requirements 10.4, 10.5**
    - Capture, modify game state, capture again, verify data differs
    - _Requirements: 10.4, 10.5_

- [ ] 7. Checkpoint - Verify complete capture works
  - Ensure all capture tests pass, ask the user if questions arise

- [ ] 8. Integrate with MCP Server
  - [x] 8.1 Add GameStateCapture node to autoload
    - Register GameStateCapture as singleton in project settings
    - Ensure it's available to MCPServer
    - _Requirements: 6.1_
  
  - [x] 8.2 Add get_game_state tool handler to MCPServer.cs
    - Add tool registration in GetAvailableTools
    - Implement HandleGetGameState method
    - Use TaskCompletionSource for async coordination
    - Queue capture on main thread
    - Serialize GameStateData to JSON
    - Format response according to MCP protocol
    - _Requirements: 6.1, 6.2, 6.3, 3.2_
  
  - [x] 8.3 Implement error handling in MCP handler
    - Catch exceptions from capture
    - Return MCP-formatted error responses
    - Log errors for debugging
    - _Requirements: 6.4, 9.1, 9.2, 9.3_
  
  - [ ] 8.4 Write unit tests for MCP integration
    - Test tool registration
    - Test successful capture flow
    - Test error handling
    - _Requirements: 6.1, 6.2, 6.4_

- [ ] 9. Performance testing and optimization
  - [ ] 9.1 Write property test for performance bound
    - **Property 11: Performance Bound**
    - **Validates: Requirements 8.1**
    - Measure capture time across multiple captures, verify all complete within 100ms
    - _Requirements: 8.1_
  
  - [ ] 9.2 Write property test for concurrent performance
    - **Property 12: Concurrent Performance**
    - **Validates: Requirements 8.5**
    - Issue multiple concurrent captures, verify average time within 150ms
    - _Requirements: 8.5_
  
  - [ ] 9.3 Optimize if performance tests fail
    - Profile capture operations
    - Optimize grid state extraction
    - Optimize serialization
    - _Requirements: 8.1, 8.5_

- [ ] 10. Integration testing with Python MCP bridge
  - [x] 10.1 Write integration test script
    - Start game with MCP server
    - Connect via Python bridge
    - Call get_game_state tool
    - Verify response format
    - Validate screenshot data
    - Validate grid state data
    - Count icons from structured data
    - _Requirements: 1.1, 2.1, 3.1, 4.5_
  
  - [ ] 10.2 Test error scenarios
    - Test with invalid game state
    - Test with missing game board
    - Verify error responses
    - _Requirements: 9.1, 9.2, 9.3_

- [ ] 11. Documentation and cleanup
  - [ ] 11.1 Update GodotMCPServer.md documentation
    - Document get_game_state tool
    - Provide usage examples
    - Document response format
    - Document error codes
    - _Requirements: 6.1_
  
  - [ ] 11.2 Update docLastConversationState.md
    - Mark game state capture as implemented
    - Document key findings
    - Update next steps
  
  - [ ] 11.3 Clean up temporary files
    - Remove or archive analysis documents in TempFolder
    - Keep backup files for reference

- [ ] 12. Final checkpoint - Complete system verification
  - Ensure all tests pass, verify end-to-end functionality, ask the user if ready to deploy

## Notes

- All tasks are required for comprehensive implementation with full test coverage
- Property 2 (Icon Counting Accuracy) is THE KEY TEST - it validates the core problem solution
- Each property test should run minimum 100 iterations
- Reference `.kiro/TempFolder/MCPServer_Backup_WithScreenshot.cs` for screenshot implementation
- Grid state extraction is game-specific and may need adjustment based on actual scene structure
- Performance tests should be run on representative game states
- Integration tests require the game to be running with MCP server active
