import os,sys
import inspect


def s(cls, *args,**kw):
    fram = inspect.currentframe().f_back
    name = fram.f_code.co_name
    #print fram.f_code.__name__
    #super(cls,self).__init__(*args,**kw)
    args_,varargs,keywords,locals_ = inspect.getargvalues(fram)
    self = locals_[args_[0]]
    return getattr(super(cls,self),name)(*args,**kw)
   
#print(repr( sys.version))
