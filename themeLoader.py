"""
themeLoader.py

Αυτό το αρχείο φορτώνει τον πίνακα THEME_MATRIX από το αρχείο CSV (themeMatrix.csv)
και παρέχει συναρτήσεις για εύκολη πρόσβαση στις χρωματικές τιμές κάθε theme.
Υποστηρίζει CSV με BOM (utf-8-sig) για πλήρη συμβατότητα με Excel.
Το αρχείο αυτό χρησιμοποιείται απο το themeManager.py
"""

import csv

CSV_FILE = "themeMatrix.csv"

def load_theme_matrix_from_csv(path=CSV_FILE):
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix, fieldnames

def get_all_theme_names():
    matrix, fieldnames = load_theme_matrix_from_csv()
    return fieldnames[1:]  # skip 'key'


def get_theme(theme_name):
    matrix, fieldnames = load_theme_matrix_from_csv()
    theme = {}
    for row in matrix:
        key = row["key"]
        theme[key] = row.get(theme_name)
    return theme