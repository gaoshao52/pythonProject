#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, DATE, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("mysql+pymysql://sam:sam@10.100.203.154:3306/test?charset=utf8")

Base = declarative_base()

class_m2m_student = Table("class_m2m_student", Base.metadata,
                          Column("class_id", Integer, ForeignKey('classes.id')),
                          Column("stud_id", Integer, ForeignKey('students.id'))
                          )

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(32), nullable=False)


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stud_name = Column(String(32), nullable=False)
    qq = Column(String(32), nullable=False)

    classes = relationship("Classes", secondary=class_m2m_student, backref='students')


class Class_records(Base):
    __tablename__ = 'class_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_time = Column(DATE, nullable=False)

    class_id = Column(Integer, ForeignKey('classes.id'))

    classes = relationship("Classes", backref="class_records")


class Stud_records(Base):
    __tablename__ = 'stud_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer)
    task = Column(String(64), nullable=True, default="no")

    stud_id = Column(Integer, ForeignKey('students.id'))

    class_records_id = Column(Integer, ForeignKey('class_records.id'))

    students = relationship("Students", foreign_keys=[stud_id], backref="stud_records")

    class_records = relationship("Class_records", foreign_keys=[class_records_id], backref="stud_records")



Base.metadata.create_all(engine)

if __name__ == '__main__':
    session = sessionmaker(bind=engine)()
    # stud_obj = Students(stud_name="高绍阳", qq="287586479")
    # session.add(stud_obj)
    # session.commit()
    # stud_obj = session.query(Students).filter(Students.qq == "28758479").first()
    # print(stud_obj)
    # print(stud_obj.qq, stud_obj.stud_name)
    res = session.query(func.sum(Stud_records.score), Stud_records.stud_id).group_by(Stud_records.stud_id).all()
    print(res)
    max = 0
    k = 0
    for i in range(len(res)):
        max = int(res[i][0])
        for j in range(len(res)):
            if max < int(res[j][0]):
                max = int(res[j][0])
                k = j

    print(max, k)







