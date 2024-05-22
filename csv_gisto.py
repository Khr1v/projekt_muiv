import csv
import random



file_name = "datqGISTo.csv"

cifr = ["pushcares buys","people  "]
# cifr = []


data = [cifr]

for _ in range(30):
    x = random.randint(0,30)
    y = random.randint(0,30)
    # x = _
    # y = _ +1
    data.append([x,y])

with open(file_name, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)