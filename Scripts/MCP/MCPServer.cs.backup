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
	
	// Screenshot task queue for thread-safe execution
	private Queue<TaskCompletionSource<string>> _screenshotQueue = new Queue<TaskCompletionSource<string>>();
	private object _queueLock = new object();
	
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
		
		// Process screenshot queue on main thread
		ProcessScreenshotQueue();
		
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
	
	private void ProcessScreenshotQueue()
	{
		TaskCompletionSource<string> tcs = null;
		
		// 1. Lock ONLY to dequeue - keeps lock fast
		lock (_queueLock)
		{
			if (_screenshotQueue.Count > 0)
			{
				tcs = _screenshotQueue.Dequeue();
				GD.Print($"Processing screenshot, remaining queue: {_screenshotQueue.Count}");
			}
		}
		
		// 2. If nothing to process, exit
		if (tcs == null)
			return;
		
		try
		{
			// 3. Heavy Godot API calls (must remain on main thread)
			var viewport = GetViewport();
			var texture = viewport.GetTexture();
			var image = texture.GetImage();
			
			GD.Print($"Image captured: {image.GetWidth()}x{image.GetHeight()}");
			
			byte[] pngBytes = image.SavePngToBuffer();
			GD.Print($"PNG buffer size: {pngBytes.Length} bytes");
			
			string base64 = Convert.ToBase64String(pngBytes);
			GD.Print($"PNG encoded: {base64.Length} chars");
			
			// Return MCP-compliant Image response
			var mcpImageResponse = new
			{
				content = new[]
				{
					new
					{
						type = "image",
						data = base64,
						mimeType = "image/png"
					}
				},
				isError = false
			};
			
			string jsonResponse = JsonSerializer.Serialize(mcpImageResponse);
			
			// 4. Use TrySetResult to safely complete without throwing
			// if the task was already canceled/timed out
			tcs.TrySetResult(jsonResponse);
		}
		catch (Exception e)
		{
			GD.PrintErr($"Screenshot error: {e.Message}");
			var errorResponse = new
			{
				content = new[]
				{
					new
					{
						type = "text",
						text = $"Screenshot failed: {e.Message}"
					}
				},
				isError = true
			};
			tcs.TrySetException(e);
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
			
			// Handle request asynchronously to avoid blocking main thread
			Task.Run(async () =>
			{
				string responseJson = await HandleMCPRequestAsync(mcpRequest);
				
				// Send HTTP response
				var httpResponse = $"HTTP/1.1 200 OK\r\n" +
				                   $"Content-Type: application/json\r\n" +
				                   $"Access-Control-Allow-Origin: *\r\n" +
				                   $"Content-Length: {responseJson.Length}\r\n" +
				                   $"\r\n" +
				                   $"{responseJson}";
				
				var responseBytes = Encoding.UTF8.GetBytes(httpResponse);
				client.PutData(responseBytes);
				
				// Close connection
				client.DisconnectFromHost();
			});
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
					
				case "get_screenshot":
					return await GetScreenshotAsync();
					
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
	
	private async Task<string> GetScreenshotAsync()
	{
		GD.Print("get_screenshot requested - queuing task");
		
		// CRITICAL: RunContinuationsAsynchronously prevents deadlocks
		var tcs = new TaskCompletionSource<string>(TaskCreationOptions.RunContinuationsAsynchronously);
		
		lock (_queueLock)
		{
			_screenshotQueue.Enqueue(tcs);
			GD.Print($"Task queued, queue size: {_screenshotQueue.Count}");
		}
		
		GD.Print("Waiting for screenshot result...");
		
		// Create a timeout token
		using var cts = new System.Threading.CancellationTokenSource(TimeSpan.FromSeconds(10));
		
		try
		{
			// Await either the task completion OR the timeout
			var completedTask = await Task.WhenAny(tcs.Task, Task.Delay(-1, cts.Token));
			
			if (completedTask == tcs.Task)
			{
				GD.Print("Screenshot completed successfully");
				return await tcs.Task;
			}
			else
			{
				GD.PrintErr("Screenshot timeout!");
				return JsonSerializer.Serialize(new
				{
					content = new[]
					{
						new
						{
							type = "text",
							text = "Screenshot timeout"
						}
					},
					isError = true
				});
			}
		}
		catch (Exception ex)
		{
			GD.PrintErr($"Exception during wait: {ex.Message}");
			return JsonSerializer.Serialize(new
			{
				content = new[]
				{
					new
					{
						type = "text",
						text = $"Error: {ex.Message}"
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
