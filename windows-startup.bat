# install the program to a folder in the user dir
mkdir C:\Users\%username%\.1dsync
xcopy * C:\Users\%username%\.1dsync

# creates the init script file
echo start pythonw C:\Users\%username%\.1dsync\1dsync.py > "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\1dsync.bat"

echo Ok!
