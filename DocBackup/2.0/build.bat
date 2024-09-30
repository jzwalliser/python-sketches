pyinstaller -F -w --hidden-import psutil backup.py
pyinstaller -F -w --hidden-import tkinter --uac-admin gui.py