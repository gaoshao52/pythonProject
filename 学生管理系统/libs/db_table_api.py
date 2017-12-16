#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys, time
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from libs import db_table_arc
session = sessionmaker(bind=db_table_arc.engine)()

class DbAPI(object):

    @staticmethod
    def create_class(cl_name):
        '''class表中创建班级课程'''
        session.add(db_table_arc.Classes(class_name=cl_name))
        session.commit()

    @staticmethod
    def query_class_by_name(cl_name):
        '''通过课班级程名查课程'''
        stud_data = []
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=cl_name).first()
        if class_obj == None:
            return None
        stud_objs = class_obj.students
        if len(stud_objs) == 0:
            return []
        for stud_obj in stud_objs:
            stud_records_objs = stud_obj.stud_records

            data = {"name": stud_obj.stud_name, "qq": stud_obj.qq}
            stud_data.append(data)
        return stud_data


    @staticmethod
    def query_class_all():
        '''查所有班级课程'''
        class_data = []
        class_objs = class_obj = session.query(db_table_arc.Classes).all()
        if len(class_objs) == 0:
            return class_data
        else:
            for class_obj in class_objs:
                data = {"id": class_obj.id, "class_name": class_obj.class_name}
                class_data.append(data)
            return class_data





    @staticmethod
    def create_student(st_name, qq_id):
        stud_obj = db_table_arc.Students(stud_name=st_name, qq=qq_id)
        session.add(stud_obj)
        session.commit()

    @staticmethod
    def query_all_stud():
        stud_data = session.query(db_table_arc.Students).all()
        stud_list = []
        for stud_obj in stud_data:
            classes = stud_obj.classes
            cla_list = []
            for cla in classes:
                cla_list.append(cla.class_name)
            stud_list.append({"name": stud_obj.stud_name, "qq": stud_obj.qq, "learn_class": cla_list})

        return stud_list



    @staticmethod
    def add_stud_to_class_by_qq(qq_id, class_name):
        stud_obj = session.query(db_table_arc.Students).filter_by(qq=qq_id).first()
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=class_name).first()
        if class_obj == None:
            print("No class named %s"%class_name)
            return
        stud_obj.classes = [class_obj]
        session.commit()

    @staticmethod
    def create_class_records(cla_name):
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=cla_name).first()
        date = time.strftime("%Y-%m-%d")
        session.add(db_table_arc.Class_records(class_time=date, class_id=class_obj.id))
        session.commit()

    @staticmethod
    def create_stud_records(score, stud_id, class_records_id):
        session.add(db_table_arc.Stud_records(score=score, stud_id=stud_id, class_records_id=class_records_id))
        session.commit()

    @staticmethod
    def initialize_class_records(cla_name):
        '''创建一个课程记录，同时创建报该班所有同学的记录'''

        # 获取课程对象
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=cla_name).first()

        # 创建上课记录
        date = time.strftime("%Y-%m-%d")
        session.add(db_table_arc.Class_records(class_time=date, class_id=class_obj.id))

        # 获取该记录对象
        class_records_obj = session.query(db_table_arc.Class_records).filter_by(class_time=date).filter_by(class_id=class_obj.id).first()

        # 获取报该班的学生对象
        stud_objs = class_obj.students

        # 为每一个学生创建上课记录，并与课程记录关联
        stud_record_list = []
        for stud_obj in stud_objs:
            stud_record_list.append(db_table_arc.Stud_records(score=0, stud_id=stud_obj.id, class_records_id=class_records_obj.id))
        session.add_all(stud_record_list)

        session.commit()

    @staticmethod
    def query_class_stud_record(class_name, date):
        '''查询一个课程记录对应的所有学生记录'''
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=class_name).first()
        class_records_obj = session.query(db_table_arc.Class_records).filter_by(class_time=date).filter_by(class_id=class_obj.id).first()
        stud_records_objs = class_records_obj.stud_records

        s_r_data = []

        for stud_records_obj in stud_records_objs:
            score = stud_records_obj.score
            stud_name = stud_records_obj.students.stud_name
            stud_qq = stud_records_obj.students.qq

            # print("score: %s; name: %s; QQ: %s"%(score, stud_name, stud_qq))

            data = {"score": score, "stud_name": stud_name, "stud_qq": stud_qq}
            s_r_data.append(data)

        return s_r_data

    @staticmethod
    def query_a_class_all_records(class_name):
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=class_name).first()
        class_records = class_obj.class_records

        c_r_data = []

        for class_record in class_records:
            class_time = class_record.class_time
            # print("上课时间：%s"%class_time)
            data = {"class_time": class_time}
            c_r_data.append(data)

        return c_r_data

    @staticmethod
    def modify_stud_score(score, date, class_name, qq):
        class_obj = session.query(db_table_arc.Classes).filter_by(class_name=class_name).first()
        class_records = class_obj.class_records


        for class_record in class_records:
            # print("time:", class_record.class_time, type(class_record.class_time))
            # print("date", date)
            if str(class_record.class_time) == date:
                class_record_obj = class_record

                stud_obj = session.query(db_table_arc.Students).filter_by(qq=qq).first()
                stud_record_obj = session.query(db_table_arc.Stud_records).filter_by(stud_id=stud_obj.id).filter_by(class_records_id=class_record_obj.id).first()
                stud_record_obj.score = score
                session.commit()

    @staticmethod
    def query_stud_id(name, qq):
        stud_obj = session.query(db_table_arc.Students).filter_by(qq=qq).filter_by(stud_name=name).first()
        if stud_obj ==None:
            return -1
        else:
            return stud_obj.id


    @staticmethod
    def query_stud_info_by_id(id):
        # print("query_stud_info_by_id", id)

        stud_record_objs = session.query(db_table_arc.Stud_records).filter_by(stud_id=id).all()

        record_db_list = []
        for stud_record_obj in stud_record_objs:
            class_record_obj = stud_record_obj.class_records
            # print("课程名称：%s, 课程时间：%s"%(class_record_obj.classes.class_name, class_record_obj.class_time))
            record_db_list.append((class_record_obj.classes.class_name, class_record_obj.class_time))

        return record_db_list





        # stud_obj = session.query(db_table_arc.Students).filter_by(id=id).first()
        # class_list = stud_obj.classes
        # class_db_list =[]
        # for class_obj in class_list:
        #     class_record_list = class_obj.class_records
        #     record_db_list = []
        #     for class_record_obj in class_record_list:
        #         record_db_list.append(str(class_record_obj.class_time))
        #
        #     class_db_list.append({class_obj.class_name : record_db_list})
        #
        # return class_db_list, stud_obj.stud_name

    @staticmethod
    def query_stud_score(id, class_name):

        res = session.query(func.sum(db_table_arc.Stud_records.score), db_table_arc.Stud_records.stud_id).group_by(db_table_arc.Stud_records.stud_id).all()
        # print(res)
        count = 0
        while True:
            count += 1
            result = DbAPI.get_max_value(res)
            # print(result)
            if result[1] == id:
                break
            # print(result[2])
            res.pop(result[2])
        # print("名次：%s"% count)

        stud_obj = session.query(db_table_arc.Students).filter_by(id=id).first()
        stud_records = stud_obj.stud_records
        score_data = []

        for stud_record_obj in stud_records:
            stud_score = stud_record_obj.score
            class_record_obj = stud_record_obj.class_records
            class_record_time = class_record_obj.class_time

            stud_task = stud_record_obj.task

            # print("分数：%s; 课程时间：%s"%(stud_score, str(class_record_time)))
            score_data.append({"score": int(stud_score), "time": str(class_record_time), 'stud_task': stud_task})

        return score_data, count

    @staticmethod
    def get_max_value(res):
        max = 0
        k = 0
        for i in range(len(res)):
            max = int(res[i][0])
            for j in range(len(res)):
                if max < int(res[j][0]):
                    max = int(res[j][0])
                    k = j

        return (max, int(res[k][1]), k)

    @staticmethod
    def modify_stud_record_task(stud_id, class_name, time, task_name):
        stud_record_objs = session.query(db_table_arc.Stud_records).filter_by(stud_id=stud_id).all()
        for stud_record_obj in stud_record_objs:
            record_db_time = str(stud_record_obj.class_records.class_time)
            class_db_name = stud_record_obj.class_records.classes.class_name
            if class_name == class_db_name and time == record_db_time:
                stud_record_obj.task = task_name
                session.commit()


if __name__ == '__main__':
    # DbAPI.create_student("高绍阳", "287586479")
    # DbAPI.create_student("高绍华", "287586478")
    # DbAPI.create_student("高绍见", "287586477")
    # DbAPI.create_class("python")
    # DbAPI.add_stud_to_class_by_qq("287586479", "python")
    # DbAPI.add_stud_to_class_by_qq("287586478", "python")
    # DbAPI.add_stud_to_class_by_qq("287586477", "python")
    # DbAPI.initialize_class_records("python")
    # DbAPI.create_class("linux")
    # print(DbAPI.query_class_by_name('python'))
    # print(DbAPI.query_class_all())
    # DbAPI.query_class_stud_record("python", "2017-12-13")
    # DbAPI.query_a_class_all_records("python")

    # DbAPI.modify_stud_score(78, "2017-12-12", "python", "287586479")
    # print(DbAPI.query_all_stud())
    # print(DbAPI.query_stud_info_by_id(3))
    DbAPI.query_stud_score(5, "python")
    # DbAPI.modify_stud_record_task(1, 'python', '2017-12-12', "zuoye.zip")