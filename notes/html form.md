---
aliases:
  - html form
tags:
  - flashcard/active/ctf
---

# html form example
```html
    <form role="form" action="login.php" method="post">
      <input type="text" name="username" placeholder="Username" required 
       autofocus></br>
      <input type="password" name="password" placeholder="Password" required>
      <button type="submit" name="login">Login</button>
    </form>
```
- <form> defines {{where data is sent}}
- action="login.php" means data (<input type= ....>) {{goes to login.php}}
- method="post" means data is {{sent privately}} <!--SR:!2024-12-14,1,230!2024-12-14,1,230!2024-12-14,1,230-->

