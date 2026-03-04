---
inclusion: manual
---

# Conversation Reset Protocol

## When Fresh Session Starts

### Step 1: Read State File
1. Read `.kiro/steering/docLastConversationState.md` (if exists)
2. Read `#MainRules.md`
3. Read `#game-plan.md`

### Step 2: Verify Understanding
- What was the last task?
- What systems are working?
- What's the next priority?
- What scenes/scripts exist?

### Step 3: Continue or Confirm
- If state is clear → Continue from last task
- If unclear → Ask user for clarification

---

## When Conversation Gets Long

### Step 1: Write State to File
Write current state to `.kiro/steering/docLastConversationState.md`:
- **Clear entire file contents**, rewrite from scratch (avoid Token accumulation)
- Use template format below

### Step 2: Update Documentation (Optional)
If major architecture changes occurred, update:
1. `.kiro/steering/docLastConversationState.md` - Current state
2. `.kiro/steering/game-plan.md` - Game development plan (if design changed)
3. `.kiro/docs/` - Any architecture documentation

---

## docLastConversationState.md Template

```markdown
# Last Conversation State
*Updated: [Date]*

## Project Status
- **Engine:** Godot Engine
- **Language:** GDScript (or C#)
- **Project Type:** [Game type]
- **Phase:** [Current development phase]

## Active Goals
**Next Tasks:**
1. [Task with specific steps]
2. [Next task]

**Reason:** [Why this approach]

## Critical Context
**Key Scenes:**
- `path/to/scene.tscn` - [Purpose]

**Key Scripts:**
- `path/to/script.gd` - [Purpose]

**Breaking Changes:**
- [Recent changes affecting code]

**Architecture Pattern:**
- [How systems connect]

## Recent Conversation Summary
1. [What was accomplished]
2. [What was decided]
3. [What's pending]

## Documentation Updated
- [List of updated files]
```
