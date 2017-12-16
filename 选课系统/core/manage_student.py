#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import shelve
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from conf import settings
from libs.school import School

class Manage_student(object):
    '''学生视图'''
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
        for school in self.school_db:
            print("学校名称：%s" %school)
        self.choice_school = input("\033[32;0m输入选择注册的学校名:\033[0m").strip()
        if self.choice_school in self.school_db:
            self.school_obj = self.school_db[self.choice_school]
            student_name = input('''\033[34;0m输入学生的姓名：\033[0m''').strip()
            student_age = input('''\033[34;0m输入学生的年龄：\033[0m''').strip()
            self.school_obj.show_class_course()
            class_choice = input('''\033[34;0m输入上课的班级：\033[0m''').strip()



            if class_choice in self.school_obj.school_classes:
                course_money = self.school_obj.school_classes[class_choice].course_obj.course_price
                while True:
                    pay_money = input('''\033[34;0m该课程学费：\033[0m''').strip()
                    if int(pay_money) >= int(course_money):
                        print("\033[32;1m课程费用已支付\033[0m")
                        break
                    else:
                        print("\033[32;1m支付费用不够，请继续支付\033[0m")
                self.school_obj.create_student(student_name, student_age, class_choice, pay_money)
                self.school_db.update({self.choice_school: self.school_obj})  # 更新数据库数据
                print("\33[32;1m学生注册成功\33[0m")
            else:
                print("\33[31;1m系统错误：输入的班级不存在\33[0m")
        else:
            print("\33[31;1m系统错误：输入的学校不存在\33[0m")