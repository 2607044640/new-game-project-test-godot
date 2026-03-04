---
inclusion: manual
---

# Godot C# 开发参考

<core_architecture>
## 核心架构

### Node 系统
Godot 使用 Node 树结构组织游戏对象。每个场景是一个 Node 树，游戏是场景树的集合。

**获取节点（类型安全）：**
```csharp
// 使用泛型获取节点
Button myButton = GetNode<Button>("ButtonName");

// 避免空引用
Button myButton = GetNodeOrNull<Button>("ButtonName");
if (myButton != null) { /* 使用 */ }

// 获取父节点
Node parent = GetParent();

// 获取子节点
Node child = GetChild(0);
```

### Node 生命周期
```csharp
public override void _EnterTree()
{
    // 节点添加到场景树时调用（从根到叶）
    // 用于：初始化不依赖子节点的内容
}

public override void _Ready()
{
    // 节点及其子节点准备就绪时调用（从叶到根）
    // 用于：获取子节点引用、初始化游戏逻辑
}

public override void _Process(double delta)
{
    // 每帧调用（帧率不固定）
    // 用于：视觉更新、UI 逻辑、非物理相关的游戏逻辑
}

public override void _PhysicsProcess(double delta)
{
    // 物理帧调用（固定时间步长，默认 60 FPS）
    // 用于：物理计算、角色移动、碰撞检测
}

public override void _ExitTree()
{
    // 节点从场景树移除时调用
    // 用于：清理资源、断开信号连接
}
```

**控制生命周期：**
```csharp
SetProcess(false);        // 停止 _Process
SetPhysicsProcess(false); // 停止 _PhysicsProcess
```
</core_architecture>

<global_management>
## 全局管理系统（Autoload/Singleton）

Godot 的 Autoload 系统类似 UE 的 Subsystem 或 Unity 的 GameManager，用于创建全局可访问的单例。

### 创建 Autoload
1. 创建 C# 脚本（如 `GameManager.cs`）
2. Project Settings > Autoload > 添加脚本
3. 设置 Node Name（如 "GameManager"）

### Autoload 脚本示例
```csharp
// Scripts/GameManager.cs
using Godot;

public partial class GameManager : Node
{
    // 单例实例（可选，用于类型安全访问）
    public static GameManager Instance { get; private set; }
    
    // 全局数据
    public int Score { get; set; }
    public int Level { get; set; }
    
    public override void _Ready()
    {
        Instance = this;
    }
    
    public void SaveGame()
    {
        // 保存逻辑
    }
}
```

### 访问 Autoload
```csharp
// 方法 1：通过单例实例（推荐）
GameManager.Instance.Score += 10;

// 方法 2：通过场景树
var gm = GetNode<GameManager>("/root/GameManager");
gm.Score += 10;
```
</global_management>

<data_management>
## 数据管理系统

### Resource（数据容器）
Resource 是 Godot 的数据容器，类似 UE 的 DataAsset。可序列化、可在编辑器中编辑。

**创建自定义 Resource：**
```csharp
// Scripts/Data/ItemData.cs
using Godot;

[GlobalClass] // 使其在编辑器中可见
public partial class ItemData : Resource
{
    [Export] public string ItemName { get; set; }
    [Export] public int ItemId { get; set; }
    [Export] public Texture2D Icon { get; set; }
    [Export] public int Price { get; set; }
}
```

**使用 Resource：**
```csharp
// 在编辑器中分配
[Export] public ItemData MyItem { get; set; }

// 代码加载
ItemData item = GD.Load<ItemData>("res://Data/Items/Sword.tres");
```

### CSV/Excel 数据导入

**方法 1：CSV 文件直接读取**
```csharp
// Scripts/Data/DataLoader.cs
using Godot;
using System.Collections.Generic;

public partial class DataLoader : Node
{
    public static Dictionary<int, ItemData> LoadItemsFromCSV(string path)
    {
        var items = new Dictionary<int, ItemData>();
        var file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
        
        if (file == null)
        {
            GD.PrintErr($"无法打开文件: {path}");
            return items;
        }
        
        // 跳过标题行
        file.GetCsvLine();
        
        while (!file.EofReached())
        {
            var line = file.GetCsvLine();
            if (line.Length < 4) continue;
            
            var item = new ItemData
            {
                ItemId = line[0].ToInt(),
                ItemName = line[1],
                Price = line[2].ToInt(),
                // Icon 路径在 CSV 中，需要加载
                Icon = GD.Load<Texture2D>(line[3])
            };
            
            items[item.ItemId] = item;
        }
        
        file.Close();
        return items;
    }
}
```

**CSV 文件格式示例（res://Data/Items.csv）：**
```csv
ItemId,ItemName,Price,IconPath
1,剑,100,res://Assets/Icons/sword.png
2,盾,80,res://Assets/Icons/shield.png
3,药水,20,res://Assets/Icons/potion.png
```

**方法 2：使用 Resource 生成器（推荐）**
```csharp
// Scripts/Tools/ResourceGenerator.cs
#if TOOLS
using Godot;
using System.IO;

[Tool]
public partial class ResourceGenerator : EditorScript
{
    public override void _Run()
    {
        GenerateItemResources("res://Data/Items.csv", "res://Data/Items/");
    }
    
    private void GenerateItemResources(string csvPath, string outputDir)
    {
        var file = FileAccess.Open(csvPath, FileAccess.ModeFlags.Read);
        if (file == null) return;
        
        // 跳过标题
        file.GetCsvLine();
        
        while (!file.EofReached())
        {
            var line = file.GetCsvLine();
            if (line.Length < 4) continue;
            
            var item = new ItemData
            {
                ItemId = line[0].ToInt(),
                ItemName = line[1],
                Price = line[2].ToInt(),
                Icon = GD.Load<Texture2D>(line[3])
            };
            
            // 保存为 .tres 文件
            string savePath = $"{outputDir}{item.ItemName}.tres";
            ResourceSaver.Save(item, savePath);
            GD.Print($"生成: {savePath}");
        }
        
        file.Close();
    }
}
#endif
```

**使用方法：**
1. 创建 CSV 文件
2. 在编辑器中：File > Run Script > 选择 ResourceGenerator.cs
3. 自动生成 .tres 资源文件


### JSON 数据管理
```csharp
// 保存数据
public void SaveToJson(string path, object data)
{
    var json = Json.Stringify(data);
    var file = FileAccess.Open(path, FileAccess.ModeFlags.Write);
    file.StoreString(json);
    file.Close();
}

// 加载数据
public T LoadFromJson<T>(string path) where T : new()
{
    var file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
    if (file == null) return new T();
    
    var json = file.GetAsText();
    file.Close();
    
    var result = Json.ParseString(json);
    return result.As<T>();
}
```
</data_management>

<signals>
## 信号系统（Signals）

信号是 Godot 的事件系统，用于解耦通信。

### 声明和发射信号
```csharp
public partial class Player : Node2D
{
    // 声明信号
    [Signal]
    public delegate void HealthChangedEventHandler(int newHealth);
    
    [Signal]
    public delegate void DiedEventHandler();
    
    private int _health = 100;
    
    public void TakeDamage(int damage)
    {
        _health -= damage;
        
        // 发射信号
        EmitSignal(SignalName.HealthChanged, _health);
        
        if (_health <= 0)
        {
            EmitSignal(SignalName.Died);
        }
    }
}
```

### 连接信号
```csharp
// 方法 1：使用 += 操作符（推荐）
player.HealthChanged += OnPlayerHealthChanged;
player.Died += OnPlayerDied;

private void OnPlayerHealthChanged(int newHealth)
{
    GD.Print($"玩家生命值: {newHealth}");
}

private void OnPlayerDied()
{
    GD.Print("玩家死亡");
}

// 方法 2：使用 Connect
player.Connect(Player.SignalName.HealthChanged, 
    Callable.From<int>(OnPlayerHealthChanged));

// 断开信号（避免内存泄漏）
player.HealthChanged -= OnPlayerHealthChanged;
```

### Lambda 表达式连接
```csharp
// 带参数
button.Pressed += () => OnButtonPressed(itemId);

// 注意：Lambda 无法直接断开，需要保存引用
Action callback = () => OnButtonPressed(itemId);
button.Pressed += callback;
// 断开时
button.Pressed -= callback;
```
</signals>

<scene_management>
## 场景管理

### 加载和实例化场景
```csharp
// 加载 PackedScene
PackedScene scene = GD.Load<PackedScene>("res://Scenes/Enemy.tscn");

// 实例化
Node instance = scene.Instantiate();

// 类型安全实例化
Enemy enemy = scene.Instantiate<Enemy>();

// 添加到场景树
AddChild(enemy);

// 设置位置（如果是 Node2D）
if (enemy is Node2D node2D)
{
    node2D.Position = new Vector2(100, 100);
}
```

### 切换场景
```csharp
// 方法 1：使用 SceneTree
GetTree().ChangeSceneToFile("res://Scenes/MainMenu.tscn");

// 方法 2：使用 PackedScene
PackedScene nextScene = GD.Load<PackedScene>("res://Scenes/Level1.tscn");
GetTree().ChangeSceneToPacked(nextScene);
```

### 场景管理器示例
```csharp
// Scripts/SceneManager.cs (Autoload)
public partial class SceneManager : Node
{
    public static SceneManager Instance { get; private set; }
    
    [Export] public PackedScene MainMenu { get; set; }
    [Export] public PackedScene GameScene { get; set; }
    
    public override void _Ready()
    {
        Instance = this;
    }
    
    public void LoadScene(string scenePath)
    {
        GetTree().ChangeSceneToFile(scenePath);
    }
    
    public void LoadMainMenu()
    {
        GetTree().ChangeSceneToPacked(MainMenu);
    }
}
```
</scene_management>

<input_handling>
## 输入处理

### Input Actions（推荐）
在 Project Settings > Input Map 中定义动作。

```csharp
public override void _Process(double delta)
{
    // 检查动作是否按下
    if (Input.IsActionPressed("move_right"))
    {
        Position += new Vector2(speed * (float)delta, 0);
    }
    
    // 检查动作是否刚按下（单次触发）
    if (Input.IsActionJustPressed("jump"))
    {
        Jump();
    }
    
    // 检查动作是否刚释放
    if (Input.IsActionJustReleased("fire"))
    {
        StopFiring();
    }
    
    // 获取动作强度（0.0 到 1.0，用于手柄）
    float strength = Input.GetActionStrength("accelerate");
}
```

### 直接输入检测
```csharp
public override void _Input(InputEvent @event)
{
    // 鼠标按钮
    if (@event is InputEventMouseButton mouseButton)
    {
        if (mouseButton.ButtonIndex == MouseButton.Left && mouseButton.Pressed)
        {
            GD.Print($"左键点击位置: {mouseButton.Position}");
        }
    }
    
    // 鼠标移动
    if (@event is InputEventMouseMotion mouseMotion)
    {
        GD.Print($"鼠标移动: {mouseMotion.Relative}");
    }
    
    // 键盘
    if (@event is InputEventKey key)
    {
        if (key.Keycode == Key.Escape && key.Pressed)
        {
            GetTree().Quit();
        }
    }
}

// 未处理的输入（UI 未消费的输入）
public override void _UnhandledInput(InputEvent @event)
{
    // 游戏逻辑输入处理
}
```

### 获取鼠标位置
```csharp
// 屏幕坐标
Vector2 mousePos = GetViewport().GetMousePosition();

// 世界坐标（2D）
Vector2 worldPos = GetGlobalMousePosition();
```
</input_handling>

<collision_detection>
## 碰撞检测

### Area2D（触发区域）
```csharp
public partial class Coin : Area2D
{
    public override void _Ready()
    {
        // 连接信号
        BodyEntered += OnBodyEntered;
        BodyExited += OnBodyExited;
    }
    
    private void OnBodyEntered(Node2D body)
    {
        if (body is Player player)
        {
            player.CollectCoin();
            QueueFree(); // 删除自己
        }
    }
    
    private void OnBodyExited(Node2D body)
    {
        GD.Print($"{body.Name} 离开区域");
    }
    
    // 检查重叠
    public bool IsPlayerInRange()
    {
        var bodies = GetOverlappingBodies();
        foreach (var body in bodies)
        {
            if (body is Player)
                return true;
        }
        return false;
    }
}
```

### CharacterBody2D（角色物理）
```csharp
public partial class Player : CharacterBody2D
{
    [Export] public float Speed = 300.0f;
    [Export] public float JumpVelocity = -400.0f;
    
    public override void _PhysicsProcess(double delta)
    {
        Vector2 velocity = Velocity;
        
        // 重力
        if (!IsOnFloor())
        {
            velocity.Y += gravity * (float)delta;
        }
        
        // 跳跃
        if (Input.IsActionJustPressed("jump") && IsOnFloor())
        {
            velocity.Y = JumpVelocity;
        }
        
        // 移动
        float direction = Input.GetAxis("move_left", "move_right");
        velocity.X = direction * Speed;
        
        Velocity = velocity;
        MoveAndSlide();
        
        // 检查碰撞
        for (int i = 0; i < GetSlideCollisionCount(); i++)
        {
            var collision = GetSlideCollision(i);
            GD.Print($"碰撞: {collision.GetCollider()}");
        }
    }
}
```

### RayCast2D（射线检测）
```csharp
public partial class RaycastExample : Node2D
{
    private RayCast2D _raycast;
    
    public override void _Ready()
    {
        _raycast = GetNode<RayCast2D>("RayCast2D");
        _raycast.Enabled = true;
    }
    
    public override void _Process(double delta)
    {
        if (_raycast.IsColliding())
        {
            var collider = _raycast.GetCollider();
            var point = _raycast.GetCollisionPoint();
            GD.Print($"射线击中: {collider} 位置: {point}");
        }
    }
}
```
</collision_detection>

<animation>
## 动画系统

### Tween（代码动画）
```csharp
public partial class TweenExample : Node2D
{
    public void AnimatePosition()
    {
        // 创建 Tween
        Tween tween = CreateTween();
        
        // 移动到目标位置（2 秒）
        tween.TweenProperty(this, "position", new Vector2(500, 300), 2.0);
        
        // 链式调用
        tween.TweenProperty(this, "rotation", Mathf.Pi, 1.0);
        tween.TweenProperty(this, "scale", Vector2.One * 2, 0.5);
    }
    
    public void ComplexAnimation()
    {
        Tween tween = CreateTween();
        
        // 设置缓动函数
        tween.SetTrans(Tween.TransitionType.Bounce);
        tween.SetEase(Tween.EaseType.Out);
        
        // 并行动画
        tween.SetParallel(true);
        tween.TweenProperty(this, "position:x", 500, 1.0);
        tween.TweenProperty(this, "position:y", 300, 1.0);
        
        // 回调
        tween.TweenCallback(Callable.From(() => GD.Print("动画完成")));
    }
    
    public void FadeOut()
    {
        Tween tween = CreateTween();
        tween.TweenProperty(this, "modulate:a", 0.0, 1.0);
        tween.TweenCallback(Callable.From(QueueFree));
    }
}
```

### AnimationPlayer
```csharp
public partial class AnimatedCharacter : Node2D
{
    private AnimationPlayer _animPlayer;
    
    public override void _Ready()
    {
        _animPlayer = GetNode<AnimationPlayer>("AnimationPlayer");
    }
    
    public void PlayAnimation(string animName)
    {
        _animPlayer.Play(animName);
    }
    
    public void OnAnimationFinished(string animName)
    {
        GD.Print($"动画完成: {animName}");
    }
}
```
</animation>

<export_attributes>
## Export 属性（Inspector 变量）

```csharp
public partial class ExportExample : Node
{
    // 基本类型
    [Export] public int Health = 100;
    [Export] public float Speed = 5.0f;
    [Export] public string PlayerName = "Player";
    [Export] public bool IsAlive = true;
    
    // 范围限制
    [Export(PropertyHint.Range, "0,100,1")] public int Percentage = 50;
    [Export(PropertyHint.Range, "0,10,0.1")] public float Volume = 1.0f;
    
    // 文件路径
    [Export(PropertyHint.File, "*.png,*.jpg")] public string TexturePath;
    [Export(PropertyHint.Dir)] public string FolderPath;
    
    // 枚举
    public enum WeaponType { Sword, Bow, Staff }
    [Export] public WeaponType CurrentWeapon = WeaponType.Sword;
    
    // 数组
    [Export] public int[] Scores = { 10, 20, 30 };
    [Export] public string[] Names = { "Alice", "Bob" };
    
    // Godot 类型
    [Export] public PackedScene EnemyScene;
    [Export] public Texture2D Icon;
    [Export] public AudioStream Sound;
    
    // Resource
    [Export] public ItemData Item;
    
    // Node 引用
    [Export] public Node2D Target;
    
    // 多行文本
    [Export(PropertyHint.MultilineText)] public string Description;
    
    // 颜色
    [Export] public Color PlayerColor = Colors.Red;
}
```
</export_attributes>

<utilities>
## 实用工具

### 定时器
```csharp
public partial class TimerExample : Node
{
    private Timer _timer;
    
    public override void _Ready()
    {
        // 创建定时器
        _timer = new Timer();
        AddChild(_timer);
        _timer.WaitTime = 2.0; // 2 秒
        _timer.OneShot = false; // 重复触发
        _timer.Timeout += OnTimerTimeout;
        _timer.Start();
    }
    
    private void OnTimerTimeout()
    {
        GD.Print("定时器触发");
    }
    
    // 一次性延迟
    public async void DelayedAction()
    {
        await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);
        GD.Print("1 秒后执行");
    }
}
```

### 随机数
```csharp
// 使用 GD.Randf() 和 GD.Randi()
float randomFloat = GD.Randf(); // 0.0 到 1.0
int randomInt = GD.Randi(); // 0 到 2^32-1
int randomRange = GD.RandiRange(1, 10); // 1 到 10

// 使用 RandomNumberGenerator（可设置种子）
var rng = new RandomNumberGenerator();
rng.Seed = 12345;
float value = rng.RandfRange(0.0f, 100.0f);
```

### 日志输出
```csharp
GD.Print("普通日志");
GD.PrintErr("错误日志");  // 红色
GD.PushWarning("警告");   // 黄色
GD.PrintRich("[color=green]彩色文本[/color]");
```

### 节点查找
```csharp
// 按名称查找
Node node = GetNode("NodeName");

// 按路径查找
Node node = GetNode("Parent/Child/GrandChild");

// 按类型查找所有子节点
var sprites = GetChildren().OfType<Sprite2D>();

// 按组查找
GetTree().GetNodesInGroup("enemies");
```

### 组（Groups）
```csharp
// 添加到组
AddToGroup("enemies");

// 检查是否在组中
if (IsInGroup("enemies"))
{
    // ...
}

// 调用组中所有节点的方法
GetTree().CallGroup("enemies", "TakeDamage", 10);

// 移除组
RemoveFromGroup("enemies");
```
</utilities>

<best_practices>
## 最佳实践

### 命名规范
```csharp
// 类名：PascalCase
public partial class PlayerController : Node2D

// 公共属性/方法：PascalCase
public int Health { get; set; }
public void TakeDamage(int amount) { }

// 私有字段：_camelCase
private int _currentHealth;
private Timer _cooldownTimer;

// 常量：UPPER_CASE
private const int MAX_HEALTH = 100;

// Export 变量：PascalCase（必须）
[Export] public float MoveSpeed = 5.0f;
```

### 内存管理
```csharp
// 删除节点
QueueFree(); // 安全删除（在帧结束时）
Free();      // 立即删除（危险）

// 断开信号避免内存泄漏
public override void _ExitTree()
{
    player.HealthChanged -= OnHealthChanged;
}

// 释放资源
texture?.Dispose();
```

### 性能优化
```csharp
// 缓存节点引用
private Sprite2D _sprite;
public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite");
}

// 避免在 _Process 中频繁调用 GetNode
public override void _Process(double delta)
{
    // 好
    _sprite.Position += Vector2.Right;
    
    // 差
    GetNode<Sprite2D>("Sprite").Position += Vector2.Right;
}

// 使用对象池
private List<Enemy> _enemyPool = new();
```
</best_practices>

<common_patterns>
## 常用模式

### 状态机
```csharp
public partial class Player : CharacterBody2D
{
    public enum State { Idle, Running, Jumping, Falling }
    private State _currentState = State.Idle;
    
    public override void _PhysicsProcess(double delta)
    {
        switch (_currentState)
        {
            case State.Idle:
                HandleIdleState();
                break;
            case State.Running:
                HandleRunningState();
                break;
            case State.Jumping:
                HandleJumpingState();
                break;
        }
    }
    
    private void ChangeState(State newState)
    {
        _currentState = newState;
    }
}
```

### 对象池
```csharp
public partial class BulletPool : Node
{
    [Export] public PackedScene BulletScene;
    [Export] public int PoolSize = 20;
    
    private List<Bullet> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var bullet = BulletScene.Instantiate<Bullet>();
            bullet.Visible = false;
            AddChild(bullet);
            _pool.Add(bullet);
        }
    }
    
    public Bullet GetBullet()
    {
        foreach (var bullet in _pool)
        {
            if (!bullet.Visible)
            {
                bullet.Visible = true;
                return bullet;
            }
        }
        return null;
    }
    
    public void ReturnBullet(Bullet bullet)
    {
        bullet.Visible = false;
    }
}
```
</common_patterns>


<async_await>
## Async/Await 异步编程

### Partial Classes 要求
Godot 4 C# 要求所有继承自 GodotObject 的类使用 `partial` 关键字。

```csharp
// 正确
public partial class Player : CharacterBody2D

// 错误 - 会导致编译错误
public class Player : CharacterBody2D
```

### ToSignal 等待信号
```csharp
public async Task DelayAsync(float seconds)
{
    await ToSignal(GetTree().CreateTimer(seconds), Timer.SignalName.Timeout);
    GD.Print("延迟完成");
}

// 等待 Tween 完成
public async Task AnimateAsync()
{
    Tween tween = CreateTween();
    tween.TweenProperty(this, "position", new Vector2(500, 300), 2.0);
    await ToSignal(tween, Tween.SignalName.Finished);
    GD.Print("动画完成");
}
```

### 线程安全 - Task.Delay 问题
Godot 的 Scene Tree API 不是线程安全的。使用 Task.Delay 后操作节点会导致崩溃。

```csharp
// 错误 - 可能崩溃
public async Task LoadDataWrong()
{
    await Task.Delay(1000);
    AddChild(node); // 可能在非主线程执行
}

// 正确 - 使用 CallDeferred
public async Task LoadDataCorrect()
{
    await Task.Delay(1000);
    CallDeferred(MethodName.AddChild, node);
}
```

### Async 方法返回类型
```csharp
// 推荐 - 返回 Task
public async Task LoadDataAsync()
{
    await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);
}

// 推荐 - 返回 Task<T>
public async Task<int> CalculateAsync()
{
    await Task.Delay(100);
    return 42;
}

// 避免 - 只用于事件处理器
public async void OnButtonPressed()
{
    await LoadDataAsync();
}
```

### 后台加载资源
```csharp
public async Task<PackedScene> LoadSceneAsync(string path)
{
    ResourceLoader.LoadThreadedRequest(path);
    
    while (true)
    {
        var progress = new Godot.Collections.Array();
        var status = ResourceLoader.LoadThreadedGetStatus(path, progress);
        
        if (status == ResourceLoader.ThreadLoadStatus.Loaded)
        {
            return ResourceLoader.LoadThreadedGet(path) as PackedScene;
        }
        else if (status == ResourceLoader.ThreadLoadStatus.Failed)
        {
            GD.PrintErr($"加载失败: {path}");
            return null;
        }
        
        // 显示进度
        float percent = progress.Count > 0 ? (float)progress[0] : 0;
        GD.Print($"加载进度: {percent * 100}%");
        
        await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
    }
}
```
</async_await>

<threading>
## 线程安全和 CallDeferred

### CallDeferred 基础
确保方法在主线程的空闲时间执行，用于从后台线程安全地操作场景树。

```csharp
// 方法 1：使用 MethodName（推荐）
CallDeferred(MethodName.UpdateUI, data);

// 方法 2：使用 Callable.From
CallDeferred(Callable.From(() => UpdateUI(data)));

// 方法 3：使用字符串（不推荐）
CallDeferred("UpdateUI", data);
```

### 后台线程操作场景树
```csharp
public async Task LoadDataAsync()
{
    // 在后台线程加载数据
    var data = await Task.Run(() => LoadHeavyData());
    
    // 回到主线程更新 UI
    CallDeferred(MethodName.UpdateUI, data);
}

private void UpdateUI(object data)
{
    // 这里可以安全地操作节点
    label.Text = data.ToString();
}
```

### 线程安全的信号连接
```csharp
// 使用 CONNECT_DEFERRED 标志
player.Connect(Player.SignalName.HealthChanged, 
    Callable.From<int>(OnHealthChanged), 
    (uint)ConnectFlags.Deferred);
```
</threading>

<math_utilities>
## 数学工具

### Vector2 常用操作
```csharp
Vector2 a = new Vector2(1, 2);
Vector2 b = new Vector2(3, 4);

// 长度
float length = a.Length();
float lengthSquared = a.LengthSquared(); // 更快，避免开方

// 归一化
Vector2 normalized = a.Normalized();

// 距离
float distance = a.DistanceTo(b);

// 点积
float dot = a.Dot(b);

// 角度
float angle = a.AngleTo(b);
float angleToPoint = a.AngleToPoint(b);

// 方向向量
Vector2 direction = a.DirectionTo(b);

// 插值
Vector2 lerp = a.Lerp(b, 0.5f);

// 反射
Vector2 normal = new Vector2(0, 1);
Vector2 reflected = a.Reflect(normal);

// 旋转
Vector2 rotated = a.Rotated(Mathf.Pi / 4); // 旋转 45 度
```

### Vector2 常量
```csharp
Vector2.Zero      // (0, 0)
Vector2.One       // (1, 1)
Vector2.Up        // (0, -1)
Vector2.Down      // (0, 1)
Vector2.Left      // (-1, 0)
Vector2.Right     // (1, 0)
```

### Transform2D 操作
```csharp
// 创建变换
Transform2D transform = Transform2D.Identity;

// 平移
transform = transform.Translated(new Vector2(10, 20));

// 旋转
transform = transform.Rotated(Mathf.Pi / 4);

// 缩放
transform = transform.Scaled(new Vector2(2, 2));

// 应用变换到点
Vector2 point = new Vector2(5, 5);
Vector2 transformed = transform * point;

// 逆变换
Transform2D inverse = transform.Inverse();

// 获取位置、旋转、缩放
Vector2 origin = transform.Origin;
float rotation = transform.Rotation;
Vector2 scale = transform.Scale;
```
</math_utilities>

<camera_coordinates>
## Camera2D 和坐标转换

### 屏幕坐标 vs 世界坐标
```csharp
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
```

### Camera2D 坐标转换
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

### Camera2D 平滑跟随
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

### Camera2D 限制区域
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
</camera_coordinates>


<save_system>
## 存档系统

### JSON 存档（游戏数据）
```csharp
public partial class SaveSystem : Node
{
    private const string SavePath = "user://savegame.json";
    
    public class SaveData
    {
        public int Level { get; set; }
        public int Score { get; set; }
        public float[] PlayerPosition { get; set; } // Vector2 需要转换
        public Dictionary<string, bool> UnlockedItems { get; set; }
    }
    
    public void SaveGame(SaveData data)
    {
        var json = Json.Stringify(data);
        var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Write);
        
        if (file == null)
        {
            GD.PrintErr($"无法创建存档: {FileAccess.GetOpenError()}");
            return;
        }
        
        file.StoreString(json);
        file.Close();
    }
    
    public SaveData LoadGame()
    {
        if (!FileAccess.FileExists(SavePath))
            return new SaveData();
        
        var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Read);
        if (file == null) return new SaveData();
        
        var json = file.GetAsText();
        file.Close();
        
        var result = Json.ParseString(json);
        // 手动解析 Dictionary...
        return new SaveData();
    }
}
```

### ConfigFile 存档（设置）
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
        
        _config.Save(ConfigPath);
    }
    
    public void LoadSettings()
    {
        if (_config.Load(ConfigPath) != Error.Ok)
        {
            GD.Print("使用默认设置");
            return;
        }
        
        float masterVolume = (float)_config.GetValue("audio", "master_volume", 1.0f);
        AudioServer.SetBusVolumeDb(0, Mathf.LinearToDb(masterVolume));
    }
}
```

### 二进制存档
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
```

### 加密存档
```csharp
public void SaveEncrypted(SaveData data, string password)
{
    var json = Json.Stringify(data);
    var file = FileAccess.OpenEncrypted("user://savegame.enc", 
        FileAccess.ModeFlags.Write, password.ToUtf8Buffer());
    
    file.StoreString(json);
    file.Close();
}
```
</save_system>

<audio_system>
## 音频系统

### AudioStreamPlayer 类型
- AudioStreamPlayer - 全局音频（UI、BGM）
- AudioStreamPlayer2D - 2D 位置音频
- AudioStreamPlayer3D - 3D 位置音频

### 音频管理器
```csharp
public partial class AudioManager : Node
{
    [Export] public AudioStream BackgroundMusic;
    
    private AudioStreamPlayer _musicPlayer;
    private AudioStreamPlayer _sfxPlayer;
    
    public override void _Ready()
    {
        // BGM 播放器
        _musicPlayer = new AudioStreamPlayer();
        _musicPlayer.Stream = BackgroundMusic;
        _musicPlayer.Autoplay = true;
        _musicPlayer.Bus = "Music";
        AddChild(_musicPlayer);
        
        // SFX 播放器
        _sfxPlayer = new AudioStreamPlayer();
        _sfxPlayer.Bus = "SFX";
        AddChild(_sfxPlayer);
    }
    
    public void PlaySound(AudioStream sound)
    {
        _sfxPlayer.Stream = sound;
        _sfxPlayer.Play();
    }
    
    public void SetMasterVolume(float volume)
    {
        int busIndex = AudioServer.GetBusIndex("Master");
        AudioServer.SetBusVolumeDb(busIndex, Mathf.LinearToDb(volume));
    }
    
    public void SetMute(bool muted)
    {
        int busIndex = AudioServer.GetBusIndex("Master");
        AudioServer.SetBusMute(busIndex, muted);
    }
}
```

### 音频池（避免重复创建）
```csharp
public partial class AudioPool : Node
{
    [Export] public int PoolSize = 10;
    private List<AudioStreamPlayer> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var player = new AudioStreamPlayer();
            AddChild(player);
            _pool.Add(player);
        }
    }
    
    public void PlaySound(AudioStream sound)
    {
        foreach (var player in _pool)
        {
            if (!player.Playing)
            {
                player.Stream = sound;
                player.Play();
                return;
            }
        }
    }
}
```
</audio_system>

<shader_material>
## Shader 和材质

### ShaderMaterial 基础
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

### Modulate 属性
```csharp
// 修改节点颜色（乘法混合）
sprite.Modulate = new Color(1, 0, 0, 0.5f); // 红色半透明

// Self Modulate（不影响子节点）
sprite.SelfModulate = Colors.Blue;

// CanvasModulate（影响整个画布）
var canvasModulate = new CanvasModulate();
canvasModulate.Color = new Color(0.8f, 0.8f, 1.0f);
AddChild(canvasModulate);
```

### 闪光效果示例
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

**对应的 Shader（res://Shaders/Flash.gdshader）：**
```gdshader
shader_type canvas_item;

uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float flash_intensity : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    COLOR = mix(tex_color, flash_color, flash_intensity);
    COLOR.a = tex_color.a;
}
```
</shader_material>

<networking>
## 网络多人游戏

### RPC（远程过程调用）
```csharp
public partial class Player : CharacterBody2D
{
    [Rpc(MultiplayerApi.RpcMode.AnyPeer)]
    public void TakeDamage(int amount)
    {
        Health -= amount;
    }
    
    public void Attack()
    {
        // 调用所有客户端的方法
        Rpc(MethodName.TakeDamage, 10);
    }
}
```

### MultiplayerSynchronizer
```csharp
public partial class NetworkedPlayer : CharacterBody2D
{
    [Export] public int Health { get; set; } = 100;
    
    public override void _Ready()
    {
        var sync = new MultiplayerSynchronizer();
        sync.RootPath = GetPath();
        AddChild(sync);
        
        // 配置同步属性
        sync.ReplicationConfig = new SceneReplicationConfig();
        sync.ReplicationConfig.AddProperty(".:Health");
        sync.ReplicationConfig.AddProperty(".:Position");
    }
}
```
</networking>

<performance>
## 性能优化

### 使用 Profiler
- Debugger > Profiler 查看性能瓶颈
- C# 脚本需要 JetBrains Rider + dotTrace

### 缓存节点引用
```csharp
// 差
public override void _Process(double delta)
{
    GetNode<Sprite2D>("Sprite").Position += Vector2.Right;
}

// 好
private Sprite2D _sprite;
public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite");
}
public override void _Process(double delta)
{
    _sprite.Position += Vector2.Right;
}
```

### 减少 Marshalling 开销
C# 和 Godot 之间的调用需要 marshalling，频繁调用会影响性能。

```csharp
// 差 - 每次循环都调用 Godot API
for (int i = 0; i < 1000; i++)
{
    Position += Vector2.Right;
}

// 好 - 缓存到本地变量
Vector2 pos = Position;
for (int i = 0; i < 1000; i++)
{
    pos += Vector2.Right;
}
Position = pos;
```

### 对象池模式
避免频繁创建和销毁对象。

```csharp
public partial class BulletPool : Node
{
    [Export] public PackedScene BulletScene;
    [Export] public int PoolSize = 20;
    
    private List<Bullet> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var bullet = BulletScene.Instantiate<Bullet>();
            bullet.Visible = false;
            AddChild(bullet);
            _pool.Add(bullet);
        }
    }
    
    public Bullet GetBullet()
    {
        foreach (var bullet in _pool)
        {
            if (!bullet.Visible)
            {
                bullet.Visible = true;
                return bullet;
            }
        }
        return null;
    }
}
```
</performance>


<editor_plugins>
## 编辑器插件

### 创建编辑器插件
```csharp
#if TOOLS
using Godot;

[Tool]
public partial class MyEditorPlugin : EditorPlugin
{
    public override void _EnterTree()
    {
        // 插件被启用时调用
        GD.Print("插件已加载");
    }
    
    public override void _ExitTree()
    {
        // 插件被禁用时调用
        GD.Print("插件已卸载");
    }
}
#endif
```

### 自定义 Inspector
```csharp
#if TOOLS
public partial class CustomInspectorPlugin : EditorInspectorPlugin
{
    public override bool _CanHandle(GodotObject @object)
    {
        return @object is MyCustomNode;
    }
    
    public override void _ParseBegin(GodotObject @object)
    {
        var button = new Button();
        button.Text = "自定义按钮";
        AddCustomControl(button);
    }
}
#endif
```

### Tool 脚本
使脚本在编辑器中运行。

```csharp
[Tool]
public partial class EditorScript : Node
{
    public override void _Process(double delta)
    {
        if (Engine.IsEditorHint())
        {
            // 仅在编辑器中执行
        }
    }
}
```
</editor_plugins>

<advanced_topics>
## 高级主题

### 抽象类和接口
```csharp
// 抽象类
public abstract partial class Entity : Node2D
{
    public abstract void TakeDamage(int amount);
    public abstract void Die();
}

public partial class Player : Entity
{
    public override void TakeDamage(int amount)
    {
        Health -= amount;
    }
    
    public override void Die()
    {
        QueueFree();
    }
}

// 接口
public interface IDamageable
{
    void TakeDamage(int amount);
}

public partial class Enemy : CharacterBody2D, IDamageable
{
    public void TakeDamage(int amount)
    {
        Health -= amount;
    }
}
```

### 自定义属性和反射
```csharp
[AttributeUsage(AttributeTargets.Property)]
public class SaveableAttribute : Attribute
{
    public string Key { get; set; }
    
    public SaveableAttribute(string key = "")
    {
        Key = key;
    }
}

public partial class Player : Node
{
    [Saveable("player_health")]
    public int Health { get; set; } = 100;
}

// 使用反射读取
public Dictionary<string, object> GetSaveableData(object obj)
{
    var data = new Dictionary<string, object>();
    var type = obj.GetType();
    
    foreach (var prop in type.GetProperties())
    {
        var attr = prop.GetCustomAttribute<SaveableAttribute>();
        if (attr != null)
        {
            string key = string.IsNullOrEmpty(attr.Key) ? prop.Name : attr.Key;
            data[key] = prop.GetValue(obj);
        }
    }
    
    return data;
}
```

### 服务定位器模式
```csharp
public partial class ServiceLocator : Node
{
    public static ServiceLocator Instance { get; private set; }
    
    private Dictionary<Type, object> _services = new();
    
    public override void _Ready()
    {
        Instance = this;
    }
    
    public void Register<T>(T service)
    {
        _services[typeof(T)] = service;
    }
    
    public T Get<T>()
    {
        if (_services.TryGetValue(typeof(T), out var service))
        {
            return (T)service;
        }
        throw new Exception($"服务 {typeof(T)} 未注册");
    }
}

// 使用
ServiceLocator.Instance.Register<IAudioManager>(new AudioManager());
var audio = ServiceLocator.Instance.Get<IAudioManager>();
```

### 单元测试（GdUnit4Net）
```csharp
using GdUnit4;

[TestSuite]
public class PlayerTests
{
    [TestCase]
    public void TestHealthDecrease()
    {
        var player = new Player();
        player.Health = 100;
        
        player.TakeDamage(30);
        
        Assertions.AssertThat(player.Health).IsEqual(70);
    }
    
    [TestCase]
    public async Task TestPlayerSpawn()
    {
        var runner = ISceneRunner.Load("res://Scenes/Game.tscn");
        await runner.SimulateFrames(10);
        
        var player = runner.FindChild<Player>("Player");
        Assertions.AssertThat(player).IsNotNull();
    }
}
```
</advanced_topics>

<resource_loading>
## 资源加载优化

### GD.Load vs ResourceLoader
```csharp
// 推荐 - 简洁
var texture = GD.Load<Texture2D>("res://icon.png");

// 等价
var texture = ResourceLoader.Load<Texture2D>("res://icon.png");
```

### 资源缓存
Godot 自动缓存已加载的资源，多次 Load 同一路径不会重复加载。

```csharp
// 这两次调用返回同一个实例
var tex1 = GD.Load<Texture2D>("res://icon.png");
var tex2 = GD.Load<Texture2D>("res://icon.png");
// tex1 == tex2 为 true
```

### 后台加载大资源
```csharp
public async Task<PackedScene> LoadSceneAsync(string path)
{
    ResourceLoader.LoadThreadedRequest(path);
    
    while (true)
    {
        var progress = new Godot.Collections.Array();
        var status = ResourceLoader.LoadThreadedGetStatus(path, progress);
        
        if (status == ResourceLoader.ThreadLoadStatus.Loaded)
        {
            return ResourceLoader.LoadThreadedGet(path) as PackedScene;
        }
        
        float percent = progress.Count > 0 ? (float)progress[0] : 0;
        GD.Print($"加载进度: {percent * 100}%");
        
        await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
    }
}
```
</resource_loading>

<common_issues>
## 常见问题

### Partial Classes 编译错误
错误：`CS0260: Missing partial modifier`

解决：所有继承自 GodotObject 的类必须使用 `partial` 关键字。

```csharp
// 错误
public class Player : Node2D

// 正确
public partial class Player : Node2D
```

### Export 变量不显示
问题：[Export] 变量在 Inspector 中不显示。

解决方案：
1. 变量必须是 public
2. 变量名必须首字母大写（PascalCase）
3. 重新编译项目（Build 按钮）

```csharp
// 错误 - 不会显示
[Export] private int health;
[Export] public int health; // 小写

// 正确
[Export] public int Health { get; set; }
```

### 线程崩溃
错误：在非主线程操作节点导致崩溃。

解决：使用 CallDeferred。

```csharp
// 错误
await Task.Delay(1000);
AddChild(node);

// 正确
await Task.Delay(1000);
CallDeferred(MethodName.AddChild, node);
```

### 信号内存泄漏
问题：未断开信号连接导致内存泄漏。

解决：在 _ExitTree 中断开信号。

```csharp
public override void _Ready()
{
    player.HealthChanged += OnHealthChanged;
}

public override void _ExitTree()
{
    player.HealthChanged -= OnHealthChanged;
}
```
</common_issues>

<quick_reference>
## 快速参考

### 常用快捷键
- F5 - 运行项目
- F6 - 运行当前场景
- Ctrl+B - 编译 C# 项目
- Ctrl+Shift+A - 添加子节点
- Ctrl+D - 复制节点

### 常用路径
- `res://` - 项目根目录
- `user://` - 用户数据目录（Windows: %APPDATA%/Godot/app_userdata/[项目名]）

### 常用节点类型
- Node2D - 2D 基础节点
- Sprite2D - 2D 精灵
- CharacterBody2D - 2D 角色物理
- Area2D - 2D 触发区域
- Timer - 定时器
- AudioStreamPlayer - 音频播放器

### 常用方法
```csharp
GetNode<T>("path")           // 获取节点
QueueFree()                  // 删除节点
AddChild(node)               // 添加子节点
GetTree()                    // 获取场景树
EmitSignal(name, args)       // 发射信号
CallDeferred(method, args)   // 延迟调用
```
</quick_reference>
