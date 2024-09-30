file = open("abc.txt","w")
while True:
    m = input()
    if m == "ex":
        break
    try:
        exec(m)
    except:
        print(m,file=file)
file.close()
