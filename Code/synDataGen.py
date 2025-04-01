"""
This script was used to generate synthetic student data to use in early-satge algorithm 
development. Course codes were copied and pasted from CourseHero.ie
The code then generates random student 8-digit numbers between 10000000 and 99999999. 
50 students were generated for each course code in the university.
"""
import random
import csv

course_codes = [
    "TR002", "TR003", "TR004", "TR005", "TR006", "TR007", "TR009", 
    "TR015", "TR016", "TR018", "TR019", "TR021", "TR022", "TR023", 
    "TR024", "TR025", "TR028", "TR031", "TR032", "TR033", "TR034", 
    "TR035", "TR038", "TR039", "TR040", "TR041", "TR042", "TR043", 
    "TR051", "TR052", "TR053", "TR054", "TR055", "TR056", "TR060", 
    "TR061", "TR062", "TR063", "TR064", "TR072", "TR080", "TR081", 
    "TR084", "TR085", "TR086", "TR087", "TR089", "TR090", "TR091", 
    "TR093", "TR095", "TR097", "TR111", "TR112", "TR113", "TR114", 
    "TR117", "TR166", "TR173", "TR177", "TR179", "TR188", "TR197", 
    "TR198", "TR202", "TR207", "TR208", "TR209", "TR212", "TR214", 
    "TR228", "TR230", "TR231", "TR233", "TR239", "TR240", "TR241", 
    "TR262", "TR263", "TR269", "TR272", "TR276", "TR277", "TR311", 
    "TR312", "TR320", "TR322", "TR323", "TR324", "TR325", "TR326", 
    "TR328", "TR332", "TR443", "TR447", "TR449", "TR454", "TR455", 
    "TR457", "TR479", "TR482", "TR485", "TR546", "TR547", "TR548", 
    "TR554", "TR563", "TR564", "TR565", "TR566", "TR580", "TR581", 
    "TR582", "TR587", "TR588", "TR589", "TR592", "TR597", "TR598", 
    "TR599", "TR629", "TR635", "TR636", "TR638", "TR639", "TR662", 
    "TR663", "TR664", "TR665", "TR666", "TR667", "TR668", "TR669", 
    "TR670", "TR671", "TR672", "TR756", "TR757", "TR758", "TR759", 
    "TR801", "TR802", "TR803", "TR911", "TR913"
]

with open('studentData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Student Number", "Course Code"])
    
    for course_code in course_codes:
        for _ in range(50):
            student_number = random.randint(10000000, 99999999)
            writer.writerow([student_number, course_code])
