---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - File permission
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---


[type][owner][group][any user] _(why do we have these 3 types of users, what does a group owing a file even mean)_
- / d   rwx     rw-     r--
|   |
|   |
|   |_ (a folder)
|
|_ ( a file)

- / d ::: - means a file, d means a folder <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->
rwx ::: r = read, w = write, x = execute

`chmod` ::: CHange MODe. Command used to change permissions for a file or directory on a Unix machine.

`chmod` common usage exmaples ::: `chmod +x`, `chmod 777` {gives permission to everyone} (are there more examples?)

