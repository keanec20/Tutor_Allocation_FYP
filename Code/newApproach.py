"""
This script introduces hierarchical preferencing handling and tutor capacity tracking.
Tutors are filtered first by faculty and then optimal matches are found through the "Preferably" column.
This is done for each student with them being assigned to the highest-priotiy tutor with available capacity.
"""
import pandas as pd

students = pd.read_csv("studentData.csv")  
tutors = pd.read_csv("tutorData.csv")      

tutor_allocation = {tutor: [] for tutor in tutors["SPR"]}
tutor_capacity = {row["SPR"]: row["Allocate (N)"] for _, row in tutors.iterrows()}

def is_course_allowed(tutor_row, course_name):
    if course_name in tutor_row["But Never"].split(","):
        return False
    return True

def get_course_priority(tutor_row, course_name):
    if course_name == tutor_row["Preferably"]:
        return 1
    for i, column in enumerate(["Then", "Then.1", "Then.2", "Then.3"]):  # "Then" column names were adjusted manually within the file at this stage
        if course_name == tutor_row[column]:
            return i + 2
    return float("inf")  # high value == low priority if no match


for _, student in students.iterrows():
    student_id = student["Code"]
    course_name = student["Course Name"]
    student_faculty = student["Faculty/School"]
 
    eligible_tutors = tutors[
        (tutors["Allocate to Faculty"] == student_faculty) |
        (tutors["And Also"] == student_faculty)
    ]
    eligible_tutors = eligible_tutors[
        eligible_tutors.apply(lambda x: is_course_allowed(x, course_name), axis=1)
    ]

    eligible_tutors["Priority"] = eligible_tutors.apply(
        lambda x: get_course_priority(x, course_name), axis=1
    )
    eligible_tutors = eligible_tutors.sort_values(by=["Priority"])

    # students assigned to the first available tutor once capacity constraint checked
    assigned = False
    for _, tutor in eligible_tutors.iterrows():
        tutor_id = tutor["SPR"]
        if tutor_capacity[tutor_id] > len(tutor_allocation[tutor_id]):
            tutor_allocation[tutor_id].append(student_id)
            assigned = True
            break 

    if not assigned:
        print(f"Student {student_id} could not be allocated a tutor.")

for tutor_id, allocated_students in tutor_allocation.items():
    print(f"Tutor {tutor_id} is assigned students: {allocated_students}")
