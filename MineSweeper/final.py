import codecs
f = codecs.open(input(),"r","utf-8")
c = f.read()
f.close()

change = (("4r4","\n"),("4bko4","("),("4n4","\n"),("4nt4","\n    "),("4ntt4","\n        ")
          ,("4nttt4","\n            "),("\t","    "),("4r4","\n"),("4rt4","\n    "),("4rtt4","\n        ")
          ,("4rttt4","\n            "),("4eq4","="),("4bkt4","()"),("4dq4","\""),("4bkc4",")"),
          ("4cbkc4","）"),("4bbo4","{"),("4bbc4","}"),("4times","*"),("4wild4","*"),("4mbt4","[]"),("4sm4","<"),("4bg4",">"),("4cbko4","（"),("4mbo4","["),("4mbc4","]"),("4,4","，"),
          ("4:4","："),("4plus4","+"),("4ul4","_"),("4rs4","\\"),("4!4","！"),("4.4","。"))

def replace_all(sth,a,b):
    for i in range(sth.count(a)):
        try:
            sth = sth.replace(a,b)
        except:
            pass
    return sth

for i in change:
    c = replace_all(c,i[0],i[1])

print(c)
