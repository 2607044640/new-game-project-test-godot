---
inclusion: manual
---

# Development Tools & Generation

## Scene Creation

### Creating New Scenes
1. In Godot Editor: `Scene > New Scene`
2. Choose scene type:
   - 2D Scene (Node2D root)
   - 3D Scene (Node3D root)
   - User Interface (Control root)
   - Other Node (custom root)

### Scene Templates
Create reusable scene templates:
1. Create and configure scene
2. Save as `.tscn` file
3. Instance in other scenes with `Ctrl+Shift+A` > "Instance Child Scene"

---

## Script Generation

### Creating New Scripts
1. Right-click node in Scene tree
2. Select "Attach Script"
3. Choose:
   - Language: GDScript or C#
   - Template: Empty, Node, CharacterBody2D, etc.
   - Path: Where to save script

### Script Templates
**Basic Node Script:**
```gdscript
extends Node

func _ready():
    pass

func _process(delta):
    pass
```

**Basic Node2D Script:**
```gdscript
extends Node2D

func _ready():
    pass

func _process(delta):
    pass
```

---

## Resource Creation

### Creating Custom Resources
1. Create new script extending `Resource`
2. Add `@export` variables for data
3. Save as `.tres` or `.res` file

**Example:**
```gdscript
extends Resource
class_name CellData

@export var shape_type: ShapeType
@export var state: CellState
@export var position: Vector2i

enum ShapeType { TRIANGLE, SQUARE, CIRCLE }
enum CellState { HIDDEN, REVEALED, MATCHED }
```

---

## Asset Import

### Importing Images
- Drag and drop into FileSystem panel
- Godot auto-generates `.import` files
- Configure import settings in Import panel

### Import Presets
- Texture: For sprites and UI
- 2D Pixel: For pixel art (disable filter)
- Normal Map: For 3D normal maps

---

## Debugging Tools

### Built-in Debugger
- Set breakpoints with `F9`
- Run with debugger: `F5`
- Step through code: `F7`, `F8`, `F10`
- Inspect variables in Debugger panel

### Remote Debugging
- Enable: `Debug > Deploy with Remote Debug`
- Connect to running game instance
- Useful for mobile/web builds

---

## Export/Build

### Export Project
1. `Project > Export`
2. Add export template for target platform
3. Configure export settings
4. Click "Export Project"

### Export Templates
Download from: `Editor > Manage Export Templates`

---

## Useful Plugins

### Built-in Plugins
- Enable in: `Project > Project Settings > Plugins`
- Examples: Version Control, Asset Library

### Community Plugins
- Browse: `AssetLib` tab in editor
- Install directly from Asset Library
