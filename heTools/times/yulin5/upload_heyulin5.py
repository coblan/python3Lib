#!python3
# -*- encoding:utf8 -*-
from urllib.request import urlopen,Request
from urllib.parse import quote,urlencode,parse_qs
import re,os,json
import sys
from string import Template

try:
    arg=sys.argv[1]
except IndexError as e:
    print(e)
    print('please input argments : local or web')
    sys.exit(0)
    # arg='local'
if arg=='web':
    url=r'http://5.yulinhe.sinaapp.com/upload/'
    recorde='time.txt'    
    
elif arg == 'local':
    url=r'http://127.0.0.1:8000/upload/'
    recorde='localtime.txt'    
else:
    print('please input argments : local or web')
    sys.exit(0)

path=r'D:\coblan\web\yulinhe\yulin5_pages'

#d={
    #'name':'pagetest3',
    #'catagory':'car',
    #'pagePro':'500',
    #'title':'TEST_UPLOAD',
    #'content':'this is test upload',
    #'detail':'详细说明的东西',
#}

# sys.path.append(r"D:\Program Files (x86)\JetBrains\PyCharm 4.5.3\debug-eggs\pycharm-debug-py3k.egg")

def main_run():
    # import wingdbstub

    # import pydevd
    # pydevd.settrace('localhost',port=45678, stdoutToServer=True, stderrToServer=True)
    ld=LocalDir(path)
    # 本地监视的目录对象，负责提供需要更新的文件
    for modefied in ld.get_absolte_files():

        # 页面对象，负责解析页面返回Job模型需要的各个参数
        p=Page(modefied)
        context=p.resolve()

        print(context)
        up=Up(context)
        # 上传对象，负责上传context对象
        up.post()

        print('green=>%s<=END'%modefied)
        
        
class Page(object):
    para=re.compile(r'<!--para==========(.*?)==========para-->',re.M|re.S)
    cont_mat=re.compile(r'<!--content-->(.*)<!--content-->',re.M|re.S)
    python_str=re.compile(r'<!--python_start-->(.*?)<!--python_end-->',re.M|re.S)

    def __init__(self,path):
        self.path=path
        self.context={}

    def resolve(self):
        with open(self.path,encoding='utf-8') as f:
            page=f.read()
        # 滤meta信息
        mt = self.para.search(page)
        self.context=eval(mt.group(1) )
        # 滤content
        mt2=self.cont_mat.search(page)
        self.context['content']=mt2.group(1)
        
        # 滤content_python语句
        self.python_pro()

        return self.context

    def python_pro(self):
        "处理模版中的python 语句"
        out=''
        content= self.context['content']
        loc={}
        end=0
        for mt in self.python_str.finditer(content):
            
            cmd=mt.group(1)
            exec(cmd,globals(),loc)
            out+=content[end:mt.start(0)]+loc.get('rt')
            end=mt.end(0)
        out+=content[end:len(content)]
        self.context['content']=out


# class TP(Template):
#     """产生一个新函数tp用于在模版中使用。
#         更改模版界定符为$$ ，免得同 jquery 冲突"""
#     delimiter = '$$'
#
#
# def tp(str_,mapping):
#     return TP(str_).safe_substitute(mapping)


# def test():
#     rr="""
# ls=[('xihua.jpg',
#     '<img src="english.jpg">4',
#     '2004年'),
# 	]
# rt=''
# for brand,special,detail in ls:
#     rt+= "{brand},{special},{detail}".format_map({'brand':brand,'special':special,'detail':detail})
#     """
#     dc={}
#     exec(rr,dc)
#     print(dc[rt])


class Up(object):
    def __init__(self,dct):
        self.dct=dct

    def get(self):
        response=urlopen(url)
        cookie_str=response.getheader('Set-Cookie')
        cookie=parse_qs(cookie_str)
        
        self.token = cookie.get('csrftoken',['',])[0]
        
        if self.token:
            print('token is \t'+self.token)
        else:
            print(response.getheaders())

    def post(self):
        
        # 懒得用上面获取的cookie的token，直接自己定义头，
        self.token='1234556'
        
        self.dct['csrfmiddlewaretoken']=self.token
        data=urlencode(self.dct).encode('utf-8')
        dc={'Cookie':'csrftoken=%s'%self.token}
        rq=Request(url,data,headers=dc)
        response=urlopen(rq,data)
        print(response.read())
        
    def __call__(self):
        #self.get()
        self.post()


class LocalDir(object):
    def __init__(self,path):
        self.path=path
        
        self.recode=os.path.join(path,recorde)
        if not os.path.exists(self.recode):
            with open(self.recode,'w') as f:
                pass
        with open(self.recode,'r') as f:
            try:
                self.times_recodes=json.load(f)
            except ValueError as e:
                print(e)
                self.times_recodes={}

    def get_absolte_files(self):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(('.html','.py')):
                    newpath=os.path.join(dirpath,filename)
                    time=os.path.getmtime(newpath)
                    if self.times_recodes.get(newpath,0)<time:
                        self.times_recodes[newpath]=time
                        yield newpath
            
        with open(self.recode,'w') as f:
            json.dump(self.times_recodes,f)


if __name__=='__main__':
    main_run()