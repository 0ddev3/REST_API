# Student Records REST API


This project is a RESTful API that manages student records stored in a SQLite database.It lets you add students, update them, delete them, and look them up. There are also 2 filiters such as searching by GPA or major.

---

## Backend

- FastAPI  
- SQLite  
- Pydantic  

---

## Installation & Setup

### 1. Clone or download the project
```sh
git clone "https://github.com/0ddev3/REST_API"
```

### 2. Go into the project folder
```sh
cd RESTAPI
```

### 3. Create and activate a virtual environment

-Linux / macOS
```sh
python3 -m venv venv
source venv/bin/activate
```

-Windows
```sh
python -m venv venv
venv\Scripts\activate
```

### 4. Install the required packages
```sh
pip install -r requirements.txt
````

### 5. Start the server
```sh
uvicorn main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```
---

## API Endpoints

### GET /students
Returns a list of all students.  
**Status:** 200 OK

---

### GET /students/{student_id}
Returns one student by ID.  
If the ID doesn’t exist, you get a 404.  
**Status:** 200 OK, 404 Not Found

---

### GET /students/by-major?major=MajorName
Returns all students with the given major.  
**Status:** 200 OK

---

### GET /students/by-gpa?min_gpa=value
Returns students with a GPA greater than or equal to the value.  
Also checks that GPA is between 0.0 and 4.0.  
**Status:** 200 OK, 400 Bad Request

---

### POST /students
Creates a new student.  
You need: name, email, major, gpa, enrollment_year.  
**Status:** 201 Created, 400 Bad Request

---

### PUT /students/{student_id}
Updates an existing student.  
If the ID doesn’t exist, you get a 404.  
**Status:** 200 OK, 400 Bad Request, 404 Not Found

---

### DELETE /students/{student_id}
Deletes a student by ID.  
**Status:** 204 No Content, 404 Not Found

---

## Testing the API
Go to the built in-docs below:

```
http://127.0.0.1:8000/docs
```

From there you can try all the endpoints.

---

## Example Requests

### 1. Creating a student (POST /students)
```json
{
  "name": "Yvette Boyd",
  "email": "ev3@gmail.com",
  "major": "Computer Science",
  "gpa": 3.8,
  "enrollment_year": 2023
}
```

---

### 2. Getting a student by ID (GET /students/1)
```json
{
  "id": 1,
  "name": "Yvette Boyd",
  "email": "ev3@gmail.com",
  "major": "Computer Science",
  "gpa": 3.8,
  "enrollment_year": 2023
}
```

---

### 3. Updating a student (PUT /students/1)
```json
{
  "name": "Yvette Boyd.",
  "email": "ev3@gmail.com",
  "major": "Mathematics",
  "gpa": 3.9,
  "enrollment_year": 2026
}
```

---
