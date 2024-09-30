f=open('/storage/emulated/0/0temp/new.py' ,'rb')
n = 0;
s = f.read(1)
while s:
        byte = ord(s)
        n = n+1
        if n % 16 == 1:
            print(hex(n//16)[2:] + '0   ', end='')
        print(hex(byte)[2:],end=',')
        if n%16==0:
                print('')
        s = f.read(1)
print('\n\ntotal bytes: %d'%n)
f.close()