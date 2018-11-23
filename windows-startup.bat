mkdir C:\Users\%username%\.1dsync
robocopy . C:\Users\%username%\.1dsync /E

attrib +h C:\Users\%username%\.1dsync

echo start pythonw C:\Users\%username%\.1dsync\1dsync.py > "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\1dsync.bat"

echo Ok!
