#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class ITClass(object):
    '''班级类， 包括 class_name, course_obj, class_students 属性'''
    def __init__(self, class_name, course_obj):
        self.class_name = class_name
        self.course_obj = course_obj
        self.class_students = {}