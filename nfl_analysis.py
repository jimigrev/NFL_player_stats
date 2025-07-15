import csv

with open('player_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
