---
inclusion: manual
---

# Development Commands

## Godot Editor Shortcuts

### Running the Game
```
F5  - Run project
F6  - Run current scene
F7  - Step into (debugger)
F8  - Step over (debugger)
F9  - Toggle breakpoint
F10 - Step out (debugger)
```

### Scene Editing
```
Ctrl+S  - Save scene
Ctrl+D  - Duplicate node
Ctrl+Shift+D - Duplicate node with signals
Delete  - Delete selected node
```

### Script Editing
```
Ctrl+S  - Save script
Ctrl+Shift+F - Find in files
Ctrl+H  - Replace in files
Ctrl+Alt+F - Format code
```

---

## GDScript Development

### No Compilation Needed
- Save script with `Ctrl+S`
- Changes take effect immediately
- Test with `F5` or `F6`

### Debugging
```gdscript
# Print to Output panel
print("Debug message")

# Print with file/line info
print_debug("Debug with location")

# Print error
push_error("Error message")

# Print warning
push_warning("Warning message")

# Assert (stops execution if false)
assert(condition, "Assertion failed message")
```

---

## C# Development (If Using C#)

### Build Commands

**In Godot Editor:**
- Click "Build" button (top-right corner)
- Or: `Project > Tools > C# > Build Project`

**Command Line:**
```cmd
dotnet build
```

### After Build Errors
1. Check Output panel for error messages
2. Fix errors in code
3. Rebuild with "Build" button
4. If still failing, try: `Project > Tools > C# > Rebuild Project`

---

## Git Commands (Optional)

### Basic Workflow
```bash
git status
git add .
git commit -m "描述你的改动"
git push
```

### Godot-Specific .gitignore
Already configured in project. Ignores:
- `.godot/` folder (generated files)
- `*.import` files (can be regenerated)
- Build artifacts

---

## Troubleshooting

### Script Errors Not Showing
- Check Output panel (bottom of editor)
- Enable "Errors" tab in Output panel
- Check Debugger panel for runtime errors

### Scene Not Updating
- Save scene with `Ctrl+S`
- Reload scene: `Scene > Reload Saved Scene`
- Restart Godot Editor if needed

### Performance Issues
- Enable FPS display: `Debug > Visible FPS`
- Open Profiler: `Debug > Profiler`
- Check Monitor: `Debug > Monitor`
