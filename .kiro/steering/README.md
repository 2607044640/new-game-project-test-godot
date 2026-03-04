---
inclusion: manual
---

# Steering Files Index

**Purpose:** AI behavior rules and instructions only
**Documentation moved to:** `.kiro/docs/`

## Always Included (Auto-loaded)
| File | Purpose |
|------|---------|
| `MainRules.md` | Core principles, Godot workflow, testing |
| `game-plan.md` | 游戏开发计划和技术架构 |

## Manual Include (Use `#FileName` in chat)
| File | Purpose |
|------|---------|
| `InvestigationGuides.md` | Bug, performance, design problem investigation |
| `PlanningAndDocumentation.md` | Planning workflow, documentation rules |
| `ToolsAndGeneration.md` | Godot scene/script generation tools |
| `ConversationReset.md` | Session initialization protocol |
| `InstructionDesignPrinciples.md` | How to write effective steering rules |
| `dev-commands.md` | Godot development commands |

## Folders
- `TempPlan/` - Temporary planning documents
- `BugFixLogs/` - Bug fix records (.txt to avoid auto-inclusion)

## Usage
- Type `#ConversationReset` to trigger initialization protocol
- Type `#InvestigationGuides` when debugging issues
- Type `#game-plan` to review game development plan

## Project Documentation
For architecture, system guides, and references, see `.kiro/docs/`
