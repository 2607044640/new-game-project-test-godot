---
inclusion: manual
---
# Bug Investigation Protocol

## Three-Strike Rule
Attempt to fix bug 3 times maximum. On 3rd failure:
1. Stop attempting fixes
2. Generate Gemini query using template below
3. Present query in code block for user to copy

## Gemini Query Template

```
# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows

## Problem
[One sentence description]

## What I Tried
1. [First attempt and result]
2. [Second attempt and result]
3. [Third attempt and result]

## Current Code
```csharp
[Paste relevant code section]
```

## Logs
```
[Paste relevant log output]
```

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Question
[Specific question for Gemini]
```

## Investigation Steps
1. Read error logs first
2. Add targeted debug logging
3. Test one change at a time
4. Check compilation after each edit

## When to Escalate
- Same error after 3 different approaches
- Unclear error messages with no documentation
- Suspected engine/platform bug
- Deadlock or timing issues without clear cause
