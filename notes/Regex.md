---
aliases:
  - REgex
tags:
  - flashcard/active/ctf
---

# Regular Expressions Basics

## Character Classes
- `.` :: Any character except line break <!--SR:!2024-12-15,1,230-->
- `\w` :: Letters, numbers, underscore <!--SR:!2024-12-15,1,230-->
- `\d` :: Digit <!--SR:!2024-12-15,1,230-->
- `[a-z]` :: Lowercase letters <!--SR:!2024-12-18,4,270-->
- `[A-Z]` :: Uppercase letters <!--SR:!2024-12-18,4,270-->
- `[0-9]` :: Numbers <!--SR:!2024-12-18,4,270-->
- `[a-zA-Z0-9]` :: Alphanumeric <!--SR:!2024-12-15,1,230-->

## Quantifiers
- `+` :: One or more <!--SR:!2024-12-15,1,230-->
- `*` :: Zero or more <!--SR:!2024-12-15,1,230-->
- `?` :: One or none <!--SR:!2024-12-15,1,230-->
- `{5}` :: Exactly 5 times <!--SR:!2024-12-18,4,270-->
- `{3,7}` :: 3 to 7 times <!--SR:!2024-12-15,1,230-->

## Anchors
- `^` :: Start of line/string <!--SR:!2024-12-15,1,230-->
- `$` :: End of line/string <!--SR:!2024-12-15,1,230-->
- `[...]` :: One character in brackets <!--SR:!2024-12-18,4,270-->
- `[^...]` :: Not in brackets <!--SR:!2024-12-18,4,270-->

## Groups and Logic
- `|` :: OR operator <!--SR:!2024-12-15,1,230-->
- `(...)` :: Capture group <!--SR:!2024-12-15,1,230-->
- `(?:...)` :: Non-capture group <!--SR:!2024-12-15,1,230-->
- `\1` :: Reference group 1 <!--SR:!2024-12-18,4,270-->

## Common Patterns
- Email :: `^[a-z]{3,7}@(connect\.)?ust\.hk$` <!--SR:!2024-12-15,1,230-->
- Avoid greedy matching:
??
- Use `[^}]*` instead of `.*`
- Use `.*?` for lazy matching <!--SR:!2024-12-15,1,230-->

## Testing Tools
- https://regex101.com/
- grep with regex: `grep -E 'pattern' file`