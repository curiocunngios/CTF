import locale
# change locale to zh_HK.UTF8: done

# process code.txt
with open("code.txt", "rb") as f:
    code = f.read().decode("utf-8")

i = 0
idx = 0 
int_arr = [0] * 100 #int_arr = (int *)calloc(100,4);
while (i < len(code)):
    chin_char = code[i]
    if chin_char == '肉':
        if (int_arr[idx] != 0):
            while code[i] != '⽵':
                i = i - 1
    elif chin_char == '竹':
        int_arr[idx] = int_arr[idx] + 1
    elif chin_char == '牛': 
        idx = (idx + 99) % 100
    elif chin_char == '山': 
        int_arr[idx] = ord('A') # idk just randomly give a char see how it goes 
    elif chin_char == '⾁':
        print(int_arr[idx])
    elif chin_char == '⽵':
        if int_arr[idx] == 0: 
            while code[i] != '肉':
                i = i + 1
    elif (chin_char == '⼭'):
        idx = (idx + 101) % 100
                  
    elif (chin_char == '⽜'): 
        int_arr[idx] = int_arr[idx] - 1
    i = i + 1

a = 0
b = 32
c = 0
result = [''] * 100
for j in range(21, 85, 2):
    if (c & 3 == 0) or (c % 4 == 3):
        result[a + 48] = chr(int_arr[j])
        result[b] = chr(int_arr[j+1])
    else:
        result[b] = chr(int_arr[j])
        result[a + 0x30] = chr(int_arr[j+1])
    a = a + 1
    b = b - 1
    c = c + 1

print(''.join(result[48:]) )
print(''.join(result[:32]) )

'''
┌──(kali㉿kali)-[~/Desktop/CTF/5A_attendance]
└─$ nc chal.firebird.sh 35025                          
What is the base64-decoded passcode?
ilovereverseengineering
Challenge idea: https://www.facebook.com/photo.php?fbid=390833422825667

暗號？
⼭竹牛⾁
Congratulations! Here's your flag:
'''




        
    