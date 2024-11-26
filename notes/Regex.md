---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - commands 
  - Regex
  - Regular expression
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# Regular Expressions Basics

## Character Classes
- `.` - Any character except line break
- `\w` - Letters, numbers, underscore
- `\d` - Digit
- `[a-z]` - Lowercase letters
- `[A-Z]` - Uppercase letters
- `[0-9]` - Numbers
- `[a-zA-Z0-9]` - Alphanumeric

## Quantifiers
- `+` - One or more
- `*` - Zero or more
- `?` - One or none
- `{5}` - Exactly 5 times
- `{3,7}` - 3 to 7 times

## Anchors
- `^` - Start of line/string
- `$` - End of line/string
- `[...]` - One character in brackets (?)
- `[^...]` - Not in brackets (?)

## Groups and Logic
- `|` - OR operator
- `(...)` - Capture group (?)
- `(?:...)` - Non-capture group (?)
- `\1` - Reference group 1

## Common Patterns
- Email: `^[a-z]{3,7}@(connect\.)?ust\.hk$`
- Avoid greedy matching: (?)
  - Use `[^}]*` instead of `.*`
  - Use `.*?` for lazy matching

## Testing Tools
- https://regex101.com/
- grep with regex: `grep -E 'pattern' file`