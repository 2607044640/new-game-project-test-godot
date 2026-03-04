# Godot MCP Server

一个运行在Godot内部的MCP (Model Context Protocol) Server，允许AI自动测试和控制游戏。

## 🎯 功能概览

### MCP Bridge工具（6个）

通过 `.kiro/scripts/godot_mcp_bridge.py` 提供：

1. **start_game** - 启动Godot游戏（先编译再运行）
2. **build_project** - 编译C#项目
3. **get_logs** - 读取Godot日志（最近N行）
4. **get_scene_tree** - 获取场景树结构
5. **simulate_click** - 模拟鼠标点击
6. **get_screenshot** - 获取游戏截图（Base64 PNG）

### 游戏内MCP Server

运行在Godot游戏内部（端口8765），提供：
- 场景树查询
- 鼠标点击模拟
- 截图功能

---

## 📦 安装步骤

### 1. 添加MCP Server到场景

1. 打开主场景（My2DMap.tscn）
2. 添加一个新的Node节点
3. 重命名为 `MCPServer`
4. 附加脚本：`res://Scripts/MCP/MCPServer.cs`
5. 保存场景

### 2. 编译项目

```cmd
dotnet build "New Game Project Test Godot.sln"
```

### 3. 配置Godot路径

编辑 `.kiro/scripts/godot_config.json`：

```json
{
  "godot_executable": "C:\\Godot\\Godot_v4.6.1-stable_mono_win64\\Godot_v4.6.1-stable_mono_win64.exe",
  "project_root": "C:\\Godot\\new-game-project-test-godot",
  "mcp_port": 8765
}
```

### 4. 配置Kiro MCP

在 `C:\Users\[用户名]\.kiro\settings\mcp.json` 中添加：

```json
{
  "mcpServers": {
    "godot-game": {
      "command": "python",
      "args": [
        "C:\\Godot\\new-game-project-test-godot\\.kiro\\scripts\\godot_mcp_bridge.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "get_scene_tree",
        "get_screenshot",
        "simulate_click",
        "build_project",
        "get_logs"
      ]
    }
  }
}
```

### 5. 重启Kiro

重启Kiro以加载MCP配置，或在MCP Server视图中重新连接。

---

## 🚀 使用方法

### 在Kiro中使用

直接在对话中请求：

```
编译Godot项目
启动Godot游戏
查看最近的日志
获取当前场景树
在坐标(320, 240)模拟点击
获取游戏截图
```

### 命令行测试

```cmd
# 测试所有功能
python .\.kiro\scripts\test_godot_mcp_simple.py

# 测试bridge工具
python .\.kiro\scripts\test_mcp_bridge.py
```

---

## 🔧 工具详解

### 1. start_game

启动Godot游戏（自动先编译）。

**参数：** 无

**返回：**
```json
{
  "success": true,
  "message": "Godot game started (PID: 12345)",
  "pid": 12345
}
```

### 2. build_project

编译C#项目。

**参数：** 无

**返回：**
```json
{
  "success": true,
  "message": "Build succeeded",
  "output": "Build output..."
}
```

### 3. get_logs

读取Godot日志。

**参数：**
- `lines` (可选): 读取最近N行，默认50

**返回：**
```json
{
  "success": true,
  "logs": ["log line 1", "log line 2", ...],
  "total_lines": 1234
}
```

### 4. get_scene_tree

获取场景树结构（需要游戏运行）。

**参数：** 无

**返回：**
```json
{
  "success": true,
  "data": {
    "name": "Root",
    "type": "Window",
    "path": "/root",
    "children": [...]
  }
}
```

### 5. simulate_click

模拟鼠标点击（需要游戏运行）。

**参数：**
- `x`: X坐标
- `y`: Y坐标

**返回：**
```json
{
  "success": true,
  "data": {
    "clicked": true,
    "x": 320,
    "y": 240
  }
}
```

### 6. get_screenshot

获取游戏截图（需要游戏运行）。

**参数：** 无

**返回：**
```json
{
  "success": true,
  "data": {
    "screenshot": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

截图是PNG格式的Base64编码字符串。

---

## 🧪 测试结果

所有功能已测试通过：

- ✅ build_project - 编译成功（0.76s）
- ✅ get_logs - 读取日志成功
- ✅ get_scene_tree - 场景树获取成功
- ✅ simulate_click - 点击模拟成功
- ✅ get_screenshot - 截图获取成功（4888 bytes）

---

## 🐛 故障排除

### 无法连接到游戏

**错误：** "Cannot connect to Godot. Make sure the game is running."

**解决：**
1. 在Godot中按F5运行游戏
2. 检查Output面板是否显示 "MCP Server started on port 8765"
3. 确保端口8765未被占用

### 编译失败

**错误：** "Build failed"

**解决：**
1. 检查是否安装了.NET SDK 6.0+
2. 运行 `dotnet --version` 确认
3. 在Godot编辑器中点击"Build"按钮

### start_game失败

**错误：** "Godot executable not found"

**解决：**
1. 编辑 `.kiro/scripts/godot_config.json`
2. 设置正确的 `godot_executable` 路径
3. 确保路径指向 `.exe` 文件

### 日志文件未找到

**错误：** "Log file not found"

**解决：**
1. 至少运行一次游戏以生成日志
2. 检查路径：`%APPDATA%\Godot\app_userdata\New Game Project Test Godot\logs\godot.log`

---

## 🔐 安全注意事项

⚠️ **警告：** 此MCP Server仅用于开发和测试！

- 不要在生产环境中启用
- 不要暴露到公网
- 仅在本地开发时使用

---

## 📚 扩展

### 添加新工具

1. 在 `MCPTools.cs` 中添加新的静态方法
2. 在 `MCPServer.cs` 的 `HandleMCPRequest` 中添加新的case
3. 在 `godot_mcp_bridge.py` 中添加工具定义
4. 更新文档

---

**创建日期：** 2026-03-03  
**版本：** 2.0.0  
**状态：** ✅ 完全可用
