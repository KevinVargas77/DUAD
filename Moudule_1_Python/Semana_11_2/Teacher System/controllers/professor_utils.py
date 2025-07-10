import csv

def get_professor_name(professor_id, filename="data/professors.csv"):
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == professor_id:
                return row["Full_name"]
    return None
