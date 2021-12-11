#!/usr/bin/python3

# Basic shellcode crypter for C# payloads
# By Cas van Cooten

import re
import platform
import argparse
import subprocess
from random import randint

if platform.system() != "Linux":
    exit("[x] ERROR: Only Linux is supported for this utility script.")

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Parse input arguments
def auto_int(x):
    return int(x, 0)

parser = argparse.ArgumentParser()
parser.add_argument("path", help="the path to load the raw shellcode payload from", nargs='?', default="/tmp/payload.bin")
parser.add_argument("format", help="the language to format the output in ('cs' or 'cpp')", nargs='?', default="cs")
parser.add_argument("encoding", help="the encoding type to use ('xor' or 'rot')", nargs='?', default="xor")
parser.add_argument("key", help="the key to encode the payload with (integer)", type=auto_int, nargs='?', default=randint(1,255))
args = parser.parse_args()

# Generate the shellcode given the input path
print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Generating payload for path {bcolors.OKGREEN}{args.path}{bcolors.ENDC}.")
try:
    with open(args.path, "rb") as f:
        payload = f.read()

except:
    exit(f'{bcolors.BOLD}{bcolors.FAIL}[-] Cannot read file: {args.path}{bcolors.ENDC}')

# Format the output payload
if args.format == "cs": 
    # Encode the payload with the chosen type and key
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Encoding payload with type {bcolors.OKGREEN}{args.encoding}{bcolors.OKBLUE} and key {bcolors.OKGREEN}{hex(args.key)}{bcolors.ENDC}")
    encodedPayload = []
    payloadFormatted = ""
    for byte in payload:
        byteInt = int(byte)

        if args.encoding == "xor":
            byteInt = byteInt ^ args.key
        elif args.encoding == "rot":
            byteInt = byteInt + args.key & 255
        else:
            exit(f"{bcolors.BOLD}{bcolors.FAIL}[x] ERROR: Invalid encoding type.{bcolors.ENDC}")

        encodedPayload.append("{0:#0{1}x}".format(byteInt,4))

    payLen = len(encodedPayload)
    encodedPayload = re.sub("(.{65})", "\\1\n", ','.join(encodedPayload), 0, re.DOTALL)
    payloadFormatted += f"// Payload {args.encoding}-encoded with key {hex(args.key)}\n"
    payloadFormatted += f"byte[] buf = new byte[{str(payLen)}] {{\n{encodedPayload.strip()}\n}};"
    if payLen > 1000:
        f = open("/tmp/payload.txt", "w")
        f.write(payloadFormatted)
        f.close()
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+]{bcolors.OKBLUE} Encoded payload written to {bcolors.OKGREEN}/tmp/payload.txt{bcolors.OKBLUE} in CSharp format!{bcolors.ENDC}")
    else:
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+]{bcolors.OKBLUE} Encoded payload (CSharp):{bcolors.ENDC}")
        print(payloadFormatted + "\n")

    print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Decoding function:{bcolors.ENDC}")
    if args.encoding == "xor":
        decodingFunc = f"""for (int i = 0; i < buf.Length; i++)
    {{
        buf[i] = (byte)((uint)buf[i] ^ {hex(args.key)});
    }}"""

    if args.encoding == "rot":
        decodingFunc = f"""for (int i = 0; i < buf.Length; i++)
    {{
        buf[i] = (byte)(((uint)buf[i] - {hex(args.key)}) & 0xFF);
    }}"""

    print(decodingFunc)

elif args.format == "cpp":
    # Encode the payload with the chosen type and key
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Encoding payload with type {bcolors.OKGREEN}{args.encoding}{bcolors.OKBLUE} and key {bcolors.OKGREEN}{hex(args.key)}{bcolors.ENDC}")
    encodedPayload = []
    payloadFormatted = ""
    for byte in payload:
        byteInt = int(byte)

        if args.encoding == "xor":
            byteInt = byteInt ^ args.key
        elif args.encoding == "rot":
            byteInt = byteInt + args.key & 255
        else:
            exit(f"{bcolors.BOLD}{bcolors.FAIL}[x] ERROR: Invalid encoding type.{bcolors.ENDC}")

        encodedPayload.append(f"\\x{byteInt:02x}")

    payLen = len(encodedPayload)
    encodedPayload = re.sub("(.{68})", "    \"\\1\"\n", ''.join(encodedPayload), 0, re.DOTALL)
    payloadFormatted += f"// Payload {args.encoding}-encoded with key {hex(args.key)}\n"
    payloadFormatted += f"unsigned char buffer[] = \n    {encodedPayload.strip()};"
    if payLen > 1000:
        f = open("/tmp/payload.txt", "w")
        f.write(payloadFormatted)
        f.close()
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+]{bcolors.OKBLUE} Encoded payload written to {bcolors.OKGREEN}/tmp/payload.txt{bcolors.OKBLUE} in C++ format!{bcolors.ENDC}")
    else:
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+]{bcolors.OKBLUE} Encoded payload (C++):{bcolors.ENDC}")
        print(payloadFormatted + "\n")

    # Provide the decoding function for the heck of it
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Decoding function:{bcolors.ENDC}")
    if args.encoding == "xor":
        decodingFunc = f"""char bufferx[sizeof buffer];
int i;
for (i = 0; i < sizeof bufferx; ++i)
    bufferx[i] = (char)(buffer[i] ^ {hex(args.key)});
        """

    if args.encoding == "rot":
        decodingFunc = f"""char bufferx[sizeof buffer];
int i;
for (i = 0; i < sizeof bufferx; ++i)
    bufferx[i] = (char)(buffer[i] - {hex(args.key)} & 255);
        """

    print(decodingFunc)

else:
    exit(f"{bcolors.BOLD}{bcolors.FAIL}[x] ERROR: Invalid formatting type (choose 'cs' for CSharp or 'cpp' for C++).{bcolors.ENDC}")