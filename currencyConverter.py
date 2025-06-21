#currencyConverter

# currencyConverter.py
# ==========================================================
# Αυτό το αρχείο υλοποιεί ένα γραφικό widget μετατροπής νομισμάτων ως υποκλάση του customtkinter.CTkFrame.
# Παρέχει τη δυνατότητα στον χρήστη να:
# - Επιλέξει αρχικό και τελικό νόμισμα.
# - Εισάγει ποσό προς μετατροπή.
# - Δει το αποτέλεσμα της μετατροπής και την τρέχουσα ισοτιμία.
# Χρησιμοποιεί δεδομένα από το API exchangerate-api.com για την απόκτηση ισοτιμιών.
# Η εμφάνιση προσαρμόζεται δυναμικά με βάση το θέμα (theme) που παρέχεται.
# Περιλαμβάνει επίσης χειρισμό σφαλμάτων για μη έγκυρες εισόδους ή προβλήματα κατά την κλήση του API.
# ==========================================================


import customtkinter                # Εισαγωγή της βιβλιοθήκης customtkinter για τη δημιουργία γραφικών στοιχείων
from themeManager import get_theme  # Εισαγωγή της συνάρτησης get_theme για τη λήψη του θέματος εμφάνισης
import requests                     # Εισαγωγή της βιβλιοθήκης requests για την εκτέλεση HTTP αιτημάτων

#=========== CurrencyConverter Class ===========#
class CurrencyConverter(customtkinter.CTkFrame):    # Κλάση που υλοποιεί το widget μετατροπής νομισμάτων
    def __init__(self, master, theme, sound_enabled, **kwargs): # Αρχικοποίηση της κλάσης με παραμέτρους master, theme και sound_enabled
        super().__init__(master, fg_color=theme.get("background", "#222222"), corner_radius=0, **kwargs)
        self.theme = theme  # Αποθήκευση του θέματος εμφάνισης
        self.sound_enabled = sound_enabled  # Αποθήκευση της κατάστασης ήχου (αν είναι ενεργοποιημένος ή όχι)
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"   # Βασικό URL για την κλήση του API για τις ισοτιμίες

        #=========== Grid Configuration ===========#
        self.grid_columnconfigure(0, weight=1)  # Ρύθμιση βάρους για την πρώτη στήλη
        self.grid_columnconfigure(1, weight=1)  # Ρύθμιση βάρους για τη δεύτερη στήλη
        self.grid_columnconfigure(2, weight=1)  # Ρύθμιση βάρους για την τρίτη στήλη
        self.grid_rowconfigure(0, weight=1) # Ρύθμιση βάρους για την πρώτη γραμμή
        self.grid_rowconfigure(1, weight=1) # Ρύθμιση βάρους για τη δεύτερη γραμμή
        self.grid_rowconfigure(2, weight=1) # Ρύθμιση βάρους για την τρίτη γραμμή
        self.grid_rowconfigure(3, weight=1) # Ρύθμιση βάρους για την τέταρτη γραμμή
        self.grid_rowconfigure(4, weight=1) # Ρύθμιση βάρους για την πέμπτη γραμμή
        self.grid_rowconfigure(5, weight=1) # Ρύθμιση βάρους για την έκτη γραμμή

        #=========== Title Label ===========#
        title_text_color = self.theme.get("display_text", "#00ff00")   # Χρώμα κειμένου τίτλου
        self.title_label = customtkinter.CTkLabel(  
            self, 
            text="CURRENCY CONVERTER",  # Τίτλος της εφαρμογής
            font=("Arial", 20, "bold"),
            text_color=title_text_color
            )  
        self.title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)  # Τοποθέτηση της ετικέτας τίτλου

        #=========== Currency Selection ===========#
        # Ετικέτα "Από"
        from_label_color = self.theme.get("label_text", "#ffffff")      # Χρώμα κειμένου ετικέτας "Από"
        self.from_label = customtkinter.CTkLabel(
            self, 
            text="FROM:", 
            font=("Arial", 16, "bold"),
            text_color=from_label_color
            )
        self.from_label.grid(row=1, column=0, padx=(20, 5), pady=(0, 0), sticky="s")    # Τοποθέτηση της ετικέτας "Από"

        # Ετικέτα "Προς"
        to_label_color = self.theme.get("label_text", "#ffffff")   # Χρώμα κειμένου ετικέτας "Προς"
        self.to_label = customtkinter.CTkLabel(
            self, 
            text="TO:", 
            font=("Arial", 16, "bold"),
            text_color=to_label_color
            ) 
        self.to_label.grid(row=1, column=2, padx=(5, 20), pady=(0, 0), sticky="s")  # Τοποθέτηση της ετικέτας "Προς"

        # Combobox για επιλογή αρχικού νομίσματος
        combobox_bg_color = self.theme.get("menu_button_bg", "#eb7c16")             # Χρώμα φόντου combobox
        combobox_dropdown_fg_color = self.theme.get("dropdown_fg", "#4f4f4f")       # Χρώμα φόντου dropdown combobox
        combobox_text_color = self.theme.get("menu_text_color", "#ffffff")          # Χρώμα κειμένου combobox
        self.from_currency_menu = customtkinter.CTkComboBox(
            self,
            values=["USD", "EUR", "GBP", "JPY", "CAD"],     # Δημιουργία combobox για επιλογή νομίσματος
            button_color=combobox_bg_color,                 # Χρώμα κουμπιού combobox
            dropdown_fg_color=combobox_dropdown_fg_color,   # Χρώμα φόντου dropdown combobox
            dropdown_text_color=combobox_text_color,        # Χρώμα κειμένου dropdown combobox
            text_color=combobox_text_color,                 # Χρώμα κειμένου combobox
            border_width=2,                                 # Πλάτος περιγράμματος combobox
            border_color=self.theme.get("menu_button_bg", "#eb7c16") # Χρώμα περιγράμματος combobox, αν δεν υπάρχει ορισμένο χρώμα στο θέμα, χρησιμοποιούμε #eb7c16	
            )                 
        self.from_currency_menu.set("USD")                  # Αρχική τιμή για το combobox
        self.from_currency_menu.grid(row=2, column=0, padx=(20, 5), pady=(0, 10), sticky="ew")

        # Combobox για επιλογή τελικού νομίσματος
        self.to_currency_menu = customtkinter.CTkComboBox(
            self, 
            values=["EUR", "GBP", "JPY", "CAD", "USD"],     # Δημιουργία combobox για επιλογή τελικού νομίσματος
            button_color=combobox_bg_color,                 # Χρώμα κουμπιού combobox
            dropdown_fg_color=combobox_dropdown_fg_color,   # Χρώμα φόντου dropdown combobox
            dropdown_text_color=combobox_text_color,        # Χρώμα κειμένου dropdown combobox
            text_color=combobox_text_color,                 # Χρώμα κειμένου combobox
            border_width=2,                                 # Πλάτος περιγράμματος combobox
            border_color=self.theme.get("menu_button_bg", "#eb7c16") # Χρώμα περιγράμματος combobox, αν δεν υπάρχει ορισμένο χρώμα στο θέμα, χρησιμοποιούμε #eb7c16
            )   
        self.to_currency_menu.set("EUR")  # Αρχική τιμή
        self.to_currency_menu.grid(row=2, column=2, padx=(5, 20), pady=(0, 10), sticky="ew")   # Τοποθέτηση του combobox για επιλογή τελικού νομίσματος

        #=========== Amount Input ===========#
        # Ετικέτα "Ποσό"
        amount_label_color = self.theme.get("label_text", "#ffffff")   # Χρώμα κειμένου ετικέτας "Ποσό"
        self.amount_label = customtkinter.CTkLabel(
            self, text="AMOUNT:", 
            font=("Arial", 16, "bold"),
            text_color=amount_label_color
            ) 
        self.amount_label.grid(row=3, column=0, columnspan=4, pady=(30, 2), sticky="s")     # Τοποθέτηση της ετικέτας "Ποσό"

        # Πεδίο εισαγωγής ποσού
        entry_fg_color = self.theme.get("entry_fg", "#ffffff")      # Χρώμα φόντου πεδίου εισαγωγής
        text_color = self.theme.get("text_input", "#000000")        # Χρώμα κειμένου πεδίου εισαγωγής
        self.amount_entry = customtkinter.CTkEntry(
            self, 
            fg_color=entry_fg_color, 
            text_color=text_color,
            font=("Arial", 20, "bold"),
            height=40,
            justify="center",  # Κεντράρισμα του κειμένου στο πεδίο εισαγωγής
            placeholder_text="Enter amount",  # Placeholder κείμενο για το πεδίο εισαγωγής
            placeholder_text_color=self.theme.get("placeholder_text","#BEBEBE")  # Χρώμα placeholder κειμένου
            )
        self.amount_entry.grid(row=4, column=0, columnspan=4, padx=80, pady=(0, 30), sticky="ew")    # Τοποθέτηση του πεδίου εισαγωγής ποσού

        #=========== Convert Button ===========#
        button_fg_color = self.theme.get("special_button_fg", "#eb7c16")    # Χρώμα φόντου κουμπιού μετατροπής
        button_text_color = self.theme.get("op_button_text","#ffffff")         # Χρώμα κειμένου κουμπιού μετατροπής
        button_hover_color = self.theme.get("op_hover", "#5e5e5e")      # Χρώμα hover κουμπιού μετατροπής
        self.convert_button = customtkinter.CTkButton(  
            self,                               # Δημιουργία κουμπιού μετατροπής            
            text="CONVERT",                     # Κείμενο κουμπιού μετατροπής
            font=("Arial", 16, "bold"),
            height=40,                          # Ύψος κουμπιού μετατροπής
            command=self.convert_currency,      # Συνάρτηση που καλείται όταν πατάμε το κουμπί μετατροπής 
            fg_color=button_fg_color,           # Χρώμα φόντου κουμπιού μετατροπής  
            text_color=button_text_color,       # Χρώμα κειμένου κουμπιού μετατροπής
            hover_color=button_hover_color      # Χρώμα hover κουμπιού μετατροπής
            ) 
        self.convert_button.grid(row=5, column=0, columnspan=4, padx=80, pady=10, sticky="ew")  # Τοποθέτηση του κουμπιού μετατροπής

        #=========== Result Display ===========#
        # Ετικέτα αποτελέσματος
        result_label_color = self.theme.get("label_text", "#ffffff") # Χρώμα κειμένου ετικέτας αποτελέσματος
        self.result_label = customtkinter.CTkLabel(     
            self,                           # Δημιουργία ετικέτας αποτελέσματος
            text="RESULT:",                 # Κείμενο ετικέτας αποτελέσματος
            font=("Arial", 16, "bold"),     # Γραμματοσειρά ετικέτας αποτελέσματος
            text_color=result_label_color   # Χρώμα κειμένου ετικέτας αποτελέσματος
            )
        self.result_label.grid(row=6, column=0, padx=(20, 5), pady=(10, 100), sticky="e")

        # Πεδίο εμφάνισης αποτελέσματος
        result_value_color = self.theme.get("display_text", "#00ff00")  # Χρώμα κειμένου πεδίου εμφάνισης αποτελέσματος 
        # Δημιουργία ετικέτας για την εμφάνιση του αποτελέσματος της μετατροπής
        self.result_value_label = customtkinter.CTkLabel(
            self, 
            text="",                        # Αρχικά κενό, θα ενημερωθεί μετά τη μετατροπή
            font=("Arial", 20, "bold"),     # Γραμματοσειρά ετικέτας αποτελέσματος
            text_color=result_value_color   # Χρώμα κειμένου ετικέτας αποτελέσματος
            )
        self.result_value_label.grid(row=6, column=1, columnspan=3, padx=(5, 20), pady=(5, 100), sticky="w")    # Τοποθέτηση της ετικέτας αποτελέσματος

        #=========== Exchange Rate Display ===========#
        # Νέα ετικέτα για εμφάνιση ισοτιμίας (αρχικά κενή)
        rate_text_color = self.theme.get("placeholder_text",  "#aaaaaa")  # Χρώμα κειμένου ετικέτας ισοτιμίας
        self.exchange_rate_label = customtkinter.CTkLabel(      # Δημιουργία ετικέτας για την εμφάνιση της ισοτιμίας
            self,   
            text="",                        # Αρχικά κενό, θα ενημερωθεί μετά τη μετατροπή
            font=("Arial", 12, "italic"),   # Γραμματοσειρά ετικέτας ισοτιμίας
            text_color=rate_text_color      # Χρώμα κειμένου ετικέτας ισοτιμίας
        )
        self.exchange_rate_label.grid(row=7, column=0, columnspan=4, padx=20, pady=(0, 20), sticky="ew")    # Τοποθέτηση της ετικέτας ισοτιμίας

    #=========== Conversion Logic ===========#
    def convert_currency(self): # Συνάρτηση που καλείται όταν πατάμε το κουμπί μετατροπής
        from_currency = self.from_currency_menu.get()   # Λήψη του νομίσματος από το οποίο μετατρέπουμε
        to_currency = self.to_currency_menu.get()       # Λήψη του νομίσματος στο οποίο μετατρέπουμε
        amount_str = self.amount_entry.get()            # Λήψη του ποσού από το πεδίο εισαγωγής

        try:
            amount = float(amount_str)  # Μετατροπή του ποσού σε float, αν δεν είναι έγκυρο θα προκαλέσει ValueError
            # Κάνουμε κλήση στο API για να λάβουμε τις ισοτιμίες
            url = f"{self.base_url}{from_currency.upper()}" # Δημιουργία URL για το API με βάση το νόμισμα από το οποίο μετατρέπουμε
            response = requests.get(url)    # Κλήση στο API για να λάβουμε τις ισοτιμίες
            response.raise_for_status()     # Αν υπάρχει σφάλμα στην κλήση, θα το αναδείξει
            data = response.json()          # Μετατροπή της απάντησης σε JSON
            rates = data.get("rates")       # Λήψη των ισοτιμιών από το JSON

            if rates and to_currency.upper() in rates:          # Έλεγχος αν οι ισοτιμίες υπάρχουν και αν το νόμισμα στο οποίο μετατρέπουμε είναι έγκυρο
                conversion_rate = rates[to_currency.upper()]    # Λήψη της ισοτιμίας για το νόμισμα στο οποίο μετατρέπουμε
                result = amount * conversion_rate               # Υπολογισμός του αποτελέσματος της μετατροπής
                self.result_value_label.configure(text=f"{result:.2f} {to_currency.upper()}")   # Ενημέρωση της ετικέτας αποτελέσματος με το αποτέλεσμα της μετατροπής
                #--------------------------------------------------
                rate_text = f"(1 {from_currency.upper()} = {conversion_rate:.4f} {to_currency.upper()})"    # Δημιουργία κειμένου για την ισοτιμία
                self.exchange_rate_label.configure(text=rate_text)  # Ενημέρωση της ετικέτας ισοτιμίας με την ισοτιμία της μετατροπής
                #--------------------------------------------------
            else:
                self.result_value_label.configure(text="Conversion rate not found") # Αν δεν βρεθεί η ισοτιμία, ενημερώνουμε την ετικέτα αποτελέσματος
                self.exchange_rate_label.configure(text="")                         # Αν δεν βρεθεί η ισοτιμία, καθαρίζουμε και την ετικέτα ισοτιμίας

        except ValueError:  # Αν η είσοδος ποσού δεν είναι έγκυρη (π.χ. δεν είναι αριθμός)
            self.result_value_label.configure(text="Invalid Amount")            # Ενημέρωση της ετικέτας αποτελέσματος με μήνυμα σφάλματος
            self.exchange_rate_label.configure(text="")                         # Αν δεν είναι έγκυρη η είσοδος ποσού, καθαρίζουμε και την ετικέτα ισοτιμίας

        except requests.exceptions.RequestException as e:                       # Αν υπάρχει σφάλμα κατά την κλήση στο API
            self.result_value_label.configure(text=f"Error fetching data: {e}") # Ενημέρωση της ετικέτας αποτελέσματος με μήνυμα σφάλματος
            self.exchange_rate_label.configure(text="")                         # Αν υπάρχει σφάλμα κατά την κλήση στο API, καθαρίζουμε και την ετικέτα ισοτιμίας
    
    #=========== Interface Compatibility Methods ===========#
    # Οι παρακάτω συναρτήσεις είναι απαραίτητες για να διατηρήσουμε τη συμβατότητα με το interface, αλλά δεν χρησιμοποιούνται σε αυτό το mode
    def get_display_value(self):
        return ""  # Δεν χρειαζόμαστε τιμή display για αυτό το mode

    def set_display_value(self, value): # Δεν χρειαζόμαστε τιμή display για αυτό το mode
        pass  # Δεν χρειαζόμαστε τιμή display για αυτό το mode, την καλούμε μόνο για να διατηρήσουμε τη συμβατότητα με το interface

    def handle_key_input(self, key):    # Διαχείριση εισόδου από το πληκτρολόγιο
        if key == "\x08":  # Backspace 
            self.amount_entry.delete(0, customtkinter.END)  # Διαγραφή του περιεχομένου του πεδίου εισαγωγής ποσού
        elif key == "\r":  # Enter  
            self.convert_currency() # Κλήση της συνάρτησης μετατροπής όταν πατάμε Enter

#=========== Standalone Test ===========#
if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("400x600")
    theme = get_theme("dark")  # Μπορείς να αλλάξεις το θέμα για δοκιμή
    converter = CurrencyConverter(app, theme, True)
    converter.pack(fill="both", expand=True, padx=20, pady=(20, 40))
    app.mainloop()