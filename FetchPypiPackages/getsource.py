import os
get = ("pyftpdlib","py2exe","wmi","pyzbar","qrcode","pyautogui","pandas","numpy","pip2pi","pygame","pyinstaller","requests","psutil","pynput","ttkthemes","pillow","opencv-python","python-tkdnd","matplotlib","bokeh","mitmproxy","chardet","uncompyle6","pydub","pyperclip","seaborn","send2trash","wxpython","rarfile")
for i in get:
    os.system("pip download " + i + " -i https://mirrors.cloud.tencent.com/pypi/simple --no-binary :all:")
