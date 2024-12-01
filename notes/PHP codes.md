---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - PHP
  - programming 
  - coding
  - syntaxes
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

## About @ and _POST

```php
// 1. Get POST data
$hostname = @$_POST['hostname'];
// @ suppresses warnings if 'hostname' isn't set
// $_POST['hostname'] gets data from form submission

// 2. Check if hostname is set
if (isset($hostname)) {
    echo "<pre>";  // Format output as preformatted text
    // 3. Execute command
    passthru("ping -c 1 -W 1 $hostname");
    // passthru() executes command and outputs raw result
    echo "</pre>";
}

// Without @:
$hostname = $_POST['hostname'];
// If form not submitted, shows warning:
// "Notice: Undefined index 'hostname'"

// With @:
$hostname = @$_POST['hostname'];
// Silently returns null, no warning

Similar to:
try:
    input = some_dict['key']  # Python
except KeyError:
    pass
```


## $_POST vs Input Functions

```php
- Not exactly like cin/input()
- It's an associative array (like Python dictionary)
- Contains ALL POST data from form

PHP:                    Python equivalent:
$_POST['hostname']      form_data['hostname']

HTML form:
<input name="hostname">  <!-- Creates $_POST['hostname'] -->b
```


## <pre> tag 
```php
Normal text:
Line   1
Line     2

With <pre>:
Line   1
Line     2

<pre> preserves:
- Spaces
- Line breaks
- Formatting
```
![alt text](php_pre.png)

## passthru()
```php
// passthru() vs system():
system("ls");     // Returns last line of output
passthru("ls");   // Outputs everything directly

Similar to:
Python: os.system()
C++: system()

// It's like typing commands in terminal/command prompt,
// but from inside your code
```
## preg_match
preg_match is similar to {{re.match}} in python _(so what does it do?)_
```php
Example:
preg_match('/^[a-zA-Z0-9.-]+$/', 'google.com')    // Matches
preg_match('/^[a-zA-Z0-9.-]+$/', 'google;cat')    // No match

Similar to:
Python: re.match(r'^[a-zA-Z0-9.-]+$', hostname)
```
<!--SR:!2024-12-02,1,230-->

