using Godot;
using System;
using System.Collections.Generic;

public static class MCPTools
{
	/// <summary>
	/// Get the current scene tree as a hierarchical structure
	/// </summary>
	public static object GetSceneTree(Node root)
	{
		return BuildNodeTree(root);
	}
	
	private static Dictionary<string, object> BuildNodeTree(Node node)
	{
		var nodeData = new Dictionary<string, object>
		{
			["name"] = node.Name,
			["type"] = node.GetType().Name,
			["path"] = node.GetPath().ToString()
		};
		
		// Add position for Node2D
		if (node is Node2D node2D)
		{
			nodeData["position"] = new { x = node2D.Position.X, y = node2D.Position.Y };
			nodeData["visible"] = node2D.Visible;
		}
		
		// Add position for Control
		if (node is Control control)
		{
			nodeData["position"] = new { x = control.Position.X, y = control.Position.Y };
			nodeData["size"] = new { width = control.Size.X, height = control.Size.Y };
			nodeData["visible"] = control.Visible;
		}
		
		// Recursively build children
		var children = new List<Dictionary<string, object>>();
		foreach (Node child in node.GetChildren())
		{
			children.Add(BuildNodeTree(child));
		}
		
		if (children.Count > 0)
		{
			nodeData["children"] = children;
		}
		
		return nodeData;
	}
	
	/// <summary>
	/// Simulate a mouse click at the specified position
	/// </summary>
	public static void SimulateClick(Viewport viewport, Vector2 position)
	{
		// Create mouse button press event
		var pressEvent = new InputEventMouseButton
		{
			ButtonIndex = MouseButton.Left,
			Pressed = true,
			Position = position,
			GlobalPosition = position
		};
		
		// Create mouse button release event
		var releaseEvent = new InputEventMouseButton
		{
			ButtonIndex = MouseButton.Left,
			Pressed = false,
			Position = position,
			GlobalPosition = position
		};
		
		// Send events
		Input.ParseInputEvent(pressEvent);
		Input.ParseInputEvent(releaseEvent);
		
		GD.Print($"Simulated click at ({position.X}, {position.Y})");
	}
	
	/// <summary>
	/// Get a screenshot of the current viewport as Base64
	/// </summary>
	public static string GetScreenshot(Viewport viewport)
	{
		// Get the viewport texture
		var image = viewport.GetTexture().GetImage();
		
		// Convert to PNG
		var pngData = image.SavePngToBuffer();
		
		// Convert to Base64
		string base64 = Convert.ToBase64String(pngData);
		
		GD.Print($"Screenshot captured: {pngData.Length} bytes");
		
		return base64;
	}
}
