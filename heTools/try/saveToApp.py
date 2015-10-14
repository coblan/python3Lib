import re

fields = []
def norml_type(cls_fname):
    def func(cls):
        cls.recongnize = re.compile(r'^\s+\w+\s*=\s*%s\W+'%cls_fname)
        cls.pattern = re.compile(r'^(\s+)(\w+)\s*=\s*%s(.*)'%cls_fname ,re.DOTALL)
        cls.cls_fname = cls_fname
        fields.append(cls)
        return cls
    return func


block_pat = re.compile(r'\'.*?\'|".*?"|\(.*\)|\{.*\}',re.DOTALL)
brace_pat = re.compile(r'\(.*\)|\{.*\}',re.DOTALL)
str_pat = re.compile ('u?(\'.*?\'|".*?")',re.DOTALL)

eq_pat = re.compile(r'(\w+)\s*=')

def split_argsstr(arg_str):
    str_blocks =[]
    brace_blocks=[]
    left = []
    start = 0
    for mt in str_pat.finditer(arg_str):
        str_blocks.append((mt.start(),mt.end()-mt.start() ))
        left.append(arg_str[start:mt.start()])
        start = mt.end()
    left.append(arg_str[start:])
    left_str = ''.join(left)
    left.clear()
    start = 0
    for mt in brace_pat.finditer(left_str):
        brace_blocks.append((mt.start(),mt.end()-mt.start() ))
        left.append(left_str[start:mt.start()])
        start = mt.end()
    left.append(left_str[start:])
    
    left_str = ''.join(left)
    coma_ls = left_str.split(',')
    
    flag=''
    cnt = 0
    #print('comals is :',coma_ls)
    for i in coma_ls:
        flag +='0'*len(i)+','
    #print('flag1',flag)
    for s,l in brace_blocks:
        flag = flag[:s]+'1'*l +flag[s:]
    for s,l in str_blocks:
        flag = flag[:s]+'2'*l +flag[s:]
    
    args =[]
    kw ={}
    ls = flag.split(',')
    start = 0
    for i in ls:
        end = start +len(i)
        crt_str = arg_str[start:end]
        mt = eq_pat.search(crt_str)
        if  mt and i[0] =='0':
            kw[mt.group(1)] = crt_str
        else:
            args.append(crt_str)
        start = end +1
        
    #去掉空的项
    tmp = args
    args = []
    for i in tmp:
        if i.strip():
            args.append(i)    
        
    return args,kw
    
        
        

def split_argsstr_old(arg_str):
    '输入参数字符，输出args和kw '
    coma_args = []
    start = 0
    
    
    for mt in block_pat.finditer(arg_str):
        #block.append((mt.start(),mt.end()))
        norm_str = arg_str[start:mt.start()]
        comma_ls = norm_str.split(',')
        if comma_ls:
            comma_ls[-1] += arg_str[mt.start():mt.end()]
        start = mt.end()
        
        coma_args.extend(comma_ls)
        
    norm_str = arg_str[start:]
    comma_ls = norm_str.split(',')
    coma_args.extend(comma_ls)
    
    #去掉空的项
    tmp = coma_args
    coma_args = []
    for i in tmp:
        if i.strip():
            coma_args.append(i)
    
    # 输出两种类型参数
    args = []
    kw={}
    for i in coma_args:
        ls = block_pat.split(i)
        mt = eq_pat.search( ls[0] )
        if mt:
            kw[mt.group(1)] = i
        else:
            args.append(i)
    return args,kw


class NormField:
    pattern = ''
    brace_rm = re.compile( '\((.*)\)',re.DOTALL)
    @classmethod
    def is_me(cls,line):
        return cls.recongnize.match(line)
    
    def split_args(self,args_with_brace):
        arg_str = self.brace_rm.search(args_with_brace).group(1)
        return split_argsstr(arg_str)
    
    def reguler(self):
        mt = self.pattern.match(self.code)
        args ,kw = self.split_args(mt.group(3))
    
        if not args:
            vname = kw.pop( 'verbose_name',None)
            if vname:
                args = [re.match('=(.*)',vname).group(1)]
            else:
                args = ["u'%s'"%mt.group(2)]
        rq_kw = []
        rq_kw.append(kw.pop('db_column',"db_column = u'%s'"%mt.group(2)))
        rq_kw.append(kw.pop('blank','blank = True'))
        kw.pop('null','')
    
        if hasattr(self,'sp_field'):
            for ag_pair in self.sp_field:
                rq_kw.append(kw.pop(*ag_pair))
        other_kw =[]
        for k ,v in kw.items():
            other_kw.append(v)
    
        totle = args + rq_kw + other_kw
        p_str = ','.join(totle)
        code = '%s%s = %s(%s)\n'%(mt.group(1),mt.group(2),self.cls_fname,p_str)
        return code        

class KeyField(NormField):
    def reguler(self):
        mt = self.pattern.match(self.code)
        args ,kw = self.split_args(mt.group(3))
    
        rq_kw = []
        #rq_kw.append(kw.pop('max_length', 'max_length = 50'))
        rq_kw.append(kw.pop('verbose_name',"verbose_name = u'%s'"%mt.group(2))) 
        rq_kw.append(kw.pop('db_column',"db_column = u'%s'"%mt.group(2)))
        rq_kw.append(kw.pop('blank','blank = True'))
        kw.pop('null','')
        
        if hasattr(self,'sp_field'):
            for ag_pair in self.sp_field:
                rq_kw.append(kw.pop(*ag_pair))
        other_kw =[]
        for k ,v in kw.items():
            other_kw.append(v)
    
        totle = args + rq_kw + other_kw
        p_str = ','.join(totle)
        code = '%s%s = %s(%s)\n'%(mt.group(1),mt.group(2),self.cls_fname,p_str)
        return code
    
        

@norml_type('models.CharField')
class CharField(NormField):
    sp_field = [('max_length', 'max_length = 50'),]
    
    
    

@norml_type('models.ForeignKey')
class ForeignKey(KeyField):
    pass
    #recongnize = re.compile(r'^\s+\w+\s*=\s*models.ForeignKey\W+')
    #pattern = re.compile(r'^(\s+)(\w+)\s*=\s*models.ForeignKey(.*)')
    #cls_fname = 'models.ForeignKey'

@norml_type('models.FloatField')
class FloatField(NormField):
    pass

@norml_type('models.DateTimeField')
class DateTimeField(NormField):
    pass

@norml_type('models.OneToOneField')
class OneToOneField(KeyField):
    pass

@norml_type('models.TextField')
class TextField(NormField):
    pass

@norml_type('models.DateField')
class DateField(NormField):
    pass

is_brace_end = re.compile(r'^.*\)\s*$')
start_model_pat = re.compile(r'^class\s+')
finish_fields = re.compile(r'^\s+(def|class)\s+')

def reguler_code(code):
    crt_field = ''
    code_lines = []
    start_model = False
    finish_parsefield = False
    for line in code.splitlines(True):
        if not start_model and start_model_pat.match(line):
            start_model = True
            code_lines.append(line)
            continue
            
        if finish_parsefield or finish_fields.match(line):
            finish_parsefield =True
            code_lines.append(line)
            continue
        
        if crt_field:
            crt_field.code += line
        else:
            for field in fields:
                if field.is_me(line):
                    crt_field = field()
                    crt_field.code = line
                    break
                
            # 未实现的field type
            if not crt_field:
                code_lines.append(line)
                
        if is_brace_end.match(line):
            if crt_field:
                code_lines.append(crt_field.reguler())
            crt_field = ''
            #if crt_field:
                #crt_field.code += line
    
    dog = ''.join(code_lines)
    dog = dog.strip()
    dog+= '\n\n'
    return dog
        
        
            
                
            

def sort_models(app,models):
    pass



if __name__ == '__main__':
    test_code ="""
class IapInfo(models.Model):
    app = models.ForeignKey('app_info.App', verbose_name=u'App',
        limit_choices_to={'status': 'V'})
    request_id = models.CharField(u'Request ID', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField(u'Timestamp', auto_now_add=True)
    local_doc = models.CharField(u'IAP Doc (Local)', max_length=1000, null=True,
        blank=True, default='')
    remote_doc = models.CharField(u'IAP Doc (Dropbox)', max_length=1000, null=True,
        blank=True, default='')
    status = models.CharField(u'Request Status', max_length=1, choices=REQUEST_STATUS,
        default='N')
    editor = models.EmailField(u'Editor Email', null=True, blank=True, default='')

    def __unicode__(self):
        return self.request_id

    def get_iap_list(self):
        return self.iap_set.all()

    class Meta:
        verbose_name = u'IAP Request'
        verbose_name_plural = u'IAP Request'
        ordering = ('-status',)
        
    """
    print( reguler_code(test_code) )
   
    #argstr = """u'Product ID', widget=forms.TextInput(
        #attrs={'style': '''width: 450px;'''}), max_length=200
    #"""
    #print(repr(argstr))
    #print(len(argstr))
    #print(  split_argsstr(argstr) )