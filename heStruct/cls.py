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