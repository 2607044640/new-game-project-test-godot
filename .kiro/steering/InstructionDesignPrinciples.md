---
inclusion: manual
---
# Documentation Design Rules

## Maintain Lean Information Density
- Keep sentences short and concise
- **Don't oversimplify** - preserve original meaning
- Delete ruthlessly: generic advice, contradictions, duplicates

## Keep Actionable
Bad: "Be careful with pointers"
Good: "Validate pointers before dereferencing: if (!ptr) return;"

## Default to Imperative Instructions
"Validate input: if (len > MAX) return;"
NOT: "Don't forget to validate"

Exception - Use prohibitions when:
- Blocking dangerous APIs: "Never use gets() - always use fgets()"
- The wrong thing is more concrete: "Don't commit generated files to /src"

## Positive guidance
Telling the model "what to do" is usually more efficient than telling it "not to do" through a long series of negative words.

## Structure with XML Tags
Use XML tags to separate distinct sections:
```xml
<instructions>
Your task-specific commands
</instructions>

<context>
Background information Claude needs
</context>

<examples>
Concrete demonstrations of desired output
</examples>
```

**Tag Guidelines:**
- Use consistent tag names throughout
- Nest tags for hierarchical content: `<outer><inner></inner></outer>`
- Reference tags by name: "Using the code in `<code>` tags..."
- Custom tag names are fine - make them descriptive

## Provide Concrete Examples
Show, don't just tell:
```xml
<example>
<input>User login with invalid password</input>
<expected_behavior>Return 401, log attempt, increment counter</expected_behavior>
</example>
```

Bad: "Handle errors properly"
Good: Include 2-3 examples showing error handling patterns

## Prioritize by Importance
Put must-know information at top. Move optional details to bottom.

## Anti-Noise Checklist
**Delete:**
- Generic advice AI already knows (textbook principles, common sense)
- Contradictory guidelines
- Duplicate information across files
- Excessive role-playing ("You are the world's best...")
- Over-engineering (longer ≠ better)