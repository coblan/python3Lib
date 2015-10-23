from urllib.request import urlopen,build_opener,ProxyHandler,install_opener
from urllib import parse
from bs4 import BeautifulSoup
import threading,re,sys,time,os

import argparse 
parser = argparse.ArgumentParser() 
# 添加一个位置参数
parser.add_argument("-p", help="proxy s:http://216.12.198.102:8888 c: http://10.0.18.3:8888") 
parser.add_argument('-number',help =' 条数' ,type =int)
parser.add_argument('-url' ,help = 'url' )
args = parser.parse_args()
if not args.p:
    proxy_handler = ProxyHandler({})
elif args.p =='s':
    proxy_handler = ProxyHandler({"http" : 'http://216.12.198.102:8888'})
elif args.p =='c':
    proxy_handler = ProxyHandler({"http" : 'http://10.0.18.3:8888'})
else:
    proxy_handler = ProxyHandler({"http" : args.p})
  
print('代理服务器：%s'%args.p)
print('获取 %s条'%args.number)

opener = build_opener(proxy_handler)
install_opener(opener)

class Parser(object):
    def __init__(self,urls,count=9999999):
        self.urls = urls
        self.maxcount = count
        self._count = 0
        self.parsedUrl =[]
        self._imageCount =0 
        try:
            os.mkdir('ts')
        except FileExistsError:
            pass
        
    def dispath_work(self):
        
        for i in self.urls:
            t=threading.Thread(target=self.parse,args=(i,) )
            t.start()
        while True:
            if self._count>self.maxcount:
                time.sleep(0.1)
                break
    
    def parse(self,url):
        cntn_urls = [url,]
        while cntn_urls:
            self.parsedUrl = list(set(self.parsedUrl ))
            dog = cntn_urls
            cntn_urls = []
            for suburl in dog:
                urls = self.get_sub_urls(suburl)
                if urls:
                    cntn_urls.extend(urls)  
                
    def get_sub_urls(self,url):
        if self._count >self.maxcount:
            return
        try:
            ss = urlopen(url).read()
        except:
            return
        
        self._count+=1
        
        print(url)
        cntn_urls = []
        soup = BeautifulSoup(ss ,"html.parser")
        for i in soup.select('a'):
            urltext = i.get('href','')
            if not urltext.startswith('http'):
                urltext = parse.urljoin(url,urltext)
               
            if  urltext.startswith('http'):
                self.parsedUrl.append(urltext)
                cntn_urls.append(urltext)  
        self.save_imgs(url, soup)
        
        return cntn_urls
                
                
    def save_imgs(self,url, soup):
        for img in soup.select('img'):
            src = img.get('src','')
            if not src:
                continue
            elif not src.startswith('http'):
                 
                src = parse.urljoin(url,src)
                if self._count> self.maxcount:
                    return 
                try:
                    imgdata = urlopen(src).read()
                    self._count+=1
                except:
                    continue
                mt = re.search(r'\.(\w+)$',src)
                if not mt:
                    continue
                
                #global imgcount
                self._imageCount +=1
                with open(r'ts\image%s.%s'%(self._imageCount ,mt.group(1)), 'wb') as f:
                    print('----------- img %s'%src)
                    f.write(imgdata)
        
        
urls = ["http://www.hao123.com/","http://www.sina.com/","http://news.163.com/","http://www.sohu.com/","http://www.yixun.com/","http://home.sina.com/"]

if args.url:
    urls=[args.url,]
if args.number:
    ps = Parser(urls,args.number)
else:
    ps= Parser(urls)
ps.dispath_work()

sys.exit(0)



#  down is no action



totle_count = 0
max_count = 10

validUrl = []
imgcount =0 
def control_number():
    if max_count <0:
        return
    else:
        global totle_count
        totle_count+=1 
        if totle_count > max_count:
            sys.exit(0)    


#def get_urls(url):
    #ss = urlopen(url).read()
    #soup = BeautifulSoup(ss, "html.parser")
    #for i in soup.select('a'):
        #urltext = i.get('href','').strip()
        #if not re.match(r'^\W*http', urltext):
        
            #urltext = parse.urljoin(url,urltext)
            #if re.match(r'^\W*http', urltext):
                #yield urltext
        #else:
            #yield urltext

#for i in get_urls("http://www.sohu.com/"):
    #print(i)
#def save_img(url):
    




def getcntn_urls(url):
    cntn_urls = []
    ss = urlopen(url).read()
    print(url)
    control_number()
        
    soup = BeautifulSoup(ss ,"html.parser")
    for i in soup.select('a'):
        urltext = i.get('href','')
        if not urltext.startswith('http'):
        
            urltext = parse.urljoin(url,urltext)
           
        if urltext not  in validUrl and urltext.startswith('http'):
            validUrl.append(urltext)
            cntn_urls.append(urltext)
                
    
        
    
    for img in soup.select('img'):
        src = img.get('src','')
        if not src:
            continue
        elif not src.startswith('http'):
            src = parse.urljoin(url,src)
            try:
                imgdata = urlopen(src).read()
            except:
                continue
            
            control_number()
            
            mt = re.search(r'\.(\w+)$',src)
            if not mt:
                continue
            
            global imgcount
            imgcount+=1
            with open(r'D:\try\spiderimag\image%s.%s'%(imgcount,mt.group(1)), 'wb') as f:
                print('----------- img %s'%src)
                f.write(imgdata)

    return cntn_urls

def run(url):
    cntn_urls = [url,]
    global validUrl
    while cntn_urls:
        validUrl=list(set(validUrl))
        dog = cntn_urls
        cntn_urls = []
        for i in dog:
            
            dig = getcntn_urls(i)
            cntn_urls.extend(dig)

                    
run("http://www.hao123.com/")

#for i in urls:
    #t=threading.Thread(target=run,args=(i,) )
    #t.start()
    #jj.append(t)

#import time
#def getlen():
    #cnt = 0
    #while True:
        #cnt+=1
        #time.sleep(60)
        #with open("d:/cnt.txt",'a+') as f:
            #f.write("%s--%s\n"%(cnt,len(validUrl)))   


#getlen()
    