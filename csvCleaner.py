"""
csv_cleaner.py

Αυτό το εργαλείο:
- Διαβάζει ένα αρχείο CSV που χρησιμοποιεί `;` ως διαχωριστικό
- Ελέγχει αν η πρώτη γραμμή περιέχει σωστά headers (π.χ. 'key')
- Αντικαθιστά τα `;` με `,`
- Σώζει νέο αρχείο ως καθαρό CSV για χρήση με DictReader ή pandas

Χρήση:
    python csv_cleaner.py εισαγωμενο.csv καθαρο.csv
"""

import sys

def clean_csv(input_path, output_path):
    with open(input_path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        cleaned_line = line.replace(";", ",")
        cleaned_lines.append(cleaned_line)

    # Προειδοποίηση αν η πρώτη γραμμή δεν περιέχει "key"
    if "key" not in cleaned_lines[0].lower():
        print("⚠️ Προσοχή: Η πρώτη γραμμή δεν περιέχει 'key'! Μήπως το Excel άλλαξε τα headers;")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print(f"✅ Το αρχείο καθαρίστηκε και αποθηκεύτηκε ως: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = input("Δώσε όνομα εισαγόμενου αρχείου CSV: ")
        output_file = input("Δώσε όνομα για το καθαρό αρχείο CSV: ")
    clean_csv(input_file, output_file)
