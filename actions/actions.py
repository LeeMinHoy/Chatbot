# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import connection
from .models import Users, Course, Class, Registration

DATABASE_URL = 'mysql+pymysql://root:vanchuong135b@localhost:3306/chatbot'
engine = connection.connect(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
class ActionCheckDBConnection(Action):
    def name(self):
        return "action_check_db_connection"

    def run(self, dispatcher, tracker, domain):
        try:
            connection = engine.connect()
            dispatcher.utter_message("Kết nối thành công!")
            connection.close()
        except Exception as e:
            dispatcher.utter_message(f"Kết nối thất bại: {e}")

        return []

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ValidateStudentID(Action):

    def name(self) -> str:
        return "action_validate_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        student_id = next(tracker.get_latest_entity_values("student_id"), None)

        student_id_validate = session.query(Users).filter_by(student_id = student_id)

        if student_id_validate and re.fullmatch(r"\d{8}", student_id):

            dispatcher.utter_message(text=f"Mã sinh viên bạn đang sử dụng để đăng ký là {student_id}.\n Hãy nhập mã môn học bạn đang muốn đăng ký")
            
            return [SlotSet("id_student", student_id)]
        else:
            dispatcher.utter_message(text="Mã sinh viên không hợp lệ hoặc không có . Vui lòng nhập lại mã sinh viên của bạn gồm 8 chữ số.")
            return [SlotSet("id_student", None)]
        

class ValidateSubjectID(Action):
    def name(self) -> str:
        return "action_validate_subject_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        subject_id = next(tracker.get_latest_entity_values("subject_id"), None)
        course_id_validate = session.query(Course).filter_by(id = subject_id)

        if course_id_validate and re.fullmatch(r"[a-zA-Z]{3}\d{4}", subject_id):
            dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {subject_id}.")
            return [SlotSet("subject_id", subject_id)]
        else:
            dispatcher.utter_message(text="Mã môn học không hợp lệ hoặc hiện chưa mở. Mời nhập mã môn học khác.")
            return [SlotSet("subject_id", None)]


class ValidateClassID(Action):
    def name(self) -> str:
        return "action_validate_subject_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject_id = next(tracker.get_latest_entity_values("subject_id"), None)
        class_id = next(tracker.get_latest_entity_values("class_id"), None)

        class_id_validate = session.query(Class).filter_by(id=class_id, subject_id=subject_id)

        if class_id_validate and re.fullmatch(r"[a-zA-Z]{2}\d{2}", class_id):
            dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {class_id}.")

            return [SlotSet("class_id", class_id)]
        else:
            dispatcher.utter_message(text="Mã môn học không hợp lệ hoặc hiện chưa mở. Mời nhập mã môn học khác.")
            return [SlotSet("class_id", None)]

class RegistrationCourse(Action):
    def name(self) -> str:
        return "registration_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        class_ = session.query(Class).filter_by()


class RegistrationTest(Action):
    def name(self) -> str:
        return "all_scene_registration_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Validate student_id
        student_id = next(tracker.get_latest_entity_values("student_id"), None)
        student_id_validate = session.query(Users).filter_by(student_id=student_id)
        if not student_id_validate or not re.fullmatch(r"\d{8}", student_id):
            dispatcher.utter_message(text="Mã sinh viên không hợp lệ hoặc không tồn tại. Vui lòng nhập lại mã sinh viên gồm 8 chữ số.")
            return [SlotSet("id_student", None)]
        dispatcher.utter_message(text=f"Mã sinh viên bạn đang sử dụng để đăng ký là {student_id}.")
        slot_values = [SlotSet("id_student", student_id)]
        
        # Validate subject_id
        subject_id = next(tracker.get_latest_entity_values("subject_id"), None)
        course_id_validate = session.query(Course).filter_by(id=subject_id)
        if not course_id_validate or not re.fullmatch(r"[a-zA-Z]{3}\d{4}", subject_id):
            dispatcher.utter_message(text="Mã môn học không hợp lệ hoặc hiện chưa mở. Vui lòng nhập mã môn học khác.")
            return slot_values + [SlotSet("subject_id", None)]
        dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {subject_id}.")
        slot_values.append(SlotSet("subject_id", subject_id))
        
        # Validate class_id
        class_id = next(tracker.get_latest_entity_values("class_id"), None)
        class_id_validate = session.query(Class).filter_by(id=class_id, subject_id=subject_id)
        if not class_id_validate or not re.fullmatch(r"[a-zA-Z]{2}\d{2}", class_id):
            dispatcher.utter_message(text="Mã lớp học không hợp lệ. Vui lòng nhập mã lớp học khác.")
            return slot_values + [SlotSet("class_id", None)]
        dispatcher.utter_message(text=f"Lớp học bạn đang đăng ký là {class_id}.")
        slot_values.append(SlotSet("class_id", class_id))

        max_slots = class_id_validate.max_slots
        current_slots = class_id_validate.current_slots
        if current_slots < max_slots:
            registration = Registration(
                student_id=student_id_validate.id,
                class_id=class_id_validate.id
            )
            current_slots +=1
            session.add(registration)
            session.commit()
            dispatcher.utter_message(text="Bạn đã đăng ký thành công lớp học.")
            return slot_values
        else:
            dispatcher.utter_message(text="Lớp học này đã đầy. Vui lòng chọn lớp khác.")
            return slot_values + [SlotSet("class_id", None)]
            

        