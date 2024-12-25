# �

context: puts reading raw bytes until 0x00 null terminator and keeps printing some `�`
The reason they appear as � is because these bytes:

    Aren't valid UTF-8/ASCII characters
    Terminal tries to interpret them as printable characters and fails
    Different terminals might show them differently

When you see �, it usually means you're seeing raw memory contents that include:

    Address values
    Stack contents
    Uninitialized memory
    Non-printable bytes

This is particularly useful in CTFs because these "garbage" values might actually be important memory addresses or other leaked information you can use.