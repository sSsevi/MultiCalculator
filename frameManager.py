# frameManager.py
# ==========================================================
# Αυτό το αρχείο διαχειρίζεται τα διαφορετικά frames (λειτουργίες) της αριθμομηχανής.
# Περιλαμβάνει:
# - Εισαγωγή των κλάσεων που αντιπροσωπεύουν κάθε λειτουργία (Standard, Scientific, Currency Converter, Number Converter).
# - Ορισμό ενός λεξικού `frame_data` που περιέχει πληροφορίες για κάθε λειτουργία:
#   - Το frame που αντιστοιχεί στη λειτουργία.
#   - Τη διαδρομή του εικονιδίου που χρησιμοποιείται για την εμφάνιση της λειτουργίας στο GUI.
# ==========================================================

#==================== ΕΙΣΑΓΩΓΗ ΚΛΑΣΕΩΝ ====================
from standardCalc import StandardCalculator      # Εισαγωγή της κλάσης για την Standard λειτουργία
from scientificCalc import ScientificCalculator  # Εισαγωγή της κλάσης για την Scientific λειτουργία
from currencyConverter import CurrencyConverter  # Εισαγωγή της κλάσης για τη λειτουργία μετατροπής νομισμάτων
from numberConverter import NumberBaseConverter  # Εισαγωγή της κλάσης για τη λειτουργία μετατροπής αριθμών

#==================== ΛΕΞΙΚΟ frame_data ====================
frame_data = {                                # Ορισμός του λεξικού που περιέχει πληροφορίες για κάθε λειτουργία
    "standard": {                             # Ενότητα για την Standard λειτουργία
        "frame":     StandardCalculator,      # Κλάση που αντιπροσωπεύει το frame της Standard λειτουργίας
        "icon_path": "images/standard.png",   # Διαδρομή του εικονιδίου για την Standard λειτουργία
    },

    "scientific": {                           # Ενότητα για την Scientific λειτουργία
        "frame":     ScientificCalculator,    # Κλάση που αντιπροσωπεύει το frame της Scientific λειτουργίας
        "icon_path": "images/scientific.png", # Διαδρομή του εικονιδίου για την Scientific λειτουργία
    },

    "Currency Converter": {                   # Ενότητα για τη λειτουργία μετατροπής νομισμάτων
        "frame":     CurrencyConverter,       # Κλάση που αντιπροσωπεύει το frame της λειτουργίας μετατροπής νομισμάτων
        "icon_path": "images/converter.png",  # Διαδρομή του εικονιδίου για τη λειτουργία μετατροπής νομισμάτων
    },

    "Number Converter": {                     # Ενότητα για τη λειτουργία μετατροπής αριθμών
        "frame":     NumberBaseConverter,     # Κλάση που αντιπροσωπεύει το frame της λειτουργίας μετατροπής αριθμών
        "icon_path": "images/converter.png",  # Διαδρομή του εικονιδίου για τη λειτουργία μετατροπής αριθμών
    },
}
