using Godot;
using System;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace GameStateCaptureSystem
{
    /// <summary>
    /// Orchestrates game state capture including screenshots, grid state, and statistics.
    /// Provides structured data for AI analysis alongside visual context for humans.
    /// </summary>
    public partial class GameStateCapture : Node
    {
        /// <summary>
        /// Main capture method that orchestrates all state collection.
        /// Returns combined screenshot and structured game state data.
        /// </summary>
        public async Task<GameStateData> CaptureStateAsync()
        {
            var result = new GameStateData();

            try
            {
                // Capture screenshot (graceful degradation if fails)
                result.Screenshot = await CaptureScreenshotAsync();
            }
            catch (Exception ex)
            {
                GD.PushWarning($"Screenshot capture failed: {ex.Message}");
                // Continue without screenshot - structured data is more important
            }

            try
            {
                // Capture grid state (critical - fail if unavailable)
                result.GameState = CaptureGridState();
            }
            catch (Exception ex)
            {
                GD.PrintErr($"Grid state capture failed: {ex.Message}");
                throw; // Grid state is critical
            }

            return result;
        }

        /// <summary>
        /// Captures a screenshot of the current viewport.
        /// Returns base64-encoded PNG with dimensions.
        /// </summary>
        private async Task<ScreenshotData> CaptureScreenshotAsync()
        {
            // Must execute on main thread - Godot API requirement
            var viewport = GetTree().Root.GetViewport();
            if (viewport == null)
            {
                throw new InvalidOperationException("Viewport not found");
            }

            var texture = viewport.GetTexture();
            if (texture == null)
            {
                throw new InvalidOperationException("Viewport texture not found");
            }

            var image = texture.GetImage();
            if (image == null)
            {
                throw new InvalidOperationException("Failed to get image from texture");
            }

            // Encode as PNG
            byte[] pngBytes = image.SavePngToBuffer();
            if (pngBytes == null || pngBytes.Length == 0)
            {
                throw new InvalidOperationException("Failed to encode PNG");
            }

            // Convert to base64
            string base64 = Convert.ToBase64String(pngBytes);

            return new ScreenshotData
            {
                Base64 = base64,
                Width = image.GetWidth(),
                Height = image.GetHeight(),
                MimeType = "image/png"
            };
        }

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
        /// Captures current game statistics (score, moves, phase).
        /// Returns statistics data for AI decision-making.
        /// </summary>
        private GameStatistics CaptureStatistics()
        {
            // Simple placeholder implementation
            return new GameStatistics
            {
                Score = 0,
                RemainingMoves = 0,
                GamePhase = "testing",
                CustomData = new Dictionary<string, object>
                {
                    { "note", "Placeholder statistics - implement game manager integration" }
                }
            };
        }

        /// <summary>
        /// Finds all Sprite2D nodes (icons) recursively in the scene tree.
        /// Only includes nodes that are visible in the tree.
        /// </summary>
        private List<Sprite2D> FindIconsRecursive(Node node)
        {
            var icons = new List<Sprite2D>();

            if (node is Sprite2D sprite && node.Name.ToString().Contains("Icon"))
            {
                // Only add if visible in the scene tree
                if (sprite.IsVisibleInTree())
                {
                    icons.Add(sprite);
                }
            }

            foreach (Node child in node.GetChildren())
            {
                icons.AddRange(FindIconsRecursive(child));
            }

            return icons;
        }
    }
}
