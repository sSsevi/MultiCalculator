# =========================
# Εισαγωγές βιβλιοθηκών και modules
# =========================
"""
Εισάγει όλα τα απαραίτητα modules και βιβλιοθήκες για το GUI, διαχείριση CSV, επιλογή χρώματος, previews, tooltips και εικόνες.
"""
import customtkinter
import tkinter as tk
import csv
from tkinter import colorchooser

from scientificCalcPreview import ScientificCalcPreview
from standardPreview import StandardPreview
from tooltipInjector import inject_tooltips_from_map
from tooltipMap import TooltipMap
from tooltipMap import TopBarTooltipMap
from mainCalcPreview import MainCalcPreview
from mainCalc import MainCalculatorApp
from PIL import Image

# =========================
# Αρχικοποίηση εμφάνισης customtkinter
# =========================
"""
Ορίζει το appearance mode του customtkinter σε "dark" για σκοτεινό θέμα.
"""
customtkinter.set_appearance_mode("dark")

# =========================
# Σταθερά για το αρχείο CSV
# =========================
"""
Ορίζει το όνομα του αρχείου CSV που περιέχει τα themes.
"""
CSV_FILE = "themeMatrix.csv"

# =========================
# Συνάρτηση: Φόρτωση theme matrix από CSV
# =========================
"""
Διαβάζει το αρχείο CSV και επιστρέφει τη λίστα με τα themes και τα ονόματα των πεδίων.
"""
def load_theme_matrix_from_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        matrix = [row for row in reader]
        return matrix, fieldnames

# =========================
# Συνάρτηση: Αποθήκευση theme matrix σε CSV
# =========================
"""
Αποθηκεύει τη λίστα με τα themes και τα πεδία στο αρχείο CSV.
"""
def save_theme_matrix_to_csv(matrix, fieldnames, path):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matrix)

# =========================
# Κύρια Κλάση: ThemeEditor (GUI εφαρμογή)
# =========================
"""
Η βασική κλάση του Theme Editor GUI. Διαχειρίζεται το παράθυρο, τα δεδομένα, τα widgets και τις λειτουργίες του editor.
"""
class ThemeEditor(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎨 Theme Editor")
        self.geometry("1200x850")
        self.configure(padx=20, pady=20)

        # Φόρτωση δεδομένων και αρχικοποίηση μεταβλητών
        self.matrix, self.headers = load_theme_matrix_from_csv(CSV_FILE)
        self.themes = self.headers[1:]
        self.entries = {}
        self.preview_boxes = {}
        self.original_values = {}
        self.previous_values = {}

        # Δημιουργία UI
        self.build_ui()

    # =========================
    # Συνάρτηση: Δημιουργία UI
    # =========================
    """
    Δημιουργεί όλα τα widgets του γραφικού περιβάλλοντος: επιλογή θέματος, mode, scrollable λίστα χρωμάτων, preview, κουμπιά αποθήκευσης και επαναφοράς.
    """
    def build_ui(self):
        # Top controls (επιλογή θέματος, mode)
        self.top_controls = customtkinter.CTkFrame(self, fg_color="#222222")
        self.top_controls.pack(fill="x", pady=(0, 15))

        # Επιλογή θέματος
        self.combo = customtkinter.CTkOptionMenu(
            self.top_controls,
            values=self.themes,
            command=self.display_theme,
            fg_color="#eb7c16",
            button_color="#eb7c16",
            button_hover_color="#d06c11")
        self.combo.set(self.themes[0])
        self.combo.pack(side="left", padx=10, pady=10)

        # Επιλογή mode (Standard/Scientific)
        self.toggle_mode = customtkinter.StringVar(value="Scientific")
        self.toggle = customtkinter.CTkSegmentedButton(
            self.top_controls,
            fg_color="#eb7c16",
            selected_color="#cc4d15",
            unselected_color="#eb7c16",
            selected_hover_color="#eb7c16",
            unselected_hover_color="#eb7c16",
            values=["Standard", "Scientific"],
            variable=self.toggle_mode,
            command=self.build_preview
        )
        self.toggle.pack(side="left", padx=10)

        # Κύριο frame
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Scrollable frame για τα χρώματα
        self.scroll = customtkinter.CTkScrollableFrame(self.main_frame, width=600)
        self.scroll.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Preview frame
        self.preview_frame = customtkinter.CTkFrame(self.main_frame)
        self.preview_frame.pack(side="left", fill="both", expand=True)

        # Δημιουργία γραμμών για κάθε key
        """
        Για κάθε key (στοιχείο theme), δημιουργεί γραμμή με label, entry, preview, picker, undo και reset κουμπιά.
        """
        for row_index, row in enumerate(self.matrix):
            key = row["key"]
            # Ετικέτα key
            key_label = customtkinter.CTkLabel(self.scroll, text=key, width=180, anchor="w")
            key_label.grid(row=row_index, column=0, padx=5, pady=2)

            # Entry για το χρώμα
            entry = customtkinter.CTkEntry(self.scroll, width=120)
            entry.grid(row=row_index, column=1, padx=5)
            self.entries[key] = entry

            # Preview κουτί χρώματος
            preview = customtkinter.CTkLabel(self.scroll, text="", width=30)
            preview.grid(row=row_index, column=2, padx=5)
            self.preview_boxes[key] = preview

            # Bind events για ενημέρωση preview
            entry.bind("<Return>", lambda e, k=key: self.update_preview(k))
            entry.bind("<FocusOut>", lambda e, k=key: self.update_preview(k))
            entry.bind("<Button-3>", self.make_context_menu_callback(entry))

            # Κουμπί επιλογής χρώματος
            btn = customtkinter.CTkButton(self.scroll, text="🎨", width=30, fg_color="#4f4f4f", text_color="#ff80c0",
                                          command=self.make_picker(entry, preview))
            btn.grid(row=row_index, column=3, padx=2)

            # Κουμπί undo
            undo_btn = customtkinter.CTkButton(self.scroll, text="↩️", width=0, fg_color="#4f4f4f", text_color="#00ffff",
                                               command=lambda k=key: self.undo_change(k))
            undo_btn.grid(row=row_index, column=4, padx=(2,0))

            # Κουμπί reset
            reset_btn = customtkinter.CTkButton(self.scroll, text="♻️", width=30, fg_color="#4f4f4f", text_color="#008000",
                                                command=lambda k=key: self.reset_to_original(k))
            reset_btn.grid(row=row_index, column=5, padx=2)

        # Κουμπί αποθήκευσης
        self.save_button = customtkinter.CTkButton(self, text="💾 Αποθήκευση", fg_color="#eb7c16", command=self.save_theme)
        self.save_button.pack(pady=(10, 5))

        # Κουμπί επαναφοράς όλων
        self.reset_all_button = customtkinter.CTkButton(self, text="♻️ Επαναφορά Όλων", fg_color="#eb7c16", command=self.reset_all)
        self.reset_all_button.pack(pady=(0, 20))

        # Εμφάνιση αρχικού θέματος και preview
        self.display_theme(self.themes[0])
        self.build_preview()

    # =========================
    # Συνάρτηση: Δημιουργία context menu για entry
    # =========================
    """
    Επιστρέφει callback για εμφάνιση context menu (δεξί κλικ) σε κάθε entry.
    """
    def make_context_menu_callback(self, entry):
        return lambda e: self.show_context_menu(e, entry)

    # =========================
    # Συνάρτηση: Εμφάνιση context menu (copy/paste/cut)
    # =========================
    """
    Εμφανίζει context menu με επιλογές copy, paste, cut για το entry.
    """
    def show_context_menu(self, event, entry):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Copy", command=lambda: self.copy(entry))
        menu.add_command(label="Paste", command=lambda: self.paste(entry))
        menu.add_command(label="Cut", command=lambda: self.cut(entry))
        menu.tk_popup(event.x_root, event.y_root)

    # =========================
    # Συνάρτηση: Copy από entry
    # =========================
    """
    Αντιγράφει το περιεχόμενο του entry στο clipboard.
    """
    def copy(self, entry):
        try:
            self.clipboard_clear()
            self.clipboard_append(entry.get())
        except Exception:
            pass

    # =========================
    # Συνάρτηση: Paste σε entry
    # =========================
    """
    Επικολλά το περιεχόμενο του clipboard στο entry και αποθηκεύει την προηγούμενη τιμή για undo.
    """
    def paste(self, entry):
        try:
            text = self.clipboard_get()
            self.previous_values[entry] = entry.get()
            entry.delete(0, "end")
            entry.insert(0, text)
        except Exception:
            pass

    # =========================
    # Συνάρτηση: Cut από entry
    # =========================
    """
    Κόβει το περιεχόμενο του entry, το βάζει στο clipboard και αποθηκεύει την προηγούμενη τιμή για undo.
    """
    def cut(self, entry):
        try:
            self.clipboard_clear()
            self.clipboard_append(entry.get())
            self.previous_values[entry] = entry.get()
            entry.delete(0, "end")
        except Exception:
            pass

    # =========================
    # Συνάρτηση: Picker επιλογής χρώματος
    # =========================
    """
    Επιστρέφει συνάρτηση που ανοίγει color picker, ενημερώνει το entry και το preview με το νέο χρώμα.
    """
    def make_picker(self, entry, preview):
        def pick():
            color = colorchooser.askcolor(title="Επιλογή Χρώματος", initialcolor=entry.get())[1]
            if color:
                self.previous_values[entry] = entry.get()
                entry.delete(0, "end")
                entry.insert(0, color)
                preview.configure(fg_color=color)
                self.update_preview_live()
        return pick

    # =========================
    # Συνάρτηση: Ενημέρωση preview για συγκεκριμένο key
    # =========================
    """
    Ενημερώνει το preview κουτί για το συγκεκριμένο key αν η τιμή είναι έγκυρο hex χρώμα.
    """
    def update_preview(self, key):
        entry = self.entries[key]
        value = entry.get()
        if value.startswith("#") and len(value) == 7:
            self.preview_boxes[key].configure(fg_color=value)
            self.update_preview_live()

    # =========================
    # Συνάρτηση: Ενημέρωση live preview
    # =========================
    """
    Ενημερώνει το live preview calculator και το top bar με τα τρέχοντα χρώματα.
    """
    def update_preview_live(self):
        if hasattr(self, "calc_preview"):
            theme_dict = {k: self.entries[k].get() for k in self.entries}
            self.calc_preview.apply_theme(theme_dict)

        if hasattr(self, "top_bar"):
            self.top_bar.set_theme(theme_dict)

    # =========================
    # Συνάρτηση: Εμφάνιση επιλεγμένου θέματος
    # =========================
    """
    Φορτώνει τις τιμές του επιλεγμένου θέματος στα entries και στα preview boxes.
    """
    def display_theme(self, theme_name):
        self.original_values.clear()
        self.previous_values.clear()
        for row in self.matrix:
            key = row["key"]
            value = row.get(theme_name, "") or "#ffffff"
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, value)
            self.preview_boxes[key].configure(fg_color=value)
            self.original_values[key] = value
        self.update_preview_live()

    # =========================
    # Συνάρτηση: Undo αλλαγής για συγκεκριμένο key
    # =========================
    """
    Επαναφέρει το entry στην προηγούμενη τιμή του (αν υπάρχει) για το συγκεκριμένο key.
    """
    def undo_change(self, key):
        entry = self.entries[key]
        prev_value = self.previous_values.get(entry)
        if prev_value:
            entry.delete(0, "end")
            entry.insert(0, prev_value)
            self.update_preview(key)

    # =========================
    # Συνάρτηση: Επαναφορά αρχικής τιμής για συγκεκριμένο key
    # =========================
    """
    Επαναφέρει το entry στην αρχική τιμή του theme για το συγκεκριμένο key.
    """
    def reset_to_original(self, key):
        value = self.original_values.get(key)
        if value:
            entry = self.entries[key]
            entry.delete(0, "end")
            entry.insert(0, value)
            self.update_preview(key)

    # =========================
    # Συνάρτηση: Επαναφορά όλων των τιμών στις αρχικές
    # =========================
    """
    Επαναφέρει όλα τα entries στις αρχικές τιμές του επιλεγμένου theme.
    """
    def reset_all(self):
        for key in self.entries:
            self.reset_to_original(key)

    # =========================
    # Συνάρτηση: Αποθήκευση αλλαγών στο CSV
    # =========================
    """
    Αποθηκεύει τις αλλαγές του τρέχοντος theme στο CSV αρχείο και εμφανίζει μήνυμα επιτυχίας.
    """
    def save_theme(self):
        theme_name = self.combo.get()
        for row in self.matrix:
            key = row["key"]
            row[theme_name] = self.entries[key].get()
        save_theme_matrix_to_csv(self.matrix, self.headers, CSV_FILE)
        self.display_theme(theme_name)
        saved_label = customtkinter.CTkLabel(self, text=f"✅ Αποθηκεύτηκε το θέμα: {theme_name}", text_color="green")
        saved_label.pack()
        saved_label.after(3000, saved_label.destroy)

    # =========================
    # Συνάρτηση: Δημιουργία preview calculator
    # =========================
    """
    Δημιουργεί το preview του calculator (standard ή scientific) και το top bar, εφαρμόζοντας τα τρέχοντα χρώματα.
    """
    def build_preview(self, *args):
        # Καθαρισμός προηγούμενων widgets
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        # Εξωτερικό container preview
        self.fixed_preview_container = customtkinter.CTkFrame(
            self.preview_frame,
            width=400,
            height=600,
            border_width=2,
            border_color="#444444",
            corner_radius=10
        )
        self.fixed_preview_container.pack(pady=20)
        self.fixed_preview_container.pack_propagate(False)

        # Φόρτωση theme & calculator
        theme_dict = {k: self.entries[k].get() for k in self.entries}
        mode = self.toggle_mode.get()

        if mode == "Standard":
            self.calc_preview = StandardPreview(self.fixed_preview_container, theme_dict)
        else:
            self.calc_preview = ScientificCalcPreview(self.fixed_preview_container, theme_dict)

        # Top bar preview
        self.top_bar = MainCalcPreview(self.fixed_preview_container)
        self.top_bar.pack(fill="x", pady=(0, 0))

        # Ο calculator γεμίζει το fixed container
        self.calc_preview.pack(expand=True, fill="both")

        # Εισαγωγή tooltips
        inject_tooltips_from_map(self.calc_preview, TooltipMap)
        print("Available widgets:", self.__dict__.keys())
        inject_tooltips_from_map(self.top_bar, TopBarTooltipMap)

# =========================
# Εκκίνηση εφαρμογής
# =========================
"""
Εκκινεί την εφαρμογή ThemeEditor αν το αρχείο τρέχει ως main.
"""
if __name__ == "__main__":
    app = ThemeEditor()
    app.mainloop()
