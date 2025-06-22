"""
themeLoader.py

Αυτό το αρχείο φορτώνει τον πίνακα THEME_MATRIX από το αρχείο CSV (themeMatrix.csv)
και παρέχει συναρτήσεις για εύκολη πρόσβαση στις χρωματικές τιμές κάθε theme.
Υποστηρίζει CSV με BOM (utf-8-sig) για πλήρη συμβατότητα με Excel.
"""

import csv

# --------------------------------------------------
# Διάβασμα του themeMatrix.csv με υποστήριξη BOM (utf-8-sig)
# --------------------------------------------------

def load_theme_matrix_from_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        matrix = {}
        for row in reader:
            key = row.get("key")
            if not key:
                continue
            matrix[key] = [row[theme] for theme in reader.fieldnames[1:]]
        return matrix

# Φορτώνουμε τον πίνακα κατά την εισαγωγή του module
THEME_MATRIX = load_theme_matrix_from_csv("themeMatrix.csv")

def get_theme_names():
    return ["dark", "light", "purple", "oceanic", "goth", "mondrian", "rainbow", "excel2003", "windows95"]

def get_theme_value(key, theme_name, fallback=""):
    try:
        theme_index = get_theme_names().index(theme_name)
        return THEME_MATRIX[key][theme_index]
    except (KeyError, ValueError, IndexError):
        return fallback

def get_theme(mode="dark"):
    return {key: get_theme_value(key, mode) for key in THEME_MATRIX}

def list_available_keys():
    return list(THEME_MATRIX.keys())
