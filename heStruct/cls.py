# -*- encoding:utf8 -*-

# 本页面主要用于改善类的创建
# 
# 以下三个函数用于主板接插式的函数回调
"""
使用方法
@首先在内中装饰要被子对象监听的函数
class A:
   @sub_obj_call
   def fun():
       A_do()
class B:
   def fun():
      B_do()
a=A()
b=B()
#将子对象注册到父对象
add_sub_obj(a,b)
#以后再调用父对象的被监听函数后，子对象的同名函数也会被调用
a.fun()

"""



def component_call(components):
    def _sub(fun):
        def __sub(self, *args,**kw):
            rt = fun(self, *args,**kw)
            # if not hasattr(cls, "comps"):
            #     return
            for comp in components:
                if not hasattr(comp, fun.__name__):
                    continue
                else:
                    getattr(comp, fun.__name__)(self,*args,**kw)
            return rt
        return __sub
    return _sub
def add_component(components, comp):
    if comp not in components:
        components.append(comp)


index = 0
def sub_obj_call(fun):
    """装饰器，用在需要插入子对象的mainBoard方法上
    例如：
    class XX:
        @sub_obj_call
        def keypress(self):
            dosome()
    
    注意： 返回值是最后调用的sub_obj的bool()!=None的值
    """
    def _sub(mainBoard, *args):
        if not hasattr(mainBoard, "sub_objs"):
            mainBoard.sub_objs = {}
        rt = fun(mainBoard, *args)
        for k, obj in mainBoard.sub_objs.items():
            if not hasattr(obj, fun.__name__):
                continue
            else:
                methord = getattr(obj, fun.__name__)
                if is_bound(methord):
                    methord( *args)
                else:
                    methord(obj, *args)
 
        return rt

    return _sub
def add_sub_obj(mainBoard, obj):
    if not hasattr(mainBoard, "sub_objs"):
        mainBoard.sub_objs = {}
    global index
    index += 1   
    mainBoard.sub_objs[index] = obj
    obj.sub_obj_index = index
    return index
    
def del_sub_obj(mainBoard, obj):
    if not hasattr(mainBoard, "sub_objs") or not hasattr(obj, "sub_obj_index"):
        return
    if obj.sub_obj_index is not None:
        del mainBoard.sub_objs[obj.sub_obj_index]
        obj.sub_obj_index = None
########################################################################
def dynplug(dynstate):
    '''用来给类对象动态的插入各种函数。
    一个类对象在不同的状态间切换，根据状态的不同，各种回调函数应该调用不同的函数，而这些调用函数由item提交，进行映射。
    构建时，类需要有：
    
    母类中：
    1.self.mapfunc={}
    2. self.dynstate = 'createLine'
    3. 在母类中，需要映射的函数，添加@dynplug
    
    子类中：
    1. 撰写函数为:
       @staticmethod
       itemfunc(motherfunc,mother,*args,**kw)
    2. 构建一个函数，填写好mother.mapfunc字典，如：
       mother.mapfunc['createLine'] ={
                'mouseMoveEvent':itemfuncMove,
                'mousePressEvent':itemfuncPress,
            }
       初试化item类staticmethod需要用到的各种变量。
    
    使用时，只需要设置mother.dynsate = 'createLine' 就可以自动切换状态。
    
    
    class Drawer:
        def mousePressEvent(self, view, func, event):
            pass
    '''

    def _dynplug(func):
        def _func(self, *args, **kw):
            #if not hasattr(self,'dynstate'):
                #return func(self, *args, **kw)
            #if isinstance(dynstate,str):
            state_obj = getattr(self,dynstate)
            #else:
                #state_obj = dynstate
            if state_obj:
                sub_func = getattr(state_obj, func.__name__)#self.mapfunc.get(state, None)
                if state_obj and sub_func:
                    #rfunc = funmaps.get(func.__name__,None)
                    return sub_func( *args, **kw)
            return func(self, *args, **kw)
        return _func
    return _dynplug


 
####################################################
        
def sub_obj_route(fun):
    def _sub(mainBoard, *args):
        if not hasattr(mainBoard, "sub_objs"):
            mainBoard.sub_objs = {}
        rt = fun(mainBoard, *args) 
        if isinstance(rt, int):
            obj = mainBoard.sub_objs[rt]
            if not hasattr(obj, fun.__name__):
                return
            methord = getattr(mainBoard.sub_objs[rt], fun.__name__)
            if is_bound(methord):
                return methord( *args)
            else:
                return methord(mainBoard, *args)
    return _sub

def is_bound(m):
    """判断方法是否绑定"""
    return hasattr(m, '__self__')
# 关于判断方法绑定与否 http://stackoverflow.com/questions/53225/how-do-you-check-whether-a-python-method-is-bound-or-not