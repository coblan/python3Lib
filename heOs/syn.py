#!python3
# -*- coding:utf-8 -*-

"""
syn_copy(_from,_to,except_=None,except_name=func_copy) :
      见函数docstring
"""

import sys,os
from os.path import *
import heOs.path as hePath

def main():
##    for k in walk(r'D:\try\scrapy'):
##        print(k)
    syn_copy(r'D:\try\test',r'D:\try\testsyn')
    

def cmpDir(x,y):
    try:
        s=relpath(x,y)
    except:
        s=""
    if s.endswith(r".."):
        return 1
    elif s and not s.startswith(".."):
        return -1
    else:
        return 0

def not_modefied(_from,_to):
    """简便函数，用作copy的默认判断函数，能够判断修改时间的先后"""
    try:
        return getmtime(_from)<getmtime(_to)
    except OSError as e:
        return False
    
##    if QFile.exists(_to) and \
##       QFileInfo(_from).lastModified()<=QFileInfo(_to).lastModified():
##        return True


def syn_copy(_from,_to,except_=None,except_name=not_modefied):
    """同步拷贝。_from:样板目录；_to:修正目录；
    except:func(from_dir_name),传入_from中的目录名，return True时改目录不被处理，也就不会同步；
    except_name:func(from_name,to_name),传入的from_name文件名或目录是肯定存在的，to_name是目标路径(当前不一定存在)
                return True 时，文件/目录不被拷贝，注意:如果是目录，其子孙文件同样会被处理"""
    for root,dirs,files in walk(_from,except_):
        rel=relpath(root,_from)
        root_to=normpath(join(_to,rel))
        if not except_name or not except_name(root,root_to):
            try:
                os.mkdir(root_to)
            except:
                pass
        for ii in dirs:
            drnm=normpath(join(root_to,ii))
            if not except_name or not except_name(join(root,ii),drnm):
                try:
                    os.mkdir(drnm)
                    print("创建文件夹:"+drnm)
                except:
                    pass
        for jj in files:
            flnm=normpath(join(root_to,jj))
            if not except_name or not except_name(join(root,jj),flnm):
                try:
                    if exists(flnm):
                        os.remove(flnm)
                    if hePath.copy(join(root,jj),flnm):
                        print("复制文件 :从"+join(root,jj)+"到---->>>"+flnm)
                except Exception as e:
                    print("复制文件  %s错误, 错误为:%s"%(flnm,e))


def delDir(dir_,except_=None,except_name=None):
    """该函数用于删除某个目录
    dir_:需要被删除的目录名
    except_:func(dir_name)一个函数，接受目录名,return True，该目录名中所有文件都不会在删除列表中
    except_name:fun(name)，函数，接受文件名或目录名,return True，该文件或目录确定不会被删除
    用法，使用except_函数控制整个文件夹的删除与否。使用except_name控制单个文件的删除与否
"""
    del_dirs=[]
    del_files=[]
    for root,dirs,files in walk(dir_,except_):
        for ii in dirs:
            if not except_name or not except_name(join(root,ii)):
                del_dirs.append(join(root,ii))
        for jj in files:
            if not except_name or not except_name(join(root,jj)):
                del_files.append(join(root,jj))
    for ii in del_files:
        try:
            os.remove(ii)
            print("已经删除文件:"+ii)
        except Exception as e:
            print("删除文件 %s 错误,原因:%s"%(ii,e))
    del_dirs.sort(reverse=True)
    for jj in del_dirs:
        try:
            os.rmdir(jj)
            print("已经 删除文件夹:"+jj)
        except :
            pass
            #try:
                #delDir(jj)
            #except Exception,e:
                #print("删除文件夹 %s 错误,原因:%s"%(jj,e))
    try:
        os.rmdir(dir_)
        print("成功删除了文件夹: "+dir_)
    except:
        pass
        #print("删除文件夹 %s 错误 :%s"%(dir_,e))


def syn_del(_from,_to,except_=None,except_name=None):
    """该函数用于同步_from与_to目录，如果_to中的某些文件或文件夹在_from不存在，应该删除。
    _from:样本目录;_to:修正目录
    except:func(dir_name),函数，接受_to中的文件目录名,return True，改文件夹不会被修正
    except_name:func(from_name,to_name),函数，接受文件或目录名，return True，该文件或裸目录不会被修正。\
由于遍历的是_to目录，所以to_name是肯定存在的，from_name是组合出来的，可以判断from_name文件是否存在从而判断是否删除to_name
"""
    del_dirs=[]
    del_files=[]
    print("正在整理目录"+"...")
    for root,dirs,files in walk(_to,except_):
        root_from=normpath(join(_from,relpath(root,_to)))

        for ii in dirs:
            from_now=os.path.join(root_from,ii)
            to_now=join(root,ii)
            if (not except_name or not except_name(from_now,to_now)) \
               and not QFileInfo(from_now).exists():
                del_dirs.append(to_now)

        for jj in files:
            from_now=join(root_from,jj)
            to_now=join(root,jj)
            if (not except_name or not except_name(from_now,to_now)) \
               and not QFileInfo(from_now).exists():
                del_files.append(to_now)
    for ff in del_files:
        try:
            os.remove(ff)
            print("已经删除文件:"+ff)
        except Exception as e:
            print("删除  %s  出错 ,原因:%s"%(ff,e))

    for dd in del_dirs:
        try:
            os.rmdir(dd)
            print("经常删除文件夹:"+dd)
        except:
            pass


def walk(dir_,except_=None):
    """@ dir_: best unicode
    @except_: func(dir):return True ,when wan't show dir
    返回的结果与os.walk的结果一致
    """

    if not except_ or not except_(dir_):
        out=__req(dir_)
        if out:
            yield out
            dirs=out[1]
            for ii in dirs:
                for jj in  walk(join(out[0],ii),except_):
                    yield jj          


def __req(dir_):
    ls=os.listdir(dir_)
    root=dir_
    dirs=[]
    files=[]
    for ii in ls:
        if isdir(join(root,ii)):
            dirs.append(ii)
        else:
            files.append(ii)
    return (root,dirs,files)

if __name__=='__main__':
    main()