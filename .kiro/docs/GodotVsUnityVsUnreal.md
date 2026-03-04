# Godot vs Unity vs Unreal - 概念对比

## 预制体系统 (Prefab/Scene)

| 概念 | Unity | Godot | Unreal |
|------|-------|-------|--------|
| **名称** | Prefab | Scene | Blueprint Class |
| **文件格式** | `.prefab` | `.tscn` | `.uasset` |
| **创建方式** | 拖拽GameObject到Project | 保存任何节点树 | 创建Blueprint |
| **实例化** | 拖拽到场景 | Instance Child Scene | Place Actor |

---

## 🎯 Godot Scene 系统（最灵活）

### 核心特点
- **任何节点树都是Scene** - 不需要"转换为Prefab"
- **Scene即Prefab** - 没有区别
- **支持继承** - Scene可以继承另一个Scene

### 创建和使用

**创建Scene（预制体）：**
1. 在场景树中构建节点结构
2. `Scene > Save Scene` 或 `Ctrl+S`
3. 保存为 `.tscn` 文件
4. 完成！这就是一个可复用的"Prefab"

**实例化Scene：**
1. 在另一个场景中，右键节点
2. `Instance Child Scene` 或 `Ctrl+Shift+A`
3. 选择要实例化的 `.tscn` 文件

**Scene继承（Godot独有）：**
1. 右键场景根节点
2. `Change Type` > `Load`
3. 选择父Scene
4. 子Scene继承父Scene的所有内容
5. 可以覆盖任何属性

### 代码实例化

```csharp
// 加载Scene
var cellScene = GD.Load<PackedScene>("res://Scenes/Cell.tscn");

// 实例化
var cellInstance = cellScene.Instantiate<Cell>();

// 添加到场景树
AddChild(cellInstance);

// 设置属性
cellInstance.Position = new Vector2(100, 100);
```

---

## 🎮 Unity Prefab 系统

### 创建Prefab
1. 在Hierarchy中创建GameObject
2. 拖拽到Project窗口
3. 变成蓝色 = Prefab

### 实例化Prefab
- 拖拽到场景
- 或代码：`Instantiate(prefab)`

### 限制
- 需要手动"转换为Prefab"
- Prefab和普通GameObject有区别
- 嵌套Prefab支持有限（旧版本）

---

## 🏗️ Unreal Engine（没有传统Prefab）

### Blueprint Class
- 类似Prefab，但更像"类定义"
- 创建Blueprint Class
- 在关卡中放置实例

### Actor Component
- 组件化系统
- 可复用组件，但不是完整Actor

### 为什么没有Prefab？
- Unreal更注重Blueprint Class（类）
- 而不是实例的复用（Prefab）
- 更接近面向对象编程思维

---

## 📊 对比总结

| 特性 | Unity Prefab | Godot Scene | Unreal Blueprint |
|------|-------------|-------------|------------------|
| **创建难度** | 中等 | 简单 | 复杂 |
| **灵活性** | 中等 | 高 | 高 |
| **继承支持** | 有限 | 完整 | 完整 |
| **嵌套支持** | 有限 | 完整 | 完整 |
| **学习曲线** | 平缓 | 平缓 | 陡峭 |

---

## 🎯 Godot的优势

### 1. 统一的Scene概念
- 不区分"场景"和"预制体"
- 任何Scene都可以实例化
- 减少概念负担

### 2. Scene继承
```
BaseEnemy.tscn (父Scene)
    ├─ Sprite
    ├─ CollisionShape
    └─ HealthBar

FlyingEnemy.tscn (继承BaseEnemy)
    └─ 覆盖Sprite，添加翅膀动画

GroundEnemy.tscn (继承BaseEnemy)
    └─ 覆盖CollisionShape，添加地面检测
```

### 3. 轻量级
- `.tscn` 是文本文件（易于版本控制）
- 可以手动编辑（高级用户）
- 合并冲突更容易解决

---

## 💡 实际应用示例

### 游戏中的Cell（格子）

**Unity做法：**
1. 创建Cell GameObject
2. 添加组件（Sprite, Collider, Script）
3. 拖拽到Project创建Prefab
4. 在代码中Instantiate

**Godot做法：**
1. 创建Cell Scene
2. 添加节点（Sprite2D, Area2D, Script）
3. 保存Scene（自动就是"Prefab"）
4. 在代码中Instantiate

**结果：** Godot少一步"转换为Prefab"的操作

---

## 🔧 最佳实践

### Godot Scene组织

```
Scenes/
├── Main.tscn           # 主场景
├── UI/
│   ├── MainMenu.tscn
│   └── HUD.tscn
├── Game/
│   ├── Grid.tscn       # 网格
│   └── Cell.tscn       # 格子（可复用）
└── Effects/
    └── Particle.tscn
```

### 命名规范
- Scene文件：PascalCase（`Cell.tscn`）
- 脚本文件：与Scene同名（`Cell.cs`）
- 实例节点：camelCase（`cellInstance`）

---

**总结：** Godot的Scene系统比Unity的Prefab更简单、更灵活，比Unreal的Blueprint更轻量。对于你的消消乐项目，Scene系统会让格子（Cell）的复用变得非常简单。
