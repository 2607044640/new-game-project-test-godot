using Godot;
using System;
using System.Text;
using System.Text.Json;
using System.Collections.Generic;
using System.Threading.Tasks;

public partial class MCPServer : Node
{
	private TcpServer _server;
	private List<StreamPeerTcp> _clients = new List<StreamPeerTcp>();
	private ushort _port = 8765;
	
	// Queue for pending requests to process on main thread
	private Queue<(MCPRequest request, StreamPeerTcp client)> _pendingRequests = new Queue<(MCPRequest, StreamPeerTcp)>();
	private object _requestLock = new object();
	
	public override void _Ready()
	{
		GD.Print("MCP Server initializing...");
		StartServer();
	}
	
	public override void _ExitTree()
	{
		StopServer();
	}
	
	private void StartServer()
	{
		GD.Print("MCP Server _Ready called");
		try
		{
			GD.Print("Creating TcpServer...");
			_server = new TcpServer();
			GD.Print($"Calling Listen on port {_port}...");
			var error = _server.Listen(_port);
			
			GD.Print($"Listen returned: {error}");
			if (error == Error.Ok)
			{
				GD.Print($"MCP Server started on port {_port}");
			}
			else
			{
				GD.PrintErr($"Failed to start MCP Server: {error}");
			}
		}
		catch (Exception e)
		{
			GD.PrintErr($"Failed to start MCP Server: {e.Message}");
			GD.PrintErr($"Stack trace: {e.StackTrace}");
		}
	}
	
	public override void _Process(double delta)
	{
		if (_server == null || !_server.IsListening())
			return;
		
		// Process pending requests on main thread
		ProcessPendingRequests();
		
		// Accept new connections
		if (_server.IsConnectionAvailable())
		{
			var client = _server.TakeConnection();
			_clients.Add(client);
			GD.Print("New MCP client connected");
		}
		
		// Process existing clients
		for (int i = _clients.Count - 1; i >= 0; i--)
		{
			var client = _clients[i];
			
			if (client.GetStatus() != StreamPeerTcp.Status.Connected)
			{
				_clients.RemoveAt(i);
				continue;
			}
			
			if (client.GetAvailableBytes() > 0)
			{
				ProcessClient(client);
			}
		}
	}
	
	private async void ProcessPendingRequests()
	{
		(MCPRequest request, StreamPeerTcp client) pending;
		
		lock (_requestLock)
		{
			if (_pendingRequests.Count == 0)
				return;
			pending = _pendingRequests.Dequeue();
		}
		
		try
		{
			string responseJson = await HandleMCPRequestAsync(pending.request);
			
			// Send HTTP response
			var httpResponse = $"HTTP/1.1 200 OK\r\n" +
			                   $"Content-Type: application/json\r\n" +
			                   $"Access-Control-Allow-Origin: *\r\n" +
			                   $"Content-Length: {responseJson.Length}\r\n" +
			                   $"\r\n" +
			                   $"{responseJson}";
			
			var responseBytes = Encoding.UTF8.GetBytes(httpResponse);
			pending.client.PutData(responseBytes);
			
			// Close connection
			pending.client.DisconnectFromHost();
		}
		catch (Exception e)
		{
			GD.PrintErr($"Error handling request: {e.Message}");
		}
	}
	
	private void ProcessClient(StreamPeerTcp client)
	{
		try
		{
			// Read HTTP request
			var requestBytes = client.GetData((int)client.GetAvailableBytes());
			var error = requestBytes[0].As<Error>();
			if (error != Error.Ok)
				return;
			
			string request = Encoding.UTF8.GetString(requestBytes[1].As<byte[]>());
			
			// Parse HTTP request
			var lines = request.Split('\n');
			if (lines.Length == 0)
				return;
			
			// Find JSON body (after empty line)
			string jsonBody = "";
			bool foundEmptyLine = false;
			foreach (var line in lines)
			{
				if (foundEmptyLine)
				{
					jsonBody += line;
				}
				else if (string.IsNullOrWhiteSpace(line))
				{
					foundEmptyLine = true;
				}
			}
			
			if (string.IsNullOrEmpty(jsonBody))
				return;
			
			GD.Print($"MCP Request: {jsonBody}");
			
			// Parse MCP request
			var mcpRequest = JsonSerializer.Deserialize<MCPRequest>(jsonBody);
			
			// Enqueue request to be processed on main thread
			lock (_requestLock)
			{
				_pendingRequests.Enqueue((mcpRequest, client));
			}
		}
		catch (Exception e)
		{
			GD.PrintErr($"Error processing client: {e.Message}");
		}
	}

	private async Task<string> HandleMCPRequestAsync(MCPRequest request)
	{
		try
		{
			switch (request.Tool)
			{
				case "get_scene_tree":
					var sceneData = MCPTools.GetSceneTree(GetTree().Root);
					return JsonSerializer.Serialize(new
					{
						content = new[]
						{
							new
							{
								type = "text",
								text = JsonSerializer.Serialize(sceneData)
							}
						},
						isError = false
					});
					
				case "simulate_click":
					var x = request.Arguments.ContainsKey("x") ? request.Arguments["x"] : 0f;
					var y = request.Arguments.ContainsKey("y") ? request.Arguments["y"] : 0f;
					MCPTools.SimulateClick(GetViewport(), new Vector2(x, y));
					return JsonSerializer.Serialize(new
					{
						content = new[]
						{
							new
							{
								type = "text",
								text = $"Clicked at ({x}, {y})"
							}
						},
						isError = false
					});
					
				case "get_game_state":
					return await HandleGetGameStateAsync();
					
				default:
					return JsonSerializer.Serialize(new
					{
						content = new[]
						{
							new
							{
								type = "text",
								text = $"Unknown tool: {request.Tool}"
							}
						},
						isError = true
					});
			}
		}
		catch (Exception e)
		{
			GD.PrintErr($"Tool execution error: {e.Message}");
			return JsonSerializer.Serialize(new
			{
				content = new[]
				{
					new
					{
						type = "text",
						text = $"Error: {e.Message}"
					}
				},
				isError = true
			});
		}
	}
	
	private async Task<string> HandleGetGameStateAsync()
	{
		try
		{
			// Get the GameStateCapture node from the scene
			var capture = GetNode<GameStateCaptureSystem.GameStateCapture>("../GameStateCapture");
			if (capture == null)
			{
				throw new InvalidOperationException("GameStateCapture node not found in scene");
			}
			
			// Capture game state
			var gameState = await capture.CaptureStateAsync();
			
			// Serialize to JSON
			var gameStateJson = JsonSerializer.Serialize(gameState);
			
			// Return MCP response with both text and image
			return JsonSerializer.Serialize(new
			{
				content = new object[]
				{
					new
					{
						type = "text",
						text = gameStateJson
					},
					new
					{
						type = "image",
						data = gameState.Screenshot?.Base64 ?? "",
						mimeType = "image/png"
					}
				},
				isError = false
			});
		}
		catch (Exception e)
		{
			GD.PrintErr($"get_game_state error: {e.Message}");
			GD.PrintErr($"Stack trace: {e.StackTrace}");
			return JsonSerializer.Serialize(new
			{
				content = new[]
				{
					new
					{
						type = "text",
						text = $"Failed to capture game state: {e.Message}"
					}
				},
				isError = true
			});
		}
	}
	
	private void StopServer()
	{
		if (_server != null && _server.IsListening())
		{
			_server.Stop();
			GD.Print("MCP Server stopped");
		}
		
		foreach (var client in _clients)
		{
			client.DisconnectFromHost();
		}
		_clients.Clear();
	}
}
