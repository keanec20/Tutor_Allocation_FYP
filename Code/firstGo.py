"""
This script is an inital high-level approach to the problem.
Matching strategy focused solely on faculty alignment as this was hinted at as being a 
considerable factor.
Data files used were created by synDataGen.py and tutorData.py
"""
import pandas as pd

students = pd.read_csv('studentData.csv')
tutors = pd.read_csv('tutorData.csv')
courses = pd.read_csv('courses.csv')

courseFaculty = {row['Course Code']: row['Faculty'] for _, row in courses.iterrows()}
tutorCapacity = {row['Staff Number']: row['Ontake'] for _, row in tutors.iterrows()}

tutorStudents = {tutor: [] for tutor in tutorCapacity.keys()}

# looping through students to assign students to tutors
for _, student in students.iterrows():
    studentNumber = student['Student Number']
    studentCourse = student['Course Code']
    
    # match student to faculty
    student_faculty = courseFaculty.get(studentCourse)
    # match tutor to faculty
    available_tutors = [
        tutor for tutor in tutorStudents.keys() 
        if tutorCapacity[tutor] > len(tutorStudents[tutor]) 
        and tutors[tutors['Staff Number'] == tutor]['Faculty'].values[0] == student_faculty
    ]

    if available_tutors:
        # assign to the first available tutor
        assigned_tutor = available_tutors[0]
        tutorStudents[assigned_tutor].append(studentNumber)


        tutorCapacity[assigned_tutor] -= 1

# output 
for tutor, assigned_students in tutorStudents.items():
    print(f'Tutor {tutor} is assigned students: {assigned_students}')
