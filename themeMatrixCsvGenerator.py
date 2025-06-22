# generate_theme_matrix_csv.py

import csv
import sys
import os

# Προσθέστε το φάκελο που περιέχει το themeManager.py στο PYTHONPATH
# Αν το generate_theme_matrix_csv.py βρίσκεται στον ίδιο φάκελο με το themeManager.py,
# τότε η παρακάτω γραμμή δεν είναι απαραίτητη.
# Αν βρίσκεται σε υποφάκελο, ίσως χρειαστεί να προσαρμόσετε τη διαδρομή.
# Παράδειγμα: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import themeManager


def generate_theme_matrix_csv(output_csv_file="themeMatrix.csv"):
    """
    Δημιουργεί το themeMatrix.csv από τα λεξικά θεμάτων του themeManager.

    :param output_csv_file: Το όνομα του αρχείου CSV που θα δημιουργηθεί.
    """

    # Συγκεντρώνουμε όλα τα θέματα από το themeManager.get_theme()
    # Χρησιμοποιούμε ένα dummy mode για να αποκτήσουμε πρόσβαση στο λεξικό 'themes'
    # χωρίς να χρειάζεται να καλέσουμε την get_theme για κάθε θέμα ξεχωριστά.
    # Θα προσπελάσουμε απευθείας τα global λεξικά.

    # Αυτό είναι το κεντρικό λεξικό που περιέχει όλα τα θέματα
    all_themes_data = {
        "dark": themeManager.DARK_THEME,
        "light": themeManager.LIGHT_THEME,
        "purple": themeManager.PURPLE_THEME,
        "oceanic": themeManager.OCEANIC_THEME,
        "goth": themeManager.GOTH_THEME,
        "mondrian": themeManager.MONDRIAN_THEME,
        "rainbow": themeManager.RAINBOW_THEME,
        "windows95": themeManager.WIN95_ERROR_THEME,
        "excel2003": themeManager.EXCEL_2003_THEME,
    }

    # 1. Συλλέγουμε όλα τα μοναδικά χρωματικά keys (π.χ. 'background', 'top_button_bg')
    all_keys = set()
    for theme_name, theme_dict in all_themes_data.items():
        all_keys.update(theme_dict.keys())

    # Τα ταξινομούμε για σταθερή σειρά στο CSV
    sorted_keys = sorted(list(all_keys))

    # 2. Συλλέγουμε τα ονόματα των θεμάτων (π.χ. 'dark', 'light')
    theme_names = sorted(list(all_themes_data.keys()))

    # 3. Ορίζουμε τις κεφαλίδες του CSV
    fieldnames = ['key'] + theme_names

    # 4. Δημιουργούμε τη matrix δεδομένων για το CSV
    matrix_data = []
    for key in sorted_keys:
        row_data = {'key': key}
        for theme_name in theme_names:
            # Παίρνουμε την τιμή του χρώματος για το συγκεκριμένο key και θέμα
            # Αν ένα key δεν υπάρχει σε ένα θέμα, το ορίζουμε ως κενό string ή κάποια προεπιλογή
            row_data[theme_name] = all_themes_data[theme_name].get(key, "")
        matrix_data.append(row_data)

    # 5. Γράφουμε τα δεδομένα στο αρχείο CSV
    try:
        with open(output_csv_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matrix_data)
        print(f"✅ Το αρχείο '{output_csv_file}' δημιουργήθηκε/ενημερώθηκε επιτυχώς!")
    except IOError as e:
        print(f"❌ Σφάλμα κατά την εγγραφή στο αρχείο CSV: {e}")


if __name__ == "__main__":
    # Καλέστε τη συνάρτηση για να δημιουργήσετε το themeMatrix.csv
    generate_theme_matrix_csv("themeMatrix.csv")