# 研究轮次 1：Async/Await 和 Partial Classes

## Async/Await 在 Godot C# 中的使用

### 关键发现

1. **ToSignal 用于等待信号**
```csharp
await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);
```

2. **Task.Delay 的线程安全问题**
- Godot 的 Scene Tree API 不是线程安全的
- 使用 Task.Delay 后操作节点会导致崩溃
- 解决方案：使用 CallDeferred 确保在主线程执行

```csharp
// 错误做法
await Task.Delay(1000);
AddChild(node); // 可能在非主线程执行，导致崩溃

// 正确做法
await Task.Delay(1000);
CallDeferred(MethodName.AddChild, node);
```

3. **async 方法返回类型**
- 使用 `async Task` 而不是 `async void`
- `async void` 只用于事件处理器
- `async Task<T>` 用于返回值

```csharp
// 推荐
public async Task LoadDataAsync()
{
    await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);
}

// 避免（除非是事件处理器）
public async void LoadData()
{
    // ...
}
```

4. **等待 Tween 完成**
```csharp
Tween tween = CreateTween();
tween.TweenProperty(this, "position", target, 1.0);
await ToSignal(tween, Tween.SignalName.Finished);
```

## Partial Classes 和继承

### 关键发现

1. **必须使用 partial 关键字**
- Godot 4 C# 要求所有继承自 GodotObject 的类使用 partial
- 这是因为 Godot 的源生成器需要生成额外代码

```csharp
// 正确
public partial class Player : CharacterBody2D

// 错误（会导致编译错误）
public class Player : CharacterBody2D
```

2. **抽象类和接口**
- C# 支持接口，但 GDScript 不支持
- 使用抽象类实现多态

```csharp
public abstract partial class Entity : Node2D
{
    public abstract void TakeDamage(int amount);
}

public partial class Player : Entity
{
    public override void TakeDamage(int amount)
    {
        // 实现
    }
}
```

3. **[GlobalClass] 属性**
- 使自定义类在编辑器中可见
- 用于 Resource 和自定义节点类型

```csharp
[GlobalClass]
public partial class ItemData : Resource
{
    // ...
}
```

## Resource Loading 性能

### 关键发现

1. **GD.Load vs ResourceLoader.Load**
- 两者功能相同，GD.Load 是简化版本
- 推荐使用 GD.Load<T>()

2. **资源缓存**
- Godot 自动缓存已加载的资源
- 多次 Load 同一路径不会重复加载

3. **preload 在 C# 中不可用**
- preload 是 GDScript 特有的编译时加载
- C# 中使用 [Export] 在编辑器中分配资源

4. **后台加载大资源**
```csharp
ResourceLoader.LoadThreadedRequest("res://large_scene.tscn");

// 检查加载进度
while (true)
{
    var progress = new Godot.Collections.Array();
    var status = ResourceLoader.LoadThreadedGetStatus("res://large_scene.tscn", progress);
    
    if (status == ResourceLoader.ThreadLoadStatus.Loaded)
    {
        var scene = ResourceLoader.LoadThreadedGet("res://large_scene.tscn");
        break;
    }
    
    await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
}
```

## 需要添加到文档的内容

1. Async/Await 完整指南
2. 线程安全注意事项
3. Partial classes 要求
4. 抽象类和接口使用
5. 资源加载性能优化
6. 后台加载示例
