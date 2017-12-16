#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Teacher(object):
    '''教师类，包括 名字, 薪水, 和 所教的班级 '''
    def __init__(self, t_name, t_salary):
        self.t_name = t_name
        self.t_salary = t_salary
        self.t_class = {}

    def add_class(self, class_name, class_obj):
        '''教师分配的班级'''
        self.t_class[class_name] = class_obj