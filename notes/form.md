---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - Web
  - Forms in web context
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---


```
<!-- This is a form -->
<form method="post">
    <input type="text" name="hostname">     <!-- Text box -->
    <input type="submit" value="Submit">    <!-- Submit button -->
</form>

Think of it like:
┌─── Web Form ──────────────┐
│ Enter hostname:           │
│ ┌────────────────┐       │
│ │google.com      │       │  <- Input box
│ └────────────────┘       │
│      [Submit]            │  <- Submit button
└─────────────────────────┘

When you click Submit:
1. Browser collects data:
   hostname = "google.com"
2. Sends to server
3. PHP receives in $_POST['hostname']

// in PHP it's $_POST that receives the form 
```