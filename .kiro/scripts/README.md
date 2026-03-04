# Scripts 文件夹结构

## 📁 文件夹组织

```
.kiro/scripts/
├── realtime_monitoring/     # 实时监控工具
├── testing/                 # 测试脚本
├── archived/                # 已归档的旧脚本
├── godot_mcp_bridge.py      # MCP 桥接（核心工具）
└── godot_config.json        # Godot 配置文件
```

## 🔧 核心工具（根目录）

### godot_mcp_bridge.py
Python MCP 服务器，提供以下功能：
- `build_project` - 编译 C# 项目
- `start_game` - 启动 Godot 游戏
- `get_logs` - 读取游戏日志

### godot_config.json
配置文件，指定 Godot 可执行文件路径

## 📸 实时监控工具 (realtime_monitoring/)

### realtime_screenshot_monitor.py
**主要监控工具** - 持续捕获游戏截图和状态
- 每 3 秒自动捕获
- 更新 `current_screenshot.png`
- 保存时间戳副本到 `.kiro/screenshots/`
- 保存游戏状态 JSON

**使用方法:**
```cmd
cd .kiro\scripts\realtime_monitoring
python realtime_screenshot_monitor.py
```

### watch_screenshot_folder.py
**文件夹监视器** - 监控新截图出现
- 使用 watchdog 库
- 实时通知新文件
- 显示文件大小和时间

**使用方法:**
```cmd
pip install watchdog
cd .kiro\scripts\realtime_monitoring
python watch_screenshot_folder.py
```

### analyze_current_screenshot.py
**分析助手** - 显示当前游戏状态
- 读取最新截图
- 显示游戏状态摘要
- 列出图标类型和数量

**使用方法:**
```cmd
cd .kiro\scripts\realtime_monitoring
python analyze_current_screenshot.py
```

### README_REALTIME_MONITORING.md
完整的实时监控系统使用指南

## 🧪 测试脚本 (testing/)

### test_game_state.py
**集成测试** - 测试游戏状态捕获系统
- 测试 `get_game_state` MCP 工具
- 验证截图和结构化数据
- 保存测试截图

### screenshot_only.py
简单的截图捕获测试

### detailed_game_state.py
详细的游戏状态查询

### view_screenshot.py / show_screenshot.py
截图查看工具

### complete_screenshot_test.py
完整的截图功能测试

### analyze_screenshot.py
截图分析工具

### analyze_icon.py
**新增** - 分析项目 icon.png 文件
- 显示图像尺寸和格式
- 验证 PNG 文件结构
- 显示 Base64 编码信息

### test_godot_mcp.py / test_godot_mcp_simple.py
MCP 服务器测试脚本

### test_mcp_bridge.py
MCP 桥接测试

### test_start_game.py
游戏启动测试

### test_full_workflow.py
完整工作流测试

### test_game_state_screenshot.png
测试截图文件

## 📦 已归档脚本 (archived/)

这些是旧版本或不常用的脚本：
- `quick_screenshot.py`
- `simple_screenshot.py`
- `run_and_screenshot.py`
- `start_and_screenshot.py`
- `start_and_get_screenshot.py`
- `test_screenshot_now.py`
- `get_screenshot_base64.py`
- `current_screenshot.png` (旧版本)

## 🚀 快速开始

### 1. 实时监控游戏
```cmd
# 启动游戏 (F5 in Godot)
# 然后运行监控
cd C:\Godot\new-game-project-test-godot\.kiro\scripts\realtime_monitoring
python realtime_screenshot_monitor.py
```

### 2. 测试游戏状态捕获
```cmd
cd C:\Godot\new-game-project-test-godot\.kiro\scripts\testing
python test_game_state.py
```

### 3. 分析项目图标
```cmd
cd C:\Godot\new-game-project-test-godot\.kiro\scripts\testing
python analyze_icon.py
```

## 📚 相关文档

- `.kiro/docs/RealtimeScreenshotMonitoring.md` - 实时监控系统详细文档
- `.kiro/docs/GodotMCPServer.md` - MCP 服务器文档
- `.kiro/docs/TestingGuide.md` - 测试指南和自动化测试
- `.kiro/specs/game-state-capture/` - 游戏状态捕获系统规范

## 🔄 文件整理历史

**2025-03-04**: 重新组织脚本文件夹
- 创建 `realtime_monitoring/` 文件夹
- 创建 `testing/` 文件夹
- 创建 `archived/` 文件夹
- 移动相关文件到对应文件夹
- 保留核心工具在根目录
