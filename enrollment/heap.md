Yes, it's normal to find heap addresses on the stack! This happens in several common scenarios:

1. Most commonly: When you have a pointer variable in a function
   ```c
   void func() {
       char *ptr = malloc(size);  // ptr is on stack, but contains heap address
   }
   ```

2. Function parameters that are pointers to heap-allocated memory
   ```c
   void func(char *heap_ptr) {  // heap_ptr stored on stack
       // ...
   }
   ```

3. Saved pointers to heap-allocated objects/structures
   ```c
   struct Something *obj = malloc(sizeof(struct Something));
   // obj is a local variable on stack, pointing to heap
   ```

The stack is where local variables live, and when those variables are pointers, they can contain:
- Heap addresses (from malloc)
- Stack addresses
- Global/data section addresses
- etc.

This is actually important for many heap exploitation techniques, as leaking heap pointers from the stack can help defeat ASLR or find useful heap chunks.