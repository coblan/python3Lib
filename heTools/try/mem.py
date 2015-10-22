
import psutil

import os,threading
from datetime import datetime
pid = os.getpid()
container = []
p = psutil.Process(pid)
lock = threading.Lock()

def watch_memery(url):
    global container
    lock.acquire()
    dd = p.memory_info()
    now = datetime.now().strftime('[%m/%d %H:%M:%S]')
    data = [now, str(dd.rss/(1024.0*1024)),str(dd.vms/(1024.0*1024)),url]
    container.append( data)
    print( '\t'.join(data) )
    if len(container) >200:
        text = '\n'.join( ['\t'.join(dt) for dt in container])
        container =[]
        save(text)
    lock.release() 

        
def save(text):
    if os.path.exists('watch_data'):
        with open('watch_data', 'a+') as f:
            f.write(text)
    else:
        with open('watch_data', 'w') as f:
            f.write(text)        
    
for i in range(300):
    watch_memery('ddd%s'%i)
    
#python_proc = []
#for p in psutil.process_iter():
    #if p.name().startswith('python'):
        #python_proc.append(p)

#for i in python_proc:
    #print(i.name())
    #print( i.memory_info().rss/(1024.0*1024) , i.memory_info().vms/(1024.0*1024))

