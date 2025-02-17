Let me break these down in simpler terms:

1. Function Pointers:
Think of a function pointer as a variable that can hold the address of a function, just like how a normal pointer can hold the address of data.

```c
// Regular function
void sayHello(char* message) {
    printf("Hello: %s\n", message);
}

int main() {
    // Regular variable holds data
    int number = 42;
    
    // Regular pointer holds address of data
    int* numberPointer = &number;
    
    // Function pointer holds address of function
    void (*funcPointer)(char*) = sayHello;
    
    // These two do the same thing:
    sayHello("World");        // Normal way
    funcPointer("World");     // Using function pointer
    
    return 0;
}
```

So when we write:
```c
typedef void (*speakFunc)(char*);
```
We're saying: "Create a new type called 'speakFunc' that represents pointers to functions that take a char* parameter and return void"

2. Enums (Enumeration):
An enum is just a way to give names to numbers. For example:

```c
enum DaysOfWeek {
    SUNDAY,    // Gets value 0
    MONDAY,    // Gets value 1
    TUESDAY,   // Gets value 2
    WEDNESDAY  // Gets value 3
};

int main() {
    enum DaysOfWeek today = MONDAY;
    
    // These are the same:
    if(today == MONDAY) { printf("It's Monday!\n"); }
    if(today == 1) { printf("It's Monday!\n"); }
    
    return 0;
}
```

3. Animal Structure:
Think of a structure as a container that can hold different types of data together. Like a form with different fields:

```c
struct Person {
    char* name;     // Field for name
    int age;        // Field for age
    float height;   // Field for height
};
```

In the Animal structure:
```c
struct Animal {
    speakFunc speak;    // This animal's way of making sound
    enum AnimalType type;    // What kind of animal is this
    char* name;    // This animal's name
};
```

Here's a real-world example:

```c
// Different animals make different sounds
void dogSpeak(char* sound) {
    printf("Dog barks: %s\n", sound);
}

void catSpeak(char* sound) {
    printf("Cat meows: %s\n", sound);
}

int main() {
    // Create two animals
    struct Animal dog;
    struct Animal cat;
    
    // Set up the dog
    dog.name = "Buddy";
    dog.speak = dogSpeak;    // Dog will use dogSpeak function
    
    // Set up the cat
    cat.name = "Whiskers";
    cat.speak = catSpeak;    // Cat will use catSpeak function
    
    // Make them speak
    dog.speak("Woof!");      // Prints: Dog barks: Woof!
    cat.speak("Meow!");      // Prints: Cat meows: Meow!
    
    return 0;
}
```

In this example:
- Each animal has its own name
- Each animal has its own way of speaking (different function)
- We can make any animal speak by using its speak function

It's like having different toys:
- A dog toy that barks when you press it
- A cat toy that meows when you press it
They both make sound (speak) but in different ways!

Does this help clarify things? Which part would you like me to explain further?