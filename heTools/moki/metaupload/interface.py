import copy
metalist=[
    ('META-20150821004','MACY3117','New Born Sisters & Brothers - Mommy & New Baby','Update','1.1','Apple','Macy Gone Crazy',	'New','Approved','2015-10-12 14:20:44'),
    ('META-20150723001','DONUT4014','Cake Pop Princess','New','1.0','Google','','New','Pending','')
      
]

data_map = {
    'META-20150821004':{'name':'dog',
                        'Primary Language':'English',
                        'Rlease Note':'这里是Rlease Note 的内容。',
                        'Description':'这里是20150821004   长描述的内容。。。。',
                        'keywords':'dog pig fllower',
                        'Primary Category':'Books',
                        'Secondary Category':'News',
                        'Submit to kid Category':'No',
                        'Rating':'9+'},
    'META-20150723001':{'name':'pig',
                        'Primary Language':'English',
                        'Rlease Note':'这里是Rlease Note 的内容。',
                        'Description':'这里是20150723001的内容。。。。',
                        'keywords':'dog pig fllower',
                        'Primary Category':'Books',
                        'Secondary Category':'OLD',
                        'Submit to kid Category':'YES',
                        'Rating':'19+'}
}

def get_list(keywords=None, production_type=None, app_store=None, studio=None, status=None):
    out = copy.deepcopy(metalist)
    if production_type:
        for i in out[::-1]:
            if not i[3] == production_type:
                out.remove(i)        
    if app_store:
        for i in out[::-1]:
            if not i[5] == app_store:
                out.remove(i)
    if studio:
        for i in out[::-1]:
            if not i[6] == studio:
                out.remove(i)        
    if status:
        for i in out[::-1]:
            if not i[7] == status:
                out.remove(i)          
    return out

def get_data(meta_id):
    return data_map.get(meta_id,'')

def upload(metainfo):
    pass

def login(name, psw):
    return True