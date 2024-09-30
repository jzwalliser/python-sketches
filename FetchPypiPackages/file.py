packages = ("pygame","pyinstaller","requests","psutil","pynput","ttkthemes","pillow","opencv-python","python-tkdnd","matplotlib","bokeh","mitmproxy","chardet","uncompyle6","pydub","pyperclip","seaborn","send2trash","wxpython","rarfile","pyftpdlib","py2exe","wmi","pyzbar","qrcode","pyautogui","pandas","numpy","pip2pi")
pip = input("pip: ")
import os
mirror = input("mirror: ")
for i in packages:
    os.system("pip download -i" + mirror + " " + i)
