using Godot;
using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace GameStateCaptureSystem
{
    /// <summary>
    /// Root data structure containing both screenshot and structured game state data.
    /// This enables AI agents to analyze game state reliably without depending on vision models.
    /// </summary>
    public class GameStateData
    {
        [JsonPropertyName("screenshot")]
        public ScreenshotData Screenshot { get; set; }

        [JsonPropertyName("game_state")]
        public GridStateData GameState { get; set; }
    }

    /// <summary>
    /// Screenshot data with base64-encoded PNG image and dimensions.
    /// Provides visual context for human review.
    /// </summary>
    public class ScreenshotData
    {
        [JsonPropertyName("base64")]
        public string Base64 { get; set; }

        [JsonPropertyName("width")]
        public int Width { get; set; }

        [JsonPropertyName("height")]
        public int Height { get; set; }

        [JsonPropertyName("mimeType")]
        public string MimeType { get; set; } = "image/png";
    }

    /// <summary>
    /// Structured grid state data for programmatic analysis.
    /// Enables accurate counting and analysis without visual recognition.
    /// </summary>
    public class GridStateData
    {
        [JsonPropertyName("rows")]
        public int Rows { get; set; }

        [JsonPropertyName("columns")]
        public int Columns { get; set; }

        [JsonPropertyName("cells")]
        public List<CellData> Cells { get; set; }

        [JsonPropertyName("statistics")]
        public GameStatistics Statistics { get; set; }
    }

    /// <summary>
    /// Individual cell data with icon type and position.
    /// </summary>
    public class CellData
    {
        [JsonPropertyName("row")]
        public int Row { get; set; }

        [JsonPropertyName("column")]
        public int Column { get; set; }

        /// <summary>
        /// Icon type identifier (e.g., "red", "blue", "bomb", "empty").
        /// Empty cells should have a distinct value like "empty" or null.
        /// </summary>
        [JsonPropertyName("iconType")]
        public string IconType { get; set; }

        [JsonPropertyName("screenPosition")]
        public Vector2Data ScreenPosition { get; set; }
    }

    /// <summary>
    /// Vector2 data for JSON serialization (Godot's Vector2 doesn't serialize well).
    /// </summary>
    public class Vector2Data
    {
        [JsonPropertyName("x")]
        public float X { get; set; }

        [JsonPropertyName("y")]
        public float Y { get; set; }

        public Vector2Data() { }

        public Vector2Data(Vector2 vec)
        {
            X = vec.X;
            Y = vec.Y;
        }

        public Vector2 ToVector2()
        {
            return new Vector2(X, Y);
        }
    }

    /// <summary>
    /// Game statistics including score, moves, and extensible custom data.
    /// </summary>
    public class GameStatistics
    {
        [JsonPropertyName("score")]
        public int Score { get; set; }

        [JsonPropertyName("remainingMoves")]
        public int RemainingMoves { get; set; }

        /// <summary>
        /// Game phase identifier (e.g., "playing", "game_over", "paused").
        /// </summary>
        [JsonPropertyName("gamePhase")]
        public string GamePhase { get; set; }

        /// <summary>
        /// Extensible custom data for game-specific statistics.
        /// Supports adding new fields without breaking existing consumers.
        /// </summary>
        [JsonPropertyName("customData")]
        public Dictionary<string, object> CustomData { get; set; }
    }
}
