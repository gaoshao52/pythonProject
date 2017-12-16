#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Student(object):
    '''学生类， 包括  名字  年龄 学费 分数'''
    def __init__(self, s_name, s_age, s_pay_count =0, score=0):
        self.s_name = s_name
        self.s_age = s_age
        self.s_pay_count = s_pay_count
        self.score = score