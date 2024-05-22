import csv
import random
import string

file_name = "data_diagra.csv"

# labels = ['продукты', 'напитки', 'бакалерия', 'вода', 'алкоголь','фрукты','овощи','игрушки','шоколад']
labels = ['MERSEDES', 'BMW', 'AUDI', 'OPEL', 'HONDA','ROLSROYS','FERRARI','BENTLY']


data = []

# Генерируем случайные данные
for _ in range(7):
    label = random.choice(labels)  # Выбираем случайную метку из списка labels
    value = random.randint(0, 20)  # Генерация случайного значения
    data.append([label, value])

# Записываем данные в CSV файл
with open(file_name, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["labels", "values"])  # Записываем заголовки столбцов
    writer.writerows(data)