#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys, time
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from libs.db_table_api import DbAPI

class Lecturer(object):
    def __init__(self):
        pass

    def create_class(self, class_name):
        '''创建班级'''
        DbAPI.create_class(class_name)

    def query_all_class(self):
        '''查询班级'''
        data = DbAPI.query_class_all()
        if len(data) == 0:
            print("没有班级。。。。")
        else:
            for obj in data:
                print("班级名称：%s"%obj.get('class_name'))

    def create_stud(self, name, qq):
        DbAPI.create_student(name, qq)

    def query_all_student(self):
        data = DbAPI.query_all_stud()
        # print(data)
        for obj in data:
            # print(obj)
            print("姓名：{}； QQ：{}； 课程：{}".format(obj.get('name'), obj.get('qq'), obj.get('learn_class')))


    def query_stud_by_class(self, class_name):
        '''查询班级成员'''
        data = DbAPI.query_class_by_name(class_name)
        if data != [] and data != None:
            for stud in data:
                print("-" * 50)
                print("姓名：%s; qq: %s"%(stud.get('name'), stud.get('qq')))
                # print("-" * 50)

        else:
            print("没有学生。。。")

    def create_class_recors(self, class_name):
        '''创建上课记录，并为每一个学生创建记录'''
        DbAPI.initialize_class_records(class_name)

    def add_stud_to_class_by_qq(self, qq, class_name):
        '''根据学员qq号把学员加入班级'''
        DbAPI.add_stud_to_class_by_qq(qq, class_name)

    def query_class_record(self, class_name):
        data = DbAPI.query_a_class_all_records(class_name)
        print("###%s 课程记录###"%class_name)
        for class_record in data:
            print("上课时间：%s"%class_record.get('class_time'))

    def query_all_stud_record(self, class_name, date):
        data = DbAPI.query_class_stud_record(class_name, date)

        # print(data)
        for obj in data:
            print("score: %s; name: %s; QQ: %s" % (obj.get('score'), obj.get('stud_name'), obj.get('stud_qq')))

    def modify_stud_score(self, score, date, class_name, qq):

        DbAPI.modify_stud_score(score, date, class_name, qq)




if __name__ == '__main__':
    le = Lecturer()
    # le.query_all_class()
    # le.query_stud_by_class("linux")
    # le.query_all_student()
    le.query_class_record("python")