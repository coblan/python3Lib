##import itertools

##for x,y in itertools.product(range(10),range(2)):
##    print(x,y)

class kiss(object):
    def __init__(self,*args):
        #print( super().__class__ )
        print( super().__getattribute__('__class__').__bases__ )



cc=kiss()