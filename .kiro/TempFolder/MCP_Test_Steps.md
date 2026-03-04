# MCP Server 测试步骤（保留Jolt Physics）

## 当前状态
- ✅ MCPServer节点已在场景中
- ⚠️ Jolt Physics插件版本不兼容（但不影响MCP Server）
- ⏳ 需要编译C#代码

## 测试步骤

### 1. 编译C#代码

在Godot编辑器中：
- 点击右上角 "Build" 按钮
- 或 `Project > Tools > C# > Build Project`

### 2. 运行游戏（忽略Jolt错误）

- 按 `F5` 运行
- **忽略Jolt Physics的红色错误**
- 查看Output面板，寻找：`MCP Server started on port 8765`

### 3. 测试MCP连接

在命令行运行：
```cmd
python .\.kiro\scripts\test_godot_mcp_simple.py
```

## 关于Jolt Physics错误

错误信息：
```
ERROR: GDExtension only compatible with Godot version 4.4 or earlier
```

**这个错误不会阻止MCP Server运行！**

- Jolt Physics加载失败
- 但游戏的其他部分（包括MCP Server）仍然可以运行
- 只是物理引擎会回退到默认的GodotPhysics

## 长期解决方案

1. **更新Jolt Physics插件**
   - GitHub: https://github.com/godot-jolt/godot-jolt
   - 下载支持Godot 4.6的版本

2. **或者降级Godot**
   - 如果Jolt Physics对你很重要
   - 可以使用Godot 4.4版本

3. **或者等待插件更新**
   - Jolt Physics团队可能会发布4.6兼容版本
