# 研究轮次 2：编辑器插件和线程安全

## 编辑器插件（EditorPlugin）

### 关键发现

1. **创建编辑器插件**
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

2. **自定义 Inspector**
```csharp
#if TOOLS
public partial class CustomInspectorPlugin : EditorInspectorPlugin
{
    public override bool _CanHandle(GodotObject @object)
    {
        // 返回 true 表示可以处理这个对象类型
        return @object is MyCustomNode;
    }
    
    public override void _ParseBegin(GodotObject @object)
    {
        // 在 Inspector 开始处添加自定义控件
        var button = new Button();
        button.Text = "自定义按钮";
        AddCustomControl(button);
    }
    
    public override bool _ParseProperty(GodotObject @object, Variant.Type type, 
        string name, PropertyHint hintType, string hintString, 
        PropertyUsageFlags usageFlags, bool wide)
    {
        // 返回 true 表示隐藏默认属性编辑器
        // 返回 false 表示使用默认编辑器
        return false;
    }
}
#endif
```

3. **注册 Inspector 插件**
```csharp
#if TOOLS
public partial class MyEditorPlugin : EditorPlugin
{
    private CustomInspectorPlugin _inspectorPlugin;
    
    public override void _EnterTree()
    {
        _inspectorPlugin = new CustomInspectorPlugin();
        AddInspectorPlugin(_inspectorPlugin);
    }
    
    public override void _ExitTree()
    {
        RemoveInspectorPlugin(_inspectorPlugin);
    }
}
#endif
```

4. **@tool 属性**
- 使脚本在编辑器中运行
- 必须小心处理，避免编辑器崩溃

```csharp
[Tool]
public partial class EditorScript : Node
{
    public override void _Process(double delta)
    {
        // 这段代码在编辑器中也会运行
        if (Engine.IsEditorHint())
        {
            // 仅在编辑器中执行
        }
    }
}
```

## 线程安全和 CallDeferred

### 关键发现

1. **CallDeferred 的作用**
- 确保方法在主线程的空闲时间执行
- 用于从后台线程安全地操作场景树

```csharp
// 从后台线程调用
CallDeferred(MethodName.UpdateUI, data);

// 在主线程执行
private void UpdateUI(object data)
{
    // 安全地更新 UI
}
```

2. **使用 Callable**
```csharp
// 方法 1：使用 MethodName
CallDeferred(MethodName.MyMethod, arg1, arg2);

// 方法 2：使用 Callable.From
CallDeferred(Callable.From(() => MyMethod(arg1, arg2)));

// 方法 3：使用字符串（不推荐，没有类型安全）
CallDeferred("MyMethod", arg1, arg2);
```

3. **信号的线程安全**
- 信号默认不是线程安全的
- 使用 CONNECT_DEFERRED 标志确保在主线程执行

```csharp
// 线程安全的信号连接
player.Connect(Player.SignalName.HealthChanged, 
    Callable.From<int>(OnHealthChanged), 
    (uint)ConnectFlags.Deferred);
```

4. **后台线程操作场景树**
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

5. **检测是否在主线程**
- Godot 没有直接方法检测
- 使用 CallDeferred 和信号保证线程安全

## Vector 和 Transform 数学工具

### 关键发现

1. **Vector2 常用操作**
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

2. **Vector2 常量**
```csharp
Vector2.Zero      // (0, 0)
Vector2.One       // (1, 1)
Vector2.Up        // (0, -1)
Vector2.Down      // (0, 1)
Vector2.Left      // (-1, 0)
Vector2.Right     // (1, 0)
```

3. **Transform2D 操作**
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

4. **Vector3 操作（3D）**
```csharp
Vector3 a = new Vector3(1, 2, 3);
Vector3 b = new Vector3(4, 5, 6);

// 叉积（3D 特有）
Vector3 cross = a.Cross(b);

// 其他操作与 Vector2 类似
float length = a.Length();
Vector3 normalized = a.Normalized();
float distance = a.DistanceTo(b);
```

## 需要添加到文档的内容

1. 编辑器插件完整指南
2. 自定义 Inspector 示例
3. @tool 属性使用
4. CallDeferred 详细说明
5. 线程安全最佳实践
6. Vector2/Vector3 数学工具
7. Transform2D 变换操作
