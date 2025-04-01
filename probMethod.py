import pandas as pd
import numpy as np


students = pd.read_csv("Mock CAO round 1 offers.csv", usecols=["Code", "Course Name", "Faculty/School"])
tutors = pd.read_csv("mock tutor database v2.csv", usecols=["SPR", "Allocate (N)", "allocate to Faculty", "Also", "Preferably", "Then", "But never"])

# initialise
tutor_allocation = {tutor: [] for tutor in tutors["SPR"]}
tutor_capacity = {row["SPR"]: row["Allocate (N)"] for _, row in tutors.iterrows()}

def calculate_probabilities(tutor_row, course_name, student_faculty):
    """Calculate weighted probabilities for a tutor to be assigned a student."""
    weights = []
    courses = tutor_row[["Preferably", "Then"]].dropna().values
    
    if course_name in courses:
        weights.append(1.0)
    elif tutor_row["allocate to Faculty"] == student_faculty:
        weights.append(0.5)
    elif tutor_row["Also"] == student_faculty:
        weights.append(0.25)
    else:
        weights.append(0.1)  
    
    return np.mean(weights)  #normalise


unallocated_students = []

for _, student in students.iterrows():
    student_id = student["Code"]
    course_name = student["Course Name"]
    student_faculty = student["Faculty/School"]
    
    eligible_tutors = tutors.copy()
    eligible_tutors = eligible_tutors[~eligible_tutors[["But never"]].apply(lambda x: course_name in x.values, axis=1)]
    
    if eligible_tutors.empty:
        unallocated_students.append(student_id)
        continue
    
    eligible_tutors = eligible_tutors.copy()
    eligible_tutors["Probability"] = eligible_tutors.apply(lambda x: calculate_probabilities(x, course_name, student_faculty), axis=1)
    eligible_tutors = eligible_tutors.sort_values(by=["Probability"], ascending=False)
    
    assigned = False
    for _, tutor in eligible_tutors.iterrows():
        tutor_id = tutor["SPR"]
        if len(tutor_allocation[tutor_id]) < tutor_capacity[tutor_id]:
            tutor_allocation[tutor_id].append(student_id)
            assigned = True
            break
    
    if not assigned:
        unallocated_students.append(student_id)

#second try
for student_id in unallocated_students[:]:
    for tutor_id in tutor_allocation:
        if len(tutor_allocation[tutor_id]) < tutor_capacity[tutor_id]:
            tutor_allocation[tutor_id].append(student_id)
            unallocated_students.remove(student_id)
            break


if unallocated_students:
    print("Students who could not be allocated:", unallocated_students)


for tutor_id, allocated_students in tutor_allocation.items():
    print(f"Tutor {tutor_id} is assigned students: {allocated_students}")
