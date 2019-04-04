# coding : utf-8
# create by ztypl on 2018/5/10

import re

hump = re.compile(r'([a-z]|\d)([A-Z])')


def hump2line(hump_str):
    return re.sub(hump, r'\1_\2', hump_str).lower()