#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import shelve
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from conf import settings
from libs.school import School

class Manage_school(object):
    '''学校管理视图'''
    def __init__(self):
        self.choice_school = None
        self.school_obj = None
        if os.path.isfile(settings.db_file_path + '.dat'):
            self.school_db = shelve.open(settings.db_file_path)
            self.run_manage()
            # self.school_db.close()
        else:
            self.school_db = shelve.open(settings.db_file_path)
            self.initialize_school()
            self.run_manage()
            # self.school_db.close()

    def initialize_school(self):
        '''初始化学校默认信息，上海， 北京 分校'''

        # 北京分校，默认开python linux 课程
        Beijing_obj = School('Beijing', "Beijing-China")
        Beijing_obj.create_course('Linux', 12000, 6)
        Beijing_obj.create_course('Python', 15000, 8)
        self.school_db['Beijing'] = Beijing_obj

        # 上海分校，默认开 go 课程
        Shanghai_obj = School('Shanghai', "Shanghai-China")
        Shanghai_obj.create_course('Go', 18000, 7)
        self.school_db['Shanghai'] = Shanghai_obj


    def run_manage(self):
        '''运行学校管理'''
        while True:
            for school in self.school_db:
                print("学校名称：%s" %school)

            self.choice_school = input("\033[32;1m请输入要管理的学校>>>>>>\033[0m").strip()
            if self.choice_school in self.school_db:
                while True:
                    self.school_obj = self.school_db[self.choice_school]
                    info = '''\033[35;1m欢迎来到%s校区，请输入操作的字符串\033[0m
                    创建课程 add_course
                    创建班级 add_class
                    创建讲师 add_teacher
                    查看课程 check_course
                    查看班级 check_class
                    查看讲师 check_teacher
                    退出程序 exit
                    '''%self.choice_school
                    print("=" * 60)
                    print(info)
                    print("=" * 60)

                    user_choice = input(">>>>").strip()

                    if hasattr(self, user_choice):
                        getattr(self, user_choice)()
                        # print("=" * 60)
                    else:
                        print("\033[31;1m请重新输入\033[0m")
                        # print("="*60)
            else:
                print("\033[31;1m您输入的学校不存在，请重新输入\033[0m")


    def add_course(self):
        '''添加课程'''
        course_name = input('''\033[34;0m输入要添加课程的名称：\033[0m''').strip()
        course_price = input('''\033[34;0m输入要添加课程的价格：\033[0m''').strip()
        course_duration = input('''\033[34;0m输入要添加课程的时长：\033[0m''').strip()

        if course_name not in self.school_obj.school_courses:
            self.school_obj.create_course(course_name, course_price, course_duration)
            self.school_db.update({self.choice_school: self.school_obj})
            print("\033[32;0m[%s]\033[0m 课程添加成功！"%course_name)
        else:
            print("\033[31;1m课程已经存在.......\033[0m")

    def check_course(self):
        '''查看课程'''
        self.school_obj.show_courses()

    def add_class(self):
        '''添加班级'''
        class_name = input('''\033[34;0m输入要添加班级的名称：\033[0m''').strip()
        course_name = input('''\033[34;0m输入关联课程的名称：\033[0m''').strip()

        if class_name not in self.school_obj.school_classes:
            self.school_obj.create_class(class_name, course_name)
            self.school_db.update({self.choice_school: self.school_obj})
            print("\033[32;0m[%s]\033[0m 班级添加成功！" % class_name)
        else:
            print("\033[31;1m班级已经存在.......\033[0m")

    def check_class(self):
        '''查看班级'''
        self.school_obj.show_class()

    def add_teacher(self):
        t_name = input('''\033[34;0m输入添加回教师的名字：\033[0m''').strip()
        t_salary = input('''\033[34;0m输入教师的工资：\033[0m''').strip()
        class_name = input('''\033[34;0m输入关联班级的名称：\033[0m''').strip()

        if t_name not in self.school_obj.school_teachers:
            self.school_obj.create_teacher(t_name, int(t_salary), class_name)
            self.school_db.update({self.choice_school: self.school_obj})
            print("\033[32;0m[%s]\033[0m 教师添加成功！" % t_name)
        else:
            print("\033[31;1m教师已经存在.......\033[0m")

    def check_teacher(self):
        self.school_obj.show_teacher()

    def exit(self):
        self.school_db.close()
        sys.exit("\033[32;1m欢迎下次使用学员管理系统\033[0m")