import sqlite3 as sql
import datetime


def get_faculty_list():
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("SELECT faculty_name FROM faculty")

        return curs.fetchall()


def get_current_faculty_courses_list(faculty_data):
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("Select course_name from course JOIN faculty ON course.id_faculty = faculty.id_faculty where faculty_name == ?", (faculty_data,))

        return curs.fetchall()


def get_current_course_groups_list(course_data, faculty_data):
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("Select group_name from groups JOIN faculty ON course.id_faculty = faculty.id_faculty JOIN course ON groups.id_course = course.id_course where course_name == ? AND faculty_name == ?", (course_data, faculty_data))

        return curs.fetchall()


def get_current_subject_group_list(group_data, course_data):
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("SELECT subject_name FROM subjects JOIN course ON groups.id_course = course.id_course JOIN groups ON subjects.id_group = groups.id_group where group_name == ? AND course_name == ?", (group_data, course_data))

        return curs.fetchall()


def get_current_subject_date_list(subject_data, group_data): #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("SELECT schedule_date FROM schedule JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN groups ON schedule.id_group = groups.id_group where subject_name == ? AND group_name == ?", (subject_data, group_data))

        return curs.fetchall()


def get_current_subject_time_list(subject_data, group_data):  #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT subject_time FROM schedule JOIN subjects_time ON schedule.id_subjects_time = subjects_time.id_subjects_time JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN groups ON schedule.id_group = groups.id_group where subject_name == ? AND group_name == ?", (subject_data, group_data))

        return curs.fetchall()


def get_current_subject_cabinet_list(subject_data, group_data):  #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT cabinet_name FROM schedule JOIN cabinet ON schedule.id_cabinet = cabinet.id_cabinet JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN groups ON schedule.id_group = groups.id_group where subject_name == ? AND group_name == ?", (subject_data, group_data))

        return curs.fetchall()


def get_current_subject_teacher_list(subject_data, group_data):  #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT teacher_name FROM schedule JOIN teachers ON schedule.id_teachers = teachers.id_teacher JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN groups ON schedule.id_group = groups.id_group where subject_name == ? AND group_name == ?", (subject_data, group_data))

        return curs.fetchall()


def get_fteacher_list(name):
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT teacher_name FROM teachers WHERE teacher_name LIKE ?", (name,))

        return curs.fetchall()


def delete_old_schedule(date):
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "DELETE FROM schedule WHERE schedule_date == ?", (date,))


def get_fdate_list(name): #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("SELECT schedule_date FROM schedule JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN teachers ON schedule.id_teachers = teachers.id_teacher JOIN groups ON schedule.id_group = groups.id_group where teacher_name == ? ", (name,))

        return curs.fetchall()


def get_ftime_list(name):  #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT subject_time FROM schedule JOIN subjects_time ON schedule.id_subjects_time = subjects_time.id_subjects_time JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN teachers ON schedule.id_teachers = teachers.id_teacher JOIN  groups ON schedule.id_group = groups.id_group where teacher_name == ?", (name,))

        return curs.fetchall()


def get_fcabinet_list(name):  #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT cabinet_name FROM schedule JOIN cabinet ON schedule.id_cabinet = cabinet.id_cabinet JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN teachers ON schedule.id_teachers = teachers.id_teacher JOIN groups ON schedule.id_group = groups.id_group where teacher_name == ? ", (name,))

        return curs.fetchall()


def get_fsubject_list(name):  #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute(
            "SELECT subject_name FROM schedule JOIN teachers ON schedule.id_teachers = teachers.id_teacher JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN groups ON schedule.id_group = groups.id_group where teacher_name == ? ", (name,))

        return curs.fetchall()

def get_fgroup_list(name): #
    with sql.connect('intensive_schedule.db') as db:
        curs = db.cursor()
        curs.execute("SELECT group_name FROM schedule JOIN subjects ON schedule.id_subject = subjects.id_subject JOIN teachers ON schedule.id_teachers = teachers.id_teacher JOIN groups ON schedule.id_group = groups.id_group where teacher_name == ? ", (name,))

        return curs.fetchall()
