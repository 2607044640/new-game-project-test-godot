using System.Collections.Generic;
using System.Text.Json.Serialization;

/// <summary>
/// MCP Request structure
/// </summary>
public class MCPRequest
{
	[JsonPropertyName("tool")]
	public string Tool { get; set; }
	
	[JsonPropertyName("arguments")]
	public Dictionary<string, float> Arguments { get; set; } = new Dictionary<string, float>();
}

/// <summary>
/// MCP Response structure
/// </summary>
public class MCPResponse
{
	[JsonPropertyName("success")]
	public bool Success { get; set; }
	
	[JsonPropertyName("data")]
	public object Data { get; set; }
	
	[JsonPropertyName("error")]
	public string Error { get; set; }
}
