# standardCalc.py
# ----------------------------------------------------------
# Αυτό το αρχείο υλοποιεί έναν τυπικό υπολογιστή (standard calculator)
# με χρήση της βιβλιοθήκης customtkinter. Ο υπολογιστής υποστηρίζει
# αριθμητικές πράξεις, θεματική εμφάνιση, υποστήριξη ήχου και πρόσβαση
# σε online manual.

# Εισαγωγές απαραίτητων βιβλιοθηκών
import customtkinter  # Η customtkinter είναι επέκταση του tkinter με πιο σύγχρονο UI (Widgets με themes, dark mode κλπ)
import webbrowser      # Για να ανοίξουμε σύνδεσμο στο browser (το manual μας)

from themeManager import get_theme  # Εισάγουμε τη συνάρτηση που επιστρέφει ένα dictionary με τα χρώματα του theme
from buttonHandler import on_button_click  # Η βασική συνάρτηση που εκτελεί τις πράξεις όταν πατάμε κουμπιά
from manualHandler import show_manual_popup
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
        self.theme = theme or get_theme("dark")  # Αν περαστεί θέμα, το χρησιμοποιούμε, αλλιώς παίρνουμε το "dark"
        # Το theme εδώ είναι ένα dictionary (λεξικό) με ονόματα και χρώματα (π.χ. "background": "#222222")
        # Το get_theme("dark") επιστρέφει ένα τέτοιο λεξικό ανάλογα με την επιλογή χρήστη

        self.display_var = customtkinter.StringVar(value="0")  # Το κείμενο που εμφανίζεται στο display
        self.just_evaluated = False  # Flag για να ξέρουμε αν μόλις πατήθηκε "=" ώστε να μη συνεχίσουμε αμέσως με ψηφία
        self.sound_enabled = sound_enabled  # Αν είναι ενεργός ο ήχος (true ή false)

        # Ομάδες κουμπιών για εύκολη πρόσβαση κατά το theme update
        self.operation_buttons = []     # Κουμπιά για τις βασικές αριθμητικές πράξεις (+, -, x, ÷)
        self.symbol_buttons = []        # Κουμπιά για συμβολικές λειτουργίες (1/x, x², √, % κλπ)
        self.numeric_buttons = []       # Κουμπιά για αριθμούς (0-9) και το δεκαδικό σημείο
        self.ac_buttons = []            # Κουμπιά για λειτουργίες καθαρισμού (C, AC)

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
        # Δημιουργία του top frame που περιέχει τα πεδία εμφάνισης (display)
        self.top_buttons_frame = customtkinter.CTkFrame(self, corner_radius=0)  # Το top frame είναι το πάνω μέρος της αριθμομηχανής
        self.top_buttons_frame.pack(fill="x")   # Το top frame γεμίζει το πλάτος του parent frame


        self.display_container = customtkinter.CTkFrame(self.top_buttons_frame, fg_color=self.theme["display_bg"], corner_radius=0)
        self.display_container.pack(fill="x", padx=0, pady=(0, 0))  # Το display_container είναι το container για τα πεδία εμφάνισης

        # Top display – περιέχει το κουμπί που ανοίγει το manual (το ✍️)
        self.top_display = customtkinter.CTkFrame(self.display_container, height=30, fg_color=self.theme["display_bg"], corner_radius=0)
        self.top_display.pack(fill="x") # Το top_display είναι το πάνω μέρος του display container

        self.manual_button = customtkinter.CTkButton(   # Το κουμπί για το manual
            self.top_display,   # Το parent του κουμπιού είναι το top_display
            text="✍️",  # Το κείμενο του κουμπιού είναι το emoji για manual
            width=30,   # Το πλάτος του κουμπιού
            height=30,  # Το ύψος του κουμπιού
            font=("Arial", 18), # Η γραμματοσειρά του κειμένου του κουμπιού
            fg_color=self.theme["manual_button_bg"],    # Το χρώμα του background του κουμπιού
            text_color=self.theme["manual_button_text"],    # Το χρώμα του κειμένου του κουμπιού
            hover_color=self.theme["hover_manual_button"],  # Το χρώμα όταν το κουμπί είναι hover
            command=lambda: show_manual_popup(self) # Η εντολή που εκτελείται όταν πατηθεί το κουμπί (άνοιγμα manual)
        )
        self.manual_button.pack(side="left", padx=15)   # Το κουμπί τοποθετείται αριστερά στο top_display

        self.history_button = customtkinter.CTkButton(  # Το κουμπί για το ιστορικό
            self.top_display,   # Το parent του κουμπιού είναι το top_display
            text="🕘",          # Το κείμενο του κουμπιού είναι το emoji για ιστορικό
            width=30,           
            height=30,          # Το ύψος του κουμπιού
            corner_radius=0,    # Το corner_radius του κουμπιού (γωνίες)
            font=("Arial", 18), # Η γραμματοσειρά του κειμένου του κουμπιού
            fg_color=self.theme["manual_button_bg"],        # Το χρώμα του background του κουμπιού
            text_color=self.theme["manual_button_text"],    # Το χρώμα του κειμένου του κουμπιού
            hover_color=self.theme["hover_manual_button"],  # Το χρώμα όταν το κουμπί είναι hover
            command=self.open_history_window    # Η εντολή που εκτελείται όταν πατηθεί το κουμπί (άνοιγμα ιστορικού)
        )
        self.history_button.pack(side="right", padx=15) # Το κουμπί τοποθετείται δεξιά στο top_display

        #Label για το ιστορικό των πράξεων
        self.history_display_var = customtkinter.StringVar(value="")    # Αρχικοποίηση του StringVar για το ιστορικό
        self.history_display = customtkinter.CTkLabel(                  # Το label που θα δείχνει το ιστορικό
            self.display_container,textvariable=self.history_display_var,   # Το textvariable είναι το StringVar που περιέχει το ιστορικό
            height=20,          # Το ύψος του label
            corner_radius=0,    # Το corner_radius του label (γωνίες)
            font=("Arial", 12), # Η γραμματοσειρά του κειμένου του label
            anchor="e",         # Ευθυγράμμιση στα δεξιά
            fg_color=self.theme["display_bg"],      # Το χρώμα του label
            text_color=self.theme["display_text"]   # Το χρώμα του κειμένου του label
        )
        self.history_display.pack(fill="x", padx=20) # Το label γεμίζει το πλάτος του container

        # Μεσαίο label (προετοιμασία για ιστορικό ή πληροφορίες)
        self.middle_display = customtkinter.CTkLabel(   # Το μεσαίο label για πληροφορίες ή ιστορικό
            self.display_container,     # Το parent του μεσαίου label είναι το display_container
            text="",    # Αρχικά κενό, θα ενημερώνεται με πληροφορίες ή ιστορικό
            height=24,  # Το ύψος του μεσαίου label
            corner_radius=0,    # Το corner_radius του μεσαίου label (γωνίες)
            font=("Arial", 14), # Η γραμματοσειρά του κειμένου του μεσαίου label
            anchor="e", # Ευθυγράμμιση στα δεξιά
            wraplength=300, # Το wraplength για το μεσαίο label (μέγιστο πλάτος πριν την αλλαγή γραμμής)
            fg_color=self.theme["display_bg"],  # Το χρώμα του μεσαίου label
            text_color=self.theme["display_text"]   # Το χρώμα του κειμένου του μεσαίου label
        )
        self.middle_display.pack(fill="x", padx=15) # Το μεσαίο label γεμίζει το πλάτος του container

        # Κύριο πεδίο για εμφάνιση αριθμών / αποτελεσμάτων
        self.display_entry = customtkinter.CTkEntry(    # Το κύριο πεδίο για εμφάνιση αριθμών και αποτελεσμάτων
            self.display_container,         # Το parent του display entry είναι το display_container
            textvariable=self.display_var,  # Το textvariable είναι το StringVar που περιέχει την τιμή του display
            font=("Arial", 24),
            justify="right",
            state="readonly",
            height=60,
            corner_radius=0,
            border_width=0,
            fg_color=self.theme["display_bg"],      # Το χρώμα του background του display entry
            text_color=self.theme["display_text"]   # Το χρώμα του κειμένου του display entry
        )
        self.display_entry.pack(fill="x", padx=15, pady=(0, 0))

        # Ένδειξη Deg ή Rad – το βάζουμε έτσι κι αλλιώς (στο Standard απλά μένει κενό)
        # Δημιουργία label για την ένδειξη γωνιακής λειτουργίας (Deg/Rad)
        self.angle_mode_label = customtkinter.CTkLabel(   # Label για Deg/Rad (στο standard μένει κενό)
            self.display_container,                       # Parent είναι το display_container
            text="",                                     # Αρχικά κενό (στο standard calculator δεν εμφανίζεται κάτι)
            font=("Arial", 10),                          # Γραμματοσειρά και μέγεθος
            width=30,                                    # Πλάτος label
            height=16,                                   # Ύψος label
            fg_color=self.theme["display_bg"],            # Χρώμα background (ίδιο με το display)
            text_color=self.theme["display_text"]         # Χρώμα κειμένου (ίδιο με το display)
        )
        self.angle_mode_label.pack(anchor="sw", padx=10, pady=(0, 4))  # Τοποθέτηση κάτω αριστερά με padding

        self.history_log = []         # Λίστα για το ιστορικό πράξεων
        self.history_window = None    # Μεταβλητή για το παράθυρο ιστορικού (αν είναι ανοιχτό)
        self.memory = mpf("0")        # Τιμή μνήμης αριθμομηχανής (αρχικά 0, τύπος mpf για ακρίβεια)
        self.is_degree = True         # Flag για το αν είναι ενεργή η λειτουργία Degree (στο standard δεν αλλάζει)
        self.is_second_function = False   # Flag για το αν είναι ενεργή η δεύτερη λειτουργία (στο standard false)

        # Ορισμός κουμπιών σε πίνακα – layout 7 γραμμών με 4 κουμπιά η κάθε μία
        button_rows = [ 
            ["mc", "m+", "m-", "mr"],   # Λίστα με κουμπιά πρώτης γραμμής για μνήμη
            ["1/x", "%", "C", "AC"],    # Λίστα με κουμπιά δεύτερης γραμμής για καθαρισμό και συμβολικές λειτουργίες
            ["x²", "√", "+/-", "÷"],    # Λίστα με κουμπιά τρίτης γραμμής για αριθμητικές πράξεις
            ["7", "8", "9", "x"],       # Λίστα με κουμπιά τέταρτης γραμμής για αριθμούς και πολλαπλασιασμό
            ["4", "5", "6", "-"],       # Λίστα με κουμπιά πέμπτης γραμμής για αριθμούς και αφαίρεση
            ["1", "2", "3", "+"],       # Λίστα με κουμπιά έκτης γραμμής για αριθμούς και πρόσθεση
            ["0", ".", "="]             # Λίστα κουμπιών στην έβδομη γραμμή για αριθμούς και ισότητα
        ]

        self.bottom_buttons_frame = customtkinter.CTkFrame(self, fg_color=self.theme["bottom_frame_bg"])    # Το χρώμα του bottom frame
        self.bottom_buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)  # Το bottom frame γεμίζει το χώρο και έχει padding

        # Δημιουργία κουμπιών δυναμικά με βάση τα labels
        for r, row in enumerate(button_rows):   # Για κάθε γραμμή κουμπιών
            for c, label in enumerate(row):     # Για κάθε κουμπί στη γραμμή
                if label == "":     # Αν το label είναι κενό, δεν δημιουργούμε κουμπί
                    continue

                # Ελέγχουμε τον τύπο του κουμπιού
                col_span = 2 if label == "=" else 1             # Αν το label είναι "=", το κουμπί καταλαμβάνει 2 στήλες
                is_memory = label in ["mc", "m+", "m-", "mr"]   # Αν το label είναι για μνήμη, το αποθηκεύουμε σε άλλη λίστα
                is_operator = label in ["+", "-", "x", "÷"]     # Αν το label είναι αριθμητική πράξη, το αποθηκεύουμε σε άλλη λίστα
                is_symbol = label in ["1/x", "%", "+/-", "x²", "√"]     # Αν το label είναι σύμβολο, το αποθηκεύουμε σε άλλη λίστα
                is_ac = label in ["AC", "C", "="]               # Αν το label είναι για καθαρισμό ή ισότητα, το αποθηκεύουμε σε άλλη λίστα
                is_numeric = label.isdigit() or label == "."    # Αν το label είναι αριθμός ή δεκαδικό σημείο, το αποθηκεύουμε σε άλλη λίστα

                btn = customtkinter.CTkButton(  # Δημιουργία του κουμπιού
                    master=self.bottom_buttons_frame,   # Το parent του κουμπιού είναι το bottom_buttons_frame
                    text=label, # Το κείμενο του κουμπιού είναι το label
                    font=("Arial", 30 if is_numeric or is_operator else 20),    # Η γραμματοσειρά του κουμπιού
                    height=60,  # Το ύψος του κουμπιού
                    hover_color=self.theme.get("hover_default"),    # Το hover χρώμα του κουμπιού (default αν δεν είναι ειδικό)
                    command=lambda val=label: on_button_click(self, val)    # Η εντολή που εκτελείται όταν πατηθεί το κουμπί
                )

                # Εφαρμογή διαφορετικών χρωμάτων ανά τύπο κουμπιού
                if is_ac:   # Αν είναι κουμπί καθαρισμού ή ισότητας (C, AC, =)
                    btn.configure(  
                        fg_color=self.theme["ac_button_bg"],    # Το χρώμα του background για κουμπιά καθαρισμού
                        text_color=self.theme["ac_button_text"],    # Το χρώμα του κειμένου για κουμπιά καθαρισμού
                        hover_color=self.theme["ac_hover"]  # Το hover χρώμα για κουμπιά καθαρισμού
                    )
                    self.ac_buttons.append(btn) # Προσθήκη του κουμπιού καθαρισμού στη λίστα ac_buttons
                elif is_operator:   # Αν είναι αριθμητική πράξη (π.χ. +, -, x, ÷)
                    btn.configure(  
                        fg_color=self.theme["op_button_bg"],        # Το χρώμα του background για κουμπιά αριθμητικών πράξεων
                        text_color=self.theme["op_button_text"],    # Το χρώμα του κειμένου για κουμπιά αριθμητικών πράξεων
                        hover_color=self.theme["op_hover"]          # Το hover χρώμα για κουμπιά αριθμητικών πράξεων
                    )
                    self.operation_buttons.append(btn)  # Προσθήκη του κουμπιού αριθμητικής πράξης στη λίστα operation_buttons     
                elif is_symbol: # Αν είναι σύμβολο (π.χ. 1/x, x², √)
                    btn.configure(
                        fg_color=self.theme["op_button_bg"],        # Το χρώμα του background για κουμπιά συμβόλων
                        text_color=self.theme["op_button_text"],    # Το χρώμα του κειμένου για κουμπιά συμβόλων
                        hover_color=self.theme["op_hover"]          # Το hover χρώμα για κουμπιά συμβόλων
                    )
                    self.symbol_buttons.append(btn) # Προσθήκη του κουμπιού συμβόλου στη λίστα symbol_buttons
                elif is_memory: # Αν είναι κουμπί μνήμης (mc, m+, m-, mr)
                    btn.configure(
                        fg_color=self.theme["top_button_bg"],       # Το χρώμα του background για κουμπιά μνήμης
                        text_color=self.theme["top_button_text"],   # Το χρώμα του κειμένου για κουμπιά μνήμης 
                        hover_color=self.theme["top_button_hover"]  # Το hover χρώμα για κουμπιά μνήμης
                    )
                else:   # Αν είναι αριθμητικό κουμπί (0-9, .)
                    btn.configure(  
                        fg_color=self.theme["num_button_bg"],       # Το χρώμα του background για αριθμητικά κουμπιά
                        text_color=self.theme["num_button_text"],   # Το χρώμα του κειμένου για αριθμητικά κουμπιά
                        hover_color=self.theme["num_hover"]         # Το hover χρώμα για αριθμητικά κουμπιά
                    )
                    self.numeric_buttons.append(btn)

                btn.grid(row=r, column=c, columnspan=col_span, padx=4, pady=4, sticky="nsew")   # Τοποθετούμε το κουμπί στο grid layout του bottom_buttons_frame

                if col_span == 2:   # Αν το κουμπί καταλαμβάνει 2 στήλες (π.χ. το "=")
                    self.bottom_buttons_frame.columnconfigure(c + 1, weight=0)  # Η δεύτερη στήλη δεν έχει βάρος, οπότε δεν επεκτείνεται

        for i in range(7):  # Για κάθε γραμμή στο grid layout του bottom_buttons_frame
            self.bottom_buttons_frame.rowconfigure(i, weight=1) # Κάθε γραμμή έχει βάρος 1, οπότε επεκτείνεται ομοιόμορφα
        for j in range(4):         
            self.bottom_buttons_frame.columnconfigure(j, weight=1)  

        self.apply_theme(self.theme)    

    def get_display_value(self):    
        return self.display_var.get()   # Επιστρέφει την τιμή που εμφανίζεται στο display

    def set_display_value(self, value):
        self.display_var.set(value)     # Ενημερώνει την τιμή του display με το νέο value

    def apply_theme(self, theme_dict):
        # Εφαρμογή χρωμάτων σε όλα τα στοιχεία σύμφωνα με το θέμα
        self.configure(fg_color=theme_dict["background"])                           # Το χρώμα του frame 
        self.top_buttons_frame.configure(fg_color=theme_dict["top_frame_bg"])       # Το χρώμα του top frame
        self.bottom_buttons_frame.configure(fg_color=theme_dict["bottom_frame_bg"]) # Το χρώμα του bottom frame
        self.display_container.configure(fg_color=theme_dict["display_bg"])         # Το χρώμα του display container
        self.top_display.configure(fg_color=theme_dict["display_bg"])               # Το χρώμα του top display

        self.display_entry.configure(
            fg_color=theme_dict["display_bg"],      # Το χρώμα του display entry
            text_color=theme_dict["display_text"]   # Το χρώμα του κειμένου στο display entry
        )
        self.middle_display.configure(
            fg_color=theme_dict["display_bg"],      # Το χρώμα του middle display
            text_color=theme_dict["display_text"]   # Το χρώμα του κειμένου στο middle display
        )
        self.manual_button.configure(
            fg_color=theme_dict["manual_button_bg"],        # Το χρώμα του κουμπιού manual
            text_color=theme_dict["manual_button_text"],    # Το χρώμα του κειμένου του κουμπιού manual
            hover_color=theme_dict["hover_manual_button"]   # Το hover χρώμα του κουμπιού manual
        )
        self.history_display.configure(
            fg_color=theme_dict["display_bg"],      # Το χρώμα του label ιστορικού
            text_color=theme_dict["display_text"]   # Το χρώμα του κειμένου του label ιστορικού
        )

        for btn in self.symbol_buttons + self.operation_buttons:
            btn.configure(
                fg_color=theme_dict["op_button_bg"],        # Το χρώμα των κουμπιών συμβόλων και πράξεων
                text_color=theme_dict["op_button_text"],    # Το χρώμα του κειμένου των κουμπιών συμβόλων και πράξεων
                hover_color=theme_dict["op_hover"]          # Το hover χρώμα των κουμπιών συμβόλων και πράξεων
            )

        for btn in self.numeric_buttons:
            btn.configure(
                fg_color=theme_dict["num_button_bg"],
                text_color=theme_dict["num_button_text"],
                hover_color=theme_dict["num_hover"]
            )

        for btn in self.ac_buttons:
            btn.configure(
                fg_color=theme_dict["ac_button_bg"],
                text_color=theme_dict["ac_button_text"],
                hover_color=theme_dict["ac_hover"]
            )

    def open_manual(self):
        # Ανοίγει το Google Doc manual σε browser
        webbrowser.open("https://docs.google.com/document/d/1xHKVvzsmCFrH7DBCih10n8-JnZcKpbIFKqexXh1MI8w/edit?usp=sharing")

    def open_history_window(self):
        if not self.history_log:  # Αν δεν υπάρχει ιστορικό, δεν κάνουμε τίποτα
            return

        if self.history_window and self.history_window.winfo_exists():  # Αν το παράθυρο ιστορικού υπάρχει ήδη
            self.history_window.lift()  # Το φέρνουμε μπροστά
            return

        self.history_window = customtkinter.CTkToplevel(self)   # Δημιουργούμε νέο παράθυρο (Toplevel) για το ιστορικό
        self.history_window.title("History")    # Ορίζουμε τίτλο παραθύρου
        self.history_window.geometry("300x300") # Ορίζουμε αρχικό μέγεθος παραθύρου
        self.history_window.configure(fg_color=self.theme["background"])    # Ορίζουμε το χρώμα του παραθύρου ιστορικού
        self.history_window.attributes("-topmost", True)   # Το παράθυρο να είναι πάντα πάνω από τα άλλα

        parent_x = self.winfo_rootx()     # Παίρνουμε τη θέση x του γονικού παραθύρου στην οθόνη
        parent_y = self.winfo_rooty()     # Παίρνουμε τη θέση y του γονικού παραθύρου στην οθόνη
        popup_width = 300                 # Πλάτος popup παραθύρου
        popup_height = 300                # Ύψος popup παραθύρου
        parent_width = self.winfo_width() # Πλάτος γονικού παραθύρου

        popup_x = parent_x + (parent_width - popup_width) // 2   # Υπολογίζουμε x ώστε να είναι κεντραρισμένο
        popup_y = parent_y + 100                                 # Υπολογίζουμε y ώστε να εμφανίζεται λίγο πιο κάτω

        self.history_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")  # Ορίζουμε τελική θέση και μέγεθος

        scroll_frame = customtkinter.CTkScrollableFrame(self.history_window)   # Δημιουργούμε scrollable frame για τα entries
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)         # Τοποθετούμε το scroll frame στο παράθυρο

        for entry in reversed(self.history_log[-50:]):    # Για κάθε entry στα τελευταία 50 του ιστορικού (αντιστραμμένα)
            btn = customtkinter.CTkButton(
                scroll_frame,                 # Parent είναι το scroll frame
                text=entry,                   # Το κείμενο του κουμπιού είναι το entry του ιστορικού
                anchor="w",                   # Ευθυγράμμιση αριστερά
                height=30,                    # Ύψος κουμπιού
                font=("Arial", 12),           # Γραμματοσειρά
                fg_color=self.theme["top_button_bg"],         # Χρώμα background
                hover_color=self.theme["top_button_hover"],   # Χρώμα hover
                text_color=self.theme["top_button_text"],     # Χρώμα κειμένου
                command=lambda e=entry: self.insert_history_expression(e)  # Όταν πατηθεί, εισάγει το entry στο display
            )
            btn.pack(fill="x", pady=2)    # Τοποθετούμε το κουμπί στο scroll frame, γεμίζει οριζόντια με λίγο κάθετο κενό
            btn.pack(fill="x", pady=2)


    def insert_history_expression(self, entry):
        # Εισάγει μια έκφραση από το ιστορικό στο display
        if "=" in entry:  # Αν το entry περιέχει το σύμβολο "="
            expr = entry.split("=")[0].strip()  # Παίρνει το μέρος πριν το "=" και αφαιρεί κενά
            self.display_var.set(expr)  # Εμφανίζει την έκφραση στο display

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