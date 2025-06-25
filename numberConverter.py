# numberConverter.py

# Αυτό το αρχείο υλοποιεί μια εφαρμογή μετατροπής αριθμών μεταξύ διαφορετικών βάσεων (2, 8, 10, 16).
# Παρέχει γραφικό περιβάλλον χρήστη (GUI) με δυνατότητες όπως:
# - Επιλογή βάσεων εισόδου και εξόδου.
# - Ανταλλαγή βάσεων με το πάτημα ενός κουμπιού.
# - Εμφάνιση επιτρεπτών ψηφίων για κάθε βάση.
# - Μετατροπή ακέραιων και δεκαδικών αριθμών με ακρίβεια.
# - Αντιγραφή αποτελέσματος στο πρόχειρο.
# Χρησιμοποιεί τη βιβλιοθήκη customtkinter για μοντέρνο σχεδιασμό και υποστήριξη themes.


# ==================== ΕΙΣΑΓΩΓΕΣ & ΘΕΜΑ ====================
from fractions import Fraction  # Για ακριβή υπολογισμό δεκαδικών αριθμών
import customtkinter as ctk
import tkinter as tk  # Για βασικές λειτουργίες GUI
from themeManager import get_theme  # Εισαγωγή του σκούρου θέματος από το themeManager


# ==================== ΚΛΑΣΗ NumberBaseConverter ====================
class NumberBaseConverter(ctk.CTkFrame):
    def __init__(self, master, theme=None, sound_enabled=True, **kwargs):
        # Φτιάχνουμε πρώτα το theme
        if theme is not None:
            self.theme = theme
        else:
            self.theme = get_theme("dark")

        # Φτιάχνουμε το frame χωρίς fg_color και ΧΩΡΙΣ sound_enabled
        super().__init__(master, corner_radius=0)

        # Ορίζουμε το χρώμα του frame ΜΕΤΑ
        self.configure(fg_color=self.theme.get("background", "#222222"))

        # Σώζουμε το sound_enabled
        self.sound_enabled = sound_enabled


        # ==================== ΔΙΑΜΟΡΦΩΣΗ GRID ====================
        self.grid_columnconfigure((0, 4), weight=0,
                                  minsize=60)  # Ρύθμιση των στηλών 0 και 4 με βάρος 0 και ελάχιστο μέγεθος 60
        self.grid_columnconfigure((1, 2, 3), weight=1)  # Ρύθμιση των στηλών 1, 2 και 3 με βάρος 1 για επέκταση
        self.grid_rowconfigure(list(range(10)), weight=1)  # Ρύθμιση όλων των γραμμών με βάρος 1 για επέκταση

        # ==================== ΤΙΤΛΟΣ ====================
        self.title_label = ctk.CTkLabel(self, text="NUMBER BASE CONVERTER",  # Ετικέτα τίτλου
                                        font=("Arial", 18, "bold"),  # Γραμματοσειρά και μέγεθος
                                        text_color=self.theme.get("display_text", "#00ff00"))  # Χρώμα κειμένου τίτλου
        self.title_label.grid(row=0, column=0, columnspan=5, padx=20,
                              pady=(20, 40))  # Τοποθέτηση της ετικέτας στη γραμμή 0, στήλες 0-4, με περιθώρια

        # ==================== ΕΠΙΛΟΓΗ ΒΑΣΕΩΝ ====================
        self.from_label = ctk.CTkLabel(self, text="FROM BASE", font=("Arial", 14),  # Ετικέτα για τη βάση εισόδου
                                       text_color=self.theme.get("label_text", "#ffffff"))  # Χρώμα κειμένου ετικέτας
        self.from_label.grid(row=1, column=0, columnspan=2, padx=(20, 5),
                             sticky="e")  # Τοποθέτηση της ετικέτας στη γραμμή 1, στήλες 0-1, με περιθώρια και στοίχιση στα δεξιά

        # Ετικέτα για τη βάση εξόδου
        self.to_label = ctk.CTkLabel(self, text="TO BASE", font=("Arial", 14),
                                     text_color=self.theme.get("label_text", "#ffffff"))  # Χρώμα κειμένου ετικέτας
        self.to_label.grid(row=1, column=3, columnspan=2, padx=(5, 20),
                           sticky="w")  # Τοποθέτηση στη γραμμή 1, στήλες 3-4

        bases = ["2", "8", "10", "16"]  # Λίστα με τις διαθέσιμες βάσεις

        # Μενού επιλογής βάσης εισόδου
        self.from_base_menu = ctk.CTkComboBox(self, values=bases, border_width=2,
                                              command=lambda _: self.update_allowed_digits_label(),
                                              # Ενημέρωση επιτρεπτών ψηφίων όταν αλλάζει η βάση
                                              button_color=self.theme.get("menu_button_bg", "#eb7c16"),  # Χρώμα κουμπιού
                                              dropdown_fg_color=self.theme.get("dropdown_fg", "#4f4f4f"),
                                              # Χρώμα φόντου dropdown
                                              dropdown_text_color=self.theme.get("menu_text_color", "#ffffff"),
                                              # Χρώμα κειμένου dropdown
                                              text_color=self.theme.get("menu_text_color", "#ffffff"),  # Χρώμα κειμένου
                                              border_color=self.theme.get("menu_button_bg",
                                                                     "#eb7c16"))  # Χρώμα περιγράμματος
        self.from_base_menu.set("10")  # Προεπιλεγμένη τιμή: 10
        self.from_base_menu.grid(row=2, column=0, columnspan=2, padx=(30, 5), pady=(0, 2),
                                 sticky="ew")  # Τοποθέτηση στη γραμμή 2, στήλες 0-1

        # Κουμπί για ανταλλαγή βάσεων
        self.swap_button = ctk.CTkButton(self, text="↔", font=("Arial", 16), width=40,
                                         command=self.swap_bases,  # Συνάρτηση ανταλλαγής βάσεων
                                         fg_color=self.theme.get("special_button_fg", "#eb7c16"))  # Χρώμα κουμπιού
        self.swap_button.grid(row=2, column=2, padx=(15, 15), pady=(0, 2),
                              sticky="ew")  # Τοποθέτηση στη γραμμή 2, στήλη 2

        # Μενού επιλογής βάσης εξόδου
        self.to_base_menu = ctk.CTkComboBox(self, values=bases, border_width=2,
                                            button_color=self.theme.get("menu_button_bg", "#eb7c16"),  # Χρώμα κουμπιού
                                            dropdown_fg_color=self.theme.get("dropdown_fg", "#4f4f4f"),
                                            # Χρώμα φόντου dropdown
                                            dropdown_text_color=self.theme.get("menu_text_color", "#ffffff"),
                                            # Χρώμα κειμένου dropdown
                                            text_color=self.theme.get("menu_text_color", "#ffffff"),  # Χρώμα κειμένου
                                            border_color=self.theme.get("menu_button_bg", "#eb7c16"))  # Χρώμα περιγράμματος
        self.to_base_menu.set("2")  # Προεπιλεγμένη τιμή: 2
        self.to_base_menu.grid(row=2, column=3, columnspan=2, padx=(5, 30), pady=(0, 2),
                               sticky="ew")  # Τοποθέτηση στη γραμμή 2, στήλες 3-4

        # ==================== ΕΠΙΤΡΕΠΤΑ ΨΗΦΙΑ ====================
        # Ετικέτα για εμφάνιση επιτρεπτών χαρακτήρων για τη βάση εισόδου
        self.allowed_digits_label = ctk.CTkLabel(self, text="", font=("Arial", 11, "italic"),
                                                 # Γραμματοσειρά και μέγεθος
                                                 text_color=self.theme.get("placeholder_text",
                                                                           "#aaaaaa"))  # Χρώμα κειμένου
        self.allowed_digits_label.grid(row=3, column=1, columnspan=3,
                                       pady=(0, 10))  # Τοποθέτηση στη γραμμή 3, στήλες 1-3
        self.update_allowed_digits_label()  # Αρχική ενημέρωση επιτρεπτών ψηφίων

        # ==================== ΠΕΔΙΟ ΕΙΣΟΔΟΥ ====================
        # Ετικέτα για το πεδίο εισαγωγής αριθμού
        self.input_label = ctk.CTkLabel(self, text="NUMBER", font=("Arial", 16, "bold"),  # Γραμματοσειρά και μέγεθος
                                        text_color=self.theme.get("label_text", "#ffffff"))  # Χρώμα κειμένου
        self.input_label.grid(row=4, column=1, columnspan=3, pady=(10, 2),
                              sticky="s")  # Τοποθέτηση στη γραμμή 4, στήλες 1-3

        self.input_entry = ctk.CTkEntry(
            self,  # Το τρέχον frame ως γονέας
            fg_color=self.theme.get("entry_fg", "#ffffff"),  # Χρώμα φόντου του πεδίου
            text_color=self.theme.get("text_input", "#000000"),  # Χρώμα κειμένου εισόδου
            font=("Arial", 20, "bold"),  # Γραμματοσειρά και μέγεθος
            height=40,  # Ύψος πεδίου
            justify="center",  # Στοίχιση κειμένου στο κέντρο
            placeholder_text="e.g. 12.75",  # Κείμενο υπόδειξης (placeholder)
            placeholder_text_color=self.theme.get("placeholder_text", "#BEBEBE")  # Χρώμα placeholder
        )
        self.input_entry.grid(row=5, column=1, columnspan=3, padx=10, pady=(0, 0),
                              sticky="ew")  # Τοποθέτηση του πεδίου στη γραμμή 5, στήλες 1-3, με περιθώρια
        self.input_entry.bind("<Return>", lambda
            event: self.convert_number())  # Σύνδεση του πλήκτρου Enter ώστε να καλεί τη convert_number

        # ==================== ΜΗΝΥΜΑΤΑ ΒΟΗΘΕΙΑΣ/ΣΦΑΛΜΑΤΩΝ ====================
        # Ετικέτα για εμφάνιση μηνυμάτων βοήθειας ή σφαλμάτων
        # Ετικέτα για εμφάνιση μηνύματος βοήθειας ή σφαλμάτων
        self.tooltip_label = ctk.CTkLabel(
            self,  # Το τρέχον frame ως γονέας
            text="",  # Αρχικά κενό κείμενο
            font=("Arial", 12),  # Γραμματοσειρά και μέγεθος
            text_color=self.theme.get("error_text", "#ff4444")  # Χρώμα κειμένου (κόκκινο για σφάλματα)
        )
        self.tooltip_label.grid(
            row=6, column=0, columnspan=4,  # Τοποθέτηση στη γραμμή 6, στήλες 0-3
            pady=(0, 2)  # Κάθετο περιθώριο (πάνω 0, κάτω 2)
        )

        # ==================== ΚΟΥΜΠΙ ΜΕΤΑΤΡΟΠΗΣ ====================
        # Κουμπί για εκκίνηση της μετατροπής αριθμού
        self.convert_button = ctk.CTkButton(
            self,  # Το τρέχον frame ως γονέας
            text="CONVERT",  # Κείμενο κουμπιού
            font=("Arial", 16, "bold"),  # Γραμματοσειρά και μέγεθος
            height=50,  # Ύψος κουμπιού
            command=self.convert_number,  # Συνάρτηση που καλείται όταν πατηθεί το κουμπί
            fg_color=self.theme.get("special_button_fg", "#eb7c16"),  # Χρώμα φόντου κουμπιού
            text_color=self.theme.get("op_button_text", "#ffffff"),  # Χρώμα κειμένου κουμπιού
            hover_color=self.theme.get("op_hover", "#5e5e5e")  # Χρώμα όταν το ποντίκι είναι πάνω στο κουμπί
        )
        self.convert_button.grid(
            row=7, column=1, columnspan=3,  # Τοποθέτηση στη γραμμή 7, στήλες 1-3
            padx=10, pady=(0, 20),  # Περιθώρια γύρω από το κουμπί
            sticky="ew"  # Επέκταση οριζόντια
        )

        # ==================== ΑΠΟΤΕΛΕΣΜΑ ====================
        # Ετικέτα για το αποτέλεσμα της μετατροπής
        self.result_label = ctk.CTkLabel(
            self,  # Το τρέχον frame ως γονέας
            text="RESULT",  # Κείμενο ετικέτας
            font=("Arial", 14, "bold"),  # Γραμματοσειρά και μέγεθος
            text_color=self.theme.get("label_text", "#ffffff")  # Χρώμα κειμένου ετικέτας
        )
        self.result_label.grid(
            row=8, column=1, columnspan=3,  # Τοποθέτηση στη γραμμή 8, στήλες 1-3
            pady=(20, 2),  # Κάθετα περιθώρια
            sticky="s"  # Στοίχιση στο κάτω μέρος του κελιού
        )

        # Πεδίο εισαγωγής για την εμφάνιση του αποτελέσματος της μετατροπής
        self.result_entry = ctk.CTkEntry(
            self,  # Το τρέχον frame ως γονέας
            font=("Arial", 18, "bold"),  # Γραμματοσειρά και μέγεθος
            height=40,  # Ύψος πεδίου
            text_color=self.theme.get("display_text", "#00ff00"),  # Χρώμα κειμένου αποτελέσματος
            fg_color=self.theme.get("display_bg", "#000000"),  # Χρώμα φόντου πεδίου
            justify="center"  # Στοίχιση κειμένου στο κέντρο
        )
        self.result_entry.grid(
            row=9, column=1, columnspan=3,  # Τοποθέτηση στη γραμμή 9, στήλες 1-3
            padx=10, pady=(2, 0),  # Περιθώρια γύρω από το πεδίο
            sticky="ewn"  # Επέκταση οριζόντια και στο βόρειο άκρο
        )

        # ==================== ΚΟΥΜΠΙ ΑΝΤΙΓΡΑΦΗΣ ====================
        # Κουμπί για αντιγραφή του αποτελέσματος στο πρόχειρο
        self.copy_button = ctk.CTkButton(
            self,  # Το τρέχον frame ως γονέας
            text="📋",  # Εικονίδιο κουμπιού (clipboard)
            width=1,  # Πλάτος κουμπιού
            height=40,  # Ύψος κουμπιού
            font=("Arial", 16),  # Γραμματοσειρά και μέγεθος
            fg_color=self.theme.get("special_button_fg", "#eb7c16"),  # Χρώμα φόντου κουμπιού
            border_width=2,  # Πάχος περιγράμματος
            border_color=self.theme.get("border_color", "#000000"),  # Χρώμα περιγράμματος
            hover_color="#000000",  # Χρώμα όταν το ποντίκι είναι πάνω στο κουμπί
            text_color=self.theme.get("special_button_text", "#ffffff"),  # Χρώμα κειμένου
            command=self.copy_result  # Συνάρτηση που καλείται όταν πατηθεί το κουμπί
        )
        # Τοποθέτηση του κουμπιού αντιγραφής στη γραμμή 9, στήλη 4, με κάθετο περιθώριο (2, 0) και στοίχιση αριστερά-πάνω ("wn")
        self.copy_button.grid(row=9, column=4, pady=(2, 0), sticky="wn")

        # Ετικέτα για εμφάνιση μηνύματος επιτυχίας αντιγραφής (π.χ. "✔ Copied!")
        self.copy_tooltip_label = ctk.CTkLabel(
            self,  # Το τρέχον frame ως γονέας
            text="",  # Αρχικά κενό κείμενο
            font=("Arial", 11, "italic"),  # Γραμματοσειρά και μέγεθος
            text_color="#33ff33"  # Χρώμα κειμένου (πράσινο)
        )
        # Τοποθέτηση της ετικέτας στη γραμμή 10, στήλες 2-3, με κάθετο περιθώριο (0, 60), οριζόντιο περιθώριο 15 και στοίχιση δεξιά-πάνω ("en")
        self.copy_tooltip_label.grid(row=10, column=2, columnspan=2, pady=(0, 60), padx=15, sticky="en")

        # Κλήση της apply_theme για την αρχική εφαρμογή του θέματος
        self.apply_theme(self.theme)

    # ==================== ΕΝΗΜΕΡΩΣΗ ΕΠΙΤΡΕΠΤΩΝ ΨΗΦΙΩΝ ====================
    def update_allowed_digits_label(self):  # Ενημέρωση της ετικέτας με τα επιτρεπτά ψηφία για τη βάση "from"
        base = int(self.from_base_menu.get())  # Παίρνει τη βάση από το μενού επιλογής "from"
        digits = "0123456789ABCDEF"[:base]  # Επιλέγει τα επιτρεπτά ψηφία για τη βάση
        self.allowed_digits_label.configure(  # Ενημερώνει την ετικέτα με τα επιτρεπτά ψηφία
            text=f"Allowed characters: {digits}"
        )

    # ==================== ΑΝΤΑΛΛΑΓΗ ΒΑΣΕΩΝ ====================
    def swap_bases(self):  # Ανταλλαγή βάσεων
        from_base = self.from_base_menu.get()  # Παίρνει την τρέχουσα βάση "from"
        to_base = self.to_base_menu.get()  # Παίρνει την τρέχουσα βάση "to"
        self.from_base_menu.set(to_base)  # Ορίζει τη βάση "from" στη βάση "to"
        self.to_base_menu.set(from_base)  # Ορίζει τη βάση "to" στη βάση "from"
        self.update_allowed_digits_label()  # Ενημερώνει την ετικέτα επιτρεπτών ψηφίων

        value = self.input_entry.get().strip().replace(",",
                                                       ".")  # Παίρνει την τιμή από το πεδίο εισόδου και αντικαθιστά το κόμμα με τελεία
        REVERSE_MAP = "0123456789ABCDEF"  # Χάρτης επιτρεπτών ψηφίων για βάσεις έως 16
        allowed_digits = REVERSE_MAP[:int(to_base)]  # Επιτρεπτά ψηφία για τη βάση εξόδου

        self.tooltip_label.configure(text="")  # Καθαρίζει το μήνυμα βοήθειας/σφάλματος
        self.result_entry.delete(0, tk.END)  # Καθαρίζει το πεδίο αποτελέσματος

        if "." in value:  # Έλεγχος αν υπάρχει δεκαδικό μέρος
            int_part, frac_part = value.split(".")  # Διαχωρισμός σε ακέραιο και δεκαδικό μέρος
        else:
            int_part, frac_part = value, ""  # Αν δεν υπάρχει δεκαδικό μέρος

        full_value = int_part + frac_part  # Συνένωση όλων των ψηφίων για έλεγχο εγκυρότητας

        if not all(char.upper() in allowed_digits for char in
                   full_value):  # Έλεγχος αν όλα τα ψηφία είναι επιτρεπτά για τη βάση εξόδου
            self.tooltip_label.configure(
                text=f"Input '{value}' not valid in base {to_base} → please re-enter.")  # Εμφανίζει μήνυμα σφάλματος
            self.input_entry.configure(border_color="#ff4444")  # Κάνει κόκκινο το περίγραμμα του πεδίου εισόδου
            self.after(2000, lambda: self.input_entry.configure(border_color=self.theme.get("menu_button_bg",
                                                                                            "#eb7c16")))  # Επαναφέρει το περίγραμμα μετά από 2 δευτερόλεπτα
        else:
            self.input_entry.configure(border_color=self.theme.get("menu_button_bg",
                                                                   "#eb7c16"))  # Επαναφέρει το χρώμα περιγράμματος αν η είσοδος είναι έγκυρη

    # ==================== ΜΕΤΑΤΡΟΠΗ ΑΡΙΘΜΟΥ ====================
    def convert_number(self):  # Συνάρτηση μετατροπής αριθμού μεταξύ βάσεων
        value = self.input_entry.get().strip().replace(",",
                                                       ".")  # Παίρνει την τιμή εισόδου και αντικαθιστά το κόμμα με τελεία
        from_base = int(self.from_base_menu.get())  # Παίρνει τη βάση εισόδου από το μενού
        to_base = int(self.to_base_menu.get())  # Παίρνει τη βάση εξόδου από το μενού

        try:
            DIGIT_MAP = {  # Χάρτης για μετατροπή ψηφίων σε ακέραιους
                '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
                '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
                'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15
            }

            REVERSE_MAP = "0123456789ABCDEF"  # Χάρτης για μετατροπή ακέραιων σε ψηφία

            # --- Ανάλυση εισόδου σε ακέραιο και δεκαδικό μέρος ---
            if "." in value:
                int_part, frac_part = value.split(".")  # Διαχωρισμός σε ακέραιο και δεκαδικό μέρος
            else:
                int_part, frac_part = value, ""  # Αν δεν υπάρχει δεκαδικό μέρος

            # --- Έλεγχος επιτρεπτών ψηφίων για τη βάση εισόδου ---
            allowed_digits = REVERSE_MAP[:from_base]  # Επιτρεπτά ψηφία για τη βάση
            full_value = int_part + frac_part  # Όλα τα ψηφία της εισόδου
            if not all(char.upper() in allowed_digits for char in full_value):
                raise ValueError  # Εξαίρεση αν βρεθεί μη επιτρεπτό ψηφίο

            # --- Μετατροπή ακέραιου μέρους σε δεκαδικό ---
            decimal_int = 0
            for i, digit in enumerate(reversed(int_part.upper())):
                decimal_int += DIGIT_MAP[digit] * (from_base ** i)  # Υπολογισμός τιμής κάθε ψηφίου

            # --- Μετατροπή δεκαδικού μέρους σε δεκαδικό (Fraction για ακρίβεια) ---
            decimal_frac = Fraction(0, 1)  # Αρχικοποίηση δεκαδικού μέρους ως Fraction
            for i, digit in enumerate(frac_part.upper(), start=1):  # Ξεκινάμε από 1 για το δεκαδικό μέρος
                decimal_frac += Fraction(DIGIT_MAP[digit], from_base ** i)  # Πρόσθεση κάθε δεκαδικού ψηφίου

            total = Fraction(decimal_int) + decimal_frac  # Συνολική δεκαδική τιμή

            # --- Αν η βάση εξόδου είναι 10, εμφάνιση ως float ---
            if to_base == 10:  # Αν η βάση εξόδου είναι 10
                result = float(total)  # Μετατροπή σε float
                result = f"{result:.15f}".rstrip('0').rstrip('.')  # Μορφοποίηση χωρίς περιττά μηδενικά
            else:
                # --- Μετατροπή ακέραιου μέρους στη νέα βάση ---
                int_val = total.numerator // total.denominator  # Ακέραιο μέρος
                digits = []
                while int_val > 0:
                    digits.append(REVERSE_MAP[int_val % to_base])  # Υπολογισμός ψηφίων στη νέα βάση
                    int_val //= to_base
                int_conv = ''.join(reversed(digits)) if digits else "0"  # Τελικό ακέραιο μέρος στη νέα βάση

                # --- Μετατροπή δεκαδικού μέρους σε επιθυμητή βάση με ανίχνευση περιοδικότητας ---
                frac = total - int(total)  # Υπολογισμός δεκαδικού μέρους
                frac = Fraction(frac)  # Μετατροπή σε Fraction για ακριβή υπολογισμό

                digits = []  # Λίστα για τα ψηφία του δεκαδικού μέρους στη νέα βάση
                seen = {}  # Λεξικό για ανίχνευση περιοδικών κλασμάτων
                periodic_index = None  # Δείκτης έναρξης περιοδικού μέρους (αν υπάρχει)

                numerator = frac.numerator  # Αριθμητής του δεκαδικού μέρους
                denominator = frac.denominator  # Παρονομαστής του δεκαδικού μέρους

                # Επανάληψη για μετατροπή δεκαδικού μέρους (μέχρι 100 ψηφία ή αν βρεθεί περιοδικότητα)
                for i in range(100):  # Μέγιστο 100 ψηφία για αποφυγή ατέρμονων επαναλήψεων
                    if numerator == 0:  # Αν ο αριθμητής γίνει 0, σταματάμε
                        break  # Τέλος αν το δεκαδικό μέρος μηδενιστεί
                    key = (numerator, denominator)  # Δημιουργία κλειδιού για ανίχνευση περιοδικότητας
                    if key in seen:  # Έλεγχος αν το κλειδί έχει ήδη εμφανιστεί
                        periodic_index = seen[key]  # Βρέθηκε περιοδικότητα
                        break
                    seen[key] = i  # Αποθήκευση της θέσης του κλειδιού

                    numerator *= to_base  # Πολλαπλασιασμός του αριθμητή με τη βάση εξόδου
                    digit = numerator // denominator  # Υπολογισμός ψηφίου στη νέα βάση
                    digits.append(REVERSE_MAP[digit])  # Προσθήση ψηφίου στη λίστα
                    numerator %= denominator

                # --- Διαχωρισμός περιοδικού και μη περιοδικού μέρους ---
                if periodic_index is not None:  # Αν βρέθηκε περιοδικό μέρος
                    non_periodic = ''.join(digits[:periodic_index])  # Μη περιοδικό μέρος
                    periodic = ''.join(digits[periodic_index:])  # Περιοδικό μέρος
                    frac_conv = f"{non_periodic}({periodic})"  # Παρουσίαση με παρένθεση
                else:
                    frac_conv = ''.join(digits).rstrip('0')  # Χωρίς περιοδικότητα, αφαίρεση τελικών μηδενικών

                # --- Τελικό αποτέλεσμα ---
                result = f"{int_conv}.{frac_conv}" if frac_conv else int_conv  # Συνένωση ακέραιου και δεκαδικού μέρους

            # --- Ενημέρωση GUI με το αποτέλεσμα ---
            self.result_entry.delete(0, tk.END)  # Καθαρίζει το πεδίο αποτελέσματος
            self.result_entry.insert(0, str(result))  # Εισάγει το αποτέλεσμα στο πεδίο αποτελέσματος
            self.tooltip_label.configure(text="")  # Καθαρίζει το μήνυμα βοήθειας/σφάλματος
            self.input_entry.configure(  # Επαναφέρει το χρώμα περιγράμματος της εισόδου
                border_color=self.theme.get("menu_button_bg", "#eb7c16")
                # Χρήση του ίδιου χρώματος με το button_color των comboboxes
            )

        except:
            last = "0123456789ABCDEF"[from_base - 1]  # Βρίσκει το μέγιστο επιτρεπτό ψηφίο για τη βάση
            self.tooltip_label.configure(  # Ενημερώνει την ετικέτα με μήνυμα σφάλματος
                text=f"Accepted digits: 0-{last}"  # Εμφανίζει μήνυμα με τα αποδεκτά ψηφία
            )
            self.result_entry.delete(0, tk.END)  # Καθαρίζει το πεδίο αποτελέσματος
            self.input_entry.configure(
                border_color="#ff4444")  # Κάνει κόκκινο το περίγραμμα της εισόδου για ένδειξη σφάλματος
            self.after(
                2000,
                lambda: self.input_entry.configure(
                    border_color=self.theme.get("menu_button_bg", "#eb7c16")
                ),
            )  # Επαναφέρει το περίγραμμα μετά από 2 δευτερόλεπτα

    # ==================== ΑΝΤΙΓΡΑΦΗ ΑΠΟΤΕΛΕΣΜΑΤΟΣ ====================
    def copy_result(self):
        result = self.result_entry.get()  # Παίρνει το αποτέλεσμα από το πεδίο αποτελέσματος
        self.clipboard_clear()  # Καθαρίζει το πρόχειρο
        self.clipboard_append(result)  # Αντιγράφει το αποτέλεσμα στο πρόχειρο
        self.update()  # Ενημερώνει το GUI
        self.copy_tooltip_label.configure(text="✔ Copied!")  # Εμφανίζει μήνυμα επιτυχίας αντιγραφής
        self.after(
            1500,
            lambda: self.copy_tooltip_label.configure(text="")
        )  # Κρύβει το μήνυμα μετά από 1.5 δευτερόλεπτο

    # =========================================================================
    # Η ΕΦΑΡΜΟΓΗ ΘΕΜΑΤΟΣ ΜΕ ΒΑΣΗ ΤΟ SCIENTIFIC_CALC.PY ΠΡΟΤΥΠΟ
    # =========================================================================
    def apply_theme(self, theme_dict):
        """
        Εφαρμόζει το θέμα στα widgets του NumberBaseConverter,
        ακολουθώντας τη δομή του scientificCalc.py.
        """
        self.theme = theme_dict  # Ενημέρωση του θέματος της κλάσης

        # Εφαρμογή χρωμάτων στο κύριο frame
        self.configure(fg_color=theme_dict.get("background", "#222222"))

        # Ετικέτες
        if self.title_label:
            self.title_label.configure(text_color=theme_dict.get("display_text", "#00ff00"))
        if self.from_label:
            self.from_label.configure(text_color=theme_dict.get("label_text", "#ffffff"))
        if self.to_label:
            self.to_label.configure(text_color=theme_dict.get("label_text", "#ffffff"))
        if self.allowed_digits_label:
            self.allowed_digits_label.configure(text_color=theme_dict.get("placeholder_text", "#aaaaaa"))
        if self.input_label:
            self.input_label.configure(text_color=theme_dict.get("label_text", "#ffffff"))
        if self.tooltip_label:
            self.tooltip_label.configure(text_color=theme_dict.get("error_text", "#ff4444"))
        if self.result_label:
            self.result_label.configure(text_color=theme_dict.get("label_text", "#ffffff"))
        if self.copy_tooltip_label:
            # Το copy_tooltip_label έχει ένα σταθερό πράσινο χρώμα, οπότε δεν το αλλάζουμε δυναμικά από το θέμα
            pass

            # Comboboxes
        combobox_bg_color = theme_dict.get("menu_button_bg", "#eb7c16")
        combobox_dropdown_fg_color = theme_dict.get("dropdown_fg", "#4f4f4f")
        combobox_text_color = theme_dict.get("menu_text_color", "#ffffff")
        combobox_border_color = theme_dict.get("menu_button_bg", "#eb7c16")

        if self.from_base_menu:
            self.from_base_menu.configure(
                button_color=combobox_bg_color,
                dropdown_fg_color=combobox_dropdown_fg_color,
                dropdown_text_color=combobox_text_color,
                text_color=combobox_text_color,
                border_color=combobox_border_color
            )
        if self.to_base_menu:
            self.to_base_menu.configure(
                button_color=combobox_bg_color,
                dropdown_fg_color=combobox_dropdown_fg_color,
                dropdown_text_color=combobox_text_color,
                text_color=combobox_text_color,
                border_color=combobox_border_color
            )

        # Swap Button
        if self.swap_button:
            self.swap_button.configure(
                fg_color=theme_dict.get("special_button_fg", "#eb7c16")
                # Το swap button δεν έχει text_color ή hover_color στην αρχική του δήλωση,
                # οπότε δεν τα ρυθμίζουμε εδώ για να μην υπερισχύσουμε πιθανές default συμπεριφορές του CTkButton.
                # Αν χρειαστούν, θα πρέπει να προστεθούν στα θέματα και εδώ.
            )

        # Entry fields
        input_entry_fg_color = theme_dict.get("entry_fg", "#ffffff")
        input_entry_text_color = theme_dict.get("text_input", "#000000")
        input_entry_placeholder_color = theme_dict.get("placeholder_text", "#BEBEBE")

        if self.input_entry:
            self.input_entry.configure(
                fg_color=input_entry_fg_color,
                text_color=input_entry_text_color,
                placeholder_text_color=input_entry_placeholder_color
            )

        result_entry_fg_color = theme_dict.get("display_bg", "#000000")
        result_entry_text_color = theme_dict.get("display_text", "#00ff00")

        if self.result_entry:
            self.result_entry.configure(
                fg_color=result_entry_fg_color,
                text_color=result_entry_text_color
            )
            # Επίσης, το border_color του input_entry και result_entry στην convert_number
            # χρησιμοποιεί το menu_button_bg, οπότε ενημερώνουμε και εκεί το default χρώμα.
            self.input_entry.configure(border_color=theme_dict.get("menu_button_bg", "#eb7c16"))

        # Convert button
        convert_button_fg_color = theme_dict.get("special_button_fg", "#eb7c16")
        convert_button_text_color = theme_dict.get("op_button_text", "#ffffff")
        convert_button_hover_color = theme_dict.get("op_hover", "#5e5e5e")

        if self.convert_button:
            self.convert_button.configure(
                fg_color=convert_button_fg_color,
                text_color=convert_button_text_color,
                hover_color=convert_button_hover_color
            )

        # Copy button
        copy_button_fg_color = theme_dict.get("special_button_fg", "#eb7c16")
        copy_button_border_color = theme_dict.get("border_color", "#000000")  # Χρησιμοποιεί "border_color"
        copy_button_hover_color = theme_dict.get("hover_default",
                                                 "#6e6e6e")  # Το αρχικό ήταν "#000000", αλλά "hover_default" είναι πιο λογικό
        copy_button_text_color = theme_dict.get("special_button_text", "#ffffff")

        if self.copy_button:
            self.copy_button.configure(
                fg_color=copy_button_fg_color,
                border_color=copy_button_border_color,
                hover_color=copy_button_hover_color,
                text_color=copy_button_text_color
            )


# ==================== ΕΚΚΙΝΗΣΗ ΕΦΑΡΜΟΓΗΣ ====================
if __name__ == "__main__":
    import customtkinter as ctk

    app = ctk.CTk()
    app.geometry("400x600")
    app.title("Number Converter")

    frame = NumberBaseConverter(app, theme=get_theme("dark"))
    frame.pack(expand=True, fill="both")

    app.mainloop()