---
aliases:
  - linux permissions
  - file permission
tags:
  - flashcard/active/ctf/yo
---

```json
[type][owner][group][any user] _(why do we have these 3 types of users, what does a group owing a file even mean)_
- / d   rwx     rw-     r--
|   |
|   |
|   |_ (a folder)
|
|_ ( a file)
```
\-, d :: \- means a file, d means a folder <!--SR:!2024-12-17,3,250-->
rwx ::: r = read, w = write, x = execute <!--SR:!2024-12-17,3,246!2024-12-17,3,246-->

`chmod` :: CHange MODe. Command used to change permissions for a file or directory on a Unix machine. <!--SR:!2024-12-17,3,250-->

`chmod` common usage exmaples :: `chmod +x`, `chmod 777` {gives permission to everyone} (are there more examples?) <!--SR:!2024-12-17,3,246-->

