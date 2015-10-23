import pickle
class ParseTool(object):
    def get(self,globeDict):
        self.mp={}
        for k ,v in globeDict.items():
            self.mp[k]=sorted( dir(v) )
        
    def save(self,path):

        with open(path,'wb') as f:
            pickle.dump(self.mp,f,2)
    
    

#obj = ParseTool()
#obj.get(globals())
#obj.save('dogbit')