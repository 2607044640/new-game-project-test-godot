# 研究轮次 3：Shader、存档系统和相机坐标

## Shader 和材质

### 关键发现

1. **ShaderMaterial 基础**
```csharp
// 创建 ShaderMaterial
var material = new ShaderMaterial();
material.Shader = GD.Load<Shader>("res://Shaders/MyShader.gdshader");

// 应用到 Sprite
sprite.Material = material;

// 设置 Shader 参数
material.SetShaderParameter("my_color", Colors.Red);
material.SetShaderParameter("intensity", 1.5f);
```

2. **Modulate 属性**
```csharp
// 修改节点颜色（乘法混合）
sprite.Modulate = new Color(1, 0, 0, 0.5f); // 红色半透明

// Self Modulate（不影响子节点）
sprite.SelfModulate = Colors.Blue;

// CanvasModulate（影响整个画布）
var canvasModulate = new CanvasModulate();
canvasModulate.Color = new Color(0.8f, 0.8f, 1.0f); // 蓝色调
AddChild(canvasModulate);
```

3. **简单 Shader 示例**
```gdshader
// res://Shaders/Flash.gdshader
shader_type canvas_item;

uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float flash_intensity : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    COLOR = mix(tex_color, flash_color, flash_intensity);
    COLOR.a = tex_color.a; // 保持原始透明度
}
```

4. **在 C# 中使用**
```csharp
public partial class FlashEffect : Sprite2D
{
    private ShaderMaterial _material;
    
    public override void _Ready()
    {
        _material = (ShaderMaterial)Material;
    }
    
    public async void Flash()
    {
        _material.SetShaderParameter("flash_intensity", 1.0f);
        await ToSignal(GetTree().CreateTimer(0.1), Timer.SignalName.Timeout);
        _material.SetShaderParameter("flash_intensity", 0.0f);
    }
}
```

## 存档系统

### 关键发现

1. **JSON 存档（推荐用于游戏数据）**
```csharp
public partial class SaveSystem : Node
{
    private const string SavePath = "user://savegame.json";
    
    public class SaveData
    {
        public int Level { get; set; }
        public int Score { get; set; }
        public Vector2 PlayerPosition { get; set; }
        public Dictionary<string, bool> UnlockedItems { get; set; }
    }
    
    public void SaveGame(SaveData data)
    {
        var json = Json.Stringify(data);
        var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Write);
        
        if (file == null)
        {
            GD.PrintErr($"无法创建存档文件: {FileAccess.GetOpenError()}");
            return;
        }
        
        file.StoreString(json);
        file.Close();
        GD.Print("游戏已保存");
    }
    
    public SaveData LoadGame()
    {
        if (!FileAccess.FileExists(SavePath))
        {
            GD.Print("存档文件不存在");
            return new SaveData();
        }
        
        var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Read);
        if (file == null)
        {
            GD.PrintErr($"无法读取存档文件: {FileAccess.GetOpenError()}");
            return new SaveData();
        }
        
        var json = file.GetAsText();
        file.Close();
        
        var result = Json.ParseString(json);
        if (result.VariantType == Variant.Type.Dictionary)
        {
            var dict = result.AsGodotDictionary();
            return new SaveData
            {
                Level = dict["Level"].AsInt32(),
                Score = dict["Score"].AsInt32(),
                // ... 手动解析其他字段
            };
        }
        
        return new SaveData();
    }
}
```

2. **ConfigFile 存档（推荐用于设置）**
```csharp
public partial class SettingsManager : Node
{
    private const string ConfigPath = "user://settings.cfg";
    private ConfigFile _config = new();
    
    public void SaveSettings()
    {
        _config.SetValue("audio", "master_volume", 0.8f);
        _config.SetValue("audio", "music_volume", 0.6f);
        _config.SetValue("video", "fullscreen", true);
        _config.SetValue("video", "vsync", true);
        
        var error = _config.Save(ConfigPath);
        if (error != Error.Ok)
        {
            GD.PrintErr($"保存设置失败: {error}");
        }
    }
    
    public void LoadSettings()
    {
        var error = _config.Load(ConfigPath);
        if (error != Error.Ok)
        {
            GD.Print("设置文件不存在，使用默认值");
            return;
        }
        
        float masterVolume = (float)_config.GetValue("audio", "master_volume", 1.0f);
        float musicVolume = (float)_config.GetValue("audio", "music_volume", 1.0f);
        bool fullscreen = (bool)_config.GetValue("video", "fullscreen", false);
        
        // 应用设置
        AudioServer.SetBusVolumeDb(0, Mathf.LinearToDb(masterVolume));
    }
}
```

3. **二进制存档（用于大量数据）**
```csharp
public void SaveBinary(SaveData data)
{
    var file = FileAccess.Open("user://savegame.dat", FileAccess.ModeFlags.Write);
    
    file.Store32((uint)data.Level);
    file.Store32((uint)data.Score);
    file.StoreFloat(data.PlayerPosition.X);
    file.StoreFloat(data.PlayerPosition.Y);
    
    file.Close();
}

public SaveData LoadBinary()
{
    var file = FileAccess.Open("user://savegame.dat", FileAccess.ModeFlags.Read);
    
    var data = new SaveData
    {
        Level = (int)file.Get32(),
        Score = (int)file.Get32(),
        PlayerPosition = new Vector2(file.GetFloat(), file.GetFloat())
    };
    
    file.Close();
    return data;
}
```

4. **加密存档**
```csharp
public void SaveEncrypted(SaveData data, string password)
{
    var json = Json.Stringify(data);
    var file = FileAccess.OpenEncrypted("user://savegame.enc", 
        FileAccess.ModeFlags.Write, password.ToUtf8Buffer());
    
    file.StoreString(json);
    file.Close();
}

public SaveData LoadEncrypted(string password)
{
    var file = FileAccess.OpenEncrypted("user://savegame.enc", 
        FileAccess.ModeFlags.Read, password.ToUtf8Buffer());
    
    var json = file.GetAsText();
    file.Close();
    
    // 解析 JSON...
}
```

## Camera2D 和坐标转换

### 关键发现

1. **屏幕坐标 vs 世界坐标**
```csharp
public partial class CoordinateExample : Node2D
{
    public override void _Input(InputEvent @event)
    {
        if (@event is InputEventMouseButton mouseButton)
        {
            // 屏幕坐标（相对于窗口）
            Vector2 screenPos = mouseButton.Position;
            
            // 世界坐标（考虑相机变换）
            Vector2 worldPos = GetGlobalMousePosition();
            
            GD.Print($"屏幕: {screenPos}, 世界: {worldPos}");
        }
    }
}
```

2. **Camera2D 坐标转换**
```csharp
public partial class CameraHelper : Camera2D
{
    // 屏幕坐标转世界坐标
    public Vector2 ScreenToWorld(Vector2 screenPos)
    {
        var canvasTransform = GetCanvasTransform();
        return canvasTransform.AffineInverse() * screenPos;
    }
    
    // 世界坐标转屏幕坐标
    public Vector2 WorldToScreen(Vector2 worldPos)
    {
        var canvasTransform = GetCanvasTransform();
        return canvasTransform * worldPos;
    }
    
    // 获取相机可见区域（世界坐标）
    public Rect2 GetVisibleRect()
    {
        var viewportSize = GetViewportRect().Size;
        var zoom = Zoom;
        
        var size = viewportSize / zoom;
        var position = GlobalPosition - size / 2;
        
        return new Rect2(position, size);
    }
    
    // 检查点是否在相机视野内
    public bool IsPointVisible(Vector2 worldPos)
    {
        return GetVisibleRect().HasPoint(worldPos);
    }
}
```

3. **Camera2D 平滑跟随**
```csharp
public partial class FollowCamera : Camera2D
{
    [Export] public Node2D Target;
    [Export] public float SmoothSpeed = 5.0f;
    [Export] public Vector2 Offset = Vector2.Zero;
    
    public override void _Process(double delta)
    {
        if (Target == null) return;
        
        var targetPos = Target.GlobalPosition + Offset;
        GlobalPosition = GlobalPosition.Lerp(targetPos, SmoothSpeed * (float)delta);
    }
}
```

4. **Camera2D 限制区域**
```csharp
public partial class BoundedCamera : Camera2D
{
    public override void _Ready()
    {
        // 设置相机边界
        LimitLeft = 0;
        LimitTop = 0;
        LimitRight = 2000;
        LimitBottom = 1500;
        
        // 启用平滑
        PositionSmoothingEnabled = true;
        PositionSmoothingSpeed = 5.0f;
    }
}
```

5. **Viewport 坐标系统**
```csharp
// 获取 Viewport 大小
Vector2 viewportSize = GetViewportRect().Size;

// 获取鼠标在 Viewport 中的位置
Vector2 mousePos = GetViewport().GetMousePosition();

// 获取 Viewport 变换
Transform2D viewportTransform = GetViewport().GetCanvasTransform();
```

## 需要添加到文档的内容

1. ShaderMaterial 使用指南
2. Modulate 和颜色混合
3. 完整的存档系统示例（JSON、ConfigFile、二进制）
4. 加密存档
5. Camera2D 坐标转换
6. 相机跟随和边界限制
7. Viewport 坐标系统
