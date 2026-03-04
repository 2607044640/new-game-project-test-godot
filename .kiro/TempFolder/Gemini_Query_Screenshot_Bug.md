# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows
- Architecture: MCP Server running in Godot, Python client calling HTTP endpoint

## Problem
Screenshot capture in Godot C# MCP Server times out. Image is captured successfully (1152x648) and PNG buffer is created (40533 bytes), but the response never reaches the HTTP client. The TaskCompletionSource.SetResult() appears to not wake up the waiting thread.

## What I Tried

### Attempt 1: Increased timeout from 5s to 10s
- Result: Still timeout. Logs show "Screenshot timeout!" before "PNG buffer size: 40533 bytes"

### Attempt 2: Added extensive debug logging
- Result: Discovered execution order issue - Wait() times out before ProcessScreenshotQueue() completes
- Logs show image captured and PNG created, but "PNG encoded" message never appears

### Attempt 3: Added try-catch around Base64 conversion
- Result: No exception logged. Code appears to hang after "Converting to Base64..." log message

## Current Code

### ProcessClient (runs in background thread from TcpServer)
```csharp
case "get_screenshot":
    GD.Print("get_screenshot requested - queuing task");
    var tcs = new TaskCompletionSource<string>();
    lock (_queueLock)
    {
        _screenshotQueue.Enqueue(tcs);
        GD.Print($"Task queued, queue size: {_screenshotQueue.Count}");
    }
    GD.Print("Waiting for screenshot result...");
    if (tcs.Task.Wait(TimeSpan.FromSeconds(10)))  // BLOCKS HERE
    {
        GD.Print("Screenshot completed successfully");
        return tcs.Task.Result;
    }
    else
    {
        GD.PrintErr("Screenshot timeout!");
        return JsonSerializer.Serialize(new { /* timeout response */ });
    }
```

### ProcessScreenshotQueue (runs in main thread from _Process)
```csharp
public override void _Process(double delta)
{
    if (_server == null || !_server.IsListening())
        return;
    
    ProcessScreenshotQueue();  // Called every frame
    // ... handle new connections
}

private void ProcessScreenshotQueue()
{
    lock (_queueLock)
    {
        while (_screenshotQueue.Count > 0)
        {
            GD.Print($"Processing screenshot from queue (count: {_screenshotQueue.Count})");
            var tcs = _screenshotQueue.Dequeue();
            try
            {
                var viewport = GetViewport();
                var texture = viewport.GetTexture();
                var image = texture.GetImage();
                GD.Print($"Image captured: {image.GetWidth()}x{image.GetHeight()}");
                
                GD.Print("Calling SavePngToBuffer...");
                byte[] pngBytes = image.SavePngToBuffer();
                GD.Print($"PNG buffer size: {pngBytes.Length} bytes");
                
                GD.Print("Converting to Base64...");
                string base64 = Convert.ToBase64String(pngBytes);  // HANGS HERE?
                GD.Print($"PNG encoded: {base64.Length} chars");
                
                var mcpImageResponse = new { /* MCP format */ };
                string jsonResponse = JsonSerializer.Serialize(mcpImageResponse);
                tcs.SetResult(jsonResponse);  // Should wake up Wait()
            }
            catch (Exception e)
            {
                GD.PrintErr($"Screenshot error: {e.Message}");
                tcs.SetException(e);
            }
        }
    }
}
```

## Logs
```
nicework!
MCP Server initializing...
MCP Server _Ready called
Creating TcpServer...
Calling Listen on port 8765...
Listen returned: Ok
New MCP client connected
MCP Request: {"tool": "get_screenshot", "arguments": {}}
get_screenshot requested - queuing task
Task queued, queue size: 1
Waiting for screenshot result...
Screenshot timeout!
Processing screenshot from queue (count: 1)
Getting viewport...
Getting texture...
Getting image...
Image captured: 1152x648
Calling SavePngToBuffer...
PNG buffer size: 40533 bytes
Converting to Base64...
```

Note: "PNG encoded" message never appears. "Screenshot timeout!" appears BEFORE processing completes.

## Expected Behavior
1. HTTP request comes in on background thread
2. Task queued for main thread
3. Main thread processes queue in _Process()
4. tcs.SetResult() wakes up waiting thread
5. Response sent to HTTP client

## Actual Behavior
1. Task queued successfully
2. Wait() times out after 10 seconds
3. Main thread processes queue AFTER timeout
4. Image captured and PNG created successfully
5. Code hangs or stops after "Converting to Base64..." log
6. No response sent to client

## Questions
1. Why does ProcessScreenshotQueue() execute AFTER the Wait() timeout, even though _Process() should run every frame?
2. Why does the code stop/hang after "Converting to Base64..." without error or completion?
3. Is TaskCompletionSource thread-safe for cross-thread signaling in Godot C#?
4. Should I use a different synchronization mechanism (Semaphore, ManualResetEvent, async/await)?
5. Could the lock on _queueLock be causing a deadlock somehow?
