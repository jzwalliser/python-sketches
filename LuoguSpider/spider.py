import re
import urllib.request,urllib.error
import bs4
import time

baseUrl = "https://www.luogu.com.cn/problem/P"
savePath = "D:/"
ok = ['1546', '1010', '1014', '1015', '1016', '1022', '1023', '1028', '1029', '1030', '1002', '1035', '1036', '1037', '1043', '1044', '1045', '1085', '1086', '1087', '1088', '1047', '1050', '1061', '1062', '1093', '1094', '1096', '1056', '1058', '1067', '1068', '1069', '1070', '1158', '1190', '1199', '1307', '1308', '1309', '1310', '1076', '1077', '1078', '1980', '1981', '1982', '1983', '2118', '2141', '2239', '2258', '2670', '2671', '2672', '1909', '2010', '2058', '2119', '3954', '3955', '3956', '3957', '5015', '5016', '5017', '5018']
wanted = ['3954', '2058', '1076', '1062', '2669', '1909', '1014', '1048', '2119', '1093', '1077', '1179', '1010', '1056', '2010', '1035', '1044', '1086', '1309', '1002', '1015', '1050', '2671', '2239', '5016', '1158', '1055', '1548', '1028', '1070', '1009', '1190', '1046', '2670', '1045', '1088', '1042', '5015', '2258', '1049', '3956', '1307', '1037', '1078', '2672', '1057', '2141', '1036', '1058', '1047', '3954', '2058', '1076', '1062', '2669', '1909', '1014', '1048', '2119', '1093', '1077', '1179', '1010', '1056', '2010', '1035', '1044', '1086', '1309', '1002', '1015', '1050', '2671', '2239', '5016', '1158', '1055', '1548', '1028', '1070', '1009', '1190', '1046', '2670', '1045', '1088', '1042', '5015', '2258', '1049', '3956', '1307', '1037', '1078', '2672', '1057', '2141', '1036', '1058', '1047', '1061', '1087', '1980', '1043', '3957', '1094', '1008', '1068', '2118', '5017', '1199', '1308', '1069', '1085', '1096', '1060', '1983', '1067', '1059', '1023', '1981', '1095', '3955', '1310', '1982', '1075', '1022', '5018', '1030', '1029']

title = ''


def main():
    global now
    for i in range(len(wanted)):
        i += 17
        time.sleep(2)
        print(wanted.index(wanted[i]),"正在爬取P{}...".format(wanted[i]),end="")
        try:
                html = getHTML(baseUrl + str(wanted[i]))
        except:
                html = 'error'
        if html == "error":
            print("爬取失败，可能是不存在该题或无权查看")
        else:
            now = wanted[i]
            problemMD = getMD(html)
            
            
            print("爬取成功！正在保存...",end="")
            saveData(problemMD,"P"+str(wanted[i])+".md")
            print("保存成功!")
    print("爬取完毕")

def getHTML(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
    }
    request = urllib.request.Request(url = url,headers = headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if str(html).find("Exception") == -1:        #洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"

def getMD(html):
    global title
    bs = bs4.BeautifulSoup(html,"html.parser")
    print('P' + str(now),bs.title.string[:-5])
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    title = 'P' + str(now) + ' ' + bs.title.string[:-5]
    return md

def saveData(data,filename):
    try:
        cfilename = savePath + title + '.md'
        file = open(cfilename,"w",encoding="gb2312")
        for d in data:
            file.writelines(d)
        file.close()
    except:
    	print('err',title)

if __name__ == '__main__':
    main()
