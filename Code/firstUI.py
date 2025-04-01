import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import os

# ----------------------
# probability based algo
# ----------------------
def calculate_probabilities(tutor_row, course_name, student_faculty):
    
    weights = 0

    if pd.notna(tutor_row["Preferably"]) and course_name == tutor_row["Preferably"]:
        weights += 1.0
    if pd.notna(tutor_row["Then"]) and course_name == tutor_row["Then"]:
        weights += 0.5
    if tutor_row["allocate to Faculty"] == student_faculty:
        weights += 0.5
    if tutor_row["Also"] == student_faculty:
        weights += 0.25
    if pd.notna(tutor_row["But never"]) and course_name in tutor_row["But never"].split(','):
        return 0  

    return weights if weights > 0 else 0.1  

def assign_tutors(tutor_df, student_df):
    tutor_allocation = {tutor: [] for tutor in tutor_df["SPR"]}
    tutor_capacity = {row["SPR"]: row["Allocate (N)"] for _, row in tutor_df.iterrows()}
    unallocated_students = []

    for _, student in student_df.iterrows():
        course_name = student["Course Name"]
        student_faculty = student["Faculty/School"]

        eligible_tutors = tutor_df[~tutor_df["But never"].fillna('').str.contains(course_name, na=False)].copy()
        eligible_tutors["Probability"] = eligible_tutors.apply(
            lambda x: calculate_probabilities(x, course_name, student_faculty), axis=1
        )
        eligible_tutors = eligible_tutors[eligible_tutors["Probability"] > 0]

        if eligible_tutors.empty:
            unallocated_students.append(student["Code"])
            continue

        total_weight = eligible_tutors["Probability"].sum()
        eligible_tutors["Normalized Probability"] = eligible_tutors["Probability"] / total_weight

        assigned = False
        tutor_choices = eligible_tutors["SPR"].tolist()
        tutor_probabilities = eligible_tutors["Normalized Probability"].tolist()

        while tutor_choices:
            chosen_tutor = np.random.choice(tutor_choices, p=tutor_probabilities)
            if len(tutor_allocation[chosen_tutor]) < tutor_capacity[chosen_tutor]:
                tutor_allocation[chosen_tutor].append(student["Code"])
                assigned = True
                break
            else:
                index = tutor_choices.index(chosen_tutor)
                tutor_choices.pop(index)
                tutor_probabilities.pop(index)
                if tutor_probabilities:
                    tutor_probabilities = [p / sum(tutor_probabilities) for p in tutor_probabilities]

        if not assigned:
            unallocated_students.append(student["Code"])

    return tutor_allocation, unallocated_students

# ----------------------
# gui
# ----------------------
class AssignmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tutor-Student Assignment")

        self.tutor_file = ""
        self.student_file = ""
        self.assignment_result = None
        self.unallocated_students = []

        
        tk.Button(root, text="Upload Tutors CSV", command=self.upload_tutors).pack(pady=10)
        tk.Button(root, text="Upload Students CSV", command=self.upload_students).pack(pady=10)

    
        tk.Button(root, text="Run Assignment", command=self.run_assignment).pack(pady=10)

        
        tk.Button(root, text="Download Results", command=self.download_results).pack(pady=10)

    def upload_tutors(self):
        self.tutor_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        messagebox.showinfo("File Selected", f"Tutors file selected: {self.tutor_file}")

    def upload_students(self):
        self.student_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        messagebox.showinfo("File Selected", f"Students file selected: {self.student_file}")

    def run_assignment(self):
        if not self.tutor_file or not self.student_file:
            messagebox.showwarning("Input Missing", "Please upload both tutor and student CSV files.")
            return

        tutor_df = pd.read_csv(self.tutor_file)
        student_df = pd.read_csv(self.student_file)

        self.assignment_result, self.unallocated_students = assign_tutors(tutor_df, student_df)

        if self.unallocated_students:
            messagebox.showinfo("Unallocated Students", f"Some students couldn't be allocated: {self.unallocated_students}")
        else:
            messagebox.showinfo("Assignment Completed", "All students have been successfully allocated.")

    def download_results(self):
        if not self.assignment_result:
            messagebox.showwarning("No Data", "No results to download. Run the assignment first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if save_path:
            result_df = pd.DataFrame([
                {'tutor': tutor, 'students': ', '.join(map(str, students))}
                for tutor, students in self.assignment_result.items()
            ])
            result_df.to_csv(save_path, index=False)
            messagebox.showinfo("File Saved", f"Results saved to {save_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentApp(root)
    root.mainloop()
