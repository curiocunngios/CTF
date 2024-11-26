---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system 
  - Web
  - HTML
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---


```
1. HTML loads top to bottom:
   <head> loads first
     - Metadata
     - CSS (style.css)
   <body> loads next
     - Visual elements
     - Scripts

2. Scripts execute in order:
   <script src="secure.js">          // Loads first
   <script type="text/javascript">    // Runs second
     function filter(string) {...}    // Defines filter function
     window.username = "";            // Sets variables
     checkPassword(...);              // Uses function from secure.js

```