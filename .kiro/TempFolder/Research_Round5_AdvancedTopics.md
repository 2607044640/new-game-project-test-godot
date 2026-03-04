# 研究轮次 5：高级主题

## 自定义属性和反射

### 关键发现

1. **自定义属性**
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
    
    [Saveable("player_score")]
    public int Score { get; set; } = 0;
}
```

2. **使用反射读取属性**
```csharp
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

## 依赖注入和服务定位器

### 关键发现

1. **简单服务定位器**
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
```


2. **使用示例**
```csharp
// 注册服务
ServiceLocator.Instance.Register<IAudioManager>(new AudioManager());
ServiceLocator.Instance.Register<ISaveSystem>(new SaveSystem());

// 获取服务
var audio = ServiceLocator.Instance.Get<IAudioManager>();
audio.PlaySound("jump");
```

3. **AutoInject 插件（推荐）**
- chickensoft-games/AutoInject
- 基于节点树的依赖注入
- 自动提供依赖给子节点

## 单元测试

### 关键发现

1. **GdUnit4Net（推荐）**
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
    public void TestPlayerDeath()
    {
        var player = new Player();
        player.Health = 10;
        
        player.TakeDamage(20);
        
        Assertions.AssertThat(player.IsDead).IsTrue();
    }
}
```

2. **场景测试**
```csharp
[TestSuite]
public class GameSceneTests
{
    [TestCase]
    public async Task TestPlayerSpawn()
    {
        var runner = ISceneRunner.Load("res://Scenes/Game.tscn");
        
        await runner.SimulateFrames(10);
        
        var player = runner.FindChild<Player>("Player");
        Assertions.AssertThat(player).IsNotNull();
        Assertions.AssertThat(player.Health).IsEqual(100);
    }
}
```

3. **Mocking**
```csharp
[TestCase]
public void TestWithMock()
{
    var mockAudio = Mock.Create<IAudioManager>();
    
    var player = new Player();
    player.AudioManager = mockAudio;
    
    player.Jump();
    
    Mock.Verify(mockAudio, 1, "PlaySound", "jump");
}
```

## 需要添加的内容
1. 自定义属性和反射
2. 服务定位器模式
3. 单元测试框架
4. Mocking 和场景测试
