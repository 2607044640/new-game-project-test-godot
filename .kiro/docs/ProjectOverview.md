# 项目概述

## 基本信息

**项目名称：** 消消乐+扫雷混合游戏  
**引擎：** Godot Engine 4.6  
**开发语言：** C#  
**创建日期：** 2026-03-03  
**开发方法：** Vibe Coding（快速原型迭代）

---

## 游戏概念

一个结合消消乐和扫雷机制的益智游戏：

### 核心玩法
- 网格游戏，包含三种形状元素：三角形、方块、圆形
- 初始状态下，大部分格子是隐藏的
- 玩家点击任意格子后，该格子及其周围8个格子会显示出来
- 类似扫雷的揭示机制，但使用形状而非数字

### 消除机制（待定义）
- 相同形状连接消除？
- 特定图案消除？
- 其他规则？

---

## 技术架构

### 场景结构（Scene Hierarchy）
```
Main.tscn (主场景)
├── Grid (Node2D - 网格容器)
│   └── Cell.tscn (场景实例) × N
├── UI (CanvasLayer - UI层)
│   ├── ScoreLabel (Label)
│   └── GameControls (Control)
└── GameManager (Node - 游戏逻辑)
```

### 核心脚本（Scripts）
1. **GameManager.cs** - 游戏主逻辑控制器
2. **Grid.cs** - 网格管理和生成
3. **Cell.cs** - 单个格子的行为和状态
4. **CellData.cs** - 数据结构定义

### 数据结构
```csharp
public enum ShapeType { Triangle, Square, Circle }
public enum CellState { Hidden, Revealed, Matched }

public class CellData
{
    public ShapeType ShapeType { get; set; }
    public CellState State { get; set; }
    public Vector2I Position { get; set; }
}
```

---

## 开发阶段

### 第一阶段：基础框架 ⏳
- [ ] 创建网格系统
- [ ] 实现格子的显示/隐藏机制
- [ ] 实现点击检测
- [ ] 实现周围8格的揭示逻辑

### 第二阶段：视觉效果
- [ ] 设计三种形状的视觉表现
- [ ] 添加揭示动画
- [ ] 添加点击反馈效果
- [ ] 优化UI布局

### 第三阶段：游戏逻辑
- [ ] 实现消除机制
- [ ] 添加分数系统
- [ ] 添加关卡/难度系统
- [ ] 实现游戏结束条件

### 第四阶段：完善与优化
- [ ] 添加音效和背景音乐
- [ ] 添加粒子效果
- [ ] 性能优化
- [ ] 添加设置菜单

---

## 待决策的设计问题

1. **网格大小**：8×8 还是 10×10？
2. **消除规则**：具体的消除条件是什么？
3. **胜利条件**：如何判定游戏胜利？
4. **失败条件**：是否有失败机制？
5. **特殊元素**：是否需要道具或特殊格子？

---

## 技术细节

### 网格坐标系统
- 使用二维数组存储网格数据：`Cell[,] grid`
- 坐标映射：`grid[x, y]`
- 周围8格的偏移量：
  ```csharp
  Vector2I[] offsets = {
      new(-1, -1), new(0, -1), new(1, -1),
      new(-1,  0),              new(1,  0),
      new(-1,  1), new(0,  1), new(1,  1)
  };
  ```

### 场景管理
- **Main Scene**: TestScene.tscn（当前测试场景）
- **Game Scene**: Main.tscn（游戏主场景，待创建）
- **Cell Scene**: Cell.tscn（格子预制场景，待创建）

---

## 参考资源

- [Godot 官方文档](https://docs.godotengine.org/)
- [C# API 参考](https://docs.godotengine.org/en/stable/classes/index.html)
- 网格系统教程
- 消消乐游戏机制分析
- 扫雷游戏逻辑参考

---

**最后更新：** 2026-03-03  
**当前状态：** 项目初始化，C#环境配置中
