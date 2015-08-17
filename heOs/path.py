import os
import subprocess


def copy(from_,to_):
    if not os.path.exists(from_):
        raise OSError('file not exist')
    rt = subprocess.call( 'copy %s %s' % (from_, to_),shell=True,stdout=subprocess.DEVNULL)
    if rt==0:
        return True
    else:
        raise OSError('file copy erro with code %s'%rt)
    

if __name__=='__main__':
    rt=copy(r'D:\try\test\time.txt',r'D:\try\test\time')
    print(rt)