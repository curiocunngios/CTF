# _IO_stdin_used 
_IO_stdin_used is a {{special symbol used by glibc (GNU C Library)}}
- It acts as a {{Marker}}
- It helps the C runtime (initialization code) know if the program uses {{stdio functions}}
- If this symbol exists, the runtime knows it needs to {{initialize stdio streams (stdin, stdout, stderr)}}

