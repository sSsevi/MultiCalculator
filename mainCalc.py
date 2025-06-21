# mainCalc.py
# ==========================================================
# Αυτό το αρχείο υλοποιεί την κύρια εφαρμογή αριθμομηχανής.
# Παρέχει γραφικό περιβάλλον χρήστη (GUI) χρησιμοποιώντας τη βιβλιοθήκη customtkinter.
# Υποστηρίζει διάφορες λειτουργίες (modes) όπως Standard, Scientific, Programmer κ.λπ.
# Περιλαμβάνει δυνατότητες όπως:
# - Εναλλαγή μεταξύ διαφορετικών λειτουργιών (modes).
# - Εναλλαγή θεμάτων εμφάνισης (themes).
# - Πλαϊνό μενού (sidebar) με animation.
# - Ενεργοποίηση/Απενεργοποίηση ήχου.
# - Υποστήριξη πατήματος πλήκτρων από τον χρήστη.
# - Δυναμική φόρτωση εικόνων και εικονιδίων.
# ==========================================================

#==================== ΕΙΣΑΓΩΓΕΣ ====================
""""""
"""
Εισαγωγή των απαραίτητων βιβλιοθηκών και modules για τη λειτουργία της εφαρμογής:
- customtkinter: Βασική βιβλιοθήκη για τη δημιουργία του GUI με μοντέρνα εμφάνιση.
- PIL (Pillow) - Image: Χρησιμοποιείται για το χειρισμό και τη φόρτωση εικόνων (π.χ., .png)
  για τα εικονίδια των κουμπιών.
- standardCalc (StandardCalculator): Το module που περιέχει την κλάση για την προεπιλεγμένη
  λειτουργία (mode) της αριθμομηχανής.
- themeManager (get_theme): Module για τη διαχείριση και την ανάκτηση των χρωμάτων
  και ρυθμίσεων των διαφόρων θεμάτων εμφάνισης.
- customtkinter.CTkLabel: Ειδική εισαγωγή για την κλάση CTkLabel (αν και θα μπορούσε να
  χρησιμοποιηθεί και μέσω customtkinter.CTkLabel).
- frameManager (frame_data): Module που περιέχει δεδομένα για τα διαθέσιμα modes/frames
  της αριθμομηχανής (π.χ., Standard, Scientific, Programmer), συμπεριλαμβανομένων
  των κλάσεων τους και των διαδρομών για τα εικονίδιά τους.
- os: Module που παρέχει έναν τρόπο αλληλεπίδρασης με το λειτουργικό σύστημα,
  χρησιμοποιείται εδώ κυρίως για τον έλεγχο ύπαρξης αρχείων εικόνας.
"""
import customtkinter  # Βιβλιοθήκη για μοντέρνο GUI
from PIL import Image  # Χρήση εικόνων για εικονίδια
from standardCalc import StandardCalculator  # Το default mode της αριθμομηχανής
from themeManager import get_theme  # Διαχείριση θεμάτων εμφάνισης
from customtkinter import CTkLabel  # Ετικέτες για το GUI
from frameManager import frame_data  # Διαθέσιμα modes/frames για την αριθμομηχανή
import os  # Χρήση για έλεγχο ύπαρξης αρχείων

#==================== ΑΡΧΙΚΕΣ ΡΥΘΜΙΣΕΙΣ ====================
"""
Αρχικές καθολικές ρυθμίσεις της εφαρμογής:
- customtkinter.set_appearance_mode("dark"): Ορίζει το αρχικό θέμα εμφάνισης (dark mode)
  για όλα τα widgets του CustomTkinter. Αυτό πρέπει να γίνει πριν τη δημιουργία του κύριου παραθύρου.
- sound_enabled_global: Μια καθολική μεταβλητή Boolean που ελέγχει αν ο ήχος είναι ενεργοποιημένος ή απενεργοποιημένος.
  Η τιμή 'True' σημαίνει ότι ο ήχος είναι αρχικά ενεργοποιημένος.
"""
customtkinter.set_appearance_mode("dark")   # Ορίζουμε το dark mode ως αρχικό
sound_enabled_global = True                 # Μεταβλητή για ενεργοποίηση/απενεργοποίηση ήχου

# Συνάρτηση που επιστρέφει την κατάσταση του ήχου
"""
Συνάρτηση get_sound_state():
Αυτή η βοηθητική συνάρτηση παρέχει την τρέχουσα κατάσταση της καθολικής μεταβλητής 'sound_enabled_global'.
Επιτρέπει σε άλλα μέρη του κώδικα ή σε άλλα modules να ελέγξουν αν ο ήχος είναι ενεργός χωρίς να
έχουν άμεση πρόσβαση στην καθολική μεταβλητή ή στην κλάση της εφαρμογής.
"""
def get_sound_state():                      
    return sound_enabled_global             # Επιστρέφει την τρέχουσα κατάσταση του ήχου

#==================== ΚΛΑΣΗ MainCalculatorApp ====================

class MainCalculatorApp(customtkinter.CTk):     # Κύρια κλάση της εφαρμογής αριθμομηχανής
    def __init__(self):                         # Constructor της κλάσης
        """
        Constructor της κλάσης MainCalculatorApp.
        Πραγματοποιεί την αρχική ρύθμιση και δημιουργία όλων των στοιχείων του GUI
        και των μεταβλητών κατάστασης της εφαρμογής.
        """
        """
        def __init__(self): Αρχικοποιεί το κύριο παράθυρο της εφαρμογής υπολογιστή με τις ακόλουθες λειτουργίες:
        - Ορίζει τις διαστάσεις του παραθύρου και συνδέει handlers για πληκτρολόγιο και click εκτός μενού.
        - Αρχικοποιεί μεταβλητές κατάστασης για τον ήχο, το θέμα, το mode, το πλαϊνό μενού και το display.
        - Φορτώνει εικόνες για τα κουμπιά (ήχος, μενού, κλείσιμο, bullet) με έλεγχο ύπαρξης αρχείων.
        - Δημιουργεί την πάνω μπάρα με κουμπί μενού, ετικέτα mode και κουμπί ήχου.
        - Δημιουργεί το πλαϊνό μενού (sidebar) και το εσωτερικό του frame.
        - Προσθέτει ενότητα επιλογής mode με κουμπιά για κάθε διαθέσιμο mode και τα αντίστοιχα εικονίδια.
        - Προσθέτει ενότητα επιλογής θέματος με κουμπιά για κάθε διαθέσιμο θέμα.
        - Ορίζει το αρχικό frame του υπολογιστή και εφαρμόζει το default θέμα και mode με καθυστέρηση.
        - Ετοιμάζει τις δομές για την ενημέρωση θεμάτων και μενού.
        """
        super().__init__()                      # Κλήση του constructor της CTk


        #==================== ΡΥΘΜΙΣΕΙΣ ΠΑΡΑΘΥΡΟΥ ====================
        """
        Ρύθμιση του κύριου παραθύρου της εφαρμογής:
        - self.geometry("400x600"): Ορίζει τις αρχικές διαστάσεις του παραθύρου σε 400 pixels πλάτος
          και 600 pixels ύψος.
        - self.bind_all("<Key>", self.on_key_press): Συνδέει τη συνάρτηση 'on_key_press' για να χειρίζεται
          κάθε πάτημα πλήκτρου στο πληκτρολόγιο, ανεξάρτητα από το ποιο widget έχει το focus.
        - self.bind("<Button-1>", self.on_click_outside_menu): Συνδέει τη συνάρτηση 'on_click_outside_menu'
          για να χειρίζεται κάθε αριστερό κλικ του ποντικιού ('Button-1') στο παράθυρο. Αυτό χρησιμοποιείται
          για να κλείνει το πλαϊνό μενού αν ο χρήστης κάνει κλικ εκτός αυτού.
        """
        self.geometry("400x600")                                # Ορισμός διαστάσεων παραθύρου
        self.bind_all("<Key>", self.on_key_press)               # Χειρισμός πατήματος πλήκτρων
        self.bind("<Button-1>", self.on_click_outside_menu)     # Χειρισμός click εκτός μενού

        #==================== ΚΑΤΑΣΤΑΣΕΙΣ ΕΦΑΡΜΟΓΗΣ ====================
        """
        Αρχικοποίηση των μεταβλητών κατάστασης που παρακολουθούν την τρέχουσα λειτουργία της εφαρμογής:
        - self.sound_enabled: Η κατάσταση του ήχου (True/False), αρχικοποιείται από την καθολική μεταβλητή.
        - self.theme_mode: Η τρέχουσα επιλογή θέματος εμφάνισης (π.χ., "dark", "light").
        - self.current_mode: Το τρέχον επιλεγμένο mode της αριθμομηχανής (π.χ., "standard", "scientific").
        - self.sidebar_open: Κατάσταση του πλαϊνού μενού (True αν ανοιχτό, False αν κλειστό).
        - self.sidebar_x: Η τρέχουσα X συντεταγμένη του πλαϊνού μενού, χρησιμοποιείται για το animation.
          Αρχίζει στο -200 (εκτός οθόνης).
        - self.display_value: Η τιμή που εμφανίζεται αυτή τη στιγμή στο πεδίο αποτελέσματος του υπολογιστή.
          Χρησιμοποιείται για να διατηρεί την τιμή όταν αλλάζουν modes.
        - self.theme_buttons: Λεξικό που θα αποθηκεύει αναφορές στα κουμπιά επιλογής θέματος για εύκολη πρόσβαση.
        - self.mode_buttons: Λεξικό που θα αποθηκεύει αναφορές στα κουμπιά επιλογής mode.
        - self.mode_icons: Λεξικό που θα αποθηκεύει αναφορές στα εικονίδια των modes.
        """
        global sound_enabled_global
        self.sound_enabled   = sound_enabled_global   # Κατάσταση ήχου
        self.theme_mode      = "dark"                 # Αρχικό θέμα εμφάνισης
        self.current_mode    = "standard"             # Αρχικό mode
        self.sidebar_open    = False                  # Κατάσταση πλαϊνού μενού (κλειστό)
        self.sidebar_x       = -200                   # Αρχική θέση πλαϊνού μενού
        self.display_value   = ""                     # Τιμή που εμφανίζεται στο display
        self.theme_buttons   = {}                     # Λεξικό για τα κουμπιά θεμάτων
        self.mode_buttons    = {}                     # Λεξικό για τα κουμπιά modes
        self.mode_icons      = {}                     # Λεξικό για τα εικονίδια modes

        #==================== ΦΟΡΤΩΣΗ ΕΙΚΟΝΩΝ ====================
        """
        Φόρτωση εικόνων που χρησιμοποιούνται ως εικονίδια σε διάφορα κουμπιά της εφαρμογής.
        Για κάθε εικόνα:
        - Καθορίζεται η διαδρομή προς το αρχείο εικόνας.
        - Γίνεται έλεγχος με 'os.path.exists()' για να διασφαλιστεί ότι το αρχείο υπάρχει.
          Αυτό αποτρέπει σφάλματα αν μια εικόνα λείπει.
        - Αν το αρχείο βρεθεί, δημιουργείται ένα αντικείμενο customtkinter.CTkImage,
          που υποστηρίζει τόσο φωτεινή όσο και σκοτεινή λειτουργία (αν και εδώ χρησιμοποιείται μόνο 'light_image')
          και ορίζεται το μέγεθος της εικόνας.
        - Αν το αρχείο δεν βρεθεί, τυπώνεται μια προειδοποίηση στην κονσόλα και η μεταβλητή ορίζεται σε 'None'
          ή ένα placeholder μπορεί να χρησιμοποιηθεί αργότερα.
        """
        # Φόρτωση εικόνας για το εικονίδιο ενεργού ήχου (sound_on)
        sound_on_path = "images/sound_on.png"                     # Ορίζει τη διαδρομή προς το αρχείο εικόνας 'sound_on.png'
        if os.path.exists(sound_on_path):                         # Ελέγχει αν το αρχείο εικόνας υπάρχει στην καθορισμένη διαδρομή
            # Αν υπάρχει, δημιουργεί ένα αντικείμενο CTkImage για χρήση στο GUI
            self.sound_on_img = customtkinter.CTkImage(           
                light_image=Image.open(sound_on_path),            # Ανοίγει το αρχείο εικόνας χρησιμοποιώντας τη βιβλιοθήκη PIL (Pillow)
                size=(24, 24)                                     # Ορίζει το επιθυμητό μέγεθος της εικόνας σε 24x24 pixels
            )
        else:
            # Αν το αρχείο εικόνας δεν βρεθεί, εκτυπώνει ένα προειδοποιητικό μήνυμα στην κονσόλα
            print(f"Warning: Image file '{sound_on_path}' not found.")
            self.sound_on_img = None                              # Ορίζει την ιδιότητα σε None, υποδεικνύοντας ότι η εικόνα δεν φορτώθηκε

        # Φόρτωση εικόνας για το εικονίδιο απενεργοποιημένου ήχου (sound_off)
        sound_off_path = "images/sound_off.png"
        if os.path.exists(sound_off_path):                  # Ελέγχει αν το αρχείο στη διαδρομή sound_off_path υπάρχει στο σύστημα αρχείων
            self.sound_off_img = customtkinter.CTkImage(    # Αν υπάρχει, δημιουργεί ένα αντικείμενο εικόνας CTkImage και το αποθηκεύει ως ιδιότητα της κλάσης
                light_image=Image.open(sound_off_path),     # Ανοίγει το αρχείο εικόνας από το sound_off_path και το περνάει ως παράμετρο στο CTkImage
                size=(24, 24)                               # Ορίζει το μέγεθος της εικόνας στα 24x24 pixels
            )
        else:
            print(f"Warning: Image file '{sound_off_path}' not found.")     # Εμφανίζει προειδοποίηση αν δεν βρέθηκε το αρχείο εικόνας για το sound_off
            self.sound_off_img = None                       # Θέτει την εικόνα sound_off σε None (placeholder)
        
        # Φόρτωση εικόνας για το εικονίδιο του μενου (menu_icon)
        menu_icon_path = "images/menu_icon.png"             # Ορίζει το path για το εικονίδιο του μενού
        if os.path.exists(menu_icon_path):                  # Ελέγχει αν το αρχείο στη διαδρομή menu_icon_path υπάρχει στο σύστημα αρχείων
            self.menu_icon_img = customtkinter.CTkImage(    # Αν υπάρχει, δημιουργεί ένα αντικείμενο εικόνας CTkImage και το αποθηκεύει ως ιδιότητα της κλάσης
                light_image=Image.open(menu_icon_path),     # Ανοίγει το αρχείο εικόνας από το menu_icon_path και το περνάει ως παράμετρο στο CTkImage
                size=(24, 24))                              # Ορίζει το μέγεθος της εικόνας στα 24x24 pixels
        else:
            print(f"Warning: Image file '{menu_icon_path}' not found.")     # Εμφανίζει προειδοποίηση αν δεν βρέθηκε το αρχείο εικόνας για το menu_icon
            self.menu_icon_img = None                       # Θέτει την εικόνα menu_icon σε None (placeholder)

        # Φόρτωση εικόνας για το εικονίδιο κλεισίματος μενού(close_icon)
        close_icon_path = "images/close_icon.png"              # Ορίζει το path για το εικονίδιο κλεισίματος
        if os.path.exists(close_icon_path):                    # Ελέγχει αν το αρχείο στη διαδρομή close_icon_path υπάρχει στο σύστημα αρχείων
            self.close_icon = customtkinter.CTkImage(          # Αν υπάρχει, δημιουργεί ένα αντικείμενο εικόνας CTkImage και το αποθηκεύει ως ιδιότητα της κλάσης
                light_image=Image.open(close_icon_path),       # Ανοίγει το αρχείο εικόνας από το close_icon_path και το περνάει ως παράμετρο στο CTkImage
                size=(24, 24))                                 # Ορίζει το μέγεθος της εικόνας στα 24x24 pixels
        else:
            print(f"Warning: Image file '{close_icon_path}' not found.")    # Εμφανίζει προειδοποίηση αν δεν βρέθηκε το αρχείο εικόνας για το close_icon
            self.close_icon = None                             # Θέτει την εικόνα close_icon σε None (placeholder)

        # Φόρτωση εικόνας για το εικονίδιο "bullet" (bullet_icon)
        bullet_icon_path = "images/bullet.png"                 # Ορίζει το path για το εικονίδιο "bullet"
        if os.path.exists(bullet_icon_path):                   # Ελέγχει αν το αρχείο στη διαδρομή bullet_icon_path υπάρχει στο σύστημα αρχείων
            self.bullet_icon = customtkinter.CTkImage(         # Αν υπάρχει, δημιουργεί ένα αντικείμενο εικόνας CTkImage και το αποθηκεύει ως ιδιότητα της κλάσης
                light_image=Image.open(bullet_icon_path),      # Ανοίγει το αρχείο εικόνας από το bullet_icon_path και το περνάει ως παράμετρο στο CTkImage
                size=(14, 14))                                 # Ορίζει το μέγεθος της εικόνας στα 14x14 pixels
        else:
            print(f"Warning: Image file '{bullet_icon_path}' not found.")   # Εμφανίζει προειδοποίηση αν δεν βρέθηκε το αρχείο εικόνας για το bullet_icon
            self.bullet_icon = None                            # Θέτει την εικόνα bullet_icon σε None (placeholder)


        #==================== ΔΗΜΙΟΥΡΓΙΑ ΠΑΝΩ ΜΠΑΡΑΣ ====================
        """
        Δημιουργία του 'top_bar_frame':
        - Ένα customtkinter.CTkFrame που λειτουργεί ως η πάνω μπάρα της εφαρμογής.
        - Έχει σταθερό ύψος 40 pixels και μηδενική στρογγυλοποίηση γωνιών.
        - 'pack(fill="x")': Τοποθετεί το frame στο πάνω μέρος του παραθύρου και το κάνει να γεμίζει
          όλο το διαθέσιμο οριζόντιο χώρο.
        """
        self.top_bar_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0)   # Δημιουργία του frame της πάνω μπάρας (top bar)
        self.top_bar_frame.pack(fill="x")   # Γεμίζει οριζόντια το πάνω μέρος του παραθύρου


        # Κουμπί εμφάνισης/απόκρυψης πλαϊνού μενού
        """
        Δημιουργία του 'menu_button':
        - Κουμπί για το άνοιγμα/κλείσιμο του πλαϊνού μενού.
        - Τοποθετείται στο 'top_bar_frame'.
        - Είναι ένα κουμπί χωρίς κείμενο, με εικόνα ('menu_icon_img').
        - Έχει σταθερές διαστάσεις (40x40).
        - 'command=self.toggle_menu': Καθορίζει τη μέθοδο που θα καλεστεί όταν πατηθεί το κουμπί.
        - 'fg_color': Το χρώμα φόντου του κουμπιού, που λαμβάνεται δυναμικά από το θέμα.
        - 'corner_radius': Στρογγυλοποίηση γωνιών του κουμπιού.
        - 'pack(side="left", padx=5)': Τοποθετεί το κουμπί αριστερά μέσα στην πάνω μπάρα με οριζόντιο περιθώριο 5 pixels.
        """
        self.menu_button = customtkinter.CTkButton(     # Δημιουργία κουμπιού για το πλαϊνό μενού
            self.top_bar_frame,                         # Τοποθέτηση στην πάνω μπάρα
            text="",                                    # Χωρίς κείμενο (μόνο εικόνα)
            width=40,                                   # Πλάτος κουμπιού
            height=40,                                  # Ύψος κουμπιού
            image=self.menu_icon_img,                   # Εικόνα εικονιδίου μενού
            command=self.toggle_menu,                   # Συνάρτηση που καλείται όταν πατηθεί το κουμπί
            fg_color=get_theme(self.theme_mode)["top_frame_bg"],    # Χρώμα φόντου κουμπιού (ανάλογα με το θέμα)
            corner_radius=6)                            # Στρογγυλοποίηση γωνιών κουμπιού
        self.menu_button.pack(side="left", padx=5)      # Τοποθέτηση αριστερά στην πάνω μπάρα με εσωτερικό περιθώριο

        # Εμφάνιση του τρέχοντος mode
        """
        Δημιουργία του 'mode_label_display':
        - Ετικέτα που εμφανίζει το όνομα του τρέχοντος mode της αριθμομηχανής (π.χ., "Standard Calculator").
        - Τοποθετείται στο 'top_bar_frame'.
        - Ορίζονται η γραμματοσειρά και το χρώμα κειμένου, που λαμβάνεται από το θέμα.
        - 'pack(side="left", padx=10)': Τοποθετείται αριστερά, δίπλα στο κουμπί μενού, με περιθώριο.
        """
        self.mode_label_display = customtkinter.CTkLabel(   # Δημιουργία ετικέτας για εμφάνιση του τρέχοντος mode στην πάνω μπάρα
            self.top_bar_frame,                             # Τοποθέτηση της ετικέτας στην πάνω μπάρα
            text="Standard Calculator",                     # Αρχικό κείμενο: "Standard Calculator"
            font=("Arial", 16),                             # Γραμματοσειρά Arial, μέγεθος 16
            text_color=get_theme(self.theme_mode)["menu_text_color"]  # Χρώμα κειμένου ανάλογα με το θέμα
        )
        self.mode_label_display.pack(side="left", padx=10)  # Τοποθέτηση αριστερά στην πάνω μπάρα με οριζόντιο περιθώριο 10 pixels

        # Κουμπί ήχου
        """
        Δημιουργία του 'sound_button':
        - Κουμπί για την ενεργοποίηση/απενεργοποίηση του ήχου.
        - Λειτουργεί παρόμοια με το 'menu_button', αλλά με διαφορετική εικόνα.
        - 'command=self.toggle_sound': Καθορίζει τη μέθοδο που θα καλεστεί όταν πατηθεί.
        - 'pack(side="right", padx=5)': Τοποθετείται δεξιά μέσα στην πάνω μπάρα.
        """
        self.sound_button = customtkinter.CTkButton(                # Δημιουργία κουμπιού για ενεργοποίηση/απενεργοποίηση ήχου
            self.top_bar_frame,                                     # Τοποθέτηση στην πάνω μπάρα
            image=self.sound_on_img,                                # Εικόνα εικονιδίου ήχου (ενεργό)
            text="",                                                # Χωρίς κείμενο (μόνο εικόνα)
            width=40,                                               # Πλάτος κουμπιού
            height=40,                                              # Ύψος κουμπιού
            command=self.toggle_sound,                              # Συνάρτηση που καλείται όταν πατηθεί το κουμπί (εναλλαγή ήχου)
            fg_color=get_theme(self.theme_mode)["top_frame_bg"]     # Το χρώμα φόντου του κουμπιού που ανοίγει/κλείνει το μενού
        )
        
        self.sound_button.pack(side="right", padx=5)

        #==================== ΠΛΑΪΝΟ ΜΕΝΟΥ ====================
        """
        Δημιουργία του 'sidebar_frame':
        - Το κύριο frame του πλαϊνού μενού, το οποίο αρχικά είναι κρυμμένο εκτός οθόνης.
        - Έχει σταθερό πλάτος (200 pixels) και ύψος (560 pixels).
        - 'corner_radius=0': Μηδενική στρογγυλοποίηση γωνιών.
        - 'fg_color': Το χρώμα φόντου του πλαϊνού μενού, λαμβάνεται από το θέμα.
        - 'pack_propagate(False)': Αποτρέπει το frame να αλλάξει μέγεθος βάσει των περιεχομένων του.
        - 'place(x=-200, y=40)': Τοποθετεί το sidebar frame αρχικά εκτός οθόνης (x=-200) και
          κάτω από την πάνω μπάρα (y=40).
          """
        self.sidebar_frame = customtkinter.CTkFrame(            # Δημιουργία του πλαϊνού frame (sidebar) για το μενού
            self,                                               # Γονικό widget: το κύριο παράθυρο της εφαρμογής
            width=200,                                          # Πλάτος πλαϊνού μενού: 200 pixels
            height=560,                                         # Ύψος πλαϊνού μενού: 560 pixels
            corner_radius=0,                                    # Μηδενική στρογγυλοποίηση γωνιών (ορθογώνιο)
            fg_color=get_theme(self.theme_mode)["top_frame_bg"] # Χρώμα φόντου πλαϊνού μενού (ίδιο με το top_frame)
        )
        
        self.sidebar_frame.pack_propagate(False)   # Αποτρέπει το frame να αλλάξει μέγεθος βάσει των περιεχομένων του
        self.sidebar_frame.place(x=-200, y=40)     # Τοποθετεί το sidebar αρχικά εκτός οθόνης (x=-200), κάτω από την πάνω μπάρα (y=40)

        # Δημιουργία εσωτερικού frame για το πλαϊνό μενού
        """        
        Δημιουργία του 'menu_inner_frame':
        - Ένα εσωτερικό frame μέσα στο 'sidebar_frame' που περιέχει τα πραγματικά στοιχεία του μενού (modes, themes).
        - 'pack(fill="both", expand=True, padx=10, pady=10)': Το γεμίζει ολόκληρο το 'sidebar_frame' με
          εσωτερικά περιθώρια. Χρήσιμο για να δώσει γενικά περιθώρια στα στοιχεία του μενού 
          αλλά και για να παραλάβει scrollbar αν τυχόν χρειαζόταν (δεν χρειάστηκε)"""
        self.menu_inner_frame = customtkinter.CTkFrame(   # Δημιουργεί ένα frame μέσα στο sidebar για τα περιεχόμενα του μενού
            self.sidebar_frame,                           # Γονικό widget: το πλαϊνό μενού (sidebar_frame)
            corner_radius=0                               # Μηδενική στρογγυλοποίηση γωνιών (ορθογώνιο πλαίσιο)
        )
        self.menu_inner_frame.pack(                       # Τοποθετεί το εσωτερικό frame στο sidebar
            fill="both",                                  # Το κάνει να γεμίζει οριζόντια και κάθετα όλο το sidebar
            expand=True,                                  # Επιτρέπει στο frame να επεκτείνεται αν αλλάξει μέγεθος το sidebar
            padx=10,                                      # Εσωτερικό οριζόντιο περιθώριο 10 pixels
            pady=10                                       # Εσωτερικό κάθετο περιθώριο 10 pixels
        )

        #==================== ΕΝΟΤΗΤΑ Mode ====================
        """
        Δημιουργία της ετικέτας "Mode":
        - Ετικέτα τίτλου για την ενότητα επιλογής mode μέσα στο πλαϊνό μενού.
        - 'pack(anchor="w", pady=(5, 2))': Τοποθετείται αριστερά ('w' για West) με πάνω/κάτω padding. 
        """
        self.section_label = customtkinter.CTkLabel(    # Δημιουργεί μια ετικέτα (Label) για τον τίτλο της ενότητας "Mode"
            self.menu_inner_frame,                      # Τοποθετεί την ετικέτα μέσα στο εσωτερικό frame του μενού
            text="Mode",                                # Το κείμενο της ετικέτας είναι "Mode"
            font=("Arial", 14, "bold")                  # Ορίζει τη γραμματοσειρά σε Arial, μέγεθος 14, έντονη (bold)
        )
        self.section_label.pack(                        # Τοποθετεί την ετικέτα στο frame
            anchor="w",                                 # Στοίχιση αριστερά (west)
            pady=(5, 2)                                 # Κάθετο περιθώριο: 5 πάνω, 2 κάτω
        )

        # Κουμπιά για εναλλαγή μεταξύ διαφορετικών λειτουργιών (frames)
        """
        Δημιουργία κουμπιών για κάθε mode:
        - Γίνεται επανάληψη σε όλα τα διαθέσιμα modes που ορίζονται στο 'frame_data'.
        - Για κάθε mode:
          - Φορτώνεται το αντίστοιχο εικονίδιο, με έλεγχο ύπαρξης αρχείου και προειδοποίηση αν λείπει.
          - Δημιουργείται ένα customtkinter.CTkButton:
            - Το κείμενο του κουμπιού είναι το όνομα του mode με κεφαλαίο το πρώτο γράμμα ('mode.title()').
            - Περιλαμβάνει το εικονίδιο ('image=icon') και το κείμενο τοποθετείται αριστερά ('anchor="w"').
            - 'compound="left"': Το εικονίδιο εμφανίζεται αριστερά του κειμένου.
            - 'command=lambda m=mode: self.set_mode_button(m)': Χρησιμοποιείται 'lambda' για να περάσει
              το όνομα του mode ως όρισμα στη μέθοδο 'set_mode_button' όταν πατηθεί το κουμπί.
            - Τα χρώματα φόντου και κειμένου λαμβάνονται δυναμικά από το θέμα.
          - Κάθε κουμπί αποθηκεύεται στο λεξικό 'self.mode_buttons' με κλειδί το όνομα του mode.
          """
        for mode, data in frame_data.items():               # Επανάληψη για κάθε διαθέσιμο mode και τα δεδομένα του από το frame_data
            icon_path = data.get("icon_path", "")           # Παίρνει το path του εικονιδίου για το συγκεκριμένο mode (αν υπάρχει)
            if os.path.exists(icon_path):                   # Ελέγχει αν το αρχείο εικόνας υπάρχει στο σύστημα αρχείων
                icon = customtkinter.CTkImage(              # Αν υπάρχει, δημιουργεί αντικείμενο εικόνας CTkImage
                    light_image=Image.open(icon_path),      # Ανοίγει το αρχείο εικόνας με τη βιβλιοθήκη PIL (Pillow)
                    size=(20, 20)                           # Ορίζει το μέγεθος της εικόνας στα 20x20 pixels
                )
            else:
                print(f"Warning: Icon file '{icon_path}' not found for mode '{mode}'.") # Αν δεν υπάρχει το αρχείο τυπώνεται μήνυμα στη κονσόλα
                icon = None                                 # Η θέση της εικόνας μένει κενή χωρίς να επηρεάζει τη λειτουργία της εφαρμογής
            self.mode_icons[mode] = icon                    # Αποθηκεύει το εικονίδιο για το mode στο λεξικό self.mode_icons

            btn = customtkinter.CTkButton(                 # Δημιουργεί ένα κουμπί CTkButton για το mode
                self.menu_inner_frame,                     # Τοποθετεί το κουμπί στο εσωτερικό frame του μενού
                text=mode.title(),                         # Το κείμενο του κουμπιού είναι το όνομα του mode με κεφαλαίο το πρώτο γράμμα
                corner_radius=6,                           # Ορίζει στρογγυλοποίηση γωνιών του κουμπιού
                image=icon,                                # Το εικονίδιο του κουμπιού (αν υπάρχει)
                anchor="w",                                # Στοίχιση περιεχομένου αριστερά (west)
                compound="left",                           # Το εικονίδιο εμφανίζεται αριστερά από το κείμενο
                command=lambda m=mode: self.set_mode_button(m),  # Χρησιμοποιείται 'lambda' για να περάσει το όνομα του mode ως όρισμα στη μέθοδο 'set_mode_button' όταν πατηθεί το κουμπί.
                fg_color=get_theme(self.theme_mode)["top_button_bg"],       # Το χρώμα φόντου του κουμπιού (ανάλογα με το θέμα)
                text_color=get_theme(self.theme_mode)["menu_text_color"]    # Το χρώμα του κειμένου του κουμπιού (ανάλογα με το θέμα)
            )
            btn.pack(pady=2, padx=2, anchor="w", fill="x")  # Τοποθετεί το κουμπί mode στο μενού, γεμίζοντας οριζόντια (fill="x")
            self.mode_buttons[mode] = btn # Κάθε κουμπί αποθηκεύεται στο λεξικό 'self.mode_buttons' με κλειδί το όνομα του mode.

        #==================== ΕΝΟΤΗΤΑ Theme ====================
        """
        Δημιουργία της ετικέτας "Theme":
        - Ετικέτα τίτλου για την ενότητα επιλογής θέματος μέσα στο πλαϊνό μενού.
        - 'pack(anchor="w", pady=(10, 2))': Τοποθετείται αριστερά με πάνω/κάτω padding.
        """
        # Δημιουργία ετικέτας "Theme" για την ενότητα επιλογής θέματος στο πλαϊνό μενού
        self.theme_label = customtkinter.CTkLabel(           # Δημιουργεί μια ετικέτα (Label) για τον τίτλο της ενότητας "Theme"
            self.menu_inner_frame,                           # Τοποθετεί την ετικέτα μέσα στο εσωτερικό frame του μενού
            text="Theme",                                    # Το κείμενο της ετικέτας είναι "Theme"
            font=("Arial", 14, "bold")                       # Ορίζει τη γραμματοσειρά σε Arial, μέγεθος 14, έντονη (bold)
        )
        self.theme_label.pack(                               # Τοποθετεί την ετικέτα στο frame
            anchor="w",                                      # Στοίχιση αριστερά (west)
            pady=(10, 2)                                     # Κάθετο περιθώριο: 10 πάνω, 2 κάτω

        )

        # Κουμπιά επιλογής θέματος εμφάνισης
        """
                Δημιουργία κουμπιών για κάθε θέμα:
        - Γίνεται επανάληψη σε μια προκαθορισμένη λίστα ονομάτων θεμάτων.
        - Για κάθε θέμα:
          - Δημιουργείται ένα customtkinter.CTkButton.
          - Το κείμενο του κουμπιού είναι το όνομα του θέματος με κεφαλαίο το πρώτο γράμμα.
          - Περιλαμβάνει ένα εικονίδιο 'bullet_icon' για οπτική έμφαση.
          - 'compound="left"', 'anchor="w"': Τοποθέτηση εικονιδίου αριστερά, κειμένου αριστερά.
          - 'command=lambda t=theme: self.set_theme_button(t)': Χρησιμοποιείται 'lambda' για να περάσει
            το όνομα του θέματος ως όρισμα στη μέθοδο 'set_theme_button' όταν πατηθεί.
          - Τα χρώματα του κουμπιού (εκτός από το 'fg_color' που θα οριστεί αργότερα)
            θα ενημερωθούν από τη μέθοδο 'set_theme_button'.
          - Κάθε κουμπί αποθηκεύεται στο λεξικό 'self.theme_buttons'.
          """
        for theme in ["dark", "light", "purple", "oceanic", "goth", "mondrian", "rainbow", "windows95", "excel2003"]:  # Επανάληψη για κάθε διαθέσιμο θέμα
            btn = customtkinter.CTkButton(                      # Δημιουργία κουμπιού CTkButton για το θέμα
            self.menu_inner_frame,                              # Τοποθέτηση του κουμπιού στο εσωτερικό frame του μενού
            text=theme.capitalize(),                            # Κείμενο κουμπιού: το όνομα του θέματος με κεφαλαίο το πρώτο γράμμα
            corner_radius=6,                                    # Στρογγυλοποίηση γωνιών κουμπιού
            image=self.bullet_icon,                             # Εικονίδιο αριστερά (bullet)
            compound="left",                                    # Το εικονίδιο εμφανίζεται αριστερά από το κείμενο
            anchor="w",                                         # Στοίχιση περιεχομένου αριστερά (west)
            width=180,                                          # Πλάτος κουμπιού
            height=28,                                          # Ύψος κουμπιού
            font=("Arial", 12),                                 # Γραμματοσειρά Arial, μέγεθος 12
            command=lambda t=theme: self.set_theme_button(t)    # Συνάρτηση που καλείται όταν πατηθεί το κουμπί (αλλάζει θέμα)
            #Χρησιμοποιείται 'lambda' για να περάσει το όνομα του θέματος ως όρισμα στη μέθοδο 'set_theme_button' όταν πατηθεί.
            )
            btn.pack(pady=2, padx=2, anchor="w")   # Τοποθέτηση κουμπιού με κάθετο και οριζόντιο περιθώριο, αριστερή στοίχιση
            self.theme_buttons[theme] = btn        # Αποθήκευση του κουμπιού στο λεξικό self.theme_buttons με κλειδί το όνομα του θέματος
                
            


        #==================== ΕΚΚΙΝΗΣΗ DEFAULT FRAME ====================
        """
        Αρχικοποίηση και φόρτωση του προεπιλεγμένου frame της αριθμομηχανής:
        - self.calculator_frame = None: Αρχικά, δεν υπάρχει ενεργό frame αριθμομηχανής.
        - self.after(100, self.show_calculator_frame): Καθυστέρηση 100ms πριν καλέσει τη μέθοδο
          'show_calculator_frame'. Αυτό δίνει χρόνο στο GUI να αρχικοποιηθεί πλήρως πριν φορτωθεί
          το πρώτο calculator frame.
        - self.after(150, lambda: self.set_theme_button(self.theme_mode)): Καθυστέρηση 150ms για
          να εφαρμοστεί το αρχικό θέμα εμφάνισης. Αυτό ενημερώνει όλα τα χρώματα των widgets
          σύμφωνα με το 'self.theme_mode'.
        - self.after(200, lambda: self.set_mode_button(self.current_mode)): Καθυστέρηση 200ms για
          να εφαρμοστεί το αρχικό mode εμφάνισης. Αυτό ενεργοποιεί το σωστό κουμπί mode στο μενού.
        """
        self.calculator_frame = None    # Αρχικοποίηση: placeholder για το ενεργό frame αριθμομηχανής
                                        # Το πραγματικό frame θα φορτωθεί λίγο μετά μέσω της show_calculator_frame
        self.after(100, self.show_calculator_frame)                         # Προγραμματίζει την εμφάνιση του αρχικού calculator frame μετά από 100ms (για να ολοκληρωθεί το GUI)
        self.after(150, lambda: self.set_theme_button(self.theme_mode))     # Εφαρμόζει το αρχικό θέμα εμφάνισης μετά από 150ms (ενημερώνει τα χρώματα των widgets)
        self.after(200, lambda: self.set_mode_button(self.current_mode))    # Ενεργοποιεί το αρχικό mode (π.χ. Standard) μετά από 200ms (ενημερώνει το κουμπί mode)


        #==================== ΕΝΗΜΕΡΩΣΗ ΘΕΜΑΤΟΣ ΚΑΙ ΜΕΝΟΥ ====================

        # Ανανέωση κουμπιών επιλογής θέματος και modes με το τρέχον θέμα
    """
    Μέθοδος set_theme_button(self, theme):
    Εφαρμόζει το επιλεγμένο θέμα στην εφαρμογή και ενημερώνει την οπτική κατάσταση
    όλων των σχετικών widgets στο πλαϊνό μενού και την πάνω μπάρα.
    """
    def set_theme_button(self, theme):  # Ορισμός του επιλεγμένου θέματος
        """
        Καλεί τη μέθοδο 'switch_theme' για να αλλάξει το ενεργό θέμα της εφαρμογής,
        κάτι που θα επηρεάσει και το calculator frame.
        """
        self.switch_theme(theme)        # Εφαρμογή του νέου θέματος στην εφαρμογή


        # Ανανέωση κουμπιών επιλογής θέματος (Theme buttons)
        """
        Ανανέωση των κουμπιών επιλογής θέματος ('theme_buttons'):
        - Γίνεται επανάληψη σε όλα τα κουμπιά θεμάτων.
        - Κάθε κουμπί αρχικά ρυθμίζεται στο "κανονικό" του χρώμα φόντου και κειμένου
          (που αντιστοιχεί στο 'inner_frame_bg' του τρέχοντος θέματος).
        - Το 'hover_color' ορίζεται σε ένα "ειδικό" χρώμα για την αλληλεπίδραση του ποντικιού.
        - Στη συνέχεια, το συγκεκριμένο κουμπί που αντιστοιχεί στο επιλεγμένο 'theme'
          λαμβάνει ένα διαφορετικό 'fg_color' ('special_button_fg') για να δείχνει ότι είναι ενεργό.
        """
        for k, b in self.theme_buttons.items():  # Επανάληψη για κάθε κουμπί θέματος
            b.configure(
                fg_color=get_theme(self.theme_mode)["inner_frame_bg"],        # Ορισμός χρώματος φόντου κουμπιού (κανονικό)
                hover_color=get_theme(self.theme_mode)["special_button_fg"],  # Ορισμός χρώματος hover κουμπιού
                text_color=get_theme(self.theme_mode)["menu_text_color"]      # Ορισμός χρώματος κειμένου κουμπιού
            )
        if theme in self.theme_buttons:  # Αν το επιλεγμένο θέμα υπάρχει στα κουμπιά
            # Εάν το επιλεγμένο θέμα υπάρχει στα κουμπιά, ενημερώνουμε το κουμπί ώστε να φαίνεται ενεργό
            self.theme_buttons[theme].configure(
                fg_color=get_theme(self.theme_mode)["special_button_fg"]      # Ορισμός ειδικού χρώματος φόντου για το ενεργό θέμα
            )
            

        # Ανανέωση πλαϊνού μενού
        """
        Ανανέωση των χρωμάτων των frames και των κουμπιών της πάνω μπάρας και των ετικετών:
        - Το 'sidebar_frame' και το 'menu_inner_frame' ενημερώνονται με τα νέα χρώματα φόντου
          σύμφωνα με το επιλεγμένο θέμα.
        - Το 'top_bar_frame' ενημερώνεται με το χρώμα του φόντου.
        - Το 'menu_button' και το 'sound_button' ενημερώνονται με τα νέα χρώματα φόντου και hover.
        - Οι ετικέτες 'Mode', 'Theme' και 'mode_label_display' ενημερώνονται με το νέο χρώμα κειμένου.
        """
        self.sidebar_frame.configure(fg_color=get_theme(self.theme_mode)["slide_menu_bg"])      # Ενημέρωση χρώματος φόντου πλαϊνού μενού
        self.menu_inner_frame.configure(fg_color=get_theme(self.theme_mode)["inner_frame_bg"])  # Ενημέρωση χρώματος φόντου εσωτερικού frame μενού
        self.top_bar_frame.configure(fg_color=get_theme(self.theme_mode)["background"])         # Ενημέρωση χρώματος φόντου πάνω μπάρας

        # Κουμπί μενού
        self.menu_button.configure(
            fg_color=get_theme(self.theme_mode)["top_frame_bg"],        # Ενημέρωση χρώματος φόντου κουμπιού μενού
            hover_color=get_theme(self.theme_mode)["top_button_hover"]  # Ενημέρωση χρώματος hover κουμπιού μενού
        )

        # Κουμπί ήχου
        self.sound_button.configure(
            fg_color=get_theme(self.theme_mode)["top_frame_bg"],        # Ενημέρωση χρώματος φόντου κουμπιού ήχου
            hover_color=get_theme(self.theme_mode)["top_button_hover"]  # Ενημέρωση χρώματος hover κουμπιού ήχου
        )

        # Ετικέτες "Mode" και "Theme"
        self.section_label.configure(text_color=get_theme(self.theme_mode)["menu_text_color"])   # Ενημέρωση χρώματος κειμένου ετικέτας "Mode"
        self.theme_label.configure(text_color=get_theme(self.theme_mode)["menu_text_color"])     # Ενημέρωση χρώματος κειμένου ετικέτας "Theme"

        # Ετικέτα επάνω μπάρας (π.χ. "Standard Calculator")
        self.mode_label_display.configure(text_color=get_theme(self.theme_mode)["menu_text_color"])  # Ενημέρωση χρώματος κειμένου ετικέτας πάνω μπάρας


        # Επαναφορά των κουμπιών λειτουργιών (Standard, Scientific κ.λπ.) για να πάρουν σωστό χρώμα
        """
        Τέλος, καλούμε τη 'set_mode_button' με το τρέχον 'current_mode'.
        Αυτό εξασφαλίζει ότι τα κουμπιά επιλογής λειτουργίας (Standard, Scientific κ.λπ.)
        θα ενημερωθούν και αυτά με τα σωστά χρώματα του νέου θέματος (ειδικά το ενεργό mode).
        """
        self.set_mode_button(self.current_mode)


    #==================== ΕΝΑΛΛΑΓΗ MODE ====================
    """
    Μέθοδος set_mode_button(self, mode):
    Ενεργοποιεί οπτικά το κουμπί που αντιστοιχεί στο επιλεγμένο 'mode'
    και στη συνέχεια καλεί τη μέθοδο 'switch_mode' για να αλλάξει το ενεργό calculator frame.
    """
    # Ενεργοποίηση του κουμπιού mode και αλλαγή frame αριθμομηχανής
    def set_mode_button(self, mode):
        """ Μέθοδος set_mode_button(self, mode):
    Ενεργοποιεί οπτικά το κουμπί που αντιστοιχεί στο επιλεγμένο 'mode'
    και στη συνέχεια καλεί τη μέθοδο 'switch_mode' για να αλλάξει το ενεργό calculator frame."""

        """
        Ανανέωση των κουμπιών επιλογής mode ('mode_buttons'):
        - Γίνεται επανάληψη σε όλα τα κουμπιά modes.
        - Κάθε κουμπί αρχικά ρυθμίζεται στο "κανονικό" του χρώμα φόντου, hover χρώματος
          και χρώματος κειμένου, σύμφωνα με το τρέχον θέμα.
        - Στη συνέχεια, το συγκεκριμένο κουμπί που αντιστοιχεί στο επιλεγμένο 'mode'
          λαμβάνει ένα διαφορετικό 'fg_color' ('special_button_fg') για να δείχνει ότι είναι ενεργό.
        """
        # Ενημέρωση των κουμπιών επιλογής mode (mode_buttons) με βάση το τρέχον θέμα
        for k, b in self.mode_buttons.items():
            b.configure(fg_color=get_theme(self.theme_mode)["inner_frame_bg"],          # το χρώμα bg των κουμπιών του μενού για την επιλογή mode, ιδανικά ίδιο με το inner_frame
                        hover_color=get_theme(self.theme_mode)["special_button_fg"],    # το hover χρώμα των κουμπιών του μενού για την επιλογή mode
                        text_color = get_theme(self.theme_mode)["menu_text_color"]      # το χρώμα του κειμένου των κουμπιών του μενού για την επιλογή mode
                        )
        if mode in self.mode_buttons:  # Ελέγχει αν το επιλεγμένο mode υπάρχει στα κουμπιά
            self.mode_buttons[mode].configure(  # Αν ναι, διαμορφώνει το κουμπί ώστε να φαίνεται ενεργό
            fg_color=get_theme(self.theme_mode)["special_button_fg"]  # Ορίζει ειδικό χρώμα φόντου για το ενεργό κουμπί mode
            )
            """
            Καλεί τη μέθοδο 'switch_mode' για να πραγματοποιηθεί η πραγματική αλλαγή
            του ενεργού calculator frame.
            """
        # Αλλαγή του ενεργού mode της αριθμομηχανής
        self.switch_mode(mode)


    #==================== ΠΛΑΪΝΟ ΜΕΝΟΥ ====================
    def toggle_menu(self):
        """        Μέθοδος toggle_menu():
        Εναλλάσσει την κατάσταση του πλαϊνού μενού (ανοιχτό/κλειστό) και ενημερώνει
        το εικονίδιο του κουμπιού μενού στην πάνω μπάρα.        """

        """
        Ελέγχουμε αν το πλαϊνό μενού είναι ήδη ανοιχτό ('self.sidebar_open'):
        - Αν είναι ανοιχτό:
            - Επαναφέρουμε το εικονίδιο του κουμπιού μενού στο αρχικό ('menu_icon_img').
            - Καλούμε τη 'slide_out()' για να κλείσει το μενού με animation.
        - Αν είναι κλειστό:
            - Αλλάζουμε το εικονίδιο του κουμπιού μενού σε εικονίδιο κλεισίματος ('close_icon').
            - Καλούμε τη 'slide_in()' για να ανοίξει το μενού με animation.
        """
        if self.sidebar_open:                                         # Αν το πλαϊνό μενού είναι ανοιχτό
            self.menu_button.configure(image=self.menu_icon_img)      # Επαναφέρει το εικονίδιο του κουμπιού μενού στο αρχικό (εικονίδιο μενού)
            self.slide_out()                                          # Κλείνει το πλαϊνό μενού με animation
        else:                                                         # Αν το πλαϊνό μενού είναι κλειστό
            self.menu_button.configure(image=self.close_icon)         # Αλλάζει το εικονίδιο του κουμπιού μενού σε εικονίδιο κλεισίματος
            self.slide_in()                                           # Ανοίγει το πλαϊνό μενού με animation

    #==================== ΠΛΑΙΝΟ ΜΕΝΟΥ ΜΕ ANIMATION ====================
    # Άνοιγμα πλαϊνού μενού με animation
    def slide_in(self):
        """         Μέθοδος slide_in():
        Εμφανίζει το πλαϊνό μενού με ένα animation (ολίσθηση προς τα μέσα).         """

        """
        Αρχικοποιούμε τη θέση X του sidebar_frame στο -200 (εκτός οθόνης).
        """
        self.sidebar_x = -200

        """
        Εσωτερική συνάρτηση 'animate()':
        Αυτή η συνάρτηση καλείται επαναληπτικά για να δημιουργήσει το animation.
        - Ενώ το 'sidebar_x' είναι μικρότερο από 0 (δηλαδή το μενού δεν έχει φτάσει
          πλήρως στην αριστερή άκρη της οθόνης):
            - Αυξάνουμε το 'sidebar_x' κατά 20 pixels.
            - Ενημερώνουμε τη θέση του 'sidebar_frame' με τη νέα συντεταγμένη X.
            - Χρησιμοποιούμε 'self.after(10, animate)' για να καλέσουμε ξανά την 'animate'
              μετά από 10 χιλιοστά του δευτερολέπτου, δημιουργώντας την αίσθηση κίνησης.
        - Μόλις το 'sidebar_x' φτάσει ή ξεπεράσει το 0, σημαίνει ότι το μενού έχει
          φτάσει στην τελική του θέση. Τότε το τοποθετούμε ακριβώς στο 0 και ορίζουμε
          το 'self.sidebar_open' σε 'True'.
        """
        # Εσωτερική συνάρτηση για το animation του ανοίγματος του πλαϊνού μενού
        def animate(): 
            if self.sidebar_x < 0:                # Ελέγχει αν το sidebar δεν έχει φτάσει στη θέση x=0
                self.sidebar_x += 20              # Αυξάνει τη θέση x του sidebar κατά 20 pixels (κινεί προς τα δεξιά)
                self.sidebar_frame.place(x=self.sidebar_x, y=40)  # Τοποθετεί το sidebar στη νέα θέση
                self.after(10, animate)           # Επαναλαμβάνει την κίνηση μετά από 10ms (animation)
            else:
                self.sidebar_frame.place(x=0, y=40)   # Τοποθετεί το sidebar ακριβώς στη θέση x=0
                self.sidebar_open = True              # Ορίζει ότι το sidebar είναι πλέον

        """
        Αν το 'sidebar_open' είναι 'False' (δηλαδή το μενού είναι κλειστό),
        ξεκινάμε το animation καλώντας την 'animate()'.
        """
        if not self.sidebar_open:
            animate()


    # Κλείσιμο πλαϊνού μενού με animation
    def slide_out(self):
        """        Μέθοδος slide_out():
        Αποκρύπτει το πλαϊνό μενού με ένα animation (ολίσθηση προς τα έξω).   """

        """
        Εσωτερική συνάρτηση 'animate()':
        Αυτή η συνάρτηση καλείται επαναληπτικά για να δημιουργήσει το animation.
        - Ενώ το 'sidebar_x' είναι μεγαλύτερο από -200 (δηλαδή το μενού δεν έχει
          φύγει πλήρως εκτός οθόνης):
            - Μειώνουμε το 'sidebar_x' κατά 20 pixels.
            - Ενημερώνουμε τη θέση του 'sidebar_frame' με τη νέα συντεταγμένη X.
            - Χρησιμοποιούμε 'self.after(10, animate)' για να καλέσουμε ξανά την 'animate'
              μετά από 10 χιλιοστά του δευτερολέπτου.
        - Μόλις το 'sidebar_x' φτάσει ή γίνει μικρότερο από -200, σημαίνει ότι το μενού έχει
          φτάσει στην τελική του θέση εκτός οθόνης. Τότε το τοποθετούμε ακριβώς στο -200
          και ορίζουμε το 'self.sidebar_open' σε 'False'.
        """
        def animate(): 
            if self.sidebar_x > -200:                      # Ελέγχει αν το sidebar δεν έχει φτάσει στη θέση x=-200 (τελικό σημείο απόκρυψης)
                self.sidebar_x -= 20                       # Μειώνει τη θέση x του sidebar κατά 20 pixels (κινεί προς τα αριστερά)
                self.sidebar_frame.place(x=self.sidebar_x, y=40)  # Τοποθετεί το sidebar στη νέα θέση
                self.after(10, animate)                    # Επαναλαμβάνει την κίνηση μετά από 10ms (animation)
            else:
                self.sidebar_frame.place(x=-200, y=40)     # Τοποθετεί το sidebar ακριβώς στη θέση x=-200 (πλήρως κρυμμένο)
                self.sidebar_open = False                  # Ορίζει ότι το sidebar είναι

        """
        Αν το 'sidebar_open' είναι 'True' (δηλαδή το μενού είναι ανοιχτό),
        ξεκινάμε το animation καλώντας την 'animate()'.
        """
        if self.sidebar_open:
            animate()

    #==================== ΧΕΙΡΙΣΜΟΣ ΚΛΙΚ ====================
    def on_click_outside_menu(self, event):
        """        Μέθοδος on_click_outside_menu(self, event):
        Χειρίζεται τα αριστερά κλικ του ποντικιού στο παράθυρο της εφαρμογής και κλείνει
        το πλαϊνό μενού αν το κλικ έγινε εκτός των ορίων του.         """

        """
        Ελέγχουμε αν το πλαϊνό μενού είναι ανοιχτό. Αν όχι, δεν χρειάζεται να κάνουμε κάτι.
        """
        if self.sidebar_open:
            # Συντεταγμένες sidebar
            """
            Υπολογίζουμε τις συντεταγμένες του πλαϊνού μενού:
            - 'winfo_rootx()', 'winfo_rooty()': Παίρνουν τις συντεταγμένες της πάνω-αριστερής γωνίας
              του widget σε σχέση με την οθόνη.
            - 'winfo_width()', 'winfo_height()': Παίρνουν το πλάτος και το ύψος του widget.
            """
            sidebar_x1 = self.sidebar_frame.winfo_rootx()                  # Παίρνει τη συντεταγμένη x (αριστερή πλευρά) του sidebar ως προς την οθόνη
            sidebar_y1 = self.sidebar_frame.winfo_rooty()                  # Παίρνει τη συντεταγμένη y (πάνω πλευρά) του sidebar ως προς την οθόνη
            sidebar_x2 = sidebar_x1 + self.sidebar_frame.winfo_width()     # Υπολογίζει τη συντεταγμένη x (δεξιά πλευρά) του sidebar
            sidebar_y2 = sidebar_y1 + self.sidebar_frame.winfo_height()    # Υπολογίζει τη συντεταγμένη y (κάτω πλευρά) του sidebar

            # Συντεταγμένες κλικ
            """
            Παίρνουμε τις συντεταγμένες του κλικ του ποντικιού:
            - 'winfo_pointerx()', 'winfo_pointery()': Παίρνουν τις συντεταγμένες του δείκτη του ποντικιού
              σε σχέση με την οθόνη.
            """
            click_x = self.winfo_pointerx()   # Συντεταγμένη x του δείκτη ποντικιού (ως προς την οθόνη)
            click_y = self.winfo_pointery()   # Συντεταγμένη y του δείκτη ποντικιού (ως προς την οθόνη)

            # Αν το κλικ είναι ΕΚΤΟΣ sidebar
            """
            Ελέγχουμε αν το κλικ έγινε ΕΚΤΟΣ των ορίων του sidebar:
            - Αν το 'click_x' δεν είναι μεταξύ 'sidebar_x1' και 'sidebar_x2' Ή
            - Αν το 'click_y' δεν είναι μεταξύ 'sidebar_y1' και 'sidebar_y2'.
            """
            if not (sidebar_x1 <= click_x <= sidebar_x2 and sidebar_y1 <= click_y <= sidebar_y2):  # Αν το κλικ είναι εκτός του sidebar
                self.menu_button.configure(image=self.menu_icon_img)  # Επαναφέρει το εικονίδιο του κουμπιού μενού
                self.slide_out()  # Κλείνει το πλαϊνό μενού με animation


    #==================== ΠΡΟΒΟΛΗ FRAME ====================
    def show_calculator_frame(self):
        """        Μέθοδος show_calculator_frame():
        Φορτώνει και εμφανίζει το κατάλληλο calculator frame (π.χ., Standard, Scientific)
        με βάση το 'self.current_mode'. Διαχειρίζεται την αντικατάσταση του προηγούμενου frame
        και την ενημέρωση της οθόνης.        """

        """
        Εάν υπάρχει ήδη ένα ενεργό 'calculator_frame':
        - Προσπαθούμε να πάρουμε την τρέχουσα τιμή που εμφανίζεται στο display του παλιού frame.
          Αυτό γίνεται για να διατηρηθεί η τιμή όταν ο χρήστης αλλάζει mode (π.χ., από Standard σε Scientific).
          Εάν η μέθοδος 'get_display_value()' δεν υπάρχει, η 'display_value' παραμένει κενή.
        - Καταστρέφουμε το παλιό 'calculator_frame' για να απελευθερωθούν οι πόροι του.
        """
        if self.calculator_frame:                        # Ελέγχει αν υπάρχει το πλαίσιο της αριθμομηχανής (calculator_frame)
            try:
                self.display_value = self.calculator_frame.get_display_value()  # Παίρνει την τρέχουσα τιμή της οθόνης της αριθμομηχανής
            except:
                self.display_value = ""                  # Αν υπάρξει σφάλμα, θέτει την τιμή της οθόνης ως κενή συμβολοσειρά
            self.calculator_frame.destroy()              # Καταστρέφει/αφαιρεί το πλαίσιο της αριθμομηχανής από

        """
        Προετοιμασία για τη φόρτωση του νέου frame:
        - Παίρνουμε το τρέχον θέμα.
        - Ανακτούμε την κλάση του frame για το 'self.current_mode' από το 'frame_data'.
          Αν το mode δεν βρεθεί, χρησιμοποιείται ως προεπιλογή η 'StandardCalculator'.
        """
        theme = get_theme(self.theme_mode)  # Παίρνει το τρέχον θέμα εμφάνισης
        FrameClass = frame_data.get(self.current_mode, {}).get("frame", StandardCalculator)  # Παίρνει την κλάση του frame για το τρέχον mode

        """
        Δημιουργία και τοποθέτηση του νέου calculator frame:
        - Προσπαθούμε να δημιουργήσουμε ένα στιγμιότυπο της 'FrameClass', περνώντας
          το 'self' (το κύριο παράθυρο), το 'theme' και το 'sound_enabled' ως ορίσματα.
          Αυτό είναι το τυπικό setup για τα calculator frames.
        - Αν υπάρξει 'TypeError' (π.χ., αν μια κλάση frame δεν δέχεται αυτά τα ορίσματα),
          προσπαθούμε να τη δημιουργήσουμε μόνο με το 'self'.
        - 'pack(fill="both", expand=True)': Τοποθετεί το νέο frame ώστε να γεμίσει
          όλο τον διαθέσιμο χώρο στο κύριο παράθυρο.
        """
        try:
            # ΕΔΩ ΔΗΜΙΟΥΡΓΕΙΤΑΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΤΗΣ ΑΡΙΘΜΟΜΗΧΑΝΗΣ
            self.calculator_frame = FrameClass(self, theme=theme, sound_enabled=self.sound_enabled)  # Δημιουργεί το πλαίσιο αριθμομηχανής με θέμα και ήχο ενεργό/ανενεργό
        except TypeError:                                                    # Αν προκύψει TypeError (π.χ. δεν υποστηρίζονται τα ορίσματα)
            self.calculator_frame = FrameClass(self)                         # Δημιουργεί το πλαίσιο μόνο με το self

        self.calculator_frame.pack(fill="both", expand=True)                 # Τοποθετεί το πλαίσιο ώστε να γεμίζει όλο τον διαθέσιμο χώρο

        """
        Επαναφορά της τιμής στο display του νέου frame:
        - Προσπαθούμε να ορίσουμε την προηγούμενη 'display_value' στο νέο frame.
          Αυτό γίνεται για να διατηρηθεί η είσοδος του χρήστη κατά την αλλαγή mode.
          Εάν η μέθοδος 'set_display_value()' δεν υπάρχει, απλώς παραβλέπεται.
        """
        try:                                                        # Προσπαθεί να εκτελέσει τον παρακάτω κώδικα
            self.calculator_frame.set_display_value(self.display_value)  # Θέτει την τιμή της οθόνης της αριθμομηχανής στην αποθηκευμένη τιμή
        except:                                                     # Αν προκύψει οποιοδήποτε σφάλμα
            pass                                                    # Αγνοεί το σφάλμα και συνεχίζει χωρίς ενέργεια

        """
        Οπτικές ρυθμίσεις μετά τη φόρτωση του frame:
        - 'self.sidebar_frame.lift()': Φέρνει το πλαϊνό μενού στην κορυφή της στοίβας των widgets,
          διασφαλίζοντας ότι εμφανίζεται πάνω από το calculator frame όταν είναι ανοιχτό.
        - Ενημερώνουμε την ετικέτα στην πάνω μπάρα ('mode_label_display') ώστε να αντικατοπτρίζει
          το όνομα του τρέχοντος mode.
        """
        self.sidebar_frame.lift()                    # Φέρνει το πλαϊνό μενού πάνω από το calculator frame (ώστε να φαίνεται όταν είναι ανοιχτό)
        self.mode_label_display.configure(                   # Ενημερώνει την ετικέτα στην πάνω μπάρα με το όνομα του τρέχοντος mode
            text=f"{self.current_mode.title()} Calculator",  # Θέτει το κείμενο της ετικέτας (π.χ. "Standard Calculator")
            text_color=get_theme(self.theme_mode)["menu_text_color"]  # Θέτει το χρώμα του κειμένου σύμφωνα με το τρέχον θέμα
        )

    #==================== ΕΝΑΛΛΑΓΗ MODE ====================
    """
    Μέθοδος switch_mode(self, new_mode):
    Αλλάζει το 'current_mode' της εφαρμογής στο 'new_mode' και καλεί τη 'show_calculator_frame()'
    για να φορτώσει το αντίστοιχο frame.
    """
    def switch_mode(self, new_mode):        # Ορισμός της μεθόδου switch_mode με όρισμα το νέο mode
        self.current_mode = new_mode        # Ενημερώνει την τρέχουσα λειτουργία (mode) της εφαρμογής με το νέο mode
        self.show_calculator_frame()        # Καλεί τη μέθοδο για να εμφανίσει το κατάλληλο frame της αριθμομηχανής για το νέο mode

    #==================== ΕΝΑΛΛΑΓΗ ΘΕΜΑΤΟΣ ====================
    """
    Μέθοδος switch_theme(self, new_theme):
    Αλλάζει το 'theme_mode' της εφαρμογής στο 'new_theme' και καλεί τη 'show_calculator_frame()'
    για να επαναφορτώσει το τρέχον frame με το νέο θέμα.
    """
    def switch_theme(self, new_theme):                # Ορισμός της μεθόδου switch_theme με όρισμα το νέο θέμα
        self.theme_mode = new_theme                   # Ενημερώνει την τρέχουσα λειτουργία θέματος της εφαρμογής με το νέο θέμα
        self.show_calculator_frame()                  # Καλεί τη μέθοδο για να εμφανίσει το κατάλληλο frame της αριθμομηχανής με το νέο θέμα

    #==================== ΕΝΑΛΛΑΓΗ ΗΧΟΥ ====================

    def toggle_sound(self):                             # Συνάρτηση για εναλλαγή κατάστασης ήχου
        """         Μέθοδος toggle_sound():
         Εναλλάσσει την καθολική κατάσταση του ήχου και ενημερώνει το εικονίδιο του κουμπιού ήχου
         στην πάνω μπάρα.         """

        """
        - 'global sound_enabled_global': Δηλώνουμε ότι θα χρησιμοποιήσουμε και θα τροποποιήσουμε
          την καθολική μεταβλητή 'sound_enabled_global'.
        - 'sound_enabled_global = not sound_enabled_global': Αντιστρέφουμε την κατάσταση της μεταβλητής
          (True γίνεται False, False γίνεται True).
        - 'self.sound_enabled = sound_enabled_global': Ενημερώνουμε την τοπική μεταβλητή 'self.sound_enabled'
          της κλάσης για να αντικατοπτρίζει την νέα κατάσταση.
        - 'self.sound_button.configure(image=...)': Αλλάζουμε το εικονίδιο του κουμπιού ήχου
          αναλόγως της νέας κατάστασης του ήχου ('sound_on_img' αν ενεργοποιημένος, 'sound_off_img' αν απενεργοποιημένος).
        - 'self.show_calculator_frame()': Επαναφορτώνουμε το τρέχον calculator frame. Αυτό είναι σημαντικό
          γιατί τα frames ενδέχεται να χρειάζεται να ενημερώσουν τα ίδια τους τα στοιχεία ήχου
          με βάση την νέα κατάσταση του 'self.sound_enabled'.
        """
        global sound_enabled_global                     # Χρησιμοποιούμε τη global μεταβλητή για να αλλάξουμε την κατάσταση ήχου
        sound_enabled_global = not sound_enabled_global # Αντιστρέφουμε την κατάσταση ήχου
        self.sound_enabled = sound_enabled_global       # Ενημερώνουμε την κατάσταση ήχου της εφαρμογής
        self.sound_button.configure(image=self.sound_on_img if self.sound_enabled else self.sound_off_img)  # Ενημερώνουμε το εικονίδιο του κουμπιού ήχου ανάλογα με την κατάσταση
        self.show_calculator_frame()                    # Επαναφόρτωση του calculator frame για να αντικατοπτριστεί η αλλαγή ήχου

    #==================== ΧΕΙΡΙΣΜΟΣ ΠΛΗΚΤΡΩΝ ====================

    def on_key_press(self, event):  # Συνάρτηση για χειρισμό πατήματος πλήκτρων
        """        Μέθοδος on_key_press(self, event):
        Χειρίζεται τα πατήματα πλήκτρων από το πληκτρολόγιο και τα προωθεί στο ενεργό
        calculator frame για περαιτέρω επεξεργασία.        """

        """
        - 'key = event.char': Λαμβάνουμε τον χαρακτήρα που αντιστοιχεί στο πατημένο πλήκτρο.
        - Ελέγχουμε αν υπάρχει ενεργό 'self.calculator_frame' και αν αυτό το frame
          έχει τη μέθοδο 'handle_key_input' (χρησιμοποιώντας 'hasattr').
          Αυτό διασφαλίζει ότι η εφαρμογή δεν θα προσπαθήσει να καλέσει μια μέθοδο
          που δεν υπάρχει σε ένα συγκεκριμένο frame.
        - Αν ισχύουν οι παραπάνω συνθήκες, καλούμε τη μέθοδο 'handle_key_input'
          του ενεργού calculator frame, περνώντας της τον πατημένο χαρακτήρα.
          Κάθε calculator frame είναι υπεύθυνο να χειριστεί τα δικά του πλήκτρα.
        """
        key = event.char    # Λαμβάνουμε το χαρακτήρα του πατημένου πλήκτρου
        if self.calculator_frame and hasattr(self.calculator_frame, "handle_key_input"):    # Ελέγχουμε αν το τρέχον frame έχει τη μέθοδο handle_key_input
            self.calculator_frame.handle_key_input(key) # Καλούμε τη μέθοδο για να χειριστεί το πάτημα του πλήκτρου




#==================== ΕΚΚΙΝΗΣΗ ΕΦΑΡΜΟΓΗΣ ====================
"""
Εκτέλεση της εφαρμογής:
- Το 'if __name__ == "__main__":' διασφαλίζει ότι ο παρακάτω κώδικας θα εκτελεστεί
  μόνο όταν το αρχείο 'mainCalc.py' εκτελείται απευθείας (και όχι όταν εισάγεται
  ως module σε άλλο αρχείο).
- 'app = MainCalculatorApp()': Δημιουργεί ένα στιγμιότυπο της κύριας κλάσης της εφαρμογής,
  το οποίο αρχικοποιεί το GUI.
- 'app.mainloop()': Ξεκινάει τον κύριο βρόχο εκδηλώσεων (event loop) της εφαρμογής.
  Αυτό κάνει το παράθυρο να εμφανιστεί και να παραμείνει ενεργό, περιμένοντας
  για αλληλεπιδράσεις χρήστη (κλικ, πατήματα πλήκτρων κ.λπ.).
"""
if __name__ == "__main__":         # Εκτελείται μόνο αν το αρχείο τρέχει ως κύριο πρόγραμμα
    app = MainCalculatorApp()      # Δημιουργεί το κύριο αντικείμενο της εφαρμογής αριθμομηχανής
    app.mainloop()                 # Εκκινεί τον κύριο βρόχο του GUI (εμφανίζει το παράθυρο και περιμένει ενέργειες χρήστη)