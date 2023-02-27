import ctypes
import subprocess
import sys

class disable_file_system_redirection:
    def __init__(self):
        self.is_64bits = sys.maxsize > 2**32
        self.old_value = None
    
    def __enter__(self):
        if self.is_64bits:
            self.old_value = ctypes.c_long()
            ctypes.windll.kernel32.Wow64DisableWow64FsRedirection(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.is_64bits and self.old_value is not None:
            ctypes.windll.kernel32.Wow64RevertWow64FsRedirection(self.old_value)

print('Top 10 files based on the size')
print('*******************************')

with disable_file_system_redirection():
    cmd = r'powershell.exe "Get-ChildItem C:\ -Recurse -ErrorAction SilentlyContinue | Sort-Object -Property Length -Descending | Select-Object -First 10"'
    result = subprocess.check_output(cmd, shell=True, text=True)
    print(result)
