# -*- encoding:utf8 -*-

import sys
class IPickle(object):
    """
    需要注意的只有两个变量：self.constructArgs 和 self.pickleDict。
    constructArgs : 一般不用管，就是构造对象时传入的参数，这里只保存了位置参数。注意，这些位置参数必须是可以pickle的。
    self.pickleDict:需要输出的字典,它应该是来自于self.__dict__。你也可以自定义。
    可以在 子类 中 重载 函数__reduce__，定义pickleDict。见下面的test例子。
    __setstate__ 一般不用override
    """
    def __init__(self, *args):
        try:
            # 继承的时候，IPickle不要排在最后，因为最后的object不能接受args，会报错。
            super().__init__( *args)     
        except TypeError as e:
            print(e,file=sys.stderr)
        self.constructArgs=args
        self.pickleDict = {}
    def __reduce__(self):
        return self.__class__,self.constructArgs,self.pickleDict
    
    def __setstate__(self,state):
        self.pickleDict=state
        self.__dict__.update(state)

#################################
# 以为为测试代码
################################
        
class jj(object):
    pass
class test(IPickle,jj):
    def __init__(self,name):
        super().__init__(name)
        self.name = name
    
    def __reduce__(self):
        self.pickleDict={'name':self.name}
        return super().__reduce__()
if __name__=='__main__':
    import pickle
    
    me=test("heyulin")
    ss = pickle.dumps(me)
    print(ss)
    jj = pickle.loads(ss)
    print(jj.name)