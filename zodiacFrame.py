""" 
# ΕΙΣΑΓΩΓΕΣ ΒΙΒΛΙΟΘΗΚΩΝ ΚΑΙ ΔΕΔΟΜΕΝΩΝ
Εδώ εισάγονται όλες οι απαραίτητες βιβλιοθήκες και τα δεδομένα που θα χρησιμοποιηθούν στο πρόγραμμα.
"""
import tkinter as tk  # Εισαγωγή της βασικής βιβλιοθήκης tkinter για GUI
import customtkinter  # Εισαγωγή της customtkinter για βελτιωμένα widgets
import datetime  # Εισαγωγή για διαχείριση ημερομηνιών
import random  # Εισαγωγή για τυχαίες επιλογές
import pygame  # Εισαγωγή για αναπαραγωγή ήχου
import os  # Εισαγωγή για λειτουργίες συστήματος αρχείων
from customtkinter import CTkFont  # Εισαγωγή της CTkFont για προσαρμοσμένες γραμματοσειρές

# Εισαγωγή δεδομένων και widgets από άλλα αρχεία του project
from predictions import funny_predictions, fortune_teller_quotes, fortune_hint_messages  # Προβλέψεις και μηνύματα
from zodiacIconWidget import ZoomingZodiac  # Widget για τα εικονίδια των ζωδίων
from themeManager import get_theme  # Συνάρτηση για το θέμα εμφάνισης

pygame.init()  # Αρχικοποίηση του pygame για χρήση ήχου

""" 
# ΣΤΑΤΙΚΑ ΔΕΔΟΜΕΝΑ ΖΩΔΙΩΝ ΚΑΙ ΜΕΤΑΒΛΗΤΕΣ ΚΑΤΑΣΤΑΣΗΣ
Περιέχει τα ζώδια, μετρητές και λίστες για την κατάσταση του προγράμματος.
"""
zodiac_data = [
    ("Κριός", "Aries"), ("Ταύρος", "Taurus"), ("Δίδυμος", "Gemini"),
    ("Καρκίνος", "Cancer"), ("Λέων", "Leo"), ("Παρθένος", "Virgo"),
    ("Ζυγός", "Libra"), ("Σκορπιός", "Scorpio"), ("Τοξότης", "Sagittarius"),
    ("Αιγόκερως", "Capricorn"), ("Υδροχόος", "Aquarius"), ("Ιχθύς", "Pisces")
]

prediction_counter = {"date": None, "zodiacs": {}}  # Μετρητής για να μην αλλάζει η πρόβλεψη κάθε μέρα
active_delays = []  # Λίστα για τα ενεργά χρονικά delays (after)

""" 
# ΚΥΡΙΑ ΚΛΑΣΗ ZodiacFrame
Η βασική κλάση που περιέχει όλο το GUI και τη λογική για τα ζώδια και τις προβλέψεις.
"""
class ZodiacFrame(customtkinter.CTkFrame):  # Κλάση για το βασικό frame των ζωδίων
    def __init__(self, master, sound_enabled=True, mode="dark"):
        """
        # ΑΡΧΙΚΟΠΟΙΗΣΗ ΤΟΥ FRAME
        Εδώ δημιουργούνται όλα τα widgets και γίνεται η αρχική ρύθμιση του frame.
        """
        super().__init__(master)  # Κλήση του constructor της υπερκλάσης
        self.sound_enabled = sound_enabled  # Ενεργοποίηση ήχου
        self.mode = mode  # Λειτουργία (dark/light)
        self.theme = get_theme(self.mode)  # Λήψη του θέματος εμφάνισης
        self.configure(fg_color=self.theme["background"])  # Ορισμός χρώματος φόντου

        frame_buttons = customtkinter.CTkFrame(master=self, fg_color=self.theme["background"])  # Frame για τα κουμπιά ζωδίων
        frame_buttons.pack(pady=0)  # Τοποθέτηση του frame

        self.text_box = customtkinter.CTkTextbox(
            self, wrap=tk.WORD, width=360, height=155, font=("Arial", 15),
            fg_color=self.theme["display_bg"], text_color=self.theme["display_text"]
        )  # Περιοχή κειμένου για προβλέψεις
        self.text_box.pack(pady=5)  # Τοποθέτηση της περιοχής κειμένου

        self.btn_fortune = customtkinter.CTkButton(
            master=self,
            text="Πες μου και τον καφέ!",
            width=360,
            command=self.show_fortune,
            fg_color=self.theme["special_button_fg"],
            hover_color=self.theme["special_button_hover"],
            text_color=self.theme["ac_button_text"],
            corner_radius= 5,
            font=customtkinter.CTkFont(size=15, weight="bold")
        )  # Κουμπί για εμφάνιση "καφετζού" πρόβλεψης
        self.btn_fortune.pack_forget()  # Απόκρυψη του κουμπιού αρχικά

        row = 0  # Μετρητής γραμμής για το grid
        column = 0  # Μετρητής στήλης για το grid

        for name, slug in zodiac_data:  # Δημιουργία widgets για κάθε ζώδιο
            widget = ZoomingZodiac(frame_buttons, slug=slug, name=name, mode=self.mode)  # Widget ζωδίου
            widget.canvas.bind("<Button-1>", lambda e, s=slug, n=name: self.show_zodiac_prediction(s, n))  # Σύνδεση click
            widget.grid(row=row, column=column, padx=5, pady=2)  # Τοποθέτηση στο grid

            column += 1  # Επόμενη στήλη
            if column == 4:  # Αν φτάσουμε στη στήλη 4, πάμε νέα γραμμή
                column = 0
                row += 1

    """
    # ΑΝΑΠΑΡΑΓΩΓΗ ΜΟΥΣΙΚΗΣ
    Συνάρτηση για να παίξει μουσική όταν εμφανίζεται πρόβλεψη.
    """
    def play_dreamy_music(self):
        if self.sound_enabled:
            try:
                dreamy_music = pygame.mixer.Sound("assets/zodiac_sounds/dreamy_music.wav")  # Φόρτωση αρχείου ήχου
                dreamy_music.play()  # Αναπαραγωγή
            except FileNotFoundError:
                print("Το αρχείο 'dreamy_music.wav' δεν βρέθηκε.")

    """
    # ΠΡΟΒΛΕΨΗ ΗΜΕΡΑΣ ΓΙΑ ΖΩΔΙΟ
    Επιστρέφει μια τυχαία πρόβλεψη για το συγκεκριμένο ζώδιο, ίδια κάθε μέρα.
    """
    def get_today_prediction(self, zodiac_slug):
        seed_base = datetime.date.today().toordinal()  # Βάση seed για τυχαίο
        random.seed(f"{zodiac_slug}{seed_base}")  # Ορισμός seed
        return random.choice(funny_predictions.get(zodiac_slug, []))  # Επιλογή πρόβλεψης

    """
    # ΕΜΦΑΝΙΣΗ ΠΡΟΒΛΕΨΗΣ ΖΩΔΙΟΥ
    Εμφανίζει την πρόβλεψη για το επιλεγμένο ζώδιο και ξεκινά τα animations.
    """
    def show_zodiac_prediction(self, zodiac_slug, zodiac_name):
        global prediction_counter
        for delay in active_delays:  # Ακύρωση προηγούμενων χρονικών delays
            self.after_cancel(delay)
        active_delays.clear()

        self.play_dreamy_music()  # Αναπαραγωγή μουσικής
        today = datetime.date.today().isoformat()  # Ημερομηνία σήμερα

        if prediction_counter["date"] != today:  # Αν αλλάξει η μέρα, μηδενισμός μετρητή
            prediction_counter = {"date": today, "zodiacs": {}}

        if zodiac_slug in prediction_counter["zodiacs"]:  # Αν υπάρχει ήδη πρόβλεψη για το ζώδιο
            prediction = prediction_counter["zodiacs"][zodiac_slug]
        else:
            prediction = self.get_today_prediction(zodiac_slug)  # Νέα πρόβλεψη
            prediction_counter["zodiacs"][zodiac_slug] = prediction  # Αποθήκευση

        self.text_box.delete("1.0", "end")  # Καθαρισμός περιοχής κειμένου
        self.text_box.insert("end", f" ★ {zodiac_name} - {today}  ★\n\n")  # Εισαγωγή τίτλου
        active_delays.append(self.after(1000, lambda: self.text_box.insert("end", f"{prediction}")))  # Εμφάνιση πρόβλεψης με καθυστέρηση
        active_delays.append(self.after(3000, self.show_fortune_hint))  # Εμφάνιση hint μετά από λίγο

    """
    # ΕΜΦΑΝΙΣΗ HINT ΚΑΦΕΤΖΟΥ
    Εμφανίζει ένα μήνυμα hint με typing animation και ήχο.
    """
    def show_fortune_hint(self):
        for delay in active_delays:  # Ακύρωση προηγούμενων delays
            self.after_cancel(delay)
        active_delays.clear()

        message = random.choice(fortune_hint_messages)  # Επιλογή τυχαίου μηνύματος
        self.text_box.insert("end", "\n\n\n")  # Κενές γραμμές

        def type_hint(i=0):  # Συνάρτηση για "γράψιμο" χαρακτήρα-χαρακτήρα
            if i < len(message):
                if self.sound_enabled:
                    try:
                        blip_sound = pygame.mixer.Sound("blip.wav")  # Ήχος για κάθε χαρακτήρα
                        blip_sound.play()
                    except:
                        pass
                self.text_box.insert("end", message[i])  # Εισαγωγή χαρακτήρα
                self.text_box.see("end")  # Scroll στο τέλος
                active_delays.append(self.after(20, type_hint, i + 1))  # Επόμενος χαρακτήρας
            else:
                self.reveal_fortune_button()  # Όταν τελειώσει, εμφάνιση κουμπιού

        type_hint()  # Εκκίνηση typing

    """
    # ΕΜΦΑΝΙΣΗ ΚΟΥΜΠΙΟΥ ΚΑΦΕΤΖΟΥ ΜΕ ANIMATION
    Εμφανίζει το κουμπί "Πες μου και τον καφέ!" με animation και ήχο.
    """
    def reveal_fortune_button(self):
        if self.sound_enabled:
            try:
                magic_sound = pygame.mixer.Sound("assets/zodiac_sounds/magic.wav")  # Ήχος μαγείας
                magic_sound.play()
            except Exception as e:
                print("Ήχος μαγείας δεν βρέθηκε:", e)

        def animate_step(step=0):  # Animation για το κουμπί
            fade_colors = [
                "#1a1a1a", "#222222", "#292929", "#303030",
                "#363636", "#3d3d3d", "#444444", "#4b4b4b"
            ]
            if step == 0:
                self.btn_fortune.pack(pady=5)  # Εμφάνιση κουμπιού
                self.btn_fortune.configure(fg_color=fade_colors[0], font=("Arial", 1))
            if step < len(fade_colors):
                self.btn_fortune.configure(fg_color=fade_colors[step])  # Αλλαγή χρώματος
                self.btn_fortune.configure(font=("Arial", 1 + step))  # Αλλαγή μεγέθους γραμματοσειράς
                self.after(30, lambda: animate_step(step + 1))  # Επόμενο βήμα
            else:
                self.btn_fortune.configure(fg_color=self.theme["special_button_fg"], font=("Arial", 15, "bold"))  # Τελικό στυλ

        self.after(400, animate_step)  # Εκκίνηση animation

    """
    # ΕΜΦΑΝΙΣΗ ΠΡΟΒΛΕΨΗΣ ΚΑΦΕΤΖΟΥ
    Εμφανίζει μια τυχαία πρόβλεψη καφετζού με ήχο.
    """
    def show_fortune(self):
        self.play_dreamy_music()  # Ήχος
        prediction = random.choice(fortune_teller_quotes)  # Τυχαία πρόβλεψη
        self.text_box.delete("1.0", "end")  # Καθαρισμός
        self.text_box.insert("end", f" ★ Καφετζού Mode ★\n\n{prediction}")  # Εμφάνιση

"""
# ΒΟΗΘΗΤΙΚΗ ΣΥΝΑΡΤΗΣΗ ΔΗΜΙΟΥΡΓΙΑΣ FRAME
Επιστρέφει ένα νέο ZodiacFrame για χρήση σε άλλα modules.
"""
def create_zodiac_frame(parent, sound_enabled=True, mode="dark"):
    return ZodiacFrame(parent, sound_enabled=sound_enabled, mode=mode)

"""
# ΕΚΚΙΝΗΣΗ ΤΗΣ ΕΦΑΡΜΟΓΗΣ (TEST MODE)
Αν το αρχείο τρέχει μόνο του, δημιουργεί ένα παράθυρο για δοκιμή του ZodiacFrame.
"""
if __name__ == "__main__":
    app = customtkinter.CTk()  # Δημιουργία παραθύρου εφαρμογής
    app.geometry("400x600")  # Ορισμός διαστάσεων
    app.title("Zodiac Frame Test")  # Τίτλος παραθύρου

    frame = create_zodiac_frame(app, sound_enabled=True, mode="dark")  # Δημιουργία ZodiacFrame
    frame.pack(padx=10, pady=10, fill="both", expand=True)  # Τοποθέτηση στο παράθυρο

    app.mainloop()  # Εκκίνηση του mainloop της εφαρμογής
