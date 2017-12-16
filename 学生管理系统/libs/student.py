#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys, time
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from libs.db_table_api import DbAPI

class Student(object):

    def __init__(self, stud_id):
        self.stud_id = stud_id

    def submit_task(self, class_name, time, text_name):
        DbAPI.modify_stud_record_task(self.stud_id, class_name, time, text_name)

    def query_score(self, class_name):
        data = DbAPI.query_stud_score(self.stud_id, class_name)
        print("名次：%s"%data[1])
        for obj_data in data[0]:
            print("分数：%s, 课程时间：%s, 作业： %s"%(obj_data['score'], obj_data['time'], obj_data['stud_task']))


