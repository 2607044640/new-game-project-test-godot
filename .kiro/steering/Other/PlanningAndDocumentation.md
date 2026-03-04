---
inclusion: manual
---

# Planning & Documentation

## Planning Before Coding

### When to Stop and Think
- User mentions "design", "architecture", "how should we", "discuss"
- Feature involves multiple scenes/scripts (>3 files)
- Feature requires data structure changes
- Unclear requirements or conflicting information

### Create Temp Design Note
**Location:** `.kiro/TempFolder/[feature_name]_design.md`

```markdown
# [Feature Name] - Design Notes
**Date**: YYYY-MM-DD
**Status**: Planning Phase - No Code Yet

## Core Requirements
- [Bullet points of CORRECTED understanding]

## Architecture Decisions
- [Key design choices with rationale]

## Implementation Phases
- [ ] Phase 1: ...
- [ ] Phase 2: ...

## Open Questions
- Q: [Question]
- A: [Answer or TBD]
```

---

## Documentation Design Rules

### Keep Lean
- Short, concise sentences
- Don't oversimplify - preserve original meaning
- Delete ruthlessly: generic advice, contradictions, duplicates

### Keep Actionable
- **Bad:** "Be careful with null references"
- **Good:** "Check node exists: `if has_node("NodeName"):`"

### Default to Imperative Instructions
"Validate input: `if value > MAX: return`"
NOT: "Don't forget to validate"

### Provide Concrete Examples
Show, don't just tell.

---

## Game Plan Maintenance

**Update when:**
- Major game mechanic changes
- Architecture decisions made
- New systems added
- Design questions answered

**Don't update for:**
- Minor bug fixes
- Small script additions
- Implementation details

---

## Conversation Reset Summary

### When Fresh Session Starts

1. **Read Core Files:**
   - `.kiro/steering/MainRules.md`
   - `.kiro/steering/docLastConversationState.md`
   - `.kiro/steering/game-plan.md`

2. **Provide Status Summary:**
   - Working Systems
   - Active Issues
   - Next Priority
   - Architecture patterns
   - Focus Area

---

## Analysis First Rule

**Please don't write code first! Understand and check code logic first.**

1. Read extensively - follow function calls through entire system
2. Verify implementations - check actual behavior, not assumed behavior
3. Think about final vision and summarize project parts
4. For Godot: Check scene structure and node relationships
