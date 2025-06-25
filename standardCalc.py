# standardCalc.py
# ----------------------------------------------------------
# Αυτό το αρχείο υλοποιεί έναν τυπικό υπολογιστή (standard calculator)
# με χρήση της βιβλιοθήκης customtkinter. Ο υπολογιστής υποστηρίζει
# αριθμητικές πράξεις, θεματική εμφάνιση, υποστήριξη ήχου και πρόσβαση
# σε online manual.

# Εισαγωγές απαραίτητων βιβλιοθηκών
import customtkinter  # Η customtkinter είναι επέκταση του tkinter με πιο σύγχρονο UI (Widgets με themes, dark mode κλπ)

from themeManager import get_theme  # Εισάγουμε τη συνάρτηση που επιστρέφει ένα dictionary με τα χρώματα του theme
from buttonHandler import on_button_click  # Η βασική συνάρτηση που εκτελεί τις πράξεις όταν πατάμε κουμπιά
from manualHandler import show_manual_popup
from historyWindow import HistoryWindowModule
from mpmath import mpf  # mpf είναι τύπος αριθμού αυξημένης ακρίβειας (π.χ. 0.1+0.2 ≠ 0.3 στην float)
import pygame   # Για ήχο (π.χ. κουμπί πατήθηκε, σφάλμα κλπ)

pygame.mixer.init()
# Κλάση StandardCalculator: υλοποιεί τον κορμό του αριθμομηχανής
# ---------------------------------------------------------------
# Κάθε Calculator είναι Frame, δηλαδή GUI container. Τα attributes του αντικειμένου
# αφορούν το θέμα (θέμα = λεξικό με χρώματα), το display, τον ήχο, τη λογική κουμπιών.

class StandardCalculator(customtkinter.CTkFrame):   # Κληρονομούμε από CTkFrame για να έχουμε ένα frame με customtkinter widgets
    def __init__(self, parent, theme=None, sound_enabled=True):    # Αρχικοποίηση του Frame με γονέα (parent) και προαιρετικά θέμα και ήχο
        super().__init__(parent)  # Αρχικοποιούμε το Frame

        # Ορισμός των βασικών attributes του αντικειμένου:
        # Αν περαστεί θέμα, το χρησιμοποιούμε. Αλλιώς, παίρνουμε το "dark" θέμα ως προεπιλογή για τα χρώματα.
        if theme is not None:
            self.theme = theme
        else:
            self.theme = get_theme("dark")
        # Το theme εδώ είναι ένα dictionary (λεξικό) με ονόματα και χρώματα (π.χ. "background": "#222222")

        self.display_var = customtkinter.StringVar(value="0")  # Το κείμενο που εμφανίζεται στο display
        self.just_evaluated = False  # Flag για να ξέρουμε αν μόλις πατήθηκε "=" ώστε να μη συνεχίσουμε αμέσως με ψηφία
        self.sound_enabled = sound_enabled  # Αν είναι ενεργός ο ήχος (true ή false)

        self.top_buttons_frame = None
        self.display_container = None
        self.top_display = None
        self.manual_button = None
        self.history_button = None
        self.history_display_var = customtkinter.StringVar(value="")
        self.history_display = None
        self.middle_display = None
        self.display_entry = None
        self.angle_mode_label = None
        self.history_log = []
        self.memory = mpf("0")
        self.is_degree = True               # Placeholder για κοινή συμβατότητα με scientific — δεν χρησιμοποιείται εδώ
        self.is_second_function = False     # Placeholder για κοινή συμβατότητα με scientific — δεν χρησιμοποιείται εδώ
        self.bottom_buttons_frame = None


        self.history_handler = HistoryWindowModule(
            self,
            self.theme,
            self.history_log,
            self.insert_history_expression
        )

        # Ομάδες κουμπιών για εύκολη πρόσβαση κατά το theme update
        self.operation_buttons = []     # Κουμπιά για τις βασικές αριθμητικές πράξεις (+, -, x, ÷)
        self.symbol_buttons = []        # Κουμπιά για συμβολικές λειτουργίες (1/x, x², √, % κλπ)
        self.numeric_buttons = []       # Κουμπιά για αριθμούς (0-9) και το δεκαδικό σημείο
        self.ac_buttons = []            # Κουμπιά για λειτουργίες καθαρισμού (C, AC)
        self.memory_buttons = []        # Κουμπιά για τη memory
        self.build_ui()  # Καλούμε τη μέθοδο για να φτιαχτεί το UI



    def build_ui(self):
        """
        Κατασκευάζει το γραφικό περιβάλλον χρήστη (UI) της αριθμομηχανής.
        Δημιουργεί και τοποθετεί όλα τα βασικά widgets και frames της εφαρμογής, συμπεριλαμβανομένων:
        - Το πάνω frame με τα κουμπιά για το manual και το ιστορικό.
        - Τα πεδία εμφάνισης για το ιστορικό, πληροφορίες και το κύριο αποτέλεσμα.
        - Το label για την ένδειξη γωνιακής λειτουργίας (Deg/Rad).
        - Το κάτω frame με τα αριθμητικά, λειτουργικά, συμβολικά και μνημονικά κουμπιά, τα οποία δημιουργούνται δυναμικά.
        - Εφαρμόζει τα κατάλληλα χρώματα και στυλ σε κάθε κατηγορία κουμπιών σύμφωνα με το θέμα (theme).
        - Ρυθμίζει τις μεταβλητές κατάστασης (ιστορικό, μνήμη, λειτουργία γωνίας, κ.λπ.).
        - Καλεί τη μέθοδο apply_theme για να εφαρμόσει το θέμα σε όλα τα widgets.
        Τα σχόλια εντός της μεθόδου εξηγούν αναλυτικά κάθε βήμα και το ρόλο κάθε στοιχείου του UI.
        """
        # Ορίζουμε το χρώμα φόντου του κυρίως frame.
        self.configure(fg_color=self.theme.get("background", "#222222"))
        self.top_buttons_frame = customtkinter.CTkFrame(self, corner_radius=0)  # Το top frame είναι το πάνω μέρος της αριθμομηχανής
        self.top_buttons_frame.pack(fill="x")   # Το top frame γεμίζει το πλάτος του parent frame

        # Container για τα πεδία εμφάνισης, με χρώμα φόντου από το θέμα
        self.display_container = customtkinter.CTkFrame(self.top_buttons_frame, fg_color=self.theme.get("display_bg", "#000000"), corner_radius=0)
        self.display_container.pack(fill="x", padx=0, pady=(0, 0))  # Το display_container είναι το container για τα πεδία εμφάνισης

        # Top display – περιέχει το κουμπί που ανοίγει το manual (το ✍️)
        self.top_display = customtkinter.CTkFrame(self.display_container, height=30, fg_color=self.theme.get("display_bg", "#000000"), corner_radius=0)
        self.top_display.pack(fill="x") # Το top_display είναι το πάνω μέρος του display container

        self.manual_button = customtkinter.CTkButton(   # Το κουμπί για το manual
            self.top_display,   # Το parent του κουμπιού είναι το top_display
            text="✍️",  # Το κείμενο του κουμπιού είναι το emoji για manual
            width=30,   # Το πλάτος του κουμπιού
            height=30,  # Το ύψος του κουμπιού
            font=("Arial", 18), # Η γραμματοσειρά του κειμένου του κουμπιού
            fg_color=self.theme.get("manual_button_bg", "#000000"),    # Χρώμα φόντου, με fallback στο dark theme
            text_color=self.theme.get("manual_button_text", "#eb7c16"),    # Χρώμα κειμένου, με fallback στο dark theme
            hover_color=self.theme.get("hover_manual_button", "#000000"),  # Χρώμα hover, με fallback στο dark theme
            command=lambda: show_manual_popup(self) # Η εντομή που εκτελείται όταν πατηθεί το κουμπί (άνοιγμα manual)
        )
        self.manual_button.pack(side="left", padx=15)   # Το κουμπί τοποθετείται αριστερά στο top_display

        self.history_button = customtkinter.CTkButton(  # Το κουμπί για το ιστορικό
            self.top_display,   # Το parent του κουμπιού είναι το top_display
            text="🕘",          # Το κείμενο του κουμπιού είναι το emoji για ιστορικό
            width=30,
            height=30,          # Το ύψος του κουμπιού
            corner_radius=0,    # Το corner_radius του κουμπιού (γωνίες)
            font=("Arial", 18), # Η γραμματοσειρά του κειμένου του κουμπιού
            fg_color=self.theme.get("manual_button_bg", "#000000"),        # Χρώμα φόντου, με fallback στο dark theme
            text_color=self.theme.get("manual_button_text", "#eb7c16"),    # Χρώμα κειμένου, με fallback στο dark theme
            hover_color=self.theme.get("hover_manual_button", "#000000"),  # Χρώμα hover, με fallback στο dark theme
            command=self.history_handler.open    # Η εντομή που εκτελείται όταν πατηθεί το κουμπί (άνοιγμα ιστορικού)
        )
        self.history_button.pack(side="right", padx=15) # Το κουμπί τοποθετείται δεξιά στο top_display

        # Label για το ιστορικό των πράξεων, με χρώματα από το θέμα και fallback
        # self.history_display_var = customtkinter.StringVar(value="")    # Αρχικοποίηση του StringVar για το ιστορικό
        self.history_display = customtkinter.CTkLabel(                  # Το label που θα δείχνει το ιστορικό
            self.display_container,textvariable=self.history_display_var,   # Το textvariable είναι το StringVar που περιέχει το ιστορικό
            height=20,          # Το ύψος του label
            corner_radius=0,    # Το corner_radius του label (γωνίες)
            font=("Arial", 12), # Η γραμματοσειρά του κειμένου του label
            anchor="e",         # Ευθυγράμμιση στα δεξιά
            fg_color=self.theme.get("display_bg", "#000000"),      # Χρώμα φόντου, με fallback στο dark theme
            text_color=self.theme.get("display_text", "#00ff00")   # Χρώμα κειμένου, με fallback στο dark theme
        )
        self.history_display.pack(fill="x", padx=20) # Το label γεμίζει το πλάτος του container

        # Μεσαίο label για πληροφορίες ή ιστορικό, με χρώματα από το θέμα και fallback
        self.middle_display = customtkinter.CTkLabel(   # Το μεσαίο label για πληροφορίες ή ιστορικό
            self.display_container,     # Το parent του μεσαίου label είναι το display_container
            text="",    # Αρχικά κενό, θα ενημερώνεται με πληροφορίες ή ιστορικό
            height=24,  # Το ύψος του μεσαίου label
            corner_radius=0,    # Το corner_radius του μεσαίου label (γωνίες)
            font=("Arial", 14), # Η γραμματοσειρά του κειμένου του label
            anchor="e", # Ευθυγράμμιση στα δεξιά
            wraplength=300, # Το wraplength για το μεσαίο label (μέγιστο πλάτος πριν την αλλαγή γραμμής)
            fg_color=self.theme.get("display_bg", "#000000"),  # Χρώμα φόντου, με fallback στο dark theme
            text_color=self.theme.get("display_text", "#00ff00")   # Χρώμα κειμένου, με fallback στο dark theme
        )
        self.middle_display.pack(fill="x", padx=15) # Το μεσαίο label γεμίζει το πλάτος του container

        # Κύριο πεδίο για εμφάνιση αριθμών / αποτελεσμάτων, με χρώματα από το θέμα και fallback
        self.display_entry = customtkinter.CTkEntry(    # Το κύριο πεδίο για εμφάνιση αριθμών και αποτελεσμάτων
            self.display_container,         # Το parent του display entry είναι το display_container
            textvariable=self.display_var,  # Το textvariable είναι το StringVar που περιέχει την τιμή του display
            font=("Arial", 24),
            justify="right",
            state="readonly",
            height=60,
            corner_radius=0,
            border_width=0,
            fg_color=self.theme.get("display_bg", "#000000"),      # Χρώμα φόντου, με fallback στο dark theme
            text_color=self.theme.get("display_text", "#00ff00")   # Χρώμα κειμένου, με fallback στο dark theme
        )
        self.display_entry.pack(fill="x", padx=15, pady=(0, 0))

        # Ένδειξη Deg ή Rad – το βάζουμε έτσι και αλλιώς (στο Standard απλά μένει κενό)
        # Δημιουργία label για την ένδειξη γωνιακής λειτουργίας (Deg/Rad)
        self.angle_mode_label = customtkinter.CTkLabel(   # Label για Deg/Rad (στο standard μένει κενό)
            self.display_container,                       # Parent είναι το display_container
            text="",                                     # Αρχικά κενό (στο standard calculator δεν εμφανίζεται κάτι)
            font=("Arial", 10),                          # Γραμματοσειρά και μέγεθος
            width=30,                                    # Πλάτος label
            height=16,                                   # Ύψος label
            fg_color=self.theme.get("display_bg", "#000000"),            # Χρώμα φόντου, με fallback στο dark theme
            text_color=self.theme.get("display_text", "#00ff00")         # Χρώμα κειμένου, με fallback στο dark theme
        )
        self.angle_mode_label.pack(anchor="sw", padx=10, pady=(0, 4))  # Τοποθέτηση κάτω αριστερά με padding



        # Ορισμός κουμπιών σε πίνακα – layout 7 γραμμών με 4 κουμπιά η κάθε μία
        button_rows = [
            ["mc", "m+", "m-", "mr"],   # Λίστα με κουμπιά πρώτης γραμμής για μνήμη
            ["1/x", "%", "C", "AC"],    # Λίστα με κουμπιά δεύτερης γραμκής για καθαρισμό και συμβολικές λειτουργίες
            ["x²", "√", "+/-", "÷"],    # Λίστα με κουμπιά τρίτης γραμκής για αριθμητικές πράξεις
            ["7", "8", "9", "x"],       # Λίστα με κουμπιά τέταρτης γραμκής για αριθμούς και πολλαπλασιασμό
            ["4", "5", "6", "-"],       # Λίστα με κουμπιά πέμπτης γραμκής για αριθμούς και αφαίρεση
            ["1", "2", "3", "+"],       # Λίστα με κουμπιά έκτης γραμκής για αριθμούς και πρόσθεση
            ["0", ".", "="]             # Λίστα κουμπιών στην έβδομη γραμμή για αριθμούς και ισότητα
        ]

        # Frame που περιέχει όλα τα κουμπιά, με χρώμα φόντου από το θέμα
        self.bottom_buttons_frame = customtkinter.CTkFrame(self, fg_color=self.theme.get("bottom_frame_bg", "#222222"))
        self.bottom_buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)  # Το bottom frame γεμίζει το χώρο και έχει padding

        # Δημιουργία κουμπιών δυναμικά με βάση τα labels
        for r, row in enumerate(button_rows):   # Για κάθε γραμμή κουμπιών
            for c, label in enumerate(row):     # Για κάθε κουμπί στη γραμμή
                if label == "":     # Αν το label είναι κενό, δεν δημιουργούμε κουμπί
                    continue

                # Ελέγχουμε τον τύπο του κουμπιού
                col_span = 2 if label == "=" else 1             # Αν το label είναι "=", το κουμπί καταλαμβάνει 2 στήλες
                is_memory = label in ["mc", "m+", "m-", "mr"]   # Αν το label είναι για μνήμη
                is_operator = label in ["+", "-", "x", "÷"]     # Αν το label είναι αριθμητική πράξη
                is_symbol = label in ["1/x", "%", "+/-", "x²", "√"]     # Αν το label είναι σύμβολο
                is_ac = label in ["AC", "C", "="]               # Αν το label είναι για καθαρισμό ή ισότητα
                is_numeric = label.isdigit() or label == "."    # Αν το label είναι αριθμός ή δεκαδικό σημείο

                btn = customtkinter.CTkButton(  # Δημιουργία του κουμπιού
                    master=self.bottom_buttons_frame,   # Το parent του κουμπιού είναι το bottom_buttons_frame
                    text=label, # Το κείμενο του κουμπιού είναι το label
                    font=("Arial", 30 if is_numeric or is_operator else 20),    # Η γραμματοσειρά του κουμπιού
                    height=60,  # Το ύψος του κουμπιού
                    hover_color=self.theme.get("hover_default", "#6e6e6e"),    # Το hover χρώμα του κουμπιού, με fallback
                    command=lambda val=label: on_button_click(self, val)    # Η εντομή που εκτελείται όταν πατηθεί το κουμπί
                )

                # Εφαρμογή διαφορετικών χρωμάτων ανά τύπο κουμπιού, χρησιμοποιώντας fallback
                if is_ac:   # Αν είναι κουμπί καθαρισμού ή ισότητας (C, AC, =)
                    btn.configure(
                        fg_color=self.theme.get("ac_button_bg", "#eb7c16"),    # Χρώμα φόντου, με fallback
                        text_color=self.theme.get("ac_button_text", "#ffffff"),    # Χρώμα κειμένου, με fallback
                        hover_color=self.theme.get("ac_hover", "#f39c12")  # Χρώμα hover, με fallback
                    )
                    self.ac_buttons.append(btn) # Προσθήκη του κουμπιού καθαρισμού στη λίστα ac_buttons
                elif is_operator:   # Αν είναι αριθμητική πράξη (π.χ. +, -, x, ÷)
                    btn.configure(
                        fg_color=self.theme.get("op_button_bg", "#7c7c7c"),        # Χρώμα φόντου, με fallback
                        text_color=self.theme.get("op_button_text", "#ffffff"),    # Χρώμα κειμένου, με fallback
                        hover_color=self.theme.get("op_hover", "#8c8c8c")          # Χρώμα hover, με fallback
                    )
                    self.operation_buttons.append(btn)  # Προσθήκη του κουμπιού αριθμητικής πράξης στη λίστα operation_buttons
                elif is_symbol: # Αν είναι σύμβολο (π.χ. 1/x, x², √)
                    btn.configure(
                        fg_color=self.theme.get("op_button_bg", "#7c7c7c"),        # Χρώμα φόντου, με fallback
                        text_color=self.theme.get("op_button_text", "#ffffff"),    # Χρώμα κειμένου, με fallback
                        hover_color=self.theme.get("op_hover", "#8c8c8c")          # Χρώμα hover, με fallback
                    )
                    self.symbol_buttons.append(btn) # Προσθήκη του κουμπιού συμβόλου στη λίστα symbol_buttons

                elif is_memory: # Αν είναι κουμπί μνήμης (mc, m+, m-, mr)
                    btn.configure(
                        fg_color=self.theme.get("top_button_bg", "#4f4f4f"),       # Χρώμα φόντου, με fallback
                        text_color=self.theme.get("top_button_text", "#ffffff"),   # Χρώμα κειμένου, με fallback
                        hover_color=self.theme.get("top_button_hover", "#6e6e6e")  # Χρώμα hover, με fallback
                    )
                    self.memory_buttons.append(btn)

                else:   # Αν είναι αριθμητικό κουμπί (0-9,.)
                    btn.configure(
                        fg_color=self.theme.get("num_button_bg", "#a6a6a6"),       # Χρώμα φόντου, με fallback
                        text_color=self.theme.get("num_button_text", "#ffffff"),   # Χρώμα κειμένου, με fallback
                        hover_color=self.theme.get("num_hover", "#b6b6b6")         # Χρώμα hover, με fallback
                    )
                    self.numeric_buttons.append(btn)

                btn.grid(row=r, column=c, columnspan=col_span, padx=4, pady=4, sticky="nsew")   # Τοποθετούμε το κουμπί στο grid layout του bottom_buttons_frame

                if col_span == 2:   # Αν το κουμπί καταλαμβάνει 2 στήλες (π.χ. το "=")
                    # Διορθώθηκε: Η ρύθμιση columnconfigure(c + 1, weight=0) δεν είναι απαραίτητη και μπορεί να δημιουργήσει θέματα
                    # Εφόσον το "equal" είναι στη θέση (6, 2) με columnspan 2, καλύπτει τις στήλες 2 και 3.
                    # Οι στήλες ήδη ρυθμίζονται στο τέλος της build_ui με weight=1.
                    pass

        for i in range(7):  # Για κάθε γραμμή στο grid layout του bottom_buttons_frame
            self.bottom_buttons_frame.rowconfigure(i, weight=1) # Κάθε γραμμή έχει βάρος 1, οπότε επεκτείνεται ομοιόμορφα
        for j in range(4):
            self.bottom_buttons_frame.columnconfigure(j, weight=1)

        # Αυτή η κλήση είναι σημαντική. Επειδή καλείται στην __init__ μετά την build_ui,
        # διασφαλίζει ότι τα widgets θα έχουν τα σωστά χρώματα από την αρχή.
        # Η ίδια η build_ui χρησιμοποιεί ήδη self.theme.get(...)
        # Οπότε, εδώ το ξανακαλούμε για να "φρεσκάρουμε" τα πάντα με το αρχικό θέμα.
        self.apply_theme(self.theme) # Είναι ήδη εδώ, απλά το σχολιάζω για να το θυμόμαστε.


    def get_display_value(self):
        return self.display_var.get()   # Επιστρέφει την τιμή που εμφανίζεται στο display

    def set_display_value(self, value):  # Ορίζει την τιμή του display
        max_len = 20  # Μέγιστος αριθμός χαρακτήρων για την οθόνη
        value_str = str(value)

        if len(value_str) > max_len:
            try:
                # Προσπάθεια μετατροπής σε εκθετική μορφή αν είναι αριθμός
                num_val = mpf(value_str)
                formatted_value = f"{num_val:.{max_len - 5}e}"
                if len(formatted_value) <= max_len:
                    self.display_var.set(formatted_value)
                else:
                    self.display_var.set("OVERFLOW")
            except (ValueError, TypeError, mpf.libmp.libint.MPDecimalError):
                self.display_var.set("ERROR")
            except Exception as e:
                self.display_var.set("ERROR")
                print(f"Απροσδόκητο σφάλμα κατά τη μορφοποίηση της τιμής display: {e}")
        else:
            self.display_var.set(value_str)

    def apply_theme(self, theme_dict):
        # Εφαρμογή χρωμάτων σε όλα τα στοιχεία σύμφωνα με το θέμα, χρησιμοποιώντας fallback τιμές
        self.configure(fg_color=theme_dict.get("background", "#222222"))
        if self.top_buttons_frame:
            self.top_buttons_frame.configure(fg_color=theme_dict.get("top_frame_bg", "#222222"))
        if self.bottom_buttons_frame:
            self.bottom_buttons_frame.configure(fg_color=theme_dict.get("bottom_frame_bg", "#222222"))
        if self.display_container:
            self.display_container.configure(fg_color=theme_dict.get("display_bg", "#000000"))
        if self.top_display:
            self.top_display.configure(fg_color=theme_dict.get("display_bg", "#000000"))

        if self.display_entry:
            self.display_entry.configure(
                fg_color=theme_dict.get("display_bg", "#000000"),
                text_color=theme_dict.get("display_text", "#00ff00")
            )
        if self.middle_display:
            self.middle_display.configure(
                fg_color=theme_dict.get("display_bg", "#000000"),
                text_color=theme_dict.get("display_text", "#00ff00")
            )
        if self.manual_button:
            self.manual_button.configure(
                fg_color=theme_dict.get("manual_button_bg", "#000000"),
                text_color=theme_dict.get("manual_button_text", "#eb7c16"),
                hover_color=theme_dict.get("hover_manual_button", "#000000")
            )
        if self.history_display:
            self.history_display.configure(
                fg_color=theme_dict.get("display_bg", "#000000"),
                text_color=theme_dict.get("display_text", "#00ff00")
            )
        if self.angle_mode_label:
            self.angle_mode_label.configure( # Αυτό το κομμάτι έλειπε και το πρόσθεσα για πληρότητα
                fg_color=theme_dict.get("angle_mode_bg", "#000000"),
                text_color=theme_dict.get("angle_mode_text", "#00ff00")
            )

        # =========================================================================
        # Η ΑΠΑΡΑΙΤΗΤΗ ΠΡΟΣΘΗΚΗ ΓΙΑ ΤΟ ΚΟΥΜΠΙ HISTORY_BUTTON ΕΔΩ!
        # =========================================================================
        if self.history_button: # Αυτό ήταν το σημείο που έλειπε
            self.history_button.configure(
                fg_color=theme_dict.get("manual_button_bg", "#000000"),
                text_color=theme_dict.get("manual_button_text", "#eb7c16"),
                hover_color=theme_dict.get("hover_manual_button", "#000000")
            )
        # =========================================================================


        for btn in self.symbol_buttons + self.operation_buttons:
            btn.configure(
                fg_color=theme_dict.get("op_button_bg", "#7c7c7c"),
                text_color=theme_dict.get("op_button_text", "#ffffff"),
                hover_color=theme_dict.get("op_hover", "#8c8c8c")
            )

        for btn in self.numeric_buttons:
            btn.configure(
                fg_color=theme_dict.get("num_button_bg", "#a6a6a6"),
                text_color=theme_dict.get("num_button_text", "#ffffff"),
                hover_color=theme_dict.get("num_hover", "#b6b6b6")
            )

        for btn in self.ac_buttons:
            btn.configure(
                fg_color=theme_dict.get("ac_button_bg", "#eb7c16"),
                text_color=theme_dict.get("ac_button_text", "#ffffff"),
                hover_color=theme_dict.get("ac_hover", "#f39c12")
            )

        # κουμπιά μνήμης (memory buttons)
        for btn in self.memory_buttons:
            btn.configure(
                fg_color=theme_dict.get("top_button_bg", "#4f4f4f"),
                text_color=theme_dict.get("top_button_text", "#ffffff"),
                hover_color=theme_dict.get("top_button_hover", "#6e6e6e")
            )

        # Επίσης, πρέπει να ενημερώσουμε και το history_handler,
        # όπως κάναμε και στο scientificCalc.
        if self.history_handler:
            self.history_handler.apply_theme(theme_dict)

    def insert_history_expression(self, entry):
        """
        Παίρνει ένα string του ιστορικού τύπου "3 + 2 = 5"
        και βάζει την έκφραση πριν το '=' στο display.
        """
        if "=" not in entry:
            return

        expression = entry.split("=")[0].strip()
        self.set_display_value(expression)  # Χωρίς καμία μετατροπή

    def handle_key_input(self, key):
        # Διαχειρίζεται την είσοδο από το πληκτρολόγιο
        from keyboardInputHandler import handle_keyboard_input  # Εισάγει τη συνάρτηση διαχείρισης πληκτρολογίου
        handle_keyboard_input(key, self)  # Καλεί τη συνάρτηση με το πλήκτρο και το αντικείμενο

        if key == '1/x':  # Αν το πλήκτρο είναι "1/x"
            self.calculate_reciprocal()  # Υπολογίζει το αντίστροφο
        elif key == 'x²':  # Αν το πλήκτρο είναι "x²"
            self.calculate_square()  # Υπολογίζει το τετράγωνο

    def calculate_reciprocal(self):
        # Υπολογίζει το αντίστροφο του αριθμού στο display
        try:
            current_value = float(self.get_display_value())  # Παίρνει την τιμή του display ως float
            if current_value != 0:  # Αν δεν είναι μηδέν
                result = 1 / current_value  # Υπολογίζει το αντίστροφο
                self.set_display_value(str(result))  # Εμφανίζει το αποτέλεσμα
            else:
                self.set_display_value("Error")  # Αν μηδέν, εμφανίζει σφάλμα (διαίρεση με το μηδέν)
        except ValueError:
            self.set_display_value("Error")  # Αν δεν είναι έγκυρος αριθμός, εμφανίζει σφάλμα

    def calculate_square(self):
        # Υπολογίζει το τετράγωνο του αριθμού στο display
        try:
            current_value = float(self.get_display_value())  # Παίρνει την τιμή του display ως float
            result = current_value ** 2  # Υπολογίζει το τετράγωνο
            self.set_display_value(str(result))  # Εμφανίζει το αποτέλεσμα
        except ValueError:
            self.set_display_value("Error")  # Αν δεν είναι έγκυρος αριθμός, εμφανίζει σφάλμα


# Δημιουργία instance με επιλογή theme mode (π.χ. από dark σε light)
def create_standard_calculator_frame(parent, theme_mode="dark", sound_enabled=True):
    theme = get_theme(theme_mode)
    return StandardCalculator(parent, theme=theme, sound_enabled=sound_enabled)

# Δοκιμή εκτός εφαρμογής (standalone εκτέλεση)
if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("400x600")
    app.title("Standard Calculator Test - Clean")

    frame = StandardCalculator(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()