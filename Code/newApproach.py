import pandas as pd

# Load Data
students = pd.read_csv("studentData.csv")  # Student Data
tutors = pd.read_csv("tutorData.csv")      # Tutor Data

# Initialize Allocation
tutor_allocation = {tutor: [] for tutor in tutors["SPR"]}
tutor_capacity = {row["SPR"]: row["Allocate (N)"] for _, row in tutors.iterrows()}

# Helper Functions
def is_course_allowed(tutor_row, course_name):
    """Check if a tutor is willing to take a given course."""
    if course_name in tutor_row["But Never"].split(","):
        return False
    return True

def get_course_priority(tutor_row, course_name):
    """Determine priority for a course based on 'Preferably' and 'Then' fields."""
    if course_name == tutor_row["Preferably"]:
        return 1
    for i, column in enumerate(["Then", "Then.1", "Then.2", "Then.3"]):  # Adjust for actual column names
        if course_name == tutor_row[column]:
            return i + 2
    return float("inf")  # Lowest priority if no match

# Allocation Logic
for _, student in students.iterrows():
    student_id = student["Code"]
    course_name = student["Course Name"]
    student_faculty = student["Faculty/School"]

    # Filter eligible tutors
    eligible_tutors = tutors[
        (tutors["Allocate to Faculty"] == student_faculty) |
        (tutors["And Also"] == student_faculty)
    ]
    eligible_tutors = eligible_tutors[
        eligible_tutors.apply(lambda x: is_course_allowed(x, course_name), axis=1)
    ]

    # Rank tutors by course preference and availability
    eligible_tutors["Priority"] = eligible_tutors.apply(
        lambda x: get_course_priority(x, course_name), axis=1
    )
    eligible_tutors = eligible_tutors.sort_values(by=["Priority"])

    # Assign student to the first available tutor
    assigned = False
    for _, tutor in eligible_tutors.iterrows():
        tutor_id = tutor["SPR"]
        if tutor_capacity[tutor_id] > len(tutor_allocation[tutor_id]):
            tutor_allocation[tutor_id].append(student_id)
            assigned = True
            break

    if not assigned:
        print(f"Student {student_id} could not be allocated a tutor.")

# Output Allocation
for tutor_id, allocated_students in tutor_allocation.items():
    print(f"Tutor {tutor_id} is assigned students: {allocated_students}")
