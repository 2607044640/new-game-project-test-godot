---
inclusion: manual
---

# Investigation Guides

## Bug Investigation

### Testing Workflow
- Press `F5` in Godot Editor to run project
- Press `F6` to run current scene
- Check Output panel for errors and warnings

### Tools
- Use `print()` for debug output
- Use `print_debug()` to include file/line info
- Use `push_error()` for error messages
- Check Godot's Output panel and Debugger

### Common Issues
1. **Node not found errors**
   - Check: Node path is correct (`$NodeName` or `get_node("NodeName")`)
   - Fix: Use `has_node()` before accessing

2. **Signal connection errors**
   - Check: Signal exists and signature matches
   - Fix: Use `connect()` with correct parameters

3. **Null reference errors**
   - Check: Node/resource is initialized before use
   - Fix: Add null checks: `if node != null:`

---

## Performance Investigation

### Quick Checklist (Check First!)

1. **_process() or _physics_process() enabled?**
   - Check: Are these functions defined but not needed?
   - Fix: Remove unused process functions
   - Impact: Unnecessary per-frame overhead

2. **Too many nodes in scene?**
   - Check: Scene tree depth and node count
   - Fix: Use CanvasItem.visible = false to hide instead of removing
   - Fix: Pool and reuse nodes instead of creating/destroying

3. **Expensive operations in _process()?**
   - Check: Are you doing heavy calculations every frame?
   - Fix: Use timers or call_deferred() for non-critical updates
   - Fix: Cache results when possible

4. **Too many draw calls?**
   - Check: Number of separate sprites/textures
   - Fix: Use texture atlases
   - Fix: Batch similar objects

### Iterative Fix Loop
```
1. Modify code → 2. Save → 3. Press F5 → 4. Check Output → 5. Check FPS (Debug > Visible FPS)
If FPS < 60 → Go to step 1
If FPS ≥ 60 → Success! ✅
```

### Performance Targets
- **60 FPS:** 16.67ms per frame
- **Process time:** Should be <10ms
- **Physics time:** Should be <5ms

### Profiling Tools
- Debug menu: `Debug > Visible FPS`
- Profiler: `Debug > Profiler`
- Monitor: `Debug > Monitor`

---

## Code Design Problem Investigation

### When User Reports Design Issues

1. **Understand Root Cause**
   - Why did I choose this approach initially?
   - What assumption was wrong?

2. **Check Related Code**
   - Caller functions - how is this used?
   - Similar patterns - is this mistake repeated elsewhere?

3. **Propose Systematic Improvement**
   - Identify the design pattern that should be used
   - Check if other code needs the same refactor

---

## Deep Search Protocol

**Never guess APIs or function signatures. Search first, code second.**

### Multi-Query Triangulation
Generate 3+ diverse queries for the same problem:
```
Query 1: "Godot 4 grid system tutorial"
Query 2: "Godot TileMap vs GridContainer"
Query 3: "Godot 2D array grid implementation"
```

### Source Priority
1. Official Godot docs (docs.godotengine.org)
2. Codebase usage (patterns that already work)
3. Godot source code (github.com/godotengine/godot)
4. Forum posts (Godot Q&A, Reddit)
5. Community solutions (validate before using)
