# scientificCalc.py
# ----------------------------------------------------------
# Αυτό το αρχείο υλοποιεί επιστημονική αριθμομηχανή
# με επιπλέον συναρτήσεις, υποστήριξη themes και εναλλαγή λειτουργιών
# Rad/Deg και 2nd function. Χρησιμοποιεί την customtkinter για τη γραφική διεπαφή.

import customtkinter  # Βασικό GUI toolkit με υποστήριξη themes και responsive widgets
from themeManager import get_theme  # Επιστρέφει λεξικό με χρώματα για κάθε theme (dark, light κλπ.)
from buttonHandler import on_button_click  # Λογική χειρισμού πατημάτων κουμπιών
from mpmath import mpf, mp  # Για αριθμητική ακρίβειας πολλών ψηφίων (π.χ. για πράξεις με π)
from manualHandler import show_manual_popup  # Εμφάνιση του manual popup
from historyWindow import HistoryWindowModule


# ==========================================================
# ΚΛΑΣΗ: ScientificCalculator
# ==========================================================
# Η κλάση αυτή ορίζει ένα "πλαίσιο" (CTkFrame) το οποίο περιέχει όλα τα στοιχεία ενός
# επιστημονικού υπολογιστή, δηλαδή:
# - display (πεδίο εμφάνισης)
# - σειρές κουμπιών με λειτουργίες (sin, log, AC, +, - κλπ.)
# - υποστήριξη εναλλαγής 2nd function και Rad/Deg
# Η χρήση customtkinter δίνει ευελιξία και μοντέρνο σχεδιασμό.



class ScientificCalculator(customtkinter.CTkFrame):
    # Η υπογραφή της __init__ πρέπει να περιλαμβάνει το theme_mode
    def __init__(self, parent, mode="scientific", theme=None, sound_enabled=True, theme_mode="dark"):
        super().__init__(parent)


        # ==========================================================
        # 1. ΑΡΧΙΚΟΠΟΙΗΣΗ ΜΕΤΑΒΛΗΤΩΝ ΚΑΤΑΣΤΑΣΗΣ (State Variables)
        #    Αυτές οι μεταβλητές καθορίζουν την τρέχουσα κατάσταση
        #    της αριθμομηχανής (π.χ. τιμές στην οθόνη, μνήμη, flags).
        # ==========================================================
        self.display_var = customtkinter.StringVar(value="0")  # Η μεταβλητή για το κείμενο στην οθόνη
        self.memory = mpf("0")  # Η τιμή που είναι αποθηκευμένη στη μνήμη
        self.is_second_function = False  # True αν είναι ενεργή η 2nd λειτουργία
        self.is_degree = True  # True αν η γωνιακή λειτουργία είναι σε μοίρες (Deg), False για ακτίνια (Rad)
        self.just_evaluated = False  # True αν η τελευταία πράξη ήταν μια αξιολόγηση (=)
        self.history_log = []  # Λίστα με τις καταχωρήσεις του ιστορικού
        self.history_window = None  # Αναφορά στο παράθυρο ιστορικού (αρχικά None)
        self.sound_enabled = sound_enabled  # Καθορίζει αν οι ήχοι είναι ενεργοποιημένοι


        # ==========================================================
        # 2. ΑΡΧΙΚΟΠΟΙΗΣΗ ΛΕΞΙΚΩΝ ΓΙΑ 2ND FUNCTION
        #    Χρησιμοποιούνται για την εναλλαγή των labels των κουμπιών
        #    όταν πατιέται το πλήκτρο '2nd'.
        # ==========================================================
        self.second_map = {  # Αντιστοιχεί αρχική συνάρτηση → 2nd συνάρτηση
            "sin": "sin⁻¹", "cos": "cos⁻¹", "tan": "tan⁻¹",
            "sinh": "sinh⁻¹", "cosh": "cosh⁻¹", "tanh": "tanh⁻¹"
        }
        self.first_map = {v: k for k, v in self.second_map.items()}  # Αντιστροφή: 2nd συνάρτηση → αρχική


        # ==========================================================
        # 3. ΑΡΧΙΚΟΠΟΙΗΣΗ ΜΕΤΑΒΛΗΤΩΝ UI WIDGETS
        #    Αυτές οι μεταβλητές θα κρατήσουν αναφορές στα αντικείμενα
        #    των γραφικών στοιχείων (widgets) που θα δημιουργηθούν
        #    αργότερα στη build_ui(). Αρχικοποιούνται σε None.
        # ==========================================================
        self.display_container = None
        self.top_display = None
        self.manual_button = None
        self.history_button = None
        self.history_display_var = customtkinter.StringVar(value="")
        self.history_display = None
        self.middle_display = None
        self.display_entry = None
        self.angle_mode_label = None
        self.top_buttons_frame = None
        self.top_button_objects = []
        self.numeric_buttons = []
        self.operation_buttons = []
        self.ac_button = None
        self.c_button = None
        self.bottom_buttons_frame = None  # Προστέθηκε, αν υπάρχει στο UI σου


        # ==========================================================
        # 4. ΛΟΓΙΚΗ ΑΡΧΙΚΟΠΟΙΗΣΗΣ ΘΕΜΑΤΟΣ
        #    Αυτό το μπλοκ διασφαλίζει ότι το self.theme και
        #    το self.theme_mode είναι πάντα συνεπή και έγκυρα.
        # ==========================================================
        # Αρχικοποιούμε το theme_mode από την παράμετρο που δέχεται η __init__
        self.theme_mode = theme_mode
        # Αρχικοποιούμε το theme με το λεξικό που μας δόθηκε.
        # Η create_scientific_calculator το έχει ήδη φορτώσει.
        if theme is not None:
            self.theme = theme
        else:
            self.theme = get_theme("dark")

        # Έλεγχος ασφαλείας: Αν το παρεχόμενο 'theme' δεν είναι έγκυρο λεξικό
        if not isinstance(self.theme, dict):
            print(
                f"Προειδοποίηση: Αποτυχία φόρτωσης αρχικού θέματος '{theme_mode}' ή μη έγκυρο θέμα. Επιστροφή στο 'dark'.")

            # Προσπάθησε να φορτώσεις το 'dark' θέμα ως fallback
            fallback_theme = get_theme("dark")

            # Ένας ακόμη έλεγχος: αν ακόμα και το "dark" θέμα αποτύχει να φορτώσει
            if not isinstance(fallback_theme, dict):
                self.theme = {}  # Τελευταία λύση: ένα άδειο λεξικό για αποφυγή κρασαρίσματος
                print(
                    "Κρίσιμη Προειδοποίηση: Αποτυχία φόρτωσης ακόμα και του προκαθορισμένου θέματος 'dark'. Χρησιμοποιείται ένα κενό λεξικό θέματος.")
            else:
                self.theme = fallback_theme  # Αν το "dark" φορτώθηκε επιτυχώς, το χρησιμοποιούμε
                self.theme_mode = "dark"  # Και ενημερώνουμε το theme_mode σε "dark"


        # ==========================================================
        # 5. ΑΡΧΙΚΟΠΟΙΗΣΗ ΧΕΙΡΙΣΤΗ ΙΣΤΟΡΙΚΟΥ
        #    Χρησιμοποιεί το πλέον σωστά αρχικοποιημένο self.theme
        # ==========================================================
        self.history_handler = HistoryWindowModule(
            self,
            self.theme,
            self.history_log,
            self.insert_history_expression
        )

        # ==========================================================
        # 6. ΚΑΤΑΣΚΕΥΗ ΚΑΙ ΕΦΑΡΜΟΓΗ UI
        #    Δημιουργίζει όλα τα γραφικά στοιχεία και εφαρμόζει
        #    το τελικό αρχικό θέμα.
        # ==========================================================
        self.build_ui()  # Δημιουργεί όλα τα κουμπιά, display κλπ.
        self.apply_theme(self.theme)  # Εφαρμόζει το αρχικό theme

    # ---------------------
    # ΡΥΘΜΙΣΗ UI (USER INTERFACE)
    # ---------------------
    def build_ui(self):
        # Δημιουργία του γραφικού περιβάλλοντος του επιστημονικού υπολογιστή
        self.configure(width=400, height=600)  # Ορισμός διαστάσεων του frame

        # ----------------------- ΔΟΧΕΙΟ ΟΘΟΝΗΣ (DISPLAY CONTAINER) -----------------------
        self.display_container = customtkinter.CTkFrame(
            self,  # Το parent είναι το CTkFrame που κληρονομεί αυτή η κλάση
            fg_color=self.theme.get("display_bg", "#000000"),  # Το χρώμα του display container, με fallback
            corner_radius=0  # Γωνίες χωρίς καμπύλωση (για να ταιριάζει με το υπόλοιπο UI)
        )
        self.display_container.pack(fill="x", padx=0, pady=(0, 0))  # Γεμίζει το πλάτος του parent frame, χωρίς padding

        # Πάνω οθόνη - περιέχει το κουμπί manual
        self.top_display = customtkinter.CTkFrame(
            self.display_container,  # Το parent είναι το display_container
            height=30,  # Ύψος του top display
            fg_color=self.theme.get("display_bg", "#000000"),  # Χρώμα φόντου, με fallback
            corner_radius=0  # Γωνίες χωρίς καμπύλωση
        )
        self.top_display.pack(fill="x")  # Γεμίζει το πλάτος του display_container

        # Κουμπί για το manual popup
        self.manual_button = customtkinter.CTkButton(
            self.top_display,  # Το parent είναι το top_display
            text="✍️",  # Emoji για το κουμπί manual
            width=30, height=30,  # Διαστάσεις κουμπιού
            font=("Arial", 18),  # Γραμματοσειρά
            fg_color=self.theme.get("manual_button_bg", "#000000"),  # Χρώμα φόντου, με fallback
            text_color=self.theme.get("manual_button_text", "#eb7c16"),  # Χρώμα κειμένου, με fallback
            hover_color=self.theme.get("hover_manual_button", "#000000"),  # Χρώμα hover, με fallback
            command=lambda: show_manual_popup(self)  # Εμφάνιση του manual popup
        )
        self.manual_button.pack(side="left", padx=15)  # Τοποθέτηση στο αριστερό μέρος του top_display

        # Κουμπί για το ιστορικό πράξεων
        self.history_button = customtkinter.CTkButton(
            self.top_display,  # Το parent είναι το top_display
            text="🕒",  # Emoji για το κουμπί ιστορικού
            width=30, height=30,  # Διαστάσεις κουμπιού
            font=("Arial", 18),  # Γραμματοσειρά
            fg_color=self.theme.get("manual_button_bg", "#000000"),  # Χρώμα φόντου, με fallback
            text_color=self.theme.get("manual_button_text", "#eb7c16"),  # Χρώμα κειμένου, με fallback
            hover_color=self.theme.get("hover_manual_button", "#000000"),  # Χρώμα hover, με fallback
            command=self.history_handler.open  # Εμφάνιση του παραθύρου ιστορικού
        )
        self.history_button.pack(side="right", padx=15)  # Τοποθέτηση στο δεξί μέρος του top_display

        # Ιστορικό πράξεων
        self.history_display = customtkinter.CTkLabel(  # Το label για την εμφάνιση του ιστορικού
            self.display_container,  # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            textvariable=self.history_display_var,  # Χρησιμοποιούμε StringVar για δυναμική ενημέρωση
            height=20,  # Το ύψος του label
            font=("Arial", 12),  # Το font του label
            anchor="e",  # Ευθυγράμμιση του κειμένου στο δεξί μέρος
            fg_color=self.theme.get("display_bg", "#000000"),  # Το χρώμα φόντου του label για το ιστορικό, με fallback
            text_color=self.theme.get("display_text", "#00ff00")
            # Το χρώμα του κειμένου στο label για το ιστορικό, με fallback
        )
        self.history_display.pack(fill="x", padx=20)  # Γεμίζει το πλάτος του display_container, με padding 20px

        # Κενή ενότητα για μελλοντική χρήση ή debug
        self.middle_display = customtkinter.CTkLabel(
            # Ένα label για μεσαία εμφάνιση, π.χ. για debug ή επιπλέον πληροφορίες
            self.display_container,  # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            text="",  # Αρχικά κενό, μπορεί να χρησιμοποιηθεί για debug ή άλλες πληροφορίες
            height=24,  # Το ύψος του label
            font=("Arial", 14),  # Το font του label
            anchor="e",  # Ευθυγράμμιση του κειμένου στο δεξί μέρος
            fg_color=self.theme.get("display_bg", "#000000"),
            # Το χρώμα φόντου του label για το μεσαίο display, με fallback
            text_color=self.theme.get("display_text", "#00ff00")
            # Το χρώμα του κειμένου στο label για το μεσαίο display, με fallback
        )
        self.middle_display.pack(fill="x", padx=20)  # Γεμίζει το πλάτος του display_container, με padding 20px

        # Εμφάνιση αριθμών / αποτελεσμάτων
        self.display_entry = customtkinter.CTkEntry(  # Το πεδίο εισαγωγής για αριθμούς και αποτελέσματα
            self.display_container,  # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            textvariable=self.display_var,  # Χρησιμοποιούμε StringVar για δυναμική ενημέρωση
            font=("Arial", 24),  # Το font του πεδίου εισαγωγής
            justify="right",  # Ευθυγράμμιση του κειμένου στα δεξιά (όπως σε αριθμομηχανές)
            state="readonly",  # Το πεδίο είναι μόνο για ανάγνωση (readonly) για να μην αλλάζει ο χρήστης
            height=60,  # Το ύψος του πεδίου εισαγωγής
            corner_radius=0,  # Γωνίες χωρίς καμπύλωση (για να ταιριάζει με το υπόλοιπο UI)
            border_width=0,  # Χωρίς περίγραμμα (border) για να φαίνεται πιο καθαρό
            fg_color=self.theme.get("display_bg", "#000000"),  # Το χρώμα φόντου του πεδίου εισαγωγής, με fallback
            text_color=self.theme.get("display_text", "#00ff00")
            # Το χρώμα του κειμένου στο πεδίο εισαγωγής, με fallback
        )
        # Τοποθετεί το πεδίο εισαγωγής στο display_container
        self.display_entry.pack(fill="x", padx=15, pady=(0, 0))

        # Ένδειξη Deg ή Rad – το βάζουμε έτσι και αλλιώς (στο Standard απλά μένει κενό)
        self.angle_mode_label = customtkinter.CTkLabel(  # Το label για την ένδειξη της γωνιακής μονάδας (Deg/Rad)
            self.display_container,  # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            text=("Deg" if self.is_degree else "Rad"),  # Το κείμενο αλλάζει ανάλογα με την κατάσταση
            font=("Arial", 10),  # Το font του label
            width=30,  # Το πλάτος του label
            height=16,  # Το ύψος του label
            fg_color=self.theme.get("angle_mode_bg", "#000000"),
            # Το χρώμα φόντου του label για την ένδειξη Rad/Deg, με fallback
            text_color=self.theme.get("angle_mode_text", "#00ff00")
            # Το χρώμα του κειμένου στο label για την ένδειξη Rad/Deg, με fallback
        )
        self.angle_mode_label.pack(anchor="sw", padx=10,
                                   pady=(0, 4))  # Τοποθετεί το label στο κάτω αριστερό μέρος του display_container

        # ----------- ΕΠΙΣΤΗΜΟΝΙΚΑ ΚΟΥΜΠΙΑ -----------
        # Συναρτήσεις όπως sin, cos, log, factorial, π κλπ.
        self.top_buttons_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.theme.get("top_frame_bg",
                                                                                                       "#222222"))  # Το χρώμα του top frame, με fallback
        self.top_buttons_frame.pack(fill="both", expand=False, padx=10,
                                    pady=(6, 4))  # Γεμίζει το πλάτος του parent frame, με padding

        top_buttons = [  # Κουμπιά για επιστημονικές συναρτήσεις
            ["2nd", "Rad", "Rand", "mc", "m+", "m-", "mr"],
            ["x²", "x³", "1/x", "√", "ⁿ√x", "yˣ", "2ʸ"],
            ["sin", "cos", "tan", "sinh", "cosh", "tanh", "π"],
            ["log₁₀", "log₂", "x!", "(", ")", "%", "EE"]
        ]

        self.top_button_objects = []  # Λίστα για αποθήκευση των κουμπιών του πάνω μέρους
        for r, row in enumerate(top_buttons):  # Για κάθε σειρά κουμπιών
            row_objs = []  # Λίστα για αποθήκευση των κουμπιών της σειράς
            for c, text in enumerate(row):  # Για κάθε κουμπί στη σειρά
                self.top_buttons_frame.columnconfigure(c,
                                                       weight=1)  # Ρυθμίζει το βάρος της στήλης για responsive layout

                # Ορίζουμε τα χρώματα με fallback
                fg_color = self.theme.get("top_button_bg", "#4f4f4f")
                text_color = self.theme.get("top_button_text", "#ffffff")
                hover_color = self.theme.get("top_button_hover", "#6e6e6e")

                # Ειδικός χειρισμός για τα κουμπιά "2nd" και "Rad"
                if text in ["2nd", "Rad"]:
                    fg_color = self.theme.get("special_button_fg", "#eb7c16")
                    hover_color = self.theme.get("special_button_hover", "#f39c12")
                    text_color = self.theme.get("special_button_text",
                                                "#ffffff")  # Πρόσθεσα το text_color εδώ για αυτά τα κουμπιά

                btn = customtkinter.CTkButton(  # Δημιουργεί το κουμπί
                    self.top_buttons_frame,  # Το parent είναι το top_buttons_frame που δημιουργήσαμε παραπάνω
                    text=text,  # Το κείμενο του κουμπιού
                    height=40,  # Το ύψος του κουμπιού
                    font=("Arial", 12),  # Το font του κουμπιού
                    fg_color=fg_color,  # Χρώμα φόντου, με fallback
                    text_color=text_color,  # Χρώμα κειμένου, με fallback
                    hover_color=hover_color,  # Χρώμα hover, με fallback
                    command=lambda val=text: self.handle_special_buttons(val)
                    # Κλήση της συνάρτησης για χειρισμό ειδικών κουμπιών
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")  # Τοποθετεί το κουμπί στο grid layout
                row_objs.append(btn)  # Προσθέτει το κουμπί στη λίστα της σειράς
            self.top_buttons_frame.rowconfigure(r, weight=0)  # Ρυθμίζει το βάρος της σειράς για responsive layout
            self.top_button_objects.append(row_objs)  # Προσθέτει τη σειρά κουμπιών στη λίστα των κουμπιών

        # ----------- ΚΟΥΜΠΙΑ ΚΟΙΝΟΥ ΥΠΟΛΟΓΙΣΤΗ (STANDARD CALCULATOR) -----------
        # Οι βασικές αριθμητικές πράξεις (όπως το standard calculator)
        bottom_layout = [  # Διάταξη κουμπιών για το κάτω μέρος του υπολογιστή
            (0, 0, "7", 1, "num"), (0, 1, "8", 1, "num"), (0, 2, "9", 1, "num"),
            (0, 3, "C", 1, "c"), (0, 4, "AC", 1, "ac"),
            (1, 0, "4", 1, "num"), (1, 1, "5", 1, "num"), (1, 2, "6", 1, "num"),
            (1, 3, "x", 1, "op"), (1, 4, "÷", 1, "op"),
            (2, 0, "1", 1, "num"), (2, 1, "2", 1, "num"), (2, 2, "3", 1, "num"),
            (3, 0, "0", 1, "num"), (3, 1, ".", 1, "num"), (3, 2, "+/-", 1, "num"),
            (3, 3, "+", 1, "op"), (3, 4, "-", 1, "op"),
            (3, 3, "=", 2, "op") # Αυτό το "=" είναι διπλό, πρέπει να διορθωθεί
        ]
        # Διορθωμένο bottom_layout (αντικατέστησα το "=")
        bottom_layout = [  # Διάταξη κουμπιών για το κάτω μέρος του υπολογιστή
            (0, 0, "7", 1, "num"), (0, 1, "8", 1, "num"), (0, 2, "9", 1, "num"),
            (0, 3, "C", 1, "c"), (0, 4, "AC", 1, "ac"),
            (1, 0, "4", 1, "num"), (1, 1, "5", 1, "num"), (1, 2, "6", 1, "num"),
            (1, 3, "x", 1, "op"), (1, 4, "÷", 1, "op"),
            (2, 0, "1", 1, "num"), (2, 1, "2", 1, "num"), (2, 2, "3", 1, "num"),
            (2, 3, "+", 1, "op"), (2, 4, "-", 1, "op"),
            (3, 0, "0", 1, "num"), (3, 1, ".", 1, "num"), (3, 2, "+/-", 1, "num"),
            (3, 3, "=", 2, "op") # Το "=" πρέπει να είναι στη θέση (3,3) με columnspan 2
        ]


        self.numeric_buttons = []  # Λίστα για αποθήκευση αριθμητικών κουμπιών
        self.operation_buttons = []  # Λίστα για αποθήκευση λειτουργικών κουμπιών (π.χ. +, -, ×, ÷)
        self.ac_button = None  # Το κουμπί για "AC" (All Clear)
        self.c_button = None  # Το κουμπί για "C" (Clear)
        bottom_font = ("Arial", 30)  # Το font για τα κουμπιά του κάτω μέρους

        self.bottom_buttons_frame = customtkinter.CTkFrame(  # Το πλαίσιο για τα κουμπιά του κάτω μέρους
            self,  # Το parent είναι το CTkFrame που κληρονομεί αυτή η κλάση
            corner_radius=0,  # Γωνίες χωρίς καμπύλωση (για να ταιριάζει με το υπόλοιπο UI)
            fg_color=self.theme.get("bottom_frame_bg", "#222222"))  # Το χρώμα φόντου του bottom frame, με fallback
        self.bottom_buttons_frame.pack(fill="both", expand=True, padx=10,
                                       pady=(0, 10))  # Γεμίζει το πλάτος του parent frame, με padding

        for item in bottom_layout:  # Για κάθε κουμπί στη διάταξη του κάτω μέρους
            r, c, text, cspan, btype = item  # unpacking της διάταξης

            # Αρχικοποίηση χρωμάτων με βάση τον τύπο του κουμπιού
            fg_color = ""
            text_color = ""
            hover_color = ""

            if btype == "num":
                fg_color = self.theme.get("num_button_bg", "#a6a6a6")
                text_color = self.theme.get("num_button_text", "#ffffff")
                hover_color = self.theme.get("num_hover", "#b6b6b6")
            elif btype == "op":
                fg_color = self.theme.get("op_button_bg", "#7c7c7c")
                text_color = self.theme.get("op_button_text", "#ffffff")
                hover_color = self.theme.get("op_hover", "#8c8c8c")
            elif btype in ["ac", "c"]:  # Τα ac και c κουμπιά έχουν το ίδιο χρώμα φόντου και κειμένου
                fg_color = self.theme.get("ac_button_bg", "#eb7c16")
                text_color = self.theme.get("ac_button_text", "#ffffff")
                hover_color = self.theme.get("ac_hover", "#f39c12")
            else:  # Γενικό fallback αν ο τύπος δεν ταιριάζει
                fg_color = self.theme.get("top_button_bg", "#4f4f4f")
                text_color = self.theme.get("top_button_text", "#ffffff")
                hover_color = self.theme.get("hover_default", "#6e6e6e")

            btn = customtkinter.CTkButton(  # Δημιουργεί το κουμπί
                self.bottom_buttons_frame,  # Το parent είναι το bottom_buttons_frame που δημιουργήσαμε παραπάνω
                text=text,  # Το κείμενο του κουμπιού
                width=70,  # Το πλάτος του κουμπιού
                height=60,  # Το ύψος του κουμπιού
                font=bottom_font,  # Το font του κουμπιού
                fg_color=fg_color,  # Το χρώμα φόντου του κουμπιού, με fallback
                text_color=text_color,  # Το χρώμα κειμένου του κουμπιού, με fallback
                hover_color=hover_color,  # Το χρώμα hover του κουμπιού, με fallback
                command=lambda val=text: on_button_click(self, val)
                # Κλήση της συνάρτησης για χειρισμό πατήματος κουμπιού
            )
            btn.grid(row=r, column=c, columnspan=cspan, padx=3, pady=3,
                     sticky="nsew")  # Τοποθετεί το κουμπί στο grid layout
            if btype == "num":  # Αν είναι αριθμητικό κουμπί
                self.numeric_buttons.append(btn)  # Προσθέτει το κουμπί στη λίστα των αριθμητικών κουμπιών
            elif btype == "op":  # Αν είναι λειτουργικό κουμπί (π.χ. +, -, ×, ÷)
                self.operation_buttons.append(btn)  # Προσθέτει το κουμπί στη λίστα των λειτουργικών κουμπιών
            elif btype == "ac":  # Αν είναι το κουμπί "AC" (All Clear)
                self.ac_button = btn  # Αποθηκεύει το κουμπί για μελλοντική χρήση
            elif btype == "c":  # Αν είναι το κουμπί "C" (Clear)
                self.c_button = btn  # Αποθηκεύει το κουμπί για μελλοντική χρήση

        for i in range(4):  # Ρυθμίζει το βάρος των σειρών και στηλών στο grid layout του bottom_buttons_frame
            self.bottom_buttons_frame.rowconfigure(i, weight=1)  # Κάθε σειρά έχει βάρος 1 για responsive layout
        for j in range(5):  # Για κάθε στήλη στο grid layout του bottom_buttons_frame
            self.bottom_buttons_frame.columnconfigure(j, weight=1)  # Κάθε στήλη έχει βάρος 1 για responsive layout

    def get_display_value(self):  # Επιστρέφει την τρέχουσα τιμή του display
        return self.display_var.get()  # Χρησιμοποιεί την StringVar για να πάρει την τιμή

    def set_display_value(self, value):  # Ορίζει την τιμή του display
        max_len = 20  # Μέγιστος αριθμός χαρακτήρων για την οθόνη
        value_str = str(value)

        if len(value_str) > max_len:
            try:
                # Προσπάθεια μετατροπής σε εκθετική μορφή αν είναι αριθμός
                num_val = mpf(value_str)
                # Μορφοποίηση σε εκθετική μορφή, διασφαλίζοντας ότι χωράει στο max_len (περίπου)
                # Η ακρίβεια (max_len - 5 για "e+XX") μπορεί να προσαρμοστεί
                formatted_value = f"{num_val:.{max_len - 5}e}"
                if len(formatted_value) <= max_len:
                    self.display_var.set(formatted_value)
                else:
                    self.display_var.set("OVERFLOW")  # Αν ακόμα και η εκθετική μορφή είναι πολύ μεγάλη
            except (ValueError, TypeError, mp.libmp.libint.MPDecimalError):  # Πιο συγκεκριμένες εξαιρέσεις
                self.display_var.set("ERROR")  # Για μη-αριθμητικές ή μη αναγνωρίσιμες τιμές
            except Exception as e:  # Πιάνει οποιοδήποτε άλλο απρόβλεπτο σφάλμα κατά τη μορφοποίηση
                self.display_var.set("ERROR")
                print(f"Απροσδόκητο σφάλμα κατά τη μορφοποίηση της τιμής display: {e}")  # Καταγραφή για debugging
        else:
            self.display_var.set(value_str)

    def handle_key_input(self, key):  # Χειρισμός πληκτρολογίου για την αριθμομηχανή
        from keyboardInputHandler import handle_keyboard_input  # Εισάγει τη συνάρτηση χειρισμού πληκτρολογίου
        handle_keyboard_input(key, self)  # Καλέι τη συνάρτηση με το κλειδί και το αντικείμενο της αριθμομηχανής

    # -------------------------
    # ΕΦΑΡΜΟΓΗ ΘΕΜΑΤΟΣ
    # -------------------------
    def apply_theme(self, theme_dict):  # Εφαρμόζει το θέμα που παρέχεται ως λεξικό
        self.theme = theme_dict  # Αποθηκεύει το νέο θέμα στην ιδιότητα του αντικειμένου

        print(f"Applying theme to ScientificCalculator: {self.theme_mode}")
        print(f"Display BG for history/manual buttons: {theme_dict.get('display_bg', 'DEFAULT_DISPLAY_BG')}")
        print(f"Manual Button BG for history/manual buttons: {theme_dict.get('manual_button_bg', 'DEFAULT_MANUAL_BUTTON_BG')}")


        # Εφαρμογή χρωμάτων φόντου σε όλα τα βασικά widgets με fallback
        self.configure(fg_color=theme_dict.get("background", "#222222"))

        # Ελέγχουμε αν αυτά δεν είναι None πριν τα διαμορφώσουμε
        if self.display_container: self.display_container.configure(fg_color=theme_dict.get("display_bg", "#000000"))
        if self.top_buttons_frame: self.top_buttons_frame.configure(fg_color=theme_dict.get("top_frame_bg", "#222222"))
        if self.bottom_buttons_frame: self.bottom_buttons_frame.configure(
            fg_color=theme_dict.get("bottom_frame_bg", "#222222"))
        if self.top_display: self.top_display.configure(fg_color=theme_dict.get("display_bg", "#000000"))

        if self.display_entry:
            self.display_entry.configure(
                fg_color=theme_dict.get("display_bg", "#000000"),  # Χρώμα φόντου, με fallback
                text_color=theme_dict.get("display_text", "#00ff00")  # Χρώμα κειμένου, με fallback
            )
        if self.history_display:
            self.history_display.configure(
                fg_color=theme_dict.get("display_bg", "#000000"),  # Χρώμα φόντου, με fallback
                text_color=theme_dict.get("display_text", "#00ff00")  # Χρώμα κειμένου, με fallback
            )
        if self.middle_display:
            self.middle_display.configure(
                fg_color=theme_dict.get("display_bg", "#000000"),  # Χρώμα φόντου, με fallback
                text_color=theme_dict.get("display_text", "#00ff00")  # Χρώμα κειμένου, με fallback
            )
        if self.angle_mode_label:
            self.angle_mode_label.configure(
                fg_color=theme_dict.get("angle_mode_bg", "#000000"),  # Χρώμα φόντου του label, με fallback
                text_color=theme_dict.get("angle_mode_text", "#00ff00")
                # Χρώμα κειμένου για την ένδειξη Rad/Deg, με fallback
            )
        if self.manual_button:
            current_manual_fg = theme_dict.get("manual_button_bg", "#000000")
            current_manual_text = theme_dict.get("manual_button_text", "#eb7c16")
            current_manual_hover = theme_dict.get("hover_manual_button", "#000000")
            print(f"Manual button will be configured with fg={current_manual_fg}, text={current_manual_text}, hover={current_manual_hover}")
            self.manual_button.configure(
                fg_color=current_manual_fg,  # Χρώμα φόντου του κουμπιού manual, με fallback
                text_color=current_manual_text, # Χρώμα κειμένου του κουμπιού manual, με fallback
                hover_color=current_manual_hover # Χρώμα hover του κουμπιού manual, με fallback
            )
        if self.history_button:
            current_history_fg = theme_dict.get("manual_button_bg", "#000000")
            current_history_text = theme_dict.get("manual_button_text", "#eb7c16")
            current_history_hover = theme_dict.get("hover_manual_button", "#000000")
            print(f"History button will be configured with fg={current_history_fg}, text={current_history_text}, hover={current_history_hover}")
            self.history_button.configure(
                fg_color=current_history_fg,
                text_color=current_history_text,
                hover_color=current_history_hover
            )

        # Εφαρμογή χρωμάτων σε όλα τα top buttons
        for row in self.top_button_objects:
            for btn in row:
                btn_text = btn.cget("text")  # Παίρνουμε το τρέχον κείμενο του κουμπιού για ειδικούς ελέγχους

                # Ορίζουμε τα χρώματα με fallback
                fg_color = theme_dict.get("top_button_bg", "#4f4f4f")
                text_color = theme_dict.get("top_button_text", "#ffffff")
                hover_color = theme_dict.get("top_button_hover", "#6e6e6e")

                # Ειδικός χειρισμός για τα κουμπιά "2nd" και "Rad/Deg"
                if btn_text in ["2nd", "Rad", "Deg"]:  # Το Rad/Deg αλλάζει κείμενο, αλλά το χρώμα παραμένει special
                    fg_color = theme_dict.get("special_button_fg", "#eb7c16")
                    hover_color = theme_dict.get("special_button_hover", "#f39c12")
                    text_color = theme_dict.get("special_button_text",
                                                "#ffffff")  # Πρόσθεσα το text_color εδώ για αυτά τα κουμπιά

                btn.configure(
                    fg_color=fg_color,
                    text_color=text_color,
                    hover_color=hover_color
                )

        # Εφαρμογή χρωμάτων για τα αριθμητικά κουμπιά
        for btn in self.numeric_buttons:
            btn.configure(
                fg_color=theme_dict.get("num_button_bg", "#a6a6a6"),  # Χρώμα φόντου για αριθμητικά κουμπιά, με fallback
                text_color=theme_dict.get("num_button_text", "#ffffff"),
                # Χρώμα κειμένου για αριθμητικά κουμπιά, με fallback
                hover_color=theme_dict.get("num_hover", "#b6b6b6")  # Χρώμα hover για αριθμητικά κουμπιά, με fallback
            )
        # Εφαρμογή χρωμάτων για τα κουμπιά πράξεων
        for btn in self.operation_buttons:
            btn.configure(
                fg_color=theme_dict.get("op_button_bg", "#7c7c7c"),  # Χρώμα φόντου για κουμπιά πράξεων, με fallback
                text_color=theme_dict.get("op_button_text", "#ffffff"),
                # Χρώμα κειμένου για κουμπιά πράξεων, με fallback
                hover_color=theme_dict.get("op_hover", "#8c8c8c")  # Χρώμα hover για κουμπιά πράξεων, με fallback
            )
        # Εφαρμογή χρωμάτων για τα κουμπιά AC και C
        for button in [self.ac_button, self.c_button]:
            if button:  # Αυτός ο έλεγχος είναι σημαντικός καθώς μπορεί να είναι None πριν κληθεί η build_ui()
                button.configure(
                    fg_color=theme_dict.get("ac_button_bg", "#eb7c16"),  # Χρώμα φόντου, με fallback
                    text_color=theme_dict.get("ac_button_text", "#ffffff"),  # Χρώμα κειμένου, με fallback
                    hover_color=theme_dict.get("ac_hover", "#f39c12")  # Χρώμα hover, με fallback
                )

        if self.angle_mode_label:  # Έλεγχος πριν τη διαμόρφωση
            self.angle_mode_label.configure(
                fg_color=theme_dict.get("angle_mode_bg", "#000000"),
                # Το χρώμα φόντου του label για την ένδειξη Rad/Deg, με fallback
                text_color=theme_dict.get("angle_mode_text", "#00ff00"),
                # Το χρώμα του κειμένου στο label για την ένδειξη Rad/Deg, με fallback
                text=("Deg" if self.is_degree else "Rad")  # Ενημέρωση του κειμένου ανάλογα με την κατάσταση
            )
        # ΝΕΑ ΠΡΟΣΘΗΚΗ ΕΔΩ: Ενημέρωση του παραθύρου ιστορικού
        if self.history_handler:
            self.history_handler.apply_theme(theme_dict)

    # -------------------------
    # ΕΠΙΛΟΓΕΣ ΣΥΜΠΕΡΙΦΟΡΑΣ ΚΟΥΜΠΙΩΝ
    # -------------------------
    def handle_special_buttons(self, value):  # Χειρισμός ειδικών κουμπιών όπως 2nd, Rad/Deg, mc, m+, m-, mr
        if value == "2nd":  # Εναλλαγή λειτουργίας 2nd function
            self.toggle_second_function()  # Καλεί τη συνάρτηση για εναλλαγή της 2nd function
        elif value in ["Rad", "Deg"]:  # Εναλλαγή μεταξύ Rad και Deg
            self.toggle_angle_mode()  # Καλεί τη συνάρτηση για εναλλαγή της γωνιακής μονάδας
        else:
            on_button_click(self, value)  # Καλεί τη συνάρτηση χειρισμού πατήματος κουμπιού για τα υπόλοιπα κουμπιά

    def toggle_second_function(self):  # Εναλλάσσει την κατάσταση της 2nd function
        # Αλλάζει το label σε κουμπιά trig functions για να εμφανίσουν τα αντίστροφα
        self.is_second_function = not self.is_second_function  # Εναλλάσσει την κατάσταση της 2nd function
        for row_index, row in enumerate(self.top_button_objects):  # Για κάθε σειρά κουμπιών στην κορυφή
            for col_index, btn in enumerate(row):  # Για κάθε κουμπί στη σειρά
                text = btn.cget("text")  # Παίρνει το τρέχον κείμενο του κουμπιού

                # Ενημέρωση κειμένου κουμπιού
                if self.is_second_function and text in self.second_map:  # Αν είναι ενεργή η 2nd function και το κείμενο υπάρχει στο second_map
                    btn.configure(text=self.second_map[
                        text])  # Αν είναι ενεργή η 2nd function και το κουμπί είναι trig, άλλαξε το label σε αντίστροφο (π.χ. sin → sin⁻¹)
                elif not self.is_second_function and text in self.first_map:  # Αν απενεργοποιείται η 2nd function και το κουμπί είναι αντίστροφο trig
                    btn.configure(text=self.first_map[text])  # Επαναφορά του label στο αρχικό (π.χ. sin⁻¹ → sin)

                # Ενημέρωση χρωμάτων για τα "2nd" και "Rad/Deg" κουμπιά (αν και τα Rad/Deg αλλάζουν μέσω toggle_angle_mode)
                # Εδώ απλά εξασφαλίζουμε ότι τα χρώματα είναι σωστά για το "2nd" όταν αλλάζει η κατάσταση.
                if row_index == 0 and col_index == 0:  # Το κουμπί "2nd" είναι στο [0][0]
                    fg_color = self.theme.get("special_button_fg", "#eb7c16")
                    hover_color = self.theme.get("special_button_hover", "#f39c12")
                    text_color = self.theme.get("special_button_text", "#ffffff")
                    btn.configure(fg_color=fg_color, hover_color=hover_color, text_color=text_color)

    def toggle_angle_mode(self):  # Εναλλάσσει τη γωνιακή μονάδα μεταξύ Deg και Rad
        self.is_degree = not self.is_degree  # Αντιστρέφει την κατάσταση (True/False)
        new_mode = "Deg" if self.is_degree else "Rad"  # Επιλογή νέου label ανάλογα με την κατάσταση
        if self.top_button_objects and len(self.top_button_objects[0]) > 1:  # Εξασφάλιση ότι το κουμπί υπάρχει
            self.top_button_objects[0][1].configure(text=new_mode)

        if self.angle_mode_label:  # Έλεγχος πριν τη διαμόρφωση
            self.angle_mode_label.configure(
                text=new_mode,
                fg_color=self.theme.get("angle_mode_bg", "#000000"),
                text_color=self.theme.get("angle_mode_text", "#00ff00")
            )

    def set_theme_mode(self, theme_mode):  # Αλλάζει το theme mode (π.χ. dark/light)
        self.theme_mode = theme_mode  # Αποθηκεύει το νέο theme mode
        new_theme = get_theme(theme_mode)  # Παίρνει το λεξικό χρωμάτων για το νέο theme

        # Επαλήθευση ότι το new_theme είναι λεξικό πριν το εφαρμόσουμε
        if not isinstance(new_theme, dict):
            print(f"Προειδοποίηση: Αποτυχημένη φόρτωση θέματος '{theme_mode}'. Επιστροφή στο 'dark'.")
            new_theme = get_theme("dark")  # Επιστροφή στο dark αν το ζητούμενο theme είναι άκυρο
            if not isinstance(new_theme, dict):  # Έσχατη λύση αν και το dark αποτύχει
                new_theme = {}
                print("Κρίσιμη Προειδοποίηση: Αποτυχημένη φόρτωση ακόμα και του προκαθορισμένου θέματος 'dark'.")

        self.apply_theme(new_theme)  # Εφαρμόζει το νέο theme σε όλα τα widgets


    def insert_history_expression(self, entry):
        """
        Παίρνει ένα string του ιστορικού τύπου "3 + 2 = 5"
        και βάζει την έκφραση πριν το '=' στο display.
        """
        if "=" not in entry:
            return

        expression = entry.split("=")[0].strip()
        self.set_display_value(expression)  # Χωρίς καμία μετατροπή


# -------------------------
# ΔΗΜΙΟΥΡΓΙΑ ΥΠΟΛΟΓΙΣΤΗ (για χρήση από main app)
# -------------------------
def create_scientific_calculator(parent, mode="scientific", theme_mode="dark", sound_enabled=True):
    # Παίρνει το λεξικό χρωμάτων για το επιλεγμένο theme mode (π.χ. dark/light)
    theme = get_theme(theme_mode)
    # Επιστρέφει ένα νέο αντικείμενο ScientificCalculator με τα δοσμένα ορίσματα
    return ScientificCalculator(parent, mode=mode, theme=theme, sound_enabled=sound_enabled, theme_mode=theme_mode)


# Δοκιμή αυτόνομης λειτουργίας αυτού του αρχείου
if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("400x600")
    app.title("Δοκιμή Επιστημονικής Αριθμομηχανής")

    frame = ScientificCalculator(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()