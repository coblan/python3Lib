#!python3
import argparse
import os,re,sys

parse = argparse.ArgumentParser()
parse.add_argument('dir')
args=parse.parse_args()
print('分析目录：%s'%args.dir)
if not os.path.exists(args.dir):
    print('目录不存在')
    sys.exit(1)
    
foreignkey_pat = re.compile('ForeignKey')
model_pat=re.compile(r'^class (\w+)\(models.Model\):',re.M )


def count_pt(pat,text):
    cnt = 0
    for i in pat.finditer(text):
        cnt +=1
    return cnt


foreignkey = {}
models={}
for r,d,f in os.walk(args.dir):
    for filename in [x for x in f if x=='models.py']:
        fullpath= os.path.join(r,filename)
        with open(fullpath,encoding='utf8') as pyfile:
            text = pyfile.read()
        if 'text' in locals():
            foreignkey[fullpath] = count_pt(foreignkey_pat,text)
            models[fullpath] = count_pt(model_pat,text)


#def test():
    #text = "class ddd(models.Model):\n\tdd"
    #print(count_pt(model_pat,text))
#test()


def sort_dict(dc):
    ls = list(dc.items())
    ls.sort(key= lambda x: x[1],reverse= True)
    return ls
for i in sort_dict(foreignkey):
    print(i)
print('='*30)
for i in sort_dict(models):
    print(i)
    
#ls = list( foreignkey.items() )
#ls.sort(key=lambda x:x[1],reverse=True)
#for i in ls:
    #print(i)
