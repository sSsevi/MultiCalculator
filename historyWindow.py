# historyWindow.py
# ----------------------------------------------------------
# Αυτή η μονάδα περιέχει την κλάση HistoryWindowModule,
# υπεύθυνη για τη δημιουργία και διαχείριση του popup παραθύρου
# ιστορικού, το οποίο μπορεί να χρησιμοποιηθεί από οποιονδήποτε
# τύπο αριθμομηχανής (standard, scientific κλπ).
# Περιλαμβάνει υποστήριξη για custom themes, scrollbar styling,
# δυναμική αλλαγή θέματος (apply_theme) και fallback τιμές.
# ----------------------------------------------------------

import customtkinter


class HistoryWindowModule:
    def __init__(self, parent, theme, history_log, insert_callback):
        """
        Αρχικοποίηση της μονάδας διαχείρισης παραθύρου ιστορικού.

        :param parent: Αναφορά στην αριθμομηχανή (π.χ. self).
        :param theme: Το λεξικό με τα χρώματα εμφάνισης.
        :param history_log: Η λίστα με τις εγγραφές ιστορικού.
        :param insert_callback: Συνάρτηση που καλείται όταν γίνει κλικ σε entry.
        """
        self.parent = parent
        self.theme = theme
        self.history_log = history_log
        self.insert_callback = insert_callback

        self.history_window = None
        self.scroll_frame = None

    # ----------------------------------------------------------
    # Δημιουργία και εμφάνιση παραθύρου ιστορικού (popup)
    # ----------------------------------------------------------
    def open(self):
        """
        Εμφανίζει το παράθυρο ιστορικού. Αν είναι ήδη ανοιχτό το φέρνει μπροστά.
        Αν η λίστα ιστορικού είναι άδεια, δεν κάνει τίποτα.
        """
        if not self.history_log:
            return

        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        # Δημιουργία νέου Toplevel παραθύρου
        self.history_window = customtkinter.CTkToplevel(self.parent)
        self.history_window.title("History")
        self.history_window.attributes("-topmost", True)

        # Θέση παραθύρου (τοποθέτηση όπως στο scientific)
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        popup_x = parent_x - 6
        popup_y = parent_y - 70
        self.history_window.geometry(f"300x300+{popup_x}+{popup_y}")

        # Εφαρμογή θέματος με fallback σε default τιμές
        self.history_window.configure(
            fg_color=self.theme.get("popup_history_bg", "#222222"),
            border_color=self.theme.get("popup_history_border", "#4f4f4f"),
            border_width=1
        )

        # Δημιουργία scrollable frame με προσαρμοσμένα scrollbar colors
        self.scroll_frame = customtkinter.CTkScrollableFrame(
            self.history_window,
            fg_color=self.theme.get("popup_history_fg", "#000000"),
            scrollbar_fg_color=self.theme.get("popup_history_scrollbar_bg", "#2a2a2a"),
            scrollbar_button_color=self.theme.get("popup_history_scrollbar_thumb", "#6e6e6e")
        )
        self.scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self._populate_entries()

    # ----------------------------------------------------------
    # Εμφάνιση εγγραφών ιστορικού στο scroll frame
    # ----------------------------------------------------------
    def _populate_entries(self):
        """
        Δημιουργεί κουμπιά στο scrollable frame για τις 50 τελευταίες εγγραφές.
        """
        for entry in reversed(self.history_log[-50:]):
            btn = customtkinter.CTkButton(
                self.scroll_frame,
                text=entry,
                anchor="w",
                height=30,
                font=("Arial", 12),
                fg_color=self.theme.get("popup_history_line_bg", "#4f4f4f"),
                hover_color=self.theme.get("popup_history_hover", "#6e6e6e"),
                text_color=self.theme.get("popup_history_text", "#ffffff"),
                command=lambda e=entry: self.insert_callback(e)
            )
            btn.pack(fill="x", pady=2)

    # ----------------------------------------------------------
    # Δυναμική αλλαγή θέματος σε ήδη ανοιχτό παράθυρο
    # ----------------------------------------------------------
    def apply_theme(self, theme):
        """
        Εφαρμόζει νέο θέμα στο ανοιχτό παράθυρο ιστορικού.

        :param theme: Το νέο λεξικό με τις χρωματικές τιμές.
        """
        self.theme = theme

        if self.history_window and self.history_window.winfo_exists():
            self.history_window.configure(
                fg_color=self.theme.get("popup_history_bg", "#222222"),
                border_color=self.theme.get("popup_history_border", "#4f4f4f"),
                border_width=self.theme.get("popup_history_border_width", 1)
            )

            if self.scroll_frame:
                self.scroll_frame.configure(
                    fg_color=self.theme.get("popup_history_fg", "#000000"),
                    scrollbar_fg_color=self.theme.get("popup_history_scrollbar_bg", "#2a2a2a"),
                    scrollbar_button_color=self.theme.get("popup_history_scrollbar_thumb", "#6e6e6e")
                )

                # Καθαρισμός και ανανέωση entries
                for child in self.scroll_frame.winfo_children():
                    child.destroy()
                self._populate_entries()



                """ για έλεγχο κλειδιών
                Κλειδί (key)	            Περιγραφή
                popup_history_bg	        Φόντο παραθύρου ιστορικού
                popup_history_border	    Χρώμα περιγράμματος (border) παραθύρου
                popup_history_border_width	Πάχος περιγράμματος (border width)
                popup_history_fg	        Φόντο scrollable περιοχής
                popup_history_scrollbar_bg	Χρώμα φόντου scrollbar
                popup_history_scrollbar_thumb	Χρώμα "χειρολαβής" (thumb) του scrollbar
                popup_history_line_bg	    Φόντο κουμπιού για κάθε entry
                popup_history_hover	        Hover χρώμα κάθε κουμπιού ιστορικού
                popup_history_text	        Χρώμα κειμένου στα κουμπιά ιστορικού
                """
