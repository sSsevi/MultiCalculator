# manual_handler.py

import customtkinter
import tkinter as tk
from tkhtmlview import HTMLLabel
import os

def show_manual_popup(parent_widget):
    """
    Εμφανίζει το εγχειρίδιο χρήσης σε ένα pop-up παράθυρο.

    Args:
        parent_widget: Το widget γονέα (π.χ., η κλάση Calculator ή ScientificCalculator)
                       χρησιμοποιείται για τη δημιουργία του CTkToplevel παραθύρου.
    """
    # Βρες το απόλυτο μονοπάτι προς το manual.html
    # Αυτό είναι σημαντικό για να λειτουργεί σωστά ανεξάρτητα από πού τρέχει το script.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    manual_file_path = os.path.join(current_dir, "manual.html")

    try:
        with open(manual_file_path, "r", encoding="utf-8") as f:
            manual_html_content = f.read()
    except FileNotFoundError:
        customtkinter.CTkMessagebox.show_error(
            title="Σφάλμα",
            message=f"Το αρχείο 'manual.html' δεν βρέθηκε στο μονοπάτι: {manual_file_path}\nΒεβαιωθείτε ότι βρίσκεται στον ίδιο φάκελο με την εφαρμογή."
        )
        return

    manual_window = customtkinter.CTkToplevel(parent_widget)
    manual_window.title("Εγχειρίδιο Χρήσης")
    manual_window.geometry("700x600")
    manual_window.attributes("-topmost", True)
    manual_window.resizable(True, True)

    # Κεντράρισμα του pop-up παραθύρου στην οθόνη
    screen_width = manual_window.winfo_screenwidth()
    screen_height = manual_window.winfo_screenheight()
    x = (screen_width / 2) - (700 / 2)
    y = (screen_height / 2) - (600 / 2)
    manual_window.geometry(f"700x600+{int(x)}+{int(y)}")

    html_display = HTMLLabel(
        manual_window,
        html=manual_html_content,
        font=("Arial", 12),
    )
    html_display.pack(fill="both", expand=True, padx=10, pady=10)

    manual_window.grab_set()
    parent_widget.wait_window(manual_window)