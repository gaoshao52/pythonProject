#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys, time
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from libs.lecturer import Lecturer
from libs.student import Student
import re
from libs.db_table_api import DbAPI


class MLecturer(object):
    def __init__(self):
        self.data = {
            "1": ["创建班级", "create_class"],
            "2": ["查看班级", "query_class"],
            "3": ["创建学生", "create_stud"],
            "4": ["查看学生", "query_stud"],
            "5": ["学生加入班级", "add_class_by_stud_qq"],
            "6": ["创建班级上课记录", "create_class_record"],
            "7": ["查看班级上课记录", "query_class_record"],
            "8": ["查看学生上课记录", "query_class_stud_record"],
            "9": ["修改学生成绩", "modify_stud_score"]
        }
        self.lecturer = Lecturer()

    def ops_list(self):
        print("教师操作目录".center(50, "*"))
        print("opt".ljust(10, " ") +"item".ljust(40, " "))
        print("-"*50)
        for item in self.data:
            print(item.ljust(10, " ") + self.data.get(item)[0].ljust(40, " "))
        print("-" * 50)

    def interactive(self):
        self.ops_list()
        while True:
            user_opt = input("please input your choice:").strip()
            if user_opt in self.data:
                if hasattr(self, self.data.get(user_opt)[1]):
                    func = getattr(self, self.data.get(user_opt)[1])
                    func()
                else:
                    print("实例属性不存在")
            else:
                print("选项不存在")

    def create_class(self, *args, **kwargs):
        print("create_class".center(50, "*"))
        user_class_name = input("请输入班级名称：")
        self.lecturer.create_class(user_class_name)
        print("*"*50)

    def query_class(self, *args, **kwargs):
        print("query_class".center(50, "*"))
        self.lecturer.query_all_class()
        print("*" * 50)

    def create_stud(self, *args, **kwargs):
        print("create_stud".center(50, "*"))
        while True:
            user_input = input("请输入姓名和QQ：").strip()
            s_info = user_input.split()
            if len(s_info) != 2: continue
            if re.search("^\d+$", s_info[1]) == None: continue
            break
        self.lecturer.create_stud(s_info[0].strip(), s_info[1].strip())
        print("*" * 50)

    def query_stud(self, *args, **kwargs):
        print("query_stud".center(50, "*"))
        self.lecturer.query_all_student()
        print("*" * 50)

    def add_class_by_stud_qq(self, *args, **kwargs):
        print("add_class_by_stud_qq".center(50, "*"))
        user_input = input("请输入QQ和课程名称：").strip()
        s_info = user_input.split()
        self.lecturer.add_stud_to_class_by_qq(s_info[0].strip(), s_info[1].strip())

    def create_class_record(self, *args, **kwargs):
        print("create_class_record".center(50, "*"))
        user_input = input("请输入课程名称：").strip()
        self.lecturer.create_class_recors(user_input)

    def query_class_record(self, *args, **kwargs):
        print("query_class_record".center(50, "*"))
        user_input = input("请输入课程名称：").strip()
        self.lecturer.query_class_record(user_input)
        print("*" * 50)

    def query_class_stud_record(self, *args, **kwargs):
        print("query_class_stud_record".center(50, "*"))
        while True:
            user_input = input("请输入课程和时间：").strip()
            s_info = user_input.split()
            if len(s_info) != 2: continue
            if re.search("^\d{4}-\d{2}-\d{2}$", s_info[1]) == None: continue
            self.lecturer.query_all_stud_record(s_info[0], s_info[1])
            break

    def modify_stud_score(self, *args, **kwargs):
        print("modify_stud_score".center(50, "*"))

        while True:
            user_input = input("请输入分数、学生QQ、课程名称、上课时间：").strip()
            user_info = user_input.split()
            if len(user_info) != 4: continue
            self.lecturer.modify_stud_score(user_info[0], user_info[3], user_info[2], user_info[1])  #score, date, class_name, qq
            break

class MStudent(object):
    def __init__(self):
        self.data = {
            "1": ["提交作业", "submit_task"],
            "2": ["查看成绩", "check_score"]
        }




    def ops_list(self):
        print("学生操作目录".center(50, "*"))
        print("opt".ljust(10, " ") + "item".ljust(40, " "))
        print("-" * 50)
        for item in self.data:
            print(item.ljust(10, " ") + self.data.get(item)[0].ljust(40, " "))
        print("-" * 50)

    def interactive(self):
        while True:
            user_input = input("请输入名字和QQ：").strip()
            user_info = user_input.split()
            if len(user_info) != 2: continue
            status = DbAPI.query_stud_id(user_info[0].strip(), user_info[1].strip())

            self.stud_id = int(status)
            # print("status_id: %s"%self.stud_id)
            if int(status) == -1:
                print("学员不存在")
                continue
            break
        print("学员课程信息".center(50, "-"))
        data = DbAPI.query_stud_info_by_id(int(status))
        for obj in data:
            print("课程：%s; 课程记录：%s"%(obj[0], obj[1]))
        print("-"*55)

        self.ops_list()

        while True:
            user_opt = input("please input your choice:").strip()
            if user_opt in self.data:
                if hasattr(self, self.data.get(user_opt)[1]):
                    func = getattr(self, self.data.get(user_opt)[1])
                    func()
                else:
                    print("实例属性不存在")
            else:
                print("选项不存在")

    def submit_task(self, *args, **kwargs):
        print("submit_task".center(50, '*'))
        user_input = input("请输入课程名称和时间,及作业名称：").strip()
        user_info = user_input.split()
        student = Student(self.stud_id)
        student.submit_task(user_info[0], user_info[1], user_info[2])

    def check_score(self, *args, **kwargs):
        print("check_score".center(50, '*'))
        # print(self.stud_id)
        student = Student(self.stud_id)
        user_input = input("请输入课程名称：").strip()
        student.query_score(user_input)














if __name__ == '__main__':
    MStudent().interactive()