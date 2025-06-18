These are type definitions in C. Let's break them down:

1. `typedef struct Panda Panda;`
- Creates an alias where you can use `Panda` instead of `struct Panda`
- This is a forward declaration - it tells the compiler "there will be a struct called Panda later"

2. `typedef struct Parrot Parrot;`
- Same thing for Parrot struct

3. `typedef struct Animal Animal;`
- Same thing for Animal struct

4. `typedef void (*speakFunc)(char*);`
- This is defining a function pointer type named `speakFunc`
- It points to functions that:
  - Return void
  - Take a char* as parameter
  - Example usage:
```c
void bark(char* sound) {
    printf("%s\n", sound);
}

// Now you can do:
speakFunc dog_speak = bark;
// Instead of:
void (*dog_speak)(char*) = bark;

// And call it like:
dog_speak("woof");
```

This pattern is commonly used in C for polymorphism-like behavior. For example:
```c
struct Animal {
    speakFunc speak;  // Function pointer
    char* name;
};

void meow(char* sound) { printf("Meow %s\n", sound); }
void woof(char* sound) { printf("Woof %s\n", sound); }

int main() {
    Animal cat = {.speak = meow, .name = "Kitty"};
    Animal dog = {.speak = woof, .name = "Doggy"};
    
    cat.speak("purr");  // Prints: Meow purr
    dog.speak("bark");  // Prints: Woof bark
}
```