#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Course(object):
    '''课程类，包括 名称  价格  持续时间'''
    def __init__(self, course_name, course_price, course_duration):
        self.course_name = course_name
        self.course_price = course_price
        self.course_duration = course_duration