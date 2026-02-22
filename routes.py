from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection, dict_from_row

router = APIRouter()

#-----------------------------------------------------------------------
# Endpoint 1. GET /students -> get all student records
#     status code should return 200 OK
@router.get("/students", status_code=200)
def get_all_students():
    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()  # cursor lets us run SQL commands

    # execute via the cursor. Use SQL query to get the data.
    cursor.execute("SELECT * FROM students")

    # grab all the rows of students and return them
    rows = cursor.fetchall()  # fetchall gets every row from the query
    conn.close()  # close when done

    # create an empty student array
    students = []

    # loop over the database rows
    for row in rows:
        # convert each row into a dictionary
        student = dict_from_row(row)
        students.append(student)  # add each student to the array

    # return the students array
    return students
#-----------------------------------------------------------------------

# Endpoint 2. GET /students/by-major -> retrieve students filtered by their major
@router.get("/students/by-major", status_code=200)
def get_students_by_major(major: str):
    # do i need to raise an http exception??
    
    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # get students by their major
    cursor.execute("SELECT * FROM students WHERE major = ?", (major,))
    rows = cursor.fetchall() # get all students from that major
    
    conn.close() #close when done

    # convert the rows to a list of students via dictionaries
    students =[]
    for row in rows:
        student = dict_from_row(row)
        students.append(student)
    # return the students
    return students

#-----------------------------------------------------------------------
# Endpoint 3. GET /students/by-gpa -> retrieve students filtered by their gpa (ABOVE A SPECIFIC threshold)
@router.get("/students/by-gpa", status_code=200)
def get_students_by_gpa(min_gpa: float):
    # validate the min_gpa input
    if min_gpa < 0.0 or min_gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # get students with a gpa >= min_gpa
    cursor.execute("SELECT * FROM students WHERE gpa >= ?", (min_gpa,))
    rows = cursor.fetchall()  # get them all from the database

    conn.close()  # close it

    # convert rows to list of student dictionaries
    students = []
    for row in rows:
        student = dict_from_row(row)
        students.append(student)

    return students
#-----------------------------------------------------------------------

# Endpoint 4. GET /students/{student_id} -> retrieve a specific student by their ID
@router.get("/students/{student_id}", status_code=200)
def get_student(student_id: int):
    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # get the student by their id
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()  # get the one student

    conn.close()  # close it

    # if student is NOT found, return 404 
    if row is None:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

    # convert the row into a dictionary and return it
    student = dict_from_row(row)
    return student
#-----------------------------------------------------------------------


# Endpoint 5. POST students -> Create a new student record
@router.post("/students", status_code=201)
def create_student(student: Student):
    # validations: 
    # the name cannot be empty
    if not student.name or not student.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    # validate the major
    if not student.major or not student.major.strip():
        raise HTTPException(status_code=400, detail="Major cannot be empty")

    # gpa has to be between 0.0 and 4.0
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # insert the new student
    cursor.execute(
        "INSERT INTO students (name, email, major, gpa, enrollment_year) VALUES (?, ?, ?, ?, ?)",
        (student.name, student.email, student.major, student.gpa, student.enrollment_year)
    )

    conn.commit()

    # get the id of the new student
    newID = cursor.lastrowid

    # return the created student  
    cursor.execute("SELECT * FROM students WHERE id = ?", (newID,))
    row = cursor.fetchone()

    conn.close()
    return dict_from_row(row)
#-----------------------------------------------------------------------


# Endpoint 6. PUT /students/{student_id} -> Update an existing setudent record (replace entire record).
@router.put("/students/{student_id}", status_code=200)
def update_student(student_id: int, student: Student):
    # validation checks:
    # the name cannot be empty
    if not student.name or not student.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    # validate the major
    if not student.major or not student.major.strip():
        raise HTTPException(status_code=400, detail="Major cannot be empty")

    # gpa has to be between 0.0 and 4.0
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # check if the student exists
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    existingStudent = cursor.fetchone()  # fetch the student 

    # if the student doesn't exist
    if existingStudent is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    # update the record
    cursor.execute(
        "UPDATE students SET name = ?, email = ?, major = ?, gpa = ?, enrollment_year = ? WHERE id = ?",
        (student.name, student.email, student.major, student.gpa, student.enrollment_year, student_id)
    )

    conn.commit()

    # fetch updated student
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    
    # return the student
    conn.close()
    return dict_from_row(row)
#-----------------------------------------------------------------------


# Endpoint 7. DELETE /students/{student_id} -> Delete a student record by student_id.
@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    # status code should be 204 if no content with no response body

    # connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    # check if student exists
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    existing = cursor.fetchone()

    # raise http exeception error 404 Student with id is not found
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    # delete the student
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    # return nothing if there was no content
    return
#-----------------------------------------------------------------------

