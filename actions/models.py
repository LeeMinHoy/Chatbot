from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from db import connection

DATABASE_URL = 'mysql+pymysql://root:vanchuong135b@localhost:3306/chatbot'
engine = connection.connect(DATABASE_URL)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement= True)
    student_id = Column(String(8), primary_key= True, nullable=False, unique = True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    registrations = relationship('Registration', back_populates='student')

class Course(Base):
    __tablename__ = "courses"
    id = Column(String(6), primary_key= True, nullable= False)
    name = Column(String(1000), nullable = False)
    credits = Column(Integer, nullable= False)
    classes = relationship('Class', back_populates='course')

class Class(Base):
    __tablename__ = "classes"
    id = Column(String(4), primary_key = True, nullable= False)
    max_slots = Column(Integer, nullable= False)
    current_slots = Column(Integer, default= 0)
    lecturer = Column(String(100))
    schedule = Column (String(1000))
    subject_id = Column(String(6) ,ForeignKey('courses.id'), nullable= False)
    
    course = relationship('Course', back_populates='classes')

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(8), ForeignKey('users.student_id'), nullable=False)
    class_id = Column(String(4), ForeignKey('classes.id'), nullable=False)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student = relationship('User', back_populates='registrations')
    class_ = relationship('Class', back_populates='students')



# Tạo tất cả các bảng
Base.metadata.create_all(bind=engine)