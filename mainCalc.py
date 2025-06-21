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
import customtkinter  # Βιβλιοθήκη για μοντέρνο GUI
from PIL import Image  # Χρήση εικόνων για εικονίδια
from standardCalc import StandardCalculator  # Το default mode της αριθμομηχανής
from themeManager import get_theme  # Διαχείριση θεμάτων εμφάνισης
from customtkinter import CTkLabel  # Ετικέτες για το GUI
from frameManager import frame_data  # Διαθέσιμα modes/frames για την αριθμομηχανή
import os  # Χρήση για έλεγχο ύπαρξης αρχείων

#==================== ΑΡΧΙΚΕΣ ΡΥΘΜΙΣΕΙΣ ====================
customtkinter.set_appearance_mode("dark")   # Ορίζουμε το dark mode ως αρχικό
sound_enabled_global = True                 # Μεταβλητή για ενεργοποίηση/απενεργοποίηση ήχου

# Συνάρτηση που επιστρέφει την κατάσταση του ήχου
def get_sound_state():                      
    return sound_enabled_global             # Επιστρέφει την τρέχουσα κατάσταση του ήχου

#==================== ΚΛΑΣΗ MainCalculatorApp ====================
class MainCalculatorApp(customtkinter.CTk):     # Κύρια κλάση της εφαρμογής αριθμομηχανής
    def __init__(self):                         # Constructor της κλάσης
        """
        Αρχικοποιεί το κύριο παράθυρο της εφαρμογής υπολογιστή με τις ακόλουθες λειτουργίες:
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
        self.geometry("400x600")                                # Ορισμός διαστάσεων παραθύρου
        self.bind_all("<Key>", self.on_key_press)               # Χειρισμός πατήματος πλήκτρων
        self.bind("<Button-1>", self.on_click_outside_menu)     # Χειρισμός click εκτός μενού

        #==================== ΚΑΤΑΣΤΑΣΕΙΣ ΕΦΑΡΜΟΓΗΣ ====================
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
        sound_on_path = "images/sound_on.png"
        if os.path.exists(sound_on_path):   # Έλεγχος αν υπάρχει το αρχείο
            self.sound_on_img = customtkinter.CTkImage(light_image=Image.open(sound_on_path), size=(24, 24))
        else:
            print(f"Warning: Image file '{sound_on_path}' not found.")
            self.sound_on_img = None  # Χρήση placeholder αν δεν βρεθεί

        sound_off_path = "images/sound_off.png"
        if os.path.exists(sound_off_path):
            self.sound_off_img = customtkinter.CTkImage(light_image=Image.open(sound_off_path), size=(24, 24))
        else:
            print(f"Warning: Image file '{sound_off_path}' not found.")
            self.sound_off_img = None  # Χρήση placeholder αν δεν βρεθεί
        menu_icon_path = "images/menu_icon.png"
        if os.path.exists(menu_icon_path):
            self.menu_icon_img = customtkinter.CTkImage(light_image=Image.open(menu_icon_path), size=(24, 24))
        else:
            print(f"Warning: Image file '{menu_icon_path}' not found.")
            self.menu_icon_img = None  # Χρήση placeholder αν δεν βρεθεί

        close_icon_path = "images/close_icon.png"
        if os.path.exists(close_icon_path):
            self.close_icon = customtkinter.CTkImage(light_image=Image.open(close_icon_path), size=(24, 24))
        else:
            print(f"Warning: Image file '{close_icon_path}' not found.")
            self.close_icon = None  

        bullet_icon_path = "images/bullet.png"
        if os.path.exists(bullet_icon_path):
            self.bullet_icon = customtkinter.CTkImage(light_image=Image.open(bullet_icon_path), size=(14, 14))
        else:
            print(f"Warning: Image file '{bullet_icon_path}' not found.")
            self.bullet_icon = None  # Χρήση placeholder αν δεν βρεθεί

        #==================== ΔΗΜΙΟΥΡΓΙΑ ΠΑΝΩ ΜΠΑΡΑΣ ====================
        self.top_bar_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0)
        self.top_bar_frame.pack(fill="x")   # Γεμίζει οριζόντια το πάνω μέρος του παραθύρου

        # Κουμπί εμφάνισης/απόκρυψης πλαϊνού μενού
        self.menu_button = customtkinter.CTkButton(      # Δημιουργία κουμπιού για το πλαϊνό μενού
            self.top_bar_frame,                          # Τοποθέτηση στην πάνω μπάρα
            text="",                                     # Χωρίς κείμενο (μόνο εικόνα)
            width=40,                                   # Πλάτος κουμπιού
            height=40,                                  # Ύψος κουμπιού
            image=self.menu_icon_img,                   # Εικόνα εικονιδίου μενού
            command=self.toggle_menu,                   # Συνάρτηση που καλείται όταν πατηθεί το κουμπί
            fg_color=get_theme(self.theme_mode)["top_frame_bg"],    # Χρώμα φόντου κουμπιού (ανάλογα με το θέμα)
            corner_radius=6)                            # Στρογγυλοποίηση γωνιών κουμπιού
        self.menu_button.pack(side="left", padx=5)      # Τοποθέτηση αριστερά στην πάνω μπάρα με εσωτερικό περιθώριο

        # Εμφάνιση του τρέχοντος mode
        self.mode_label_display = customtkinter.CTkLabel(
            self.top_bar_frame,
            text="Standard Calculator",
            font=("Arial", 16),
            text_color=get_theme(self.theme_mode)["menu_text_color"]
        )
        self.mode_label_display.pack(side="left", padx=10)

        # Κουμπί ήχου
        self.sound_button = customtkinter.CTkButton(
            self.top_bar_frame,
            image=self.sound_on_img,
            text="",
            width=40,
            height=40,
            command=self.toggle_sound,
            fg_color=get_theme(self.theme_mode)["top_frame_bg"]     # Το χρώμα φόντου του κουμπιού που ανοίγει/κλείνει το μενού
        )
        self.sound_button.pack(side="right", padx=5)

        #==================== ΠΛΑΪΝΟ ΜΕΝΟΥ ====================
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=200, height=560,
            corner_radius=0,
            fg_color=get_theme(self.theme_mode)["top_frame_bg"] # το χρώμα του πλαϊνού μενού (ιδανικά ίδιο με το top_frame)
        )
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.place(x=-200, y=40)

        # Εσωτερικό του πλαϊνού μενού
        self.menu_inner_frame = customtkinter.CTkFrame(self.sidebar_frame, corner_radius=0)
        self.menu_inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #==================== ΕΝΟΤΗΤΑ Mode ====================
        self.section_label = customtkinter.CTkLabel(self.menu_inner_frame, text="Mode", font=("Arial", 14, "bold"))
        self.section_label.pack(anchor="w", pady=(5, 2))

        # Κουμπιά για εναλλαγή μεταξύ διαφορετικών λειτουργιών (frames)
        for mode, data in frame_data.items():
            icon_path = data.get("icon_path", "")
            if os.path.exists(icon_path):
                icon = customtkinter.CTkImage(light_image=Image.open(icon_path), size=(20, 20))
            else:
                print(f"Warning: Icon file '{icon_path}' not found for mode '{mode}'.")
                icon = None  # Or use a default placeholder
            self.mode_icons[mode] = icon

            btn = customtkinter.CTkButton(
                self.menu_inner_frame,
                text=mode.title(),
                corner_radius=6,
                image=icon,
                anchor="w",
                compound="left",
                command=lambda m=mode: self.set_mode_button(m),
                fg_color=get_theme(self.theme_mode)["top_button_bg"],
                text_color=get_theme(self.theme_mode)["menu_text_color"]
            )
            btn.pack(pady=2, padx=2, anchor="w", fill="x")
            self.mode_buttons[mode] = btn

        #==================== ΕΝΟΤΗΤΑ Theme ====================
        self.theme_label = customtkinter.CTkLabel(self.menu_inner_frame, text="Theme", font=("Arial", 14, "bold"))
        self.theme_label.pack(anchor="w", pady=(10, 2))

        # Κουμπιά επιλογής θέματος εμφάνισης
        for theme in ["dark", "light", "purple", "oceanic", "goth", "mondrian", "rainbow", "windows95", "excel2003"]:
            btn = customtkinter.CTkButton(
                self.menu_inner_frame,
                text=theme.capitalize(),
                corner_radius=6,
                image=self.bullet_icon,
                compound="left",
                anchor="w",
                width=180,
                height=28,
                font=("Arial", 12),

                command=lambda t=theme: self.set_theme_button(t)
            )
            btn.pack(pady=2, padx=2, anchor="w")
            self.theme_buttons[theme] = btn

        #==================== ΕΚΚΙΝΗΣΗ DEFAULT FRAME ====================
        self.calculator_frame = None
        self.after(100, self.show_calculator_frame)
        self.after(150, lambda: self.set_theme_button(self.theme_mode))
        self.after(200, lambda: self.set_mode_button(self.current_mode))


        #==================== ΕΝΗΜΕΡΩΣΗ ΘΕΜΑΤΟΣ ΚΑΙ ΜΕΝΟΥ ====================
        # Ανανέωση κουμπιών επιλογής θέματος και modes με το τρέχον θέμα
    # Ορισμός του επιλεγμένου θέματος
    def set_theme_button(self, theme):
        self.switch_theme(theme)

        # Ανανέωση κουμπιών επιλογής θέματος (Theme buttons)
        for k, b in self.theme_buttons.items():
            b.configure(
                fg_color=get_theme(self.theme_mode)["inner_frame_bg"],
                hover_color=get_theme(self.theme_mode)["special_button_fg"],
                text_color=get_theme(self.theme_mode)["menu_text_color"]
            )
        if theme in self.theme_buttons:
            self.theme_buttons[theme].configure(
                fg_color=get_theme(self.theme_mode)["special_button_fg"]
            )

        # Ανανέωση πλαϊνού μενού
        self.sidebar_frame.configure(fg_color=get_theme(self.theme_mode)["slide_menu_bg"])
        self.menu_inner_frame.configure(fg_color=get_theme(self.theme_mode)["inner_frame_bg"])
        self.top_bar_frame.configure(fg_color=get_theme(self.theme_mode)["background"])

        # Κουμπί μενού
        self.menu_button.configure(
            fg_color=get_theme(self.theme_mode)["top_frame_bg"],
            hover_color=get_theme(self.theme_mode)["top_button_hover"]
        )

        # Κουμπί ήχου
        self.sound_button.configure(
            fg_color=get_theme(self.theme_mode)["top_frame_bg"],
            hover_color=get_theme(self.theme_mode)["top_button_hover"]
        )

        # Ετικέτες "Mode" και "Theme"
        self.section_label.configure(text_color=get_theme(self.theme_mode)["menu_text_color"])
        self.theme_label.configure(text_color=get_theme(self.theme_mode)["menu_text_color"])

        # Ετικέτα επάνω μπάρας (π.χ. "Standard Calculator")
        self.mode_label_display.configure(text_color=get_theme(self.theme_mode)["menu_text_color"])

        # Επαναφορά των κουμπιών λειτουργιών (Standard, Scientific κ.λπ.) για να πάρουν σωστό χρώμα
        self.set_mode_button(self.current_mode)

    #==================== ΕΝΑΛΛΑΓΗ MODE ====================
    def set_mode_button(self, mode):
        for k, b in self.mode_buttons.items():
            b.configure(fg_color=get_theme(self.theme_mode)["inner_frame_bg"],          # το χρώμα bg των κουμπιών του μενού για την επιλογή mode, ιδανικά ίδιο με το inner_frame
                        hover_color=get_theme(self.theme_mode)["special_button_fg"],    # το hover χρώμα των κουμπιών του μενού για την επιλογή mode
                        text_color = get_theme(self.theme_mode)["menu_text_color"]      # το χρώμα του κειμένου των κουμπιών του μενού για την επιλογή mode
                        )
        if mode in self.mode_buttons:
            self.mode_buttons[mode].configure(fg_color=get_theme(self.theme_mode)["special_button_fg"])
        self.switch_mode(mode)

    #==================== ΠΛΑΪΝΟ ΜΕΝΟΥ ====================
    def toggle_menu(self):
        if self.sidebar_open:
            self.menu_button.configure(image=self.menu_icon_img)
            self.slide_out()
        else:
            self.menu_button.configure(image=self.close_icon)
            self.slide_in()

    #==================== ΠΛΑΙΝΟ ΜΕΝΟΥ ΜΕ ANIMATION ====================
    # Άνοιγμα πλαϊνού μενού με animation
    def slide_in(self):
        self.sidebar_x = -200

        def animate():
            if self.sidebar_x < 0:
                self.sidebar_x += 20
                self.sidebar_frame.place(x=self.sidebar_x, y=40)
                self.after(10, animate)
            else:
                self.sidebar_frame.place(x=0, y=40)
                self.sidebar_open = True

        if not self.sidebar_open:
            animate()

    # Κλείσιμο πλαϊνού μενού με animation
    def slide_out(self):
        def animate():
            if self.sidebar_x > -200:
                self.sidebar_x -= 20
                self.sidebar_frame.place(x=self.sidebar_x, y=40)
                self.after(10, animate)
            else:
                self.sidebar_frame.place(x=-200, y=40)
                self.sidebar_open = False

        if self.sidebar_open:
            animate()

    #==================== ΧΕΙΡΙΣΜΟΣ ΚΛΙΚ ====================
    def on_click_outside_menu(self, event):
        if self.sidebar_open:
            # Συντεταγμένες sidebar
            sidebar_x1 = self.sidebar_frame.winfo_rootx()
            sidebar_y1 = self.sidebar_frame.winfo_rooty()
            sidebar_x2 = sidebar_x1 + self.sidebar_frame.winfo_width()
            sidebar_y2 = sidebar_y1 + self.sidebar_frame.winfo_height()
            # Συντεταγμένες κλικ
            click_x = self.winfo_pointerx()
            click_y = self.winfo_pointery()
            # Αν το κλικ είναι ΕΚΤΟΣ sidebar
            if not (sidebar_x1 <= click_x <= sidebar_x2 and sidebar_y1 <= click_y <= sidebar_y2):
                self.menu_button.configure(image=self.menu_icon_img)
                self.slide_out()


    #==================== ΠΡΟΒΟΛΗ FRAME ====================
    def show_calculator_frame(self):
        if self.calculator_frame:
            try:
                self.display_value = self.calculator_frame.get_display_value()
            except:
                self.display_value = ""
            self.calculator_frame.destroy()

        theme = get_theme(self.theme_mode)
        FrameClass = frame_data.get(self.current_mode, {}).get("frame", StandardCalculator)

        try:
            self.calculator_frame = FrameClass(self, theme=theme, sound_enabled=self.sound_enabled)
        except TypeError:
            self.calculator_frame = FrameClass(self)

        self.calculator_frame.pack(fill="both", expand=True)

        try:
            self.calculator_frame.set_display_value(self.display_value)
        except:
            pass

        self.sidebar_frame.lift()
        self.mode_label_display.configure(
            text=f"{self.current_mode.title()} Calculator",
            text_color=get_theme(self.theme_mode)["menu_text_color"]
        )

    #==================== ΕΝΑΛΛΑΓΗ MODE ====================
    def switch_mode(self, new_mode):        
        self.current_mode = new_mode
        self.show_calculator_frame()

    #==================== ΕΝΑΛΛΑΓΗ ΘΕΜΑΤΟΣ ====================
    def switch_theme(self, new_theme):
        self.theme_mode = new_theme
        self.show_calculator_frame()

    #==================== ΕΝΑΛΛΑΓΗ ΗΧΟΥ ====================
    def toggle_sound(self):                             # Συνάρτηση για εναλλαγή κατάστασης ήχου
        global sound_enabled_global                     # Χρησιμοποιούμε τη global μεταβλητή για να αλλάξουμε την κατάσταση ήχου
        sound_enabled_global = not sound_enabled_global # Αντιστρέφουμε την κατάσταση ήχου
        self.sound_enabled = sound_enabled_global       # Ενημερώνουμε την κατάσταση ήχου της εφαρμογής
        self.sound_button.configure(image=self.sound_on_img if self.sound_enabled else self.sound_off_img)  # Ενημερώνουμε το εικονίδιο του κουμπιού ήχου ανάλογα με την κατάσταση
        self.show_calculator_frame()                    # Επαναφόρτωση του calculator frame για να αντικατοπτριστεί η αλλαγή ήχου

    #==================== ΧΕΙΡΙΣΜΟΣ ΠΛΗΚΤΡΩΝ ====================
    def on_key_press(self, event):  # Συνάρτηση για χειρισμό πατήματος πλήκτρων
        key = event.char    # Λαμβάνουμε το χαρακτήρα του πατημένου πλήκτρου
        if self.calculator_frame and hasattr(self.calculator_frame, "handle_key_input"):    # Ελέγχουμε αν το τρέχον frame έχει τη μέθοδο handle_key_input
            self.calculator_frame.handle_key_input(key) # Καλούμε τη μέθοδο για να χειριστεί το πάτημα του πλήκτρου




#==================== ΕΚΚΙΝΗΣΗ ΕΦΑΡΜΟΓΗΣ ====================
if __name__ == "__main__":
    app = MainCalculatorApp()
    app.mainloop()