import csv
import os

def save_player_score(player_name, score, filename="scores.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player", "Score"])
        writer.writerow([player_name, score])
