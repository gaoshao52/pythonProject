#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import shelve
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from conf import settings
from libs.school import School

class Manage_teacher(object):
    '''教师视图'''
    def __init__(self):
        self.choice_school = None
        self.school_obj = None
        if os.path.isfile(settings.db_file_path + '.dat'):
            self.school_db = shelve.open(settings.db_file_path)
            self.run_manage()
            self.school_db.close()
        else:
            print("\033[31;1m数据库文件不存在，请先创建学校\033[0m")
            sys.exit(1)

    def run_manage(self):
        '''运行教师管理视图'''
        print("学校目录".center(60, '-'))
        for school_name in self.school_db:
            print("学校：%s"% school_name)
        print('-'*60)
        self.choice_school = input("请输入选择的学校>>>>>").strip()
        if self.choice_school in self.school_db:
            self.school_obj = self.school_db[self.choice_school]
            teacher_name = input("请输入教师名字：").strip()
            if teacher_name in self.school_obj.school_teachers:
                while True:
                    info = '''\033[35;1m您有以下权限，请输入要操作的字符>>>\033[0m
                    选择班级              \033[34;1mselect_class\033[0m
                    查看班级学员列表       \033[34;1mcheck_stutent_list\033[0m
                    修改所管理的学员的成绩  \033[34;1mmodify_score\033[0m
                    退出                  \033[34;1mexit\033[0m
                    '''
                    print('-'*60)
                    print(info)
                    print('-' * 60)
                    action_choice = input("请输入>>>>>").strip()
                    print('-' * 60)
                    if hasattr(self, action_choice):
                        func = getattr(self, action_choice)
                        func()
                    else:
                        print("\033[31;1m输入不正确\033[0m")

            else:
                print("\033[31;1m教师不存在......\033[0m")

        else:
            print("\033[31;1m学校不存在......\033[0m")


    def select_class(self):
        '''选择班级'''
        self.school_obj.show_class()
        class_choice = input("请输入班级>>>").strip()
        if class_choice in self.school_obj.school_classes:
            print("欢迎进入[%s]班级"% class_choice)
        else:
            print("\033[31;1m班级不存在......\033[0m")

    def check_stutent_list(self):
        '''查看班级成员列表'''
        self.school_obj.show_student()

    def modify_score(self):
        '''调整学生分数'''


        class_name = input("班级：").strip()
        s_name = input("学生名字：").strip()
        s_score = input("学生分数：").strip()
        if class_name in self.school_obj.school_classes:
            class_obj = self.school_obj.school_classes[class_name]
            if s_name in class_obj.class_students:
                s_obj = class_obj.class_students[s_name]
                s_obj.score = int(s_score)
            else:
                print("\033[31;1m学生不存在......\033[0m")
        else:
            print("\033[31;1m班级不存在......\033[0m")


    def exit(self):
        '''退出程序'''
        self.school_db.close()
        sys.exit("\033[31;1m欢迎下次光临\033[0m")