from heOs.syn import syn_copy,not_modefied
import re


def excepte_name(from_name,to_name):
    if from_name.endswith('.pyc'):
        return True
    if not_modefied(from_name,to_name):
        return True


def excepte_dir(from_name):
    # if re.search(r'static\\\\image',from_name):
    #     return True
    if from_name.endswith('image'):
        return True

syn_copy(r'D:\coblan\web\yulinhe\yulin5\yulin5',r'D:\coblan\web\yulinhe\5',except_=excepte_dir,except_name=excepte_name)