# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库


def huiwen(str1):
     str11=list(str1)
     str2=reversed(str11)
     if str11==list(str2):
          print('是回文联！')
     else:
          print('不是回文联！')


a = "asdd1sa"

print(huiwen(a))
