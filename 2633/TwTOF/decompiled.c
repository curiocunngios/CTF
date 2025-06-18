
void read_flag(void)

{
    int iVar1;
    char *pcVar2;
    code *UNRECOVERED_JUMPTABLE;
    char *pcVar3;

    syscall();
    syscall();
    syscall();
    iVar1 = strcmp(&heard_msg, &msg3);
    if (iVar1 == 0)
    {
        if ((true) || (false))
        {
            syscall();
        }
        else
        {
            syscall();
            syscall();
        }
    }
    else
    {
        syscall();
    }
    pcVar2 = (char *)0x0;
    syscall();
    pcVar3 = (char *)0x0;
    while (true)
    {
        syscall();
        if (*pcVar3 == '\n')
            break;
        pcVar2 = pcVar3 + 1;
        pcVar3 = pcVar3 + 1;
    }
    /* WARNING: Could not recover jumptable at 0x0010106a. Too many branches */
    /* WARNING: Treating indirect jump as call */
    (*UNRECOVERED_JUMPTABLE)(pcVar3, pcVar2, 1, UNRECOVERED_JUMPTABLE);
    return;
}

void format_hex(char *param_1, ulong param_2)

{
    ulong uVar1;
    int iVar2;

    iVar2 = 0x10;
    do
    {
        uVar1 = param_2 >> 0x3c;
        param_2 = param_2 << 4 | uVar1;
        *param_1 = "\nTwT: TwT: ERROR, FLAG FILE MISSING OR EMPTY\n0123456789abcdef./flag.txt"
            [uVar1 + 0x2d];
        param_1 = param_1 + 1;
        iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    /* WARNING: Treating indirect jump as return */
    return;
}

undefined8 main(void)

{
    int iVar1;
    undefined8 uStack0000000000000020;
    undefined8 in_stack_00000028;

    syscall();
    syscall();
    uStack0000000000000020 = 0x10114c;
    format_hex(&stack0x00000010, &stack0x00000010, 0x19);
    syscall();
    syscall();
    in_stack_00000028 = 0x10118e;
    format_hex(&stack0x00000010, main, 0x11);
    syscall();
    syscall();
    syscall();
    gets(&stack0x00000010);
    iVar1 = strcmp(&heard_msg, &msg3);
    if (iVar1 == 0)
    {
        syscall();
        read_flag(1, &msg5, 0x18);
    }
    else
    {
        syscall();
    }
    /* WARNING: Treating indirect jump as return */
    return 0;
}
