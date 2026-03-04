using Godot;
using OpenCvSharp;
using System;
using System.Collections.Generic;

public static class IconCounter
{
	private static Mat _template = null;
	private static bool _templateLoaded = false;
	
	/// <summary>
	/// Load the Godot icon template from project resources
	/// </summary>
	public static void LoadTemplate()
	{
		try
		{
			// Try to load the icon.png from project root
			string templatePath = "icon.png";
			
			if (!FileAccess.FileExists(templatePath))
			{
				GD.PrintErr($"Template not found: {templatePath}");
				return;
			}
			
			// Load using Godot's Image class first
			var godotImage = Image.LoadFromFile(templatePath);
			if (godotImage == null)
			{
				GD.PrintErr("Failed to load template image");
				return;
			}
			
			// Convert to PNG bytes
			byte[] pngBytes = godotImage.SavePngToBuffer();
			
			// Load into OpenCV Mat
			_template = Mat.FromImageData(pngBytes, ImreadModes.Color);
			_templateLoaded = true;
			
			GD.Print($"Template loaded successfully: {_template.Width}x{_template.Height}");
		}
		catch (Exception e)
		{
			GD.PrintErr($"Failed to load template: {e.Message}");
			_templateLoaded = false;
		}
	}
	
	/// <summary>
	/// Count Godot icons in a screenshot using template matching
	/// </summary>
	public static int CountIcons(byte[] screenshotPng)
	{
		if (!_templateLoaded || _template == null)
		{
			LoadTemplate();
			if (!_templateLoaded)
			{
				GD.PrintErr("Template not loaded, cannot count icons");
				return -1;
			}
		}
		
		try
		{
			// Decode PNG screenshot
			Mat screenshot = Mat.FromImageData(screenshotPng, ImreadModes.Color);
			
			// Template matching
			Mat result = new Mat();
			Cv2.MatchTemplate(screenshot, _template, result, TemplateMatchModes.CCoeffNormed);
			
			// Find all matches above threshold
			double threshold = 0.7; // Lower threshold for better detection
			List<OpenCvSharp.Point> matches = new List<OpenCvSharp.Point>();
			
			// Non-maximum suppression to avoid counting same icon multiple times
			int templateWidth = _template.Width;
			int templateHeight = _template.Height;
			
			for (int y = 0; y < result.Height; y++)
			{
				for (int x = 0; x < result.Width; x++)
				{
					float value = result.At<float>(y, x);
					if (value >= threshold)
					{
						// Check if this location is too close to existing matches
						bool tooClose = false;
						foreach (var match in matches)
						{
							int dx = Math.Abs(x - match.X);
							int dy = Math.Abs(y - match.Y);
							if (dx < templateWidth / 2 && dy < templateHeight / 2)
							{
								tooClose = true;
								break;
							}
						}
						
						if (!tooClose)
						{
							matches.Add(new OpenCvSharp.Point(x, y));
						}
					}
				}
			}
			
			int count = matches.Count;
			GD.Print($"OpenCV detected {count} icons (threshold: {threshold})");
			
			// Cleanup
			screenshot.Dispose();
			result.Dispose();
			
			return count;
		}
		catch (Exception e)
		{
			GD.PrintErr($"Icon counting error: {e.Message}");
			GD.PrintErr($"Stack trace: {e.StackTrace}");
			return -1;
		}
	}
	
	/// <summary>
	/// Cleanup resources
	/// </summary>
	public static void Cleanup()
	{
		if (_template != null)
		{
			_template.Dispose();
			_template = null;
		}
		_templateLoaded = false;
	}
}
