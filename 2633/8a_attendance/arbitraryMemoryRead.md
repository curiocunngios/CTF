# Arbitrary memory read 
to perform arbitrary memory read using format string, we can do something like:
`printf("%9$sAAAA\x30\xdd\xff\xff\xff\x7f\x00\x00");`, which:
- {{place the address we want to read i.e. `\x30\xdd\xff\xff\xff\x7f\x00\x00` on stack}}
- read it as {{9th argument}} using `%s` to {{read its content}}
- here first 8 bytes is {{`%9$sAAAA` with 'A's as padding to 8 bytes being the 8th argument}} 


To know the position of address we want to read:
- we first test with {{%p}}
- For example:
if
```c
print(AAAAAAAA-%5$p-%6$p-%7$p-%8$p-%9$p-%10$p-%11$p-%12$p)
```
shows
`AAAAAAAA`-<something here>-<something here>-<something here>-<something here>-`AAAAAAAA`-<something here>, then `AAAAAAAA` would be the 9th argument

