# -*- encoding:utf8 -*-

import argparse

class Watcher(object):
    def __init__(self):
        self.text = ''
        self.rss =[]
        self.vms =[]    
        self.lines =[]
        
    def get_file(self):
        parser = argparse.ArgumentParser() 
        parser.add_argument("path", help="input file path") 
        args = parser.parse_args() 
        
        with open(args.path) as f:
            self.text = f.read() 
            
    def parse(self):
        if self.text:
            self.lines = self.text.split('\n')
        for line in self.lines:
            fields = line.split('\t')
            self.rss.append(float(fields[1]))
            self.vms.append(float(fields[2]))   
    
    def showAll(self,number):
        print('+max rss  -----')
        self.showTop(self.rss,number)  
        print('+max vms  -----')
        self.showTop(self.vms,number)
        
    def showTop(self, field, count=10):
        cnt =0
        for i in getMaxLines(field):
            cnt+=1
            if cnt>count:
                break           
            if i>0:
                print('|\t%s'%self.lines[i-1])
                print('|\t%s'%self.lines[i])
                print('\t|'+'-'*30)
            else:
                print('|\t%s'%self.lines[i])
                print('\t|'+'-'*30)
            
            
              

def main():
    watcher = Watcher()
    watcher.get_file()
    watcher.parse()
    watcher.showAll(10)
    

        
def getMaxLines(field):
    dif=[new - old for old,new in pair(field)]
    # 规则化 dif,（去重，排序 ）
    reg_dif=sorted(list(set(dif)),reverse=True)
    for i in reg_dif:
        print('<%s>'%i)
        for j in findallIndex(dif,i):
            yield j+1

def findallIndex(ls,number):
    'find all index of number in ls'
    out =[]
    j=0
    for i in ls:
        if number == i:
            out.append(j)
        j+=1
    return out

def pair(ls):
    length = len(ls)
    for i in range(length):
        if i+1< length:
            yield ls[i],ls[i+1]
if __name__ =='__main__':
    #ls = list(range(55))
    #for i in pair(ls):
        #print( i )
    main()
    
