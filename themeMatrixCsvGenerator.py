# generate_theme_matrix_csv.py

import csv
import sys
import os


import themeManager


def generate_theme_matrix_csv(output_csv_file="themeMatrix.csv"):
    """
    Δημιουργεί το themeMatrix.csv από τα λεξικά θεμάτων του themeManager.
    Τώρα διαβάζει δυναμικά τα διαθέσιμα θέματα.

    :param output_csv_file: Το όνομα του αρχείου CSV που θα δημιουργηθεί.
    """

    # ---------------------------------------------------------------------------
    # Δυναμική φόρτωση όλων των θεμάτων
    # Χρησιμοποιούμε την themeManager.get_all_theme_names()
    # και τη themeManager.get_theme() για να διαβάσουμε δυναμικά τα θέματα.
    # ---------------------------------------------------------------------------
    all_themes_data = {}
    try:
        # Παίρνουμε όλα τα ονόματα των θεμάτων που είναι διαθέσιμα στο themeManager
        theme_names_from_manager = themeManager.get_all_theme_names()

        # Για κάθε όνομα θέματος, ανακτούμε το αντίστοιχο λεξικό με τα χρώματα
        for theme_name in theme_names_from_manager:
            all_themes_data[theme_name] = themeManager.get_theme(theme_name)
    except Exception as e:
        print(f"❌ Σφάλμα κατά τη δυναμική φόρτωση θεμάτων από το themeManager: {e}")
        print("Παρακαλώ βεβαιωθείτε ότι το themeManager.py είναι προσβάσιμο και σωστό.")
        return # Διακόπτουμε τη λειτουργία αν δεν μπορέσουμε να φορτώσουμε τα θέματα


    # 1. Συλλέγουμε όλα τα μοναδικά χρωματικά keys (π.χ. 'background', 'top_button_bg')
    all_keys = set()
    for theme_name, theme_dict in all_themes_data.items():
        all_keys.update(theme_dict.keys())

    # Τα ταξινομούμε για σταθερή σειρά στο CSV
    sorted_keys = sorted(list(all_keys))

    # 2. Συλλέγουμε τα ονόματα των θεμάτων (τώρα τα έχουμε ήδη από το themeManager.get_all_theme_names())
    # Χρησιμοποιούμε την ίδια ταξινομημένη λίστα για να διασφαλίσουμε συνέπεια
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