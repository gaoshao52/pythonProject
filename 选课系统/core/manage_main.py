#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from core.manage_school import Manage_school
from core.manage_student import Manage_student
from core.manage_teacher import Manage_teacher

class Manage_main(object):
    def __init__(self):
        pass

    def run(self):
        while True:
            info_data = {
                "1": "student",
                "2": "teacher",
                "3": "school"
            }

            info = '''\033[35;1m欢迎进入COURSE_SYSTEM >>>>\033[0m
            1. 学生视图
            2. 教师视图
            3. 学校视图
            \033[31;1mq 退出该系统\033[0m
            '''
            print(info)
            user_chioce = input(">>>>").strip()
            try:
                eval("Manage_%s()"%info_data[user_chioce])
            except KeyError as e:
                if user_chioce =='q': break
                print("\033[31;1m[ERROR]请输入正确的选项\033[0m")
                print("="*60)