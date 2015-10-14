import os,re

path = r'C:\Users\heyulin\Documents\work\PTS\production_tracking\src'


#model_pat=re.compile(r'^class (\w+)\s*\(models.Model\):')
cntu = re.compile(r'^(\s+|#)')
model_pat=re.compile(r'^class\s+(\w+)\s*\((.*?)\):')


class model:
    def __init__(self,name,app_name):
        self.name = name
        self.app = app_name
        self.code = ''
class App:
    def __init__(self,name,code):
        self.name = name
        self.code = code


def parse(path):
    parse_rt = []
    for r,d,f in os.walk(path):
        for modelpy in [x for x in f if x=='models.py']:
            fullpath= os.path.join(r,modelpy)
            with open(fullpath,encoding='utf8') as pyfile:
                text = pyfile.read()
            
            subcls = ['models.Model']
            if 'text' in locals():
                lines = text.splitlines(True)

                crt_model = ''
                crt_code = ''
                other_code = ''
                app_name = os.path.basename(r)
                for line in lines:
                    mt = model_pat.match(line)
                    if mt:
                        if crt_model:
                            crt_model.code = crt_code
                            crt_model = ''
                            
                        newMcls = mt.group(2).replace(' ','')
                        if newMcls in subcls:
                            model_name = mt.group(1)
                            crt_model = model(model_name,app_name)
                            parse_rt.append(crt_model)
                            subcls.append(model_name)
                            
                        if crt_model:
                            crt_code = line
                        else:
                            other_code += line
                            
                    elif crt_model:
                        if cntu.match(line):
                            crt_code += line
                        else : # 遇到其他类型了
                            #parse_rt[crt_model] = crt_code
                            crt_model.code = crt_code
                            crt_model = ''
                            other_code += line
                    else:
                        other_code += line

                #parse_rt[r ] = other_code
                if not other_code.endswith('\n'):
                    other_code+= '\n'
                parse_rt.append( App(app_name,other_code) )
                
                if crt_model:
                    if not crt_code.endswith('\n'):
                        crt_code+='\n'
                    crt_model.code = crt_code
                
                
                
                
                
                    
            #foreignkey[fullpath] = count_pt(foreignkey_pat,text)
            #models[fullpath] = count_pt(model_pat,text)

    return parse_rt