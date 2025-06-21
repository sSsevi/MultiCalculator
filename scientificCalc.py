# scientificCalc.py
# ----------------------------------------------------------
# Αυτό το αρχείο υλοποιεί επιστημονική αριθμομηχανή
# με επιπλέον συναρτήσεις, υποστήριξη themes και εναλλαγή λειτουργιών
# Rad/Deg και 2nd function. Χρησιμοποιεί την customtkinter για τη γραφική διεπαφή.

"""
Εισαγωγή Απαραίτητων Βιβλιοθηκών και Ενοτήτων:
Αυτό το μπλοκ εισάγει όλες τις απαραίτητες βιβλιοθήκες και λειτουργίες
που χρειάζεται η επιστημονική αριθμομηχανή για να λειτουργήσει.
- `customtkinter`: Για τη δημιουργία του γραφικού περιβάλλοντος (GUI) με υποστήριξη θεμάτων.
- `themeManager.get_theme`: Για τη φόρτωση των χρωμάτων του επιλεγμένου θέματος.
- `buttonHandler.on_button_click`, `buttonHandler.play_click_sound`: Για τον χειρισμό των πατημάτων των κουμπιών και την αναπαραγωγή ήχων.
- `mpmath.mpf`: Για χειρισμό αριθμών με υψηλή ακρίβεια, ιδίως για επιστημονικές πράξεις.
- `manualHandler.show_manual_popup`: Για την εμφάνιση του παραθύρου βοήθειας/manual.
"""
import customtkinter  # Βασικό GUI toolkit με υποστήριξη themes και responsive widgets
from themeManager import get_theme  # Επιστρέφει λεξικό με χρώματα για κάθε theme (dark, light κλπ.)
from buttonHandler import on_button_click, play_click_sound  # Λογική χειρισμού πατημάτων κουμπιών
from mpmath import mpf  # Για αριθμητική ακρίβειας πολλών ψηφίων (π.χ. για πράξεις με π)
from manualHandler import show_manual_popup  # Εμφάνιση του manual popup

# ------------------------------------------------------
# ΚΛΑΣΗ: ScientificCalculator
# ------------------------------------------------------
class ScientificCalculator(customtkinter.CTkFrame):
    """
    Η κλάση αυτή ορίζει ένα "πλαίσιο" (CTkFrame) το οποίο περιέχει όλα τα στοιχεία ενός
    επιστημονικού υπολογιστή, δηλαδή:
    - display (πεδίο εμφάνισης)
    - σειρές κουμπιών με λειτουργίες (sin, log, AC, +, - κλπ.)
    - υποστήριξη εναλλαγής 2nd function και Rad/Deg
    Η χρήση customtkinter δίνει ευελιξία και μοντέρνο σχεδιασμό.
    """
    """
    Κατασκευαστής της κλάσης ScientificCalculator:
    Αυτή η μέθοδος αρχικοποιεί ένα νέο αντικείμενο ScientificCalculator.
    Θέτει τις αρχικές τιμές για όλες τις μεταβλητές κατάστασης της αριθμομηχανής,
    όπως το ενεργό θέμα, την κατάσταση του ήχου, την τιμή της οθόνης,
    την κατάσταση "2nd function" και τη μονάδα γωνίας (Deg/Rad).
    Επίσης, δημιουργεί τα λεξικά για την εναλλαγή των επιστημονικών συναρτήσεων.
    Τέλος, καλεί τις μεθόδους για τη δόμηση του GUI (`build_ui`)
    και την εφαρμογή του αρχικού θέματος (`apply_theme`).
    """
    def __init__(self, parent, mode="scientific", theme=None, sound_enabled=True):
        super().__init__(parent)

        # Αποθήκευση παραμέτρων και αρχικοποίηση βασικών μεταβλητών
        self.theme = theme or get_theme("dark")             # Αν δεν δοθεί theme, χρησιμοποιείται το "dark"
        self.theme_mode = "dark"                            # Παρακολούθηση του ενεργού theme
        self.sound_enabled = sound_enabled                  # Ενεργοποίηση ήχου για κουμπιά
        self.display_var = customtkinter.StringVar(value="0")   # Τιμή που εμφανίζεται στο display
        self.memory = mpf("0")                              # Αποθηκευμένη τιμή στη μνήμη (π.χ. για m+ ή m-)
        self.is_second_function = False                     # Κατάσταση "2nd function" για εναλλακτικά κουμπιά
        self.is_degree = True                               # Κατάσταση γωνιακής μονάδας (Deg ή Rad)
        self.just_evaluated = False                         # Σημαία για αποτροπή συνέχισης πράξης μετά το "="
        self.history_log = []                               # Αποθήκευση ιστορικού πράξεων
        self.history_window = None                          # Παράθυρο ιστορικού (αρχικά None)

        # Δύο λεξικά (maps) που καθορίζουν τα labels για 2nd function mode και το αντίστροφο
        self.second_map = {  # Αντικαθιστά τα κουμπιά με τις αντίστοιχες συναρτήσεις
            "sin": "sin⁻¹", "cos": "cos⁻¹", "tan": "tan⁻¹",
            "sinh": "sinh⁻¹", "cosh": "cosh⁻¹", "tanh": "tanh⁻¹"
        }
        self.first_map = {v: k for k, v in self.second_map.items()}  # Αντιστροφή: inverse → original

        # Δημιουργία interface και εφαρμογή theme
        self.build_ui()  # Δημιουργεί όλα τα κουμπιά, display κλπ.
        self.apply_theme(self.theme)  # Εφαρμόζει το αρχικό theme

    # ----------------------------------------------
    # UI SETUP
    # ----------------------------------------------
    """
    Μέθοδος Δόμησης του Γραφικού Περιβάλλοντος (UI):
    Αυτή η μέθοδος είναι υπεύθυνη για τη δημιουργία και τη διάταξη
    όλων των οπτικών στοιχείων της επιστημονικής αριθμομηχανής.
    Περιλαμβάνει τη ρύθμιση του κύριου frame, τη δημιουργία του display
    με τα κουμπιά manual και ιστορικού, την εμφάνιση του ιστορικού,
    το κύριο πεδίο αποτελεσμάτων, την ένδειξη Rad/Deg,
    και όλα τα κουμπιά (επιστημονικά και βασικά αριθμητικά/πράξεων)
    σε ένα responsive grid layout.
    """
    def build_ui(self):
        # Δημιουργία του γραφικού περιβάλλοντος του επιστημονικού υπολογιστή
        self.configure(width=400, height=600)  # Ορισμός διαστάσεων του frame

        # ----------------------- DISPLAY CONTAINER -----------------------
        """
        Δημιουργία του Display Container:
        Αυτό το μπλοκ δημιουργεί το πλαίσιο που θα περιέχει όλα τα στοιχεία της οθόνης
        της αριθμομηχανής, όπως το κύριο display, το ιστορικό και τα κουμπιά manual/history.
        Είναι το πάνω μέρος της αριθμομηχανής, υπεύθυνο για την εμφάνιση των εισόδων και αποτελεσμάτων.
        """
        self.display_container = customtkinter.CTkFrame(
            self,  # Το parent είναι το CTkFrame που κληρονομεί αυτή η κλάση
            fg_color=self.theme["display_bg"],  # Το χρώμα του display container
            corner_radius=0  # Γωνίες χωρίς καμπύλωση (για να ταιριάζει με το υπόλοιπο UI)
        )
        self.display_container.pack(fill="x", padx=0, pady=(0, 0))  # Γεμίζει το πλάτος του parent frame, χωρίς padding

        # Top display - περιέχει το manual button
        """
        Δημιουργία Top Display και Κουμπιών Manual/Ιστορικού:
        Αυτό το μπλοκ δημιουργεί ένα μικρότερο πλαίσιο στο πάνω μέρος του display_container.
        Περιέχει δύο ειδικά κουμπιά: ένα για την εμφάνιση του manual χρήσης (✍️)
        και ένα για την εμφάνιση του ιστορικού πράξεων (🕒).
        """
        self.top_display = customtkinter.CTkFrame(
            self.display_container,  # Το parent είναι το display_container
            height=30,  # Ύψος του top display
            fg_color=self.theme["display_bg"],  # Χρώμα φόντου
            corner_radius=0  # Γωνίες χωρίς καμπύλωση
        )
        self.top_display.pack(fill="x")  # Γεμίζει το πλάτος του display_container

        # Κουμπί για το manual popup
        """
        Δημιουργία Κουμπιού Manual:
        Αυτό το μπλοκ ορίζει το κουμπί που, όταν πατηθεί, θα εμφανίσει ένα αναδυόμενο παράθυρο
        με οδηγίες χρήσης της αριθμομηχανής (manual).
        """
        self.manual_button = customtkinter.CTkButton(
            self.top_display,  # Το parent είναι το top_display
            text="✍️",  # Emoji για το κουμπί manual
            width=30, height=30,  # Διαστάσεις κουμπιού
            font=("Arial", 18),  # Γραμματοσειρά
            fg_color=self.theme["manual_button_bg"],  # Χρώμα φόντου
            text_color=self.theme["manual_button_text"],  # Χρώμα κειμένου
            hover_color=self.theme["hover_manual_button"],  # Χρώμα hover
            command=lambda: show_manual_popup(self)  # Εμφάνιση του manual popup
        )
        self.manual_button.pack(side="left", padx=15)  # Τοποθέτηση στο αριστερό μέρος του top_display

        # Κουμπί για το ιστορικό πράξεων
        """
        Δημιουργία Κουμπιού Ιστορικού:
        Αυτό το μπλοκ ορίζει το κουμπί που, όταν πατηθεί, θα εμφανίσει ένα αναδυόμενο παράθυρο
        με το ιστορικό των τελευταίων πράξεων που έχουν εκτελεστεί στην αριθμομηχανή.
        """
        self.history_button = customtkinter.CTkButton(
            self.top_display,  # Το parent είναι το top_display
            text="🕒",  # Emoji για το κουμπί ιστορικού
            width=30, height=30,  # Διαστάσεις κουμπιού
            font=("Arial", 18),  # Γραμματοσειρά
            fg_color=self.theme["manual_button_bg"],  # Χρώμα φόντου
            text_color=self.theme["manual_button_text"],  # Χρώμα κειμένου
            hover_color=self.theme["hover_manual_button"],  # Χρώμα hover
            command=self.open_history_window  # Εμφάνιση του παραθύρου ιστορικού
        )
        self.history_button.pack(side="right", padx=15)  # Τοποθέτηση στο δεξί μέρος του top_display

        # Ενότητα Εμφάνισης Τρέχουσας Πράξης (history_display)
        """
        Ενότητα Εμφάνισης Τρέχουσας Πράξης (Πάνω Πλαίσιο Display):
        Αυτό το label χρησιμοποιείται για την εμφάνιση της **ολόκληρης της τρέχουσας αριθμητικής έκφρασης**
        που συνθέτει ο χρήστης (π.χ., "2 + 3 * 5").
        Λειτουργεί ως ένα "πλαίσιο προεπισκόπησης" της πράξης, δίνοντας στον χρήστη
        πλήρη οπτική αναπαράσταση της εισόδου του πριν την αξιολόγηση,
        ή μπορεί να χρησιμοποιηθεί για να δείξει την πράξη που οδήγησε σε ένα αποτέλεσμα στο κύριο display.
        """
        self.history_display_var = customtkinter.StringVar(value="")     # Μεταβλητή για το ιστορικό display
        self.history_display = customtkinter.CTkLabel(                   # Το label για την εμφάνιση του ιστορικού
            self.display_container,                                      # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            textvariable=self.history_display_var,                       # Χρησιμοποιούμε StringVar για δυναμική ενημέρωση
            height=20,                                                   # Το ύψος του label
            font=("Arial", 12),                                          # Το font του label
            anchor="e",                                                  # Ευθυγράμμιση του κειμένου στο δεξί μέρος
            fg_color=self.theme["display_bg"],                           # Το χρώμα του label για το ιστορικό
            text_color=self.theme["display_text"]                        # Το χρώμα του κειμένου στο label για το ιστορικό
        )
        self.history_display.pack(fill="x", padx=20)    # Γεμίζει το πλάτος του display_container, με padding 20px

        # Ενότητα Εμφάνισης Πληροφοριών / Σφαλμάτων (Middle Display)
        """
        Δημιουργία Ενότητας Εμφάνισης Πληροφοριών / Σφαλμάτων (Middle Display):
        Αυτή η ενότητα στο display λειτουργεί ως κέντρο μηνυμάτων προς τον χρήστη.
        Είναι εξαιρετικά χρήσιμη για:
        - Εμφάνιση μηνυμάτων σφάλματος (π.χ., "Syntax Error", "Math Error")
          όταν προκύπτουν προβλήματα κατά την εκτέλεση πράξεων.
        - Παροχή προτροπών ή ουσιαστικών πληροφοριών για τη σωστή χρήση
          συγκεκριμένων συναρτήσεων (π.χ., "Εισάγετε θετικό αριθμό για log").
        - Εμφάνιση προειδοποιήσεων ή άλλων ενημερωτικών μηνυμάτων που καθοδηγούν τον χρήστη.
        Αρχικά είναι κενή και ενημερώνεται δυναμικά από τη λογική του υπολογιστή.
        """
        self.middle_display = customtkinter.CTkLabel(      # Ένα label για μεσαία εμφάνιση, π.χ. για debug ή επιπλέον πληροφορίες
            self.display_container,                        # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            text="",                                       # Αρχικά κενό, μπορεί να χρησιμοποιηθεί για debug ή άλλες πληροφορίες
            height=24,                                     # Το ύψος του label
            font=("Arial", 14),                            # Το font του label
            anchor="e",                                    # Ευθυγράμμιση του κειμένου στο δεξί μέρος
            fg_color=self.theme["display_bg"],              # Το χρώμα του label για το μεσαίο display
            text_color=self.theme["display_text"]           # Το χρώμα του κειμένου στο label για το μεσαίο display
        )
        self.middle_display.pack(fill="x", padx=20)   # Γεμίζει το πλάτος του display_container, με padding 20px


        # Εμφάνιση αριθμών / αποτελεσμάτων
        """
        Δημιουργία Πεδίου Εμφάνισης Αποτελεσμάτων:
        Αυτό είναι το κύριο πεδίο εμφάνισης της αριθμομηχανής, όπου εμφανίζονται
        οι αριθμοί που εισάγονται και τα αποτελέσματα των πράξεων.
        Είναι ρυθμισμένο ως `readonly` για να μην μπορεί ο χρήστης να πληκτρολογεί απευθείας σε αυτό.
        """
        self.display_entry = customtkinter.CTkEntry(              # Το πεδίο εισαγωγής για αριθμούς και αποτελέσματα
            self.display_container,                               # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            textvariable=self.display_var,                        # Χρησιμοποιούμε StringVar για δυναμική ενημέρωση
            font=("Arial", 24),                                   # Το font του πεδίου εισαγωγής
            justify="right",                                      # Ευθυγράμμιση του κειμένου στα δεξιά (όπως σε αριθμομηχανές)
            state="readonly",                                     # Το πεδίο είναι μόνο για ανάγνωση (readonly) για να μην αλλάζει ο χρήστης
            height=60,                                            # Το ύψος του πεδίου εισαγωγής
            corner_radius=0,                                      # Γωνίες χωρίς καμπύλωση (για να ταιριάζει με το υπόλοιπο UI)
            border_width=0,                                       # Χωρίς περίγραμμα (border) για να φαίνεται πιο καθαρό
            fg_color=self.theme["display_bg"],                    # Το χρώμα του πεδίου εισαγωγής
            text_color=self.theme["display_text"]                 # Το χρώμα του κειμένου στο πεδίο εισαγωγής
        )
        # Τοποθετεί το πεδίο εισαγωγής στο display_container
        self.display_entry.pack(fill="x", padx=15, pady=(0, 0))


        # Ένδειξη Deg ή Rad – το βάζουμε έτσι κι αλλιώς (στο Standard απλά μένει κενό)
        """
        Δημιουργία Ένδειξης Γωνιακής Μονάδας (Deg/Rad):
        Αυτό το label εμφανίζει την τρέχουσα μονάδα μέτρησης γωνιών (μοίρες "Deg" ή ακτίνια "Rad").
        Είναι σημαντικό για τις τριγωνομετρικές συναρτήσεις της επιστημονικής αριθμομηχανής.
        """
        self.angle_mode_label = customtkinter.CTkLabel(      # Το label για την ένδειξη της γωνιακής μονάδας (Deg/Rad)
            self.display_container,                          # Το parent είναι το display_container που δημιουργήσαμε παραπάνω
            text=("Deg" if self.is_degree else "Rad"),       # Το κείμενο αλλάζει ανάλογα με την κατάσταση
            font=("Arial", 10),                              # Το font του label
            width=30,                                        # Το πλάτος του label
            height=16,                                       # Το ύψος του label
            fg_color=self.theme["display_bg"],                # Το χρώμα του label για την ένδειξη Rad/Deg
            text_color=self.theme["display_text"]             # Το χρώμα του κειμένου στο label για την ένδειξη Rad/Deg
        )
        self.angle_mode_label.pack(anchor="sw", padx=10, pady=(0, 4))       # Τοποθετεί το label στο κάτω αριστερό μέρος του display_container



        # ----------- ΕΠΙΣΤΗΜΟΝΙΚΑ ΚΟΥΜΠΙΑ -----------
        # Συναρτήσεις όπως sin, cos, log, factorial, π κλπ.
        """
        Δημιουργία Πλαισίου Επιστημονικών Κουμπιών:
        Αυτό το μπλοκ δημιουργεί ένα πλαίσιο που θα περιέχει όλα τα επιστημονικά κουμπιά
        (π.χ., sin, cos, log, π, x², 2nd). Τα κουμπιά αυτά οργανώνονται σε ένα grid layout.
        """
        self.top_buttons_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.theme["top_frame_bg"]) # Το χρώμα του top frame
        self.top_buttons_frame.pack(fill="both", expand=False, padx=10, pady=(6, 4))        # Γεμίζει το πλάτος του parent frame, με padding

        """
        Διάταξη Επιστημονικών Κουμπιών:
        Ορίζει τη διάταξη των επιστημονικών συναρτήσεων σε λίστες, όπου κάθε εσωτερική λίστα
        αντιπροσωπεύει μια σειρά κουμπιών. Στη συνέχεια, δημιουργεί δυναμικά τα CTkButton
        και τα τοποθετεί στο `top_buttons_frame` χρησιμοποιώντας grid layout.
        Κάθε κουμπί καλεί τη μέθοδο `handle_special_buttons` όταν πατηθεί.
        """
        top_buttons = [ # Κουμπιά για επιστημονικές συναρτήσεις
            ["2nd", "Rad", "Rand", "mc", "m+", "m-", "mr"],     
            ["x²", "x³", "1/x", "√", "ⁿ√x", "yˣ", "2ʸ"],    
            ["sin", "cos", "tan", "sinh", "cosh", "tanh", "π"],
            ["log₁₀", "log₂", "x!", "(", ")", "%", "EE"]
        ]

        self.top_button_objects = []                # Λίστα για αποθήκευση των κουμπιών του πάνω μέρους
        for r, row in enumerate(top_buttons):       # Για κάθε σειρά κουμπιών
            row_objs = []                           # Λίστα για αποθήκευση των κουμπιών της σειράς
            for c, text in enumerate(row):          # Για κάθε κουμπί στη σειρά
                self.top_buttons_frame.columnconfigure(c, weight=1) # Ρυθμίζει το βάρος της στήλης για responsive layout
                btn = customtkinter.CTkButton(      # Δημιουργεί το κουμπί
                    self.top_buttons_frame,         # Το parent είναι το top_buttons_frame που δημιουργήσαμε παραπάνω   
                    text=text,                      # Το κείμενο του κουμπιού
                    height=40,                      # Το ύψος του κουμπιού
                    font=("Arial", 12),             # Το font του κουμπιού
                    hover_color=self.theme["top_button_hover"],                 # Το χρώμα hover του κουμπιού
                    command=lambda val=text: self.handle_special_buttons(val)   # Κλήση της συνάρτησης για χειρισμό ειδικών κουμπιών
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")    # Τοποθετεί το κουμπί στο grid layout
                row_objs.append(btn)                            # Προσθέτει το κουμπί στη λίστα της σειράς
            self.top_buttons_frame.rowconfigure(r, weight=0)    # Ρυθμίζει το βάρος της σειράς για responsive layout
            self.top_button_objects.append(row_objs)            # Προσθέτει τη σειρά κουμπιών στη λίστα των κουμπιών


        # ----------- ΚΟΥΜΠΙΑ STANDARD ΥΠΟΛΟΓΙΣΤΗ -----------
        # Τα βασικά αριθμητικά πλήκτρα και τελεστές (όπως το standard calculator)
        """
        Δημιουργία Πλαισίου Κουμπιών Standard Λειρουργιών Αριθμομηχανής:
        Αυτό το μπλοκ δημιουργεί το κάτω πλαίσιο της αριθμομηχανής που περιέχει
        τα βασικά αριθμητικά πλήκτρα (0-9, .), τους τελεστές (+, -, x, ÷, =),
        και τα πλήκτρα "Clear" (C) και "All Clear" (AC).
        """
        bottom_layout = [   # Διάταξη κουμπιών για το κάτω μέρος του υπολογιστή
            # Row, Column, Κείμενο Κουμπιού, Column Span, Button Type
            (0, 0, "7", 1, "num"), (0, 1, "8", 1, "num"), (0, 2, "9", 1, "num"),  (0, 3, "C", 1, "c"),  (0, 4, "AC", 1, "ac"),
            (1, 0, "4", 1, "num"), (1, 1, "5", 1, "num"), (1, 2, "6", 1, "num"),  (1, 3, "x", 1, "op"), (1, 4, "÷", 1, "op"),
            (2, 0, "1", 1, "num"), (2, 1, "2", 1, "num"), (2, 2, "3", 1, "num"),  (2, 3, "+", 1, "op"), (2, 4, "-", 1, "op"),
            (3, 0, "0", 1, "num"), (3, 1, ".", 1, "num"), (3, 2, "+/-", 1, "num"), (3, 3, "=", 2, "op")
        ]

        self.numeric_buttons = []   # Λίστα για αποθήκευση αριθμητικών κουμπιών
        self.operation_buttons = [] # Λίστα για αποθήκευση λειτουργικών κουμπιών (π.χ. +, -, ×, ÷)
        self.ac_button = None       # Το κουμπί για "AC" (All Clear)
        self.c_button = None        # Το κουμπί για "C" (Clear)
        bottom_font = ("Arial", 30) # Το font για τα κουμπιά του κάτω μέρους

        self.bottom_buttons_frame = customtkinter.CTkFrame(     # Το πλαίσιο για τα κουμπιά του κάτω μέρους
            self,               # Το parent είναι το CTkFrame που κληρονομεί αυτή η κλάση
            corner_radius=0,    # Γωνίες χωρίς καμπύλωση (για να ταιριάζει με το υπόλοιπο UI)
            fg_color=self.theme["bottom_frame_bg"])  # Το χρώμα του bottom frame
        self.bottom_buttons_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))     # Γεμίζει το πλάτος του parent frame, με padding

        """
        Διάταξη Κουμπιών Standard λειτουργιών Αριθμομηχανής:
        Δημιουργεί δυναμικά τα `customtkinter.CTkButton` για τα αριθμητικά πλήκτρα
        και τους βασικούς τελεστές. Τα τοποθετεί στο `bottom_buttons_frame`
        χρησιμοποιώντας grid layout και αναθέτει σε κάθε κουμπί τη συνάρτηση
        `on_button_click` για το χειρισμό του πατήματος.
        """
        for item in bottom_layout:              # Για κάθε κουμπί στη διάταξη του κάτω μέρους
            r, c, text, cspan, btype = item     # unpacking της διάταξης
            hover = self.theme.get(f"{btype}_hover", self.theme["hover_default"])       # Το χρώμα hover για το κουμπί, αν δεν υπάρχει ορισμένο, παίρνει το default
            btn = customtkinter.CTkButton(      # Δημιουργεί το κουμπί
                self.bottom_buttons_frame,      # Το parent είναι το bottom_buttons_frame που δημιουργήσαμε παραπάνω
                text=text,                      # Το κείμενο του κουμπιού
                width=70,                       # Το πλάτος του κουμπιού
                height=60,                      # Το ύψος του κουμπιού
                font=bottom_font,               # Το font του κουμπιού
                hover_color=hover,              # Το χρώμα hover του κουμπιού
                command=lambda val=text: on_button_click(self, val) # Κλήση της συνάρτησης για χειρισμό πατήματος κουμπιού
            )
            btn.grid(row=r, column=c, columnspan=cspan, padx=3, pady=3, sticky="ew")    # Τοποθετεί το κουμπί στο grid layout
            if btype == "num":                      # Αν είναι αριθμητικό κουμπί
                self.numeric_buttons.append(btn)    # Προσθέτει το κουμπί στη λίστα των αριθμητικών κουμπιών
            elif btype == "op":                     # Αν είναι λειτουργικό κουμπί (π.χ. +, -, ×, ÷)
                self.operation_buttons.append(btn)  # Προσθέτει το κουμπί στη λίστα των λειτουργικών κουμπιών
            elif btype == "ac":                     # Αν είναι το κουμπί "AC" (All Clear)
                self.ac_button = btn                # Αποθηκεύει το κουμπί για μελλοντική χρήση
            elif btype == "c":                      # Αν είναι το κουμπί "C" (Clear)
                self.c_button = btn                 # Αποθηκεύει το κουμπί για μελλοντική χρήση

        """
        Ρύθμιση Responsive Layout για τα Κουμπιά:
        Αυτό το μπλοκ ρυθμίζει τα βάρη των γραμμών και των στηλών στο grid layout
        του `bottom_buttons_frame`. Αυτό εξασφαλίζει ότι τα κουμπιά θα
        προσαρμόζονται σωστά σε διαφορετικά μεγέθη παραθύρων, διατηρώντας
        την αναλογία τους.
        """
        for i in range(4):  # Ρυθμίζει το βάρος των σειρών και στηλών στο grid layout του bottom_buttons_frame
            self.bottom_buttons_frame.rowconfigure(i, weight=1)     # Κάθε σειρά έχει βάρος 1 για responsive layout
        for j in range(5):  # Για κάθε στήλη στο grid layout του bottom_buttons_frame
            self.bottom_buttons_frame.columnconfigure(j, weight=1)  # Κάθε στήλη έχει βάρος 1 για responsive layout

    """
    Μέθοδος `get_display_value`:
    Επιστρέφει την τρέχουσα τιμή που εμφανίζεται στο πεδίο εισαγωγής (display)
    της αριθμομηχανής.
    """
    def get_display_value(self):    # Επιστρέφει την τρέχουσα τιμή του display
        return self.display_var.get()           # Χρησιμοποιεί την StringVar για να πάρει την τιμή

    def set_display_value(self, value):   # Ορίζει την τιμή του display
        self.display_var.set(value)      # Χρησιμοποιεί την StringVar για να ορίσει την τιμή

    """
    Μέθοδος `handle_key_input`:
    Χειρίζεται τις εισόδους από το πληκτρολόγιο του χρήστη.
    Εισάγει τη σχετική συνάρτηση από το `keyboardInputHandler.py`
    και την καλεί για να επεξεργαστεί το πατημένο πλήκτρο.
    """
    def handle_key_input(self, key):    # Χειρισμός πληκτρολογίου για την αριθμομηχανή
        from keyboardInputHandler import handle_keyboard_input      # Εισάγει τη συνάρτηση χειρισμού πληκτρολογίου
        handle_keyboard_input(key, self)        # Καλεί τη συνάρτηση με το κλειδί και το αντικείμενο της αριθμομηχανής


    # --------------------------------------------------
    # ΕΦΑΡΜΟΓΗ ΘΕΜΑΤΟΣ
    # --------------------------------------------------
    """
    Μέθοδος `apply_theme`:
    Αυτή η μέθοδος είναι υπεύθυνη για την εφαρμογή των χρωμάτων
    του επιλεγμένου θέματος σε όλα τα οπτικά στοιχεία (widgets)
    της επιστημονικής αριθμομηχανής. Ενημερώνει τα χρώματα φόντου,
    κειμένου και hover για πλαίσια, displays και κουμπιά,
    εξασφαλίζοντας μια ομοιόμορφη εμφάνιση.
    """
    def apply_theme(self, theme_dict):  # Εφαρμόζει το θέμα που παρέχεται ως λεξικό
        self.theme = theme_dict     # Αποθηκεύει το νέο θέμα στην ιδιότητα του αντικειμένου

        """
        Εφαρμογή Θέματος στα Βασικά Πλαίσια και Displays:
        Αυτό το μπλοκ εφαρμόζει τα χρώματα του θέματος
        στα κύρια πλαίσια και στα πεδία εμφάνισης της αριθμομηχανής.
        """
        for widget in [self, self.display_container, self.top_buttons_frame, self.bottom_buttons_frame]:    # Εφαρμόζει το χρώμα φόντου σε όλα τα βασικά widgets
            widget.configure(fg_color=theme_dict["background"])         # Το χρώμα φόντου του widget

        self.display_container.configure(fg_color=theme_dict["display_bg"]) # Το χρώμα φόντου του display container
        self.top_display.configure(fg_color=theme_dict["display_bg"])   # Το χρώμα φόντου του top display
        self.display_entry.configure(       # Το πεδίο εισαγωγής για αριθμούς και αποτελέσματα
            fg_color=theme_dict["display_bg"],      # Το χρώμα φόντου του πεδίου εισαγωγής
            text_color=theme_dict["display_text"]       # Το χρώμα του κειμένου στο πεδίο εισαγωγής
        )
        self.history_display.configure(     # Το label για την εμφάνιση του ιστορικού
            fg_color=theme_dict["display_bg"],      # Το χρώμα φόντου του label για το ιστορικό
            text_color=theme_dict["display_text"]       # Το χρώμα του κειμένου στο label για το ιστορικό
        )
        self.middle_display.configure(      # Το label για μεσαία εμφάνιση, π.χ. για debug ή άλλες πληροφορίες
            fg_color=theme_dict["display_bg"],      # Το χρώμα φόντου του label για το μεσαίο display
            text_color=theme_dict["display_text"]       # Το χρώμα του κειμένου στο label για το μεσαίο display
        )
        # Ενημέρωση του label για την ένδειξη Rad/Deg με τα νέα χρώματα από το θέμα
        self.angle_mode_label.configure(
            fg_color=theme_dict["display_bg"],         # Το χρώμα φόντου του label (ίδιο με το display)
            text_color=theme_dict["angle_mode_text"]   # Το χρώμα του κειμένου για την ένδειξη Rad/Deg
        )
        # Ενημέρωση του κουμπιού manual με τα νέα χρώματα από το θέμα
        self.manual_button.configure(
            fg_color=theme_dict["manual_button_bg"],       # Το χρώμα φόντου του κουμπιού manual
            text_color=theme_dict["manual_button_text"],   # Το χρώμα του κειμένου του κουμπιού manual
            hover_color=theme_dict["hover_manual_button"]  # Το χρώμα hover του κουμπιού manual
        )

        """
        Εφαρμογή Θέματος στα Επιστημονικά Κουμπιά:
        Αυτό το μπλοκ εφαρμόζει τα χρώματα του θέματος
        στα κουμπιά που αντιστοιχούν σε επιστημονικές συναρτήσεις
        (π.χ., sin, cos, log, π).
        """
        for row in self.top_button_objects:
            for btn in row:
                btn.configure(fg_color=theme_dict["top_button_bg"],
                              text_color=theme_dict["top_button_text"],
                              hover_color=theme_dict["top_button_hover"])

        # Εφαρμογή ειδικών χρωμάτων για τα κουμπιά "2nd" και "Rad/Deg"
        """
        Εφαρμογή Ειδικών χρωμάτων στα Κουμπιά "2nd" και "Rad/Deg":
        Αυτά τα συγκεκριμένα κουμπιά έχουν ειδικά χρώματα για να ξεχωρίζουν,
        καθώς ελέγχουν την εναλλαγή λειτουργιών της αριθμομηχανής.
        """
        self.top_button_objects[0][0].configure(
            fg_color=theme_dict["special_button_fg"],      # Χρώμα φόντου για το κουμπί "2nd"
            hover_color=theme_dict["special_button_hover"],# Χρώμα hover για το κουμπί "2nd"
            text_color=self.theme["special_button_text"]   # Χρώμα κειμένου για το κουμπί "2nd"
        )
        self.top_button_objects[0][1].configure(
            fg_color=theme_dict["special_button_fg"],      # Χρώμα φόντου για το κουμπί "Rad/Deg"
            hover_color=theme_dict["special_button_hover"],# Χρώμα hover για το κουμπί "Rad/Deg"
            text_color=self.theme["special_button_text"]   # Χρώμα κειμένου για το κουμπί "Rad/Deg"
        )

        # Εφαρμογή χρωμάτων για τα αριθμητικά κουμπιά
        """
        Εφαρμογή Θέματος στα Αριθμητικά Κουμπιά και Κουμπιά Πράξεων:
        Αυτά τα μπλοκ εφαρμόζουν τα κατάλληλα χρώματα του θέματος
        στα αριθμητικά κουμπιά (0-9, .) και στα κουμπιά των βασικών πράξεων (+, -, x, ÷, =).
        """
        for btn in self.numeric_buttons:
            btn.configure(
            fg_color=theme_dict["num_button_bg"],      # Χρώμα φόντου για αριθμητικά κουμπιά
            text_color=theme_dict["num_button_text"],  # Χρώμα κειμένου για αριθμητικά κουμπιά
            hover_color=theme_dict["num_hover"]        # Χρώμα hover για αριθμητικά κουμπιά
            )
        # Εφαρμογή χρωμάτων για τα κουμπιά πράξεων
        for btn in self.operation_buttons:
            btn.configure(
            fg_color=theme_dict["op_button_bg"],       # Χρώμα φόντου για κουμπιά πράξεων
            text_color=theme_dict["op_button_text"],   # Χρώμα κειμένου για κουμπιά πράξεων
            hover_color=theme_dict["op_hover"]         # Χρώμα hover για κουμπιά πράξεων
            )

        # Εφαρμογή χρωμάτων για τα κουμπιά AC και C
        """
        Εφαρμογή Θεμάτων στα Κουμπιά "AC" (All Clear) και "C" (Clear):
        Αυτά τα ειδικά κουμπιά για εκκαθάριση του display/πράξης
        λαμβάνουν τα δικά τους χρώματα από το θέμα.
        """
        for button in [self.ac_button, self.c_button]:
            if button:
                button.configure(fg_color=theme_dict["ac_button_bg"],
                                 text_color=theme_dict["ac_button_text"],
                                 hover_color=theme_dict["ac_hover"])

        """
        Τελική Ενημέρωση Ένδειξης Rad/Deg:
        Εξασφαλίζει ότι το label που δείχνει τη μονάδα γωνίας (Deg/Rad)
        έχει ενημερωμένα χρώματα και σωστό κείμενο μετά την εφαρμογή του θέματος.
        """
        self.angle_mode_label.configure(
            fg_color=theme_dict["angle_mode_bg"],       # Το χρώμα του label για την ένδειξη Rad/Deg
            text_color=theme_dict["angle_mode_text"],   # Το χρώμα του κειμένου στο label για την ένδειξη Rad/Deg
            text=("Deg" if self.is_degree else "Rad")   # Ενημέρωση του κειμένου ανάλογα με την κατάσταση
        )


    # --------------------------------------------------
    # ΕΠΙΛΟΓΕΣ ΣΥΜΠΕΡΙΦΟΡΑΣ ΚΟΥΜΠΙΩΝ
    # --------------------------------------------------
    """
    Μέθοδος `handle_special_buttons`:
    Αυτή η μέθοδος είναι ο κεντρικός χειριστής για τα πατήματα
    των ειδικών επιστημονικών κουμπιών (π.χ. "2nd", "Rad", "mc", "m+", κλπ.).
    Αναπαράγει έναν ήχο κλικ και στη συνέχεια κατευθύνει την ενέργεια
    στην κατάλληλη υπο-μέθοδο ανάλογα με την τιμή του κουμπιού.
    """
    def handle_special_buttons(self, value):    # Χειρισμός ειδικών κουμπιών όπως 2nd, Rad/Deg, mc, m+, m-, mr
        play_click_sound(self)
        if value == "2nd":                      # Εναλλαγή λειτουργίας 2nd function
            self.toggle_second_function()       # Καλεί τη συνάρτηση για εναλλαγή της 2nd function
        elif value in ["Rad", "Deg"]:           # Εναλλαγή μεταξύ Rad και Deg
            self.toggle_angle_mode()            # Καλεί τη συνάρτηση για εναλλαγή της γωνιακής μονάδας
        else:
            on_button_click(self, value)        # Καλεί τη συνάρτηση χειρισμού πατήματος κουμπιού για τα υπόλοιπα κουμπιά

    """
    Μέθοδος `toggle_second_function`:
    Εναλλάσσει την κατάσταση "2nd function" της αριθμομηχανής.
    Όταν ενεργοποιείται, αλλάζει τα labels ορισμένων τριγωνομετρικών
    κουμπιών ώστε να εμφανίζουν τις αντίστροφες συναρτήσεις τους (π.χ., sin → sin⁻¹).
    """
    def toggle_second_function(self):       # Εναλλάσσει την κατάσταση της 2nd function
        # Αλλάζει το label σε κουμπιά trig functions για να εμφανίσουν τα αντίστροφα
        self.is_second_function = not self.is_second_function   # Εναλλάσσει την κατάσταση της 2nd function
        for row in self.top_button_objects: # Για κάθε σειρά κουμπιών στην κορυφή
            for btn in row: # Για κάθε κουμπί στη σειρά
                text = btn.cget("text") # Παίρνει το τρέχον κείμενο του κουμπιού
                if self.is_second_function and text in self.second_map: # Αν είναι ενεργή η 2nd function και το κείμενο υπάρχει στο second_map
                    btn.configure(text=self.second_map[text])  # Αν είναι ενεργή η 2nd function και το κουμπί είναι trig, άλλαξε το label σε αντίστροφο (π.χ. sin → sin⁻¹)
                elif not self.is_second_function and text in self.first_map:  # Αν απενεργοποιείται η 2nd function και το κουμπί είναι αντίστροφο trig
                    btn.configure(text=self.first_map[text])  # Επαναφορά του label στο αρχικό (π.χ. sin⁻¹ → sin)

    """
    Μέθοδος `toggle_angle_mode`:
    Εναλλάσσει τη γωνιακή μονάδα μέτρησης μεταξύ Μοιρών (Deg) και Ακτινίων (Rad).
    Ενημερώνει το κείμενο του σχετικού κουμπιού και του label ένδειξης γωνίας.
    """
    def toggle_angle_mode(self):  # Εναλλάσσει τη γωνιακή μονάδα μεταξύ Deg και Rad
        self.is_degree = not self.is_degree  # Αντιστρέφει την κατάσταση (True/False)
        new_mode = "Deg" if self.is_degree else "Rad"  # Επιλογή νέου label ανάλογα με την κατάσταση
        self.top_button_objects[0][1].configure(text=new_mode)  # Ενημέρωση του κουμπιού Rad/Deg
        self.angle_mode_label.configure(text=new_mode)  # Ενημέρωση του label Rad/Deg

    """
    Μέθοδος `set_theme_mode`:
    Αλλάζει το ενεργό θέμα εμφάνισης της αριθμομηχανής (π.χ., από "dark" σε "light").
    Φορτώνει το νέο λεξικό χρωμάτων για το επιλεγμένο θέμα και καλεί την
    `apply_theme` για να ενημερώσει ολόκληρο το GUI.
    """
    def set_theme_mode(self, theme_mode):  # Αλλάζει το theme mode (π.χ. dark/light)
        self.theme_mode = theme_mode  # Αποθηκεύει το νέο theme mode
        new_theme = get_theme(theme_mode)  # Παίρνει το λεξικό χρωμάτων για το νέο theme
        self.apply_theme(new_theme)  # Εφαρμόζει το νέο theme σε όλα τα widgets

    """
    Μέθοδος `open_history_window`:
    Ανοίγει ή κλείνει ένα αναδυόμενο παράθυρο που εμφανίζει το ιστορικό
    των πράξεων της αριθμομηχανής. Αν το παράθυρο είναι ήδη ανοιχτό, το κλείνει.
    Αν δεν υπάρχει ιστορικό, δεν ανοίγει τίποτα.
    Δημιουργεί ένα `CTkScrollableFrame` για να φιλοξενήσει τα entries του ιστορικού.
    """
    def open_history_window(self):
        # Αν το παράθυρο ιστορικού υπάρχει ήδη και είναι ανοιχτό, κλείσ' το
        if self.history_window is not None and self.history_window.winfo_exists():
            self.history_window.destroy()  # Καταστροφή του παραθύρου ιστορικού
            self.history_window = None     # Μηδενισμός της μεταβλητής
            return                        # Τερματισμός της συνάρτησης

        # Αν δεν υπάρχει καθόλου ιστορικό, μην ανοίξεις τίποτα
        if not self.history_log:
            return  # Μην ανοίξεις τίποτα αν δεν έχει ιστορικό

        # Δημιουργία νέου παραθύρου (Toplevel) για το ιστορικό
        self.history_window = customtkinter.CTkToplevel(self)
        self.history_window.title("History")  # Τίτλος παραθύρου

        # Υπολογισμός θέσης για το popup παράθυρο
        parent_x = self.winfo_rootx()         # Συντεταγμένη x του parent
        parent_y = self.winfo_rooty()         # Συντεταγμένη y του parent
        popup_width = 300                     # Πλάτος popup
        popup_height = 300                    # Ύψος popup
        parent_width = self.winfo_width()     # Πλάτος parent
        popup_x = parent_x - 6                # Θέση x του popup
        popup_y = parent_y - 70               # Θέση y του popup
        self.history_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")  # Ορισμός γεωμετρίας

        self.history_window.attributes("-topmost", True)  # Το παράθυρο να είναι πάντα μπροστά
        self.history_window.configure(fg_color=self.theme["background"])  # Χρώμα φόντου

        # Scrollable frame για το ιστορικό
        scroll_frame = customtkinter.CTkScrollableFrame(self.history_window)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)  # Τοποθέτηση με padding

        # Για κάθε entry στο ιστορικό (μέχρι 50 τελευταία)
        for entry in reversed(self.history_log[-50:]):  # δείξε τα τελευταία 50
            btn = customtkinter.CTkButton(
                scroll_frame,                    # Parent: το scrollable frame
                text=entry,                      # Το κείμενο του κουμπιού είναι το entry
                anchor="w",                      # Ευθυγράμμιση αριστερά
                height=30,                       # Ύψος κουμπιού
                font=("Arial", 12),              # Font
                fg_color=self.theme["top_button_bg"],      # Χρώμα φόντου
                hover_color=self.theme["top_button_hover"],# Χρώμα hover
                text_color=self.theme["top_button_text"],  # Χρώμα κειμένου
                command=lambda e=entry: self.insert_history_expression(e)  # Ενέργεια όταν πατηθεί
            )
            btn.pack(fill="x", pady=2)           # Τοποθέτηση στο frame

    """
    Μέθοδος `insert_history_expression`:
    Εισάγει μια επιλεγμένη έκφραση από το ιστορικό πίσω στο κύριο display της αριθμομηχανής.
    Καθαρίζει την έκφραση από το αποτέλεσμα και αντικαθιστά τα σύμβολα πολλαπλασιασμού/διαίρεσης
    σε μορφή που μπορεί να επεξεργαστεί ο υπολογιστής.
    """
    def insert_history_expression(self, entry):
        # Παίρνει το expression πριν το '=' και το βάζει στο display
        expr = entry.split('=')[0].strip().replace("×", "*").replace("÷", "/")  # Καθαρισμός και αντικατάσταση συμβόλων
        self.display_var.set(expr)  # Εμφάνιση στο display


# --------------------------------------------------
# ΔΗΜΙΟΥΡΓΙΑ CALCULATOR (για χρήση από main app)
# --------------------------------------------------
"""
Συνάρτηση `create_scientific_calculator`:
Αυτή η συνάρτηση λειτουργεί ως "εργοστάσιο" (factory function)
για τη δημιουργία ενός αντικειμένου ScientificCalculator.
Χρησιμοποιείται από την κύρια εφαρμογή (`mainCalc.py`)
για να δημιουργήσει στιγμιότυπα της επιστημονικής αριθμομηχανής
με συγκεκριμένες ρυθμίσεις (parent, mode, theme, sound_enabled).
"""
def create_scientific_calculator(parent, mode="scientific", theme_mode="dark", sound_enabled=True):
    # Παίρνει το λεξικό χρωμάτων για το επιλεγμένο theme mode (π.χ. dark/light)
    theme = get_theme(theme_mode)
    # Επιστρέφει ένα νέο αντικείμενο ScientificCalculator με τα δοσμένα ορίσματα
    return ScientificCalculator(parent, mode=mode, theme=theme, sound_enabled=sound_enabled)


# Δοκιμή standalone λειτουργίας αυτού του αρχείου
"""
Κύρια Εκτέλεση (Standalone Test):
Αυτό το μπλοκ κώδικα εκτελείται μόνο όταν το αρχείο `scientificCalc.py`
τρέχει απευθείας (όχι όταν εισάγεται ως module σε άλλο αρχείο).
Δημιουργεί ένα απλό customtkinter παράθυρο και ένα στιγμιότυπο της
ScientificCalculator για δοκιμαστικούς σκοπούς, επιτρέποντας την
αυτόνομη λειτουργία και τον έλεγχο της επιστημονικής αριθμομηχανής.
"""
if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("400x600")
    app.title("Scientific Calculator Test")

    frame = ScientificCalculator(app)
    frame.pack(fill="both", expand=True)

    app.mainloop()