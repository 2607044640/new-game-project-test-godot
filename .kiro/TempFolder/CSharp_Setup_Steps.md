# Godot C# 设置和测试步骤

## 当前状态
- ✅ 已创建测试脚本：`Scripts/TestScript.cs`
- ⏳ 需要在Godot编辑器中初始化C#项目

## 详细步骤（请按顺序执行）

### 步骤1：在Godot编辑器中初始化C#支持

1. **打开Godot编辑器**
   - 双击打开项目（如果还没打开）

2. **创建测试场景**
   - 点击 `Scene > New Scene`
   - 选择 "Other Node"
   - 在弹出的对话框中选择 `Node`
   - 点击 "Create"

3. **附加C#脚本到节点**
   - 确保场景树中的 `Node` 被选中
   - 在右侧 Inspector 面板中，点击脚本图标（或右键节点 > "Attach Script"）
   - 在弹出的对话框中：
     - **Language**: 选择 `C#`
     - **Path**: 输入 `res://Scripts/TestScript.cs`
     - 点击 "Load"（因为文件已存在）
   
4. **Godot会自动生成C#项目文件**
   - 这时Godot会创建 `.csproj` 和 `.sln` 文件
   - 你会在编辑器右上角看到一个 "Build" 按钮

5. **保存场景**
   - `Scene > Save Scene`
   - 命名为 `TestScene.tscn`
   - 保存在项目根目录

### 步骤2：编译C#代码

**方法1：在Godot编辑器中编译（推荐新手）**
- 点击右上角的 "Build" 按钮
- 等待编译完成（通常2-5秒）
- 查看底部 Output 面板，确认没有错误

**方法2：使用命令行编译**
```cmd
dotnet build
```

### 步骤3：运行测试

1. **运行场景**
   - 按 `F6` 键（运行当前场景）
   - 或点击右上角的播放按钮

2. **查看输出**
   - 在底部的 Output 面板中
   - 你应该看到：`nicework!`

### 步骤4：设置为主场景（可选）

如果你想按 `F5` 直接运行：
1. `Project > Project Settings > Application > Run`
2. 设置 `Main Scene` 为 `res://TestScene.tscn`

## 常见问题

### Q: 看不到 "Build" 按钮？
A: 需要先附加一个C#脚本到场景中的节点，Godot才会生成C#项目文件。

### Q: 编译失败？
A: 
1. 确保安装了 .NET SDK（.NET 6.0 或更高版本）
2. 在命令行运行 `dotnet --version` 检查
3. 如果没有安装，从 https://dotnet.microsoft.com/download 下载

### Q: 看不到 "nicework!" 输出？
A: 
1. 确保 Output 面板是打开的（View > Output）
2. 确保脚本已正确附加到节点
3. 确保场景已保存并运行

## 下一步

完成测试后，我们可以开始创建游戏的核心架构！
