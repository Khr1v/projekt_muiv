import csv
import random

file_name = "datqwe2.csv"

cifr = ["X1","Y1","X2","Y2","X3","Y3", "X4","Y4"]
# cifr = ["X1","Y1","X2","Y2"]



data = [cifr]

for _ in range(15):
    x = random.randint(0,20)
    y = random.randint(0,20)
    x2 = random.randint(0,20)
    y2 = random.randint(0, 20)
    x3 = random.randint(0,20)
    y3 = random.randint(0, 20)
    x4 = random.randint(0,20)
    y4 = random.randint(0, 20)
    data.append([x,y,x2,y2,x3,y3,x4,y4])
    # data.append([x,y,x2,y2 ])


with open(file_name, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)