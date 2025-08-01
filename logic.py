import csv
from flask import current_app
import sqlite3

def read_csv(filename: str):
    result = []
    with open(filename, "r") as file:
        for record in csv.DictReader(file):
            result.append(record)
        
    return result


def read_sql(filename: str,table: str):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id integer primary key, name text, age integer, species text, location text);")
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    result = []
    for row in rows:
        row_dict = {}
        for i, col_name in enumerate(column_names):
            row_dict[col_name] = row[i]
        result.append(row_dict)
    conn.close()
    return result
    



"""

def query(form: dict):
    result = []
    element = read_csv("data_for_final.csv")
    for element in current_app.data:
        if form["college_major"] != element["Level and Field of Highest Degree"]: 
            continue
        result.append(element)
    return result

"""
