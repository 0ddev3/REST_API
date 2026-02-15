# API endpoints 
from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection


router = APIRouter()

#-----------------------------------------------------------------------
@router.get("/students") # TODO: Replace ??? with correct endpoint path
def get_all_students():
# TODO: Implement this
# get the connection 
    conn = get_connection()
    cursor = conn.cursor()
# 
    cursor.execute('SELECT * FROM students')

    row = cursor.fetchone()
    conn.close()

pass

#------------------------------------------------------------------
@router.get("/students/by-major") # TODO: Replace ??? with correct endpoint path
def get_students_by_major(major: str):
# TODO: Implement this
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE major = ?", (major,))
    
    row = cursor.fetchone()
    conn.close()
    
pass

#---------------------------------------------------------------------------
@router.get("/students/by-gpa") # TODO: Replace ??? with correct endpoint path
def get_students_by_gpa(min_gpa: float):
# TODO: Implement this

    conn = get_connection() 
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE gpa >= ?", (min_gpa,))
    
    
    row = cursor.fetchone()
    conn.close()

pass

#----------------------------------------------------------------------
@router.get("/students/{student_id}") # TODO: Replace ??? with correct endpoint path
def get_student(student_id: int):
# TODO: Implement this
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id))

    row = cursor.fetchone()
    conn.close()

pass

#---------------------------------------------------------------------------
@router.post("/students", status_code=201) # TODO: Replace ??? with correct endpoint

def create_student(student: Student):
# TODO: Implement this
    

pass

#-------------------------------------------------------------------------
@router.put("/students/{student_id}") # TODO: Replace ??? with correct endpoint path
def update_student(student_id: int, student: Student):
# TODO: Implement this


pass


@router.delete("/students{student_id}") # TODO: Replace ??? with correct endpoint path
def delete_student(student_id: int):
# TODO: Implement this
pas