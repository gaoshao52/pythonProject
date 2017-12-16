#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from libs.course import Course
from libs.it_class import ITClass
from libs.teacher import Teacher
from libs.student import Student
class School(object):
    '''学校类，包括 名称，地点，班级，教师，课程'''
    def __init__(self, school_name, school_addr):
        self.school_name = school_name
        self.school_addr = school_addr
        self.school_classes = {}
        self.school_teachers = {}
        self.school_courses = {}

    def create_course(self, course_name, course_price, course_duration):
        '''创建课程'''
        course_obj = Course(course_name, course_price, course_duration)
        self.school_courses[course_name] = course_obj

    def show_courses(self):
        '''查看课程信息'''
        print("课程信息".center(60, '='))
        for name in self.school_courses:
            course_obj = self.school_courses[name]
            print("\033[32;1m课程名称：{}\t价格：{}\t周期：{}月\033[0m".format(course_obj.course_name, course_obj.course_price, course_obj.course_duration))
        print("="*60)

    def create_class(self, class_name, course_name):
        '''创建班级'''
        course_obj = self.school_courses[course_name]
        class_obj= ITClass(class_name, course_obj)
        self.school_classes[class_name] = class_obj

    def show_class(self):
        '''查看班级信息'''

        print("班级信息".center(60, '='))
        for name in self.school_classes:
            class_obj = self.school_classes[name]
            print("\033[32;1m班级名称：{}\t课程：{}\033[0m".format(class_obj.class_name, class_obj.course_obj.course_name))
        print("=" * 60)

    def show_class_course(self):
        '''查看班级课程信息'''
        print("班级课程信息".center(60, '='))
        for name in self.school_classes:
            class_obj = self.school_classes[name]
            course_obj = class_obj.course_obj
            print("\033[32;1m班级名称：{}\t课程：{}\t价格：{}\t周期：{}月\033[0m".format(class_obj.class_name, course_obj.course_name, course_obj.course_price, course_obj.course_duration))
        print("=" * 60)

    def create_teacher(self, t_name, t_salary, class_name):
        '''创建教师'''
        for i in self.school_classes:
            print(i)
        class_obj = self.school_classes[class_name]
        teacher_obj = Teacher(t_name, t_salary)
        teacher_obj.add_class(class_name, class_obj)
        self.school_teachers[t_name] = teacher_obj

    def add_teacher_class(self, t_name, class_name):
        '''为教师添加课程'''
        class_obj = self.school_classes[class_name]
        teacher_obj = self.school_teachers[t_name]
        teacher_obj.add_class(class_name, class_obj)

    def show_teacher(self):
        '''查看教师信息'''
        print("教师信息".center(60, "="))
        for name in self.school_teachers:
            teacher_obj = self.school_teachers[name]
            class_list = []
            for class_name in teacher_obj.t_class:
                class_list.append(class_name)

            print("\033[32;1m教师：{}\t薪水：{}\t班级：{}\033[0m".format(teacher_obj.t_name, teacher_obj.t_salary,class_list))
        print("="*60)

    def create_student(self, s_name, s_age, class_chioce, pay_mony=0):
        '''创建学员'''
        student_obj = Student(s_name, s_age, pay_mony)   # 实例化学员
        # print(self.school_classes)
        class_object = self.school_classes[class_chioce]
        # print(class_object)
        class_object.class_students[s_name] = student_obj
        self.school_classes[class_chioce] = class_object

    def show_student(self):
        '''查看学生信息'''
        for class_name in self.school_classes:
            print('---------班级[%s]的学生信息--------------'%class_name)
            class_obj = self.school_classes[class_name]
            for s_name in class_obj.class_students:
                s_obj = class_obj.class_students[s_name]
                print("\033[33;1m姓名: {} \t 年龄: {} \t 支付学费: {}\t 分数：{}\033[0m".format(s_obj.s_name, s_obj.s_age, s_obj.s_pay_count, s_obj.score))

    def show_teacher_classinfo(self, t_name):
        '''查看教师班级信息'''
        print("教师班级信息".center(60, "="))
        teacher_obj = self.school_teachers[t_name]
        for class_name in teacher_obj.t_class:
            class_obj = self.school_classes[class_name]
            student_list = []
            for k in class_obj.class_students:
                student_list.append(k)
            print("\33[32;1m班级：%s\t关联课程：%s\t学员:%s\33[0m" % (class_obj.class_name, class_obj.course_obj.course_name,
                                                            student_list))
        print("=" * 60)



if __name__ == '__main__':
    beijing = School("老男孩", "beijing")
    beijing.create_course("python", "1000", "6")
    beijing.create_course("linux", "1200", "8")
    beijing.show_courses()

    beijing.create_class("pys13", "python")
    beijing.create_class("pys14", "linux")
    beijing.show_class()
    beijing.show_class_course()

    beijing.create_teacher("Alex", 10000, "pys13")
    beijing.add_teacher_class("Alex", "pys14")
    beijing.show_teacher()


    beijing.create_student("gao", 23, "pys14")
    beijing.create_student("gao", 23, "pys13")
    beijing.create_student("sam", 23, "pys13")

    beijing.show_teacher_classinfo("Alex")


    beijing.show_student()








