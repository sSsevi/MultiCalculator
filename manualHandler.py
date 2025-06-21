# manualHandler.py

import customtkinter                        # Εισάγει το customtkinter για custom widgets
import tkinter as tk                        # Εισάγει το κλασικό tkinter για GUI
from tkhtmlview import HTMLLabel            # Εισάγει το HTMLLabel για εμφάνιση HTML περιεχομένου
import os                                   # Εισάγει το os για λειτουργίες συστήματος αρχείων

"""
Αυτή η συνάρτηση είναι υπεύθυνη για την εμφάνιση του εγχειριδίου χρήσης σε ένα αναδυόμενο παράθυρο.
Παίρνει ως όρισμα το γονικό widget, το οποίο χρησιμοποιείται για τη δημιουργία του νέου παραθύρου.
"""
def show_manual_popup(parent_widget):       # Ορίζει τη συνάρτηση που εμφανίζει το εγχειρίδιο χρήσης
    """
    Εμφανίζει το εγχειρίδιο χρήσης σε ένα pop-up παράθυρο.

    Args:
        parent_widget: Το widget γονέα (π.χ., η κλάση Calculator ή ScientificCalculator)
                       χρησιμοποιείται για τη δημιουργία του CTkToplevel παραθύρου.
    """

    """
    Βρίσκει το απόλυτο μονοπάτι προς το αρχείο 'manual.html'.
    Είναι κρίσιμο για να διασφαλιστεί ότι το αρχείο βρίσκεται σωστά, ανεξάρτητα από
    το πού εκτελείται το script.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))      # Παίρνει τον φάκελο όπου βρίσκεται το τρέχον αρχείο
    manual_file_path = os.path.join(current_dir, "manual.html")   # Δημιουργεί το πλήρες μονοπάτι για το manual.html


    """
    Γίνεται προσπάθεια **ανοίγματος και ανάγνωσης του περιεχομένου HTML** του 'manual.html'.
    Σε περίπτωση που το αρχείο δεν βρεθεί, εμφανίζεται ένα μήνυμα σφάλματος στον χρήστη
    μέσω του `customtkinter.CTkMessagebox` και τερματίζεται η λειτουργία της συνάρτησης.
    """
    try:
        with open(manual_file_path, "r", encoding="utf-8") as f:  # Προσπαθεί να ανοίξει το manual.html για ανάγνωση
            manual_html_content = f.read()                        # Διαβάζει το περιεχόμενο του αρχείου
    except FileNotFoundError:                                     # Αν δεν βρεθεί το αρχείο manual.html
        customtkinter.CTkMessagebox.show_error(                   # Εμφανίζει μήνυμα σφάλματος με customtkinter
            title="Σφάλμα",
            message=f"Το αρχείο 'manual.html' δεν βρέθηκε στο μονοπάτι: {manual_file_path}\nΒεβαιωθείτε ότι βρίσκεται στον ίδιο φάκελο με την εφαρμογή."
        )
        return                                                   # Τερματίζει τη συνάρτηση αν δεν βρεθεί το αρχείο

    """
    Δημιουργείται ένα νέο αναδυόμενο παράθυρο (`CTkToplevel`)
    και ρυθμίζονται οι βασικές του ιδιότητες. Ορίζεται ο τίτλος, οι αρχικές διαστάσεις
    (700x600) και η δυνατότητα αλλαγής μεγέθους (`resizable`). Επιπλέον, χρησιμοποιείται το `-topmost`
    ώστε το παράθυρο του εγχειριδίου να παραμένει πάντα πάνω από τα άλλα.
    """
    manual_window = customtkinter.CTkToplevel(parent_widget)      # Δημιουργεί νέο παράθυρο (pop-up) πάνω από το parent_widget
    manual_window.title("Εγχειρίδιο Χρήσης")                      # Ορίζει τον τίτλο του παραθύρου
    manual_window.geometry("700x600")                             # Ορίζει το μέγεθος του παραθύρου
    manual_window.attributes("-topmost", True)                    # Ορίζει το παράθυρο να είναι πάντα μπροστά
    manual_window.resizable(True, True)                           # Επιτρέπει την αλλαγή μεγέθους του παραθύρου

    # Κεντράρισμα του pop-up παραθύρου στην οθόνη
    """
    Για βελτιωμένη εμπειρία χρήστη, **κεντράρεται το αναδυόμενο παράθυρο στην οθόνη**.
    Υπολογίζονται οι κατάλληλες συντεταγμένες x και y βάσει των διαστάσεων της οθόνης
    και του μεγέθους του παραθύρου.
    """
    screen_width = manual_window.winfo_screenwidth()              # Παίρνει το πλάτος της οθόνης
    screen_height = manual_window.winfo_screenheight()            # Παίρνει το ύψος της οθόνης
    x = (screen_width / 2) - (700 / 2)                            # Υπολογίζει τη θέση x για κεντράρισμα
    y = (screen_height / 2) - (600 / 2)                           # Υπολογίζει τη θέση y για κεντράρισμα
    manual_window.geometry(f"700x600+{int(x)}+{int(y)}")          # Ορίζει τη θέση του παραθύρου στο κέντρο της οθόνης

    """
    Δημιουργείται ένα `HTMLLabel` widget, σχεδιασμένο ειδικά
    για την εμφάνιση περιεχομένου HTML. Το προηγουμένως αναγνωσμένο περιεχόμενο από το 'manual.html'
    περνιέται σε αυτό το label. Στη συνέχεια, το `HTMLLabel` τοποθετείται μέσα
    στο αναδυόμενο παράθυρο, καλύπτοντας τον διαθέσιμο χώρο με μικρό περιθώριο.
    """
    html_display = HTMLLabel(                                     # Δημιουργεί ένα HTMLLabel για εμφάνιση του manual
        manual_window,
        html=manual_html_content,
        font=("Arial", 12),
    )
    html_display.pack(fill="both", expand=True, padx=10, pady=10) # Τοποθετεί το HTMLLabel στο παράθυρο με περιθώρια

    """
    Τέλος, το αναδυόμενο παράθυρο γίνεται "modal". Αυτό σημαίνει ότι ο χρήστης
    δεν μπορεί να αλληλεπιδράσει με κανένα άλλο παράθυρο της εφαρμογής
    μέχρι να κλείσει αυτό το παράθυρο του εγχειριδίου. Η γραμμή `parent_widget.wait_window`
    αναστέλλει την εκτέλεση του γονικού widget μέχρι το κλείσιμο του.
    """
    manual_window.grab_set()                                      # Κάνει το παράθυρο modal (μπλοκάρει άλλα παράθυρα μέχρι να κλείσει)
    parent_widget.wait_window(manual_window)                      # Περιμένει μέχρι να κλείσει το manual_window πριν συνεχίσει