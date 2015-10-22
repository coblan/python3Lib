from urllib.request import urlopen,build_opener,ProxyHandler,install_opener
from urllib import parse
from bs4 import BeautifulSoup
import threading,re
proxy_handler = ProxyHandler({"http" : 'http://216.12.198.102:8888'})
#proxy_handler = ProxyHandler({"http" : 'http://10.0.18.3:8888'})
#proxy_handler = ProxyHandler({})

opener = build_opener(proxy_handler)
install_opener(opener)


urls = ["http://www.hao123.com/","http://www.sina.com/","http://news.163.com/","http://www.sohu.com/","http://www.yixun.com/","http://home.sina.com/"]
#jj=[]
validUrl = []
imgcount =0 
def getcntn_urls(url):
    cntn_urls = []
    ss = urlopen(url).read()
    #print(url)
    #validUrl.append(url)
    soup = BeautifulSoup(ss)
    for i in soup.select('a'):
        urltext = i['href']
        if not urltext.startswith('http'):
            try:
                urltext = parse.urljoin(url,i)
            except:
                pass

        try:
            if urltext not  in validUrl:
                validUrl.append(urltext)
                cntn_urls.append(urltext)
                print(urltext)
            else:
                continue
        except:
            pass
    
    for img in soup.select('img'):
        src = img['src']
        if not src.startswith('http'):
            try:
                src = parse.urljoin(url,src)
            except:
                pass 
        try:
            imgdata = urlopen(src).read()
            mt = re.search(r'\.(\w+)$',src)
            if not mt:
                continue
            
            global imgcount
            imgcount+=1
            with open(r'D:\try\spiderimag\image%s.%s'%(imgcount,mt.group(1)), 'wb') as f:
                print('----------- img %s'%src)
                f.write(imgdata)
        except:
            pass
    return cntn_urls

def run(url):
    cntn_urls = [url,]
    global validUrl
    while cntn_urls:
        validUrl=list(set(validUrl))
        dog = cntn_urls
        cntn_urls = []
        for i in dog:
            try:
                dig = getcntn_urls(i)
                cntn_urls.extend(dig)
            except:
                pass
            
            


for i in urls:
    t=threading.Thread(target=run,args=(i,) )
    t.start()
    #jj.append(t)

import time
def getlen():
    cnt = 0
    while True:
        cnt+=1
        time.sleep(60)
        with open("d:/cnt.txt",'a+') as f:
            f.write("%s--%s\n"%(cnt,len(validUrl)))   


getlen()
    