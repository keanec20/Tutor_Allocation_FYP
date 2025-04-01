import random
import csv

faculties = ["Arts, Humanities and Social Sciences", "Health Sciences","Science, Technology, Engineering and Mathematics"
]
chamberSize = ["40", "80","120"]
with open('tutorData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Staff Number", "Faculty", "Ontake"])
    
    for faculty in faculties:
        for _ in range(50):
            staffNumber = random.randint(1000, 9999)
            ontake = random.choice(chamberSize)
            writer.writerow([staffNumber, faculty, ontake])