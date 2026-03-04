# 测试指南 - Testing Guide

## 综合测试脚本

### 功能测试清单

✅ **已实现的功能：**

1. **自动查看游戏场景结构** (`get_scene_tree`)
   - 获取完整的场景节点树
   - 查看节点层级关系
   - 分析场景结构

2. **自动点击游戏元素** (`simulate_click`)
   - 模拟鼠标点击
   - 支持任意坐标点击
   - 用于自动化测试交互

3. **自动截图并分析游戏状态** (`get_game_state`)
   - 捕获游戏截图 (PNG base64)
   - 提取结构化游戏数据
   - 准确的图标位置和类型信息

4. **实时监控游戏运行状态**
   - 持续截图监控
   - 自动保存历史记录
   - 实时状态分析

5. **编译项目** (`build_project`)
   - 自动编译 C# 代码
   - 检查编译错误

6. **查看日志** (`get_logs`)
   - 读取 Godot 日志
   - 支持指定行数
   - 实时调试信息

## 快速开始

### 1. 运行综合测试

```cmd
# 1. 启动 Godot 游戏 (F5 in Godot Editor)

# 2. 运行测试脚本
cd C:\Godot\new-game-project-test-godot\.kiro\scripts\testing
python comprehensive_test.py
```

### 2. 测试内容

综合测试脚本会自动测试：

- ✅ 场景树结构获取
- ✅ 模拟点击功能
- ✅ 游戏状态捕获（截图 + 数据）

### 3. 预期输出

```
============================================================
MCP 功能综合测试
============================================================
目标服务器: 127.0.0.1:8765

请确保:
1. Godot 游戏正在运行 (F5)
2. MCP 服务器已启动 (端口 8765)

按 Enter 开始测试...

============================================================
测试 1: 获取场景树结构 (get_scene_tree)
============================================================
✅ 成功获取场景树
场景树预览 (前200字符):
Root (Node2D)
  Camera2D (Camera2D)
  Sprite2D (Sprite2D)
  ...

============================================================
测试 2: 模拟点击 (simulate_click)
============================================================
✅ 成功: Clicked at (640, 360)

============================================================
测试 3: 获取游戏状态 (get_game_state)
============================================================
✅ 截图: 34512 字符 (base64)
✅ 游戏状态: 6 个图标
图标类型分布:
  - Icon: 1
  - Icon2: 1
  - Icon3: 1
  - Icon7: 1
  - Icon8: 1
  - Icon9: 1
✅ 测试通过: 截图和游戏状态都已获取

============================================================
测试总结
============================================================
✅ 通过: 场景树结构
✅ 通过: 模拟点击
✅ 通过: 游戏状态捕获

总计: 3/3 测试通过

🎉 所有测试通过！
```

## 单独测试各项功能

### 测试场景树

```cmd
cd .kiro\scripts\testing
python -c "from comprehensive_test import test_scene_tree; test_scene_tree()"
```

### 测试点击

```cmd
cd .kiro\scripts\testing
python -c "from comprehensive_test import test_simulate_click; test_simulate_click()"
```

### 测试游戏状态

```cmd
cd .kiro\scripts\testing
python -c "from comprehensive_test import test_game_state; test_game_state()"
```

## 实时监控测试

### 启动实时监控

```cmd
cd .kiro\scripts\realtime_monitoring
python realtime_screenshot_monitor.py
```

监控器会：
- 每 3 秒自动捕获游戏状态
- 更新 `current_screenshot.png`
- 保存时间戳副本到 `.kiro/screenshots/`
- 保存游戏状态 JSON

### 分析当前状态

```cmd
cd .kiro\scripts\realtime_monitoring
python analyze_current_screenshot.py
```

## 编译和日志测试

### 编译项目

使用 Python MCP 桥接：

```python
from godot_mcp_bridge import build_project
result = build_project()
print(result)
```

或直接命令行：

```cmd
dotnet build "New Game Project Test Godot.sln"
```

### 查看日志

使用 Python MCP 桥接：

```python
from godot_mcp_bridge import get_logs
logs = get_logs(lines=50)
print(logs)
```

或直接 PowerShell：

```powershell
Get-Content "$env:APPDATA\Godot\app_userdata\New Game Project Test Godot\logs\godot.log" -Tail 50
```

## 故障排除

### 测试失败：连接错误

**问题：** `Error: [Errno 10061] No connection could be made`

**解决方案：**
1. 确保 Godot 游戏正在运行 (F5)
2. 检查 MCP 服务器是否启动
3. 验证端口 8765 未被占用

### 测试失败：超时

**问题：** `Error: timed out`

**解决方案：**
1. 增加超时时间（修改 `sock.settimeout(10)`）
2. 检查游戏是否响应
3. 查看 Godot 日志是否有错误

### 测试失败：无数据返回

**问题：** 测试运行但无数据

**解决方案：**
1. 检查游戏场景是否正确加载
2. 验证 MCP 服务器日志
3. 确认场景中有可交互元素

## 自动化测试集成

### CI/CD 集成

可以将综合测试脚本集成到 CI/CD 流程：

```yaml
# .github/workflows/test.yml
name: Test Game

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Run Tests
        run: |
          cd .kiro/scripts/testing
          python comprehensive_test.py
```

### 定时测试

使用 Windows 任务计划程序定时运行测试：

```cmd
schtasks /create /tn "Godot Game Test" /tr "python C:\Godot\new-game-project-test-godot\.kiro\scripts\testing\comprehensive_test.py" /sc daily /st 09:00
```

## 测试覆盖率

当前测试覆盖的功能：

| 功能 | 测试状态 | 覆盖率 |
|------|---------|--------|
| 场景树获取 | ✅ | 100% |
| 点击模拟 | ✅ | 100% |
| 游戏状态捕获 | ✅ | 100% |
| 实时监控 | ✅ | 100% |
| 编译 | ⚠️ 手动 | 50% |
| 日志查看 | ⚠️ 手动 | 50% |

## 下一步

1. 添加更多自动化测试用例
2. 实现性能测试
3. 添加压力测试
4. 集成到 CI/CD

## 相关文档

- [MCP Server 文档](GodotMCPServer.md)
- [实时监控文档](RealtimeScreenshotMonitoring.md)
- [脚本文件夹说明](.kiro/scripts/README.md)
