# scientificCalcPreview.py
# ----------------------------------------------------------


import customtkinter  # Βασικό GUI toolkit με υποστήριξη themes και responsive widgets

from themeLoader import get_theme  # Επιστρέφει λεξικό με χρώματα για κάθε theme (dark, light κλπ.)
from buttonHandler import on_button_click  # Λογική χειρισμού πατημάτων κουμπιών
from mpmath import mpf  # Για αριθμητική ακρίβειας πολλών ψηφίων (π.χ. για πράξεις με π)
from historyWindow import HistoryWindowModule

import tkinter as tk  # Αν δεν έχεις ήδη

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 40
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid",
                         borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=4)

    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None



class ScientificCalcPreview(customtkinter.CTkFrame):
    def __init__(self, parent, mode="scientific", theme=None, sound_enabled=True):
        super().__init__(parent)

        # Η μεταβλητή self.theme είναι attribute (ιδιότητα) του αντικειμένου. Κρατά τα χρώματα του theme.
        # Αν δεν δώσουμε συγκεκριμένο theme, καλεί το get_theme("dark") για προεπιλογή.
        self.theme = theme or get_theme("dark")
        self.theme_mode = "dark"  # Απλό string για παρακολούθηση του ενεργού theme
        self.sound_enabled = sound_enabled  # Ελέγχει αν θα αναπαράγεται ήχος όταν πατιούνται κουμπιά
        self.display_var = customtkinter.StringVar(value="0")  # Η τιμή που φαίνεται στο πεδίο display
        self.memory = mpf("0")
        self.is_second_function = False  # Αν είναι ενεργή η "2nd function" για εναλλακτικά κουμπιά
        self.is_degree = True  # Deg ή Rad για trig συναρτήσεις
        self.just_evaluated = False  # Σημαία για να αποτρέψει άμεση συνέχιση πράξης μετά το =
        self.history_log = []  # Ολόκληρο το log
        self.history_window = None  # Για το drop-down

        # Δύο λεξικά (maps) που καθορίζουν τα labels για 2nd function mode και το αντίστροφο
        self.second_map = {
            "sin": "sin⁻¹", "cos": "cos⁻¹", "tan": "tan⁻¹",
            "sinh": "sinh⁻¹", "cosh": "cosh⁻¹", "tanh": "tanh⁻¹"
        }
        self.first_map = {v: k for k, v in self.second_map.items()}  # Αντιστροφή: inverse → original

        # Δημιουργία interface και εφαρμογή theme
        self.build_ui()
        self.apply_theme(self.theme)

    # ---------------------
    # UI SETUP
    # ---------------------
    def build_ui(self):
        # Το βασικό πλαίσιο του calculator
        self.configure(width=400, height=600)

        # ----------------------- DISPLAY CONTAINER -----------------------
        self.display_container = customtkinter.CTkFrame(
            self,
            fg_color=self.theme["display_bg"],
            corner_radius = 0,
            height = 130,
        )
        self.display_container.pack(fill="x", padx=0, pady=(0, 0))

        #self.display_container.pack_propagate(False) #------------------> να ξαναδώ αν θα το χρησιμοποιήσω

        # Top display - περιέχει το manual button
        self.top_display = customtkinter.CTkFrame(
            self.display_container,
            height=30,
            fg_color=self.theme["display_bg"],
            corner_radius=0,
            border_width=0
        )
        self.top_display.pack(fill="x")

        self.manual_button = customtkinter.CTkButton(
            self.top_display,
            text="✍️",
            width=30,
            height=30,
            font=("Arial", 18),
            fg_color=self.theme["manual_button_bg"],
            text_color=self.theme["manual_button_text"],
            hover_color=self.theme["hover_manual_button"],
            corner_radius=0,
            command=self.open_manual
        )
        self.manual_button.pack(side="left", padx=15)

        # Spacer στο κέντρο
        customtkinter.CTkLabel(self.top_display, text="").pack(side="left", expand=True)

        # Ιστορικό κουμπί (εικονίδιο ρολογιού)
        self.history_button = customtkinter.CTkButton(
            self.top_display,
            text="🕒",
            width=30,
            height=30,
            font=("Arial", 18),
            fg_color=self.theme["manual_button_bg"],
            text_color=self.theme["manual_button_text"],
            hover_color=self.theme["hover_manual_button"],
            corner_radius=0,
            command=self.open_history_window
        )
        self.history_button.pack(side="right", padx=15)

        # Ιστορικό πράξεων
        self.history_display_var = customtkinter.StringVar(value="")
        self.history_display = customtkinter.CTkLabel(
            self.display_container,
            textvariable=self.history_display_var,
            height=24,
            font=("Arial", 12),
            anchor="e",
            fg_color=self.theme["display_bg"],
            text_color=self.theme["display_text"],
            corner_radius=0
        )
        self.history_display.pack(fill="x",  padx=20)

        # Ενότητα για προβολή συγκεκριμένων μηνυμάτων λάθους
        self.middle_display = customtkinter.CTkLabel(
            self.display_container,
            text="",
            height=24,
            font=("Arial", 12),
            anchor="e",
            fg_color=self.theme["display_bg"],
            text_color=self.theme["display_text"],
            corner_radius=0
        )
        self.middle_display.pack(fill="x", padx=20)

        # Εμφάνιση αριθμών / αποτελεσμάτων
        self.display_entry = customtkinter.CTkEntry(
            self.display_container,
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            height=40,
            corner_radius=0,
            border_width=0,
            fg_color=self.theme["display_bg"],
            text_color=self.theme["display_text"],
        )
        self.display_entry.pack(fill="x", padx=15, pady=(0, 0))



        # Ένδειξη Deg ή Rad – το βάζουμε έτσι κι αλλιώς (στο Standard απλά μένει κενό)
        self.angle_mode_label = customtkinter.CTkLabel(
            self.display_container,
            text=("Deg" if self.is_degree else "Rad"),
            font=("Arial", 10),
            width=30,
            height=12,
            fg_color=self.theme["display_bg"],
            text_color=self.theme["display_text"],
        )
        self.angle_mode_label.pack(anchor="sw", padx=10, pady=(0, 4))

        # ----------- ΕΠΙΣΤΗΜΟΝΙΚΑ ΚΟΥΜΠΙΑ -----------
        # Συναρτήσεις όπως sin, cos, log, factorial, π κλπ.
        self.top_buttons_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.theme["top_frame_bg"])
        self.top_buttons_frame.pack(fill="both", expand=False, padx=10, pady=(6, 4))

        top_buttons = [
            ["2nd", "Rad", "Rand", "mc", "m+", "m-", "mr"],
            ["x²", "x³", "1/x", "√", "ⁿ√x", "yˣ", "2ʸ"],
            ["sin", "cos", "tan", "sinh", "cosh", "tanh", "π"],
            ["log₁₀", "log₂", "x!", "(", ")", "%", "EE"]
        ]

        self.top_button_objects = []
        for r, row in enumerate(top_buttons):
            row_objs = []
            for c, text in enumerate(row):
                self.top_buttons_frame.columnconfigure(c, weight=1)
                btn = customtkinter.CTkButton(
                    self.top_buttons_frame,
                    text=text,
                    height=40,
                    font=("Arial", 12),
                    hover_color=self.theme["top_button_hover"],
                    command=lambda val=text: self.handle_special_buttons(val)
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                row_objs.append(btn)
            self.top_buttons_frame.rowconfigure(r, weight=0)
            self.top_button_objects.append(row_objs)



        # ----------- ΚΟΥΜΠΙΑ STANDARD ΥΠΟΛΟΓΙΣΤΗ -----------
        # Οι βασικές αριθμητικές πράξεις (όπως το standard calculator)
        bottom_layout = [
            (0, 0, "7", 1, "num"), (0, 1, "8", 1, "num"), (0, 2, "9", 1, "num"),
            (0, 3, "C", 1, "c"),   (0, 4, "AC", 1, "ac"),
            (1, 0, "4", 1, "num"), (1, 1, "5", 1, "num"), (1, 2, "6", 1, "num"),
            (1, 3, "x", 1, "op"),  (1, 4, "÷", 1, "op"),
            (2, 0, "1", 1, "num"), (2, 1, "2", 1, "num"), (2, 2, "3", 1, "num"),
            (2, 3, "+", 1, "op"), (2, 4, "-", 1, "op"),
            (3, 0, "0", 1, "num"), (3, 1, ".", 1, "num"), (3, 2, "+/-", 1, "num"),
            (3, 3, "=", 2, "op")
        ]

        self.numeric_buttons = []
        self.operation_buttons = []
        self.ac_button = None
        self.c_button = None
        bottom_font = ("Arial", 30)

        self.bottom_buttons_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self.theme["bottom_frame_bg"])
        self.bottom_buttons_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for item in bottom_layout:
            r, c, text, cspan, btype = item
            hover = self.theme.get(f"{btype}_hover", self.theme["hover_default"])
            btn = customtkinter.CTkButton(
                self.bottom_buttons_frame,
                text=text,
                width=70,
                height=60,
                font=bottom_font,
                hover_color=hover,
                command=lambda val=text: on_button_click(self, val)
            )
            btn.grid(row=r, column=c, columnspan=cspan, padx=3, pady=3, sticky="ew")
            if btype == "num":
                self.numeric_buttons.append(btn)
            elif btype == "op":
                self.operation_buttons.append(btn)
            elif btype == "ac":
                self.ac_button = btn
            elif btype == "c":
                self.c_button = btn

        for i in range(4):
            self.bottom_buttons_frame.rowconfigure(i, weight=1)
        for j in range(5):
            self.bottom_buttons_frame.columnconfigure(j, weight=1)

    def get_display_value(self):
        return self.display_var.get()

    def set_display_value(self, value):
        self.display_var.set(value)

    def handle_key_input(self, key):
        from keyboardHandler import handle_keyboard_input
        handle_keyboard_input(key, self)

    # -------------------------
    # ΕΦΑΡΜΟΓΗ ΘΕΜΑΤΟΣ
    # -------------------------
    def apply_theme(self, theme_dict):
        self.theme = theme_dict

        for widget in [self, self.display_container, self.top_buttons_frame, self.bottom_buttons_frame]:
            widget.configure(fg_color=theme_dict["background"])

    # Τα displays -------------------------------------------------------------------------------------
        self.display_container.configure(fg_color=theme_dict["display_bg"])
        self.top_display.configure(fg_color=theme_dict["display_bg"])

        self.history_display.configure(
            fg_color=theme_dict["display_bg"],
            text_color=theme_dict["display_text"]
        )

        self.middle_display.configure(
            fg_color=theme_dict["display_bg"],
            text_color=theme_dict["display_text"]
        )

        self.display_entry.configure(
            fg_color=theme_dict["display_bg"],
            text_color=theme_dict["display_text"]
        )

        self.angle_mode_label.configure(
            fg_color=theme_dict["display_bg"],
            text_color=theme_dict["angle_mode_text"]
        )

        self.manual_button.configure(
            fg_color=theme_dict["manual_button_bg"],
            text_color=theme_dict["manual_button_text"],
            hover_color=theme_dict["hover_manual_button"]
        )
        self.history_button.configure(
            fg_color=theme_dict["manual_button_bg"],
            text_color=theme_dict["manual_button_text"],
            hover_color=theme_dict["hover_manual_button"]
        )

# Τα επάνω (scientific) κουμπιά του calculator------------------------------------------------
        for row in self.top_button_objects:
            for btn in row:
                btn.configure(fg_color=theme_dict["top_button_bg"],
                              text_color=theme_dict["top_button_text"],
                              hover_color=theme_dict["top_button_hover"])

        self.top_button_objects[0][0].configure(fg_color=theme_dict["special_button_fg"],
                                                hover_color=theme_dict["special_button_hover"],
                                                text_color=self.theme["special_button_text"])
        self.top_button_objects[0][1].configure(fg_color=theme_dict["special_button_fg"],
                                                hover_color=theme_dict["special_button_hover"],
                                                text_color=self.theme["special_button_text"])

        for btn in self.numeric_buttons:
            btn.configure(fg_color=theme_dict["num_button_bg"],
                          text_color=theme_dict["num_button_text"],
                          hover_color=theme_dict["num_hover"])
        for btn in self.operation_buttons:
            btn.configure(fg_color=theme_dict["op_button_bg"],
                          text_color=theme_dict["op_button_text"],
                          hover_color=theme_dict["op_hover"])
        for button in [self.ac_button, self.c_button]:
            if button:
                button.configure(fg_color=theme_dict["ac_button_bg"],
                                 text_color=theme_dict["ac_button_text"],
                                 hover_color=theme_dict["ac_hover"])

        self.angle_mode_label.configure(
            fg_color=theme_dict["angle_mode_bg"],
            text_color=theme_dict["angle_mode_text"],
            text=("Deg" if self.is_degree else "Rad")
        )

    # -------------------------
    # ΕΠΙΛΟΓΕΣ ΣΥΜΠΕΡΙΦΟΡΑΣ ΚΟΥΜΠΙΩΝ
    # -------------------------
    def handle_special_buttons(self, value):
        if value == "2nd":
            self.toggle_second_function()
        elif value in ["Rad", "Deg"]:
            self.toggle_angle_mode()
        else:
            on_button_click(self, value)



    def toggle_second_function(self):
        # Αλλάζει το label σε κουμπιά trig functions για να εμφανίσουν τα αντίστροφα
        self.is_second_function = not self.is_second_function
        for row in self.top_button_objects:
            for btn in row:
                text = btn.cget("text")
                if self.is_second_function and text in self.second_map:
                    btn.configure(text=self.second_map[text])
                elif not self.is_second_function and text in self.first_map:
                    btn.configure(text=self.first_map[text])

    def toggle_angle_mode(self):
        self.is_degree = not self.is_degree
        new_mode = "Deg" if self.is_degree else "Rad"
        self.top_button_objects[0][1].configure(text=new_mode)
        self.angle_mode_label.configure(text=new_mode)

    def set_theme_mode(self, theme_mode):
        self.theme_mode = theme_mode
        new_theme = get_theme(theme_mode)
        self.apply_theme(new_theme)

    def open_manual(self):
        import webbrowser
        webbrowser.open("https://docs.google.com/document/d/1xHKVvzsmCFrH7DBCih10n8-JnZcKpbIFKqexXh1MI8w/edit?usp=sharing")

    def open_history_window(self):
        if not self.history_log:
            return

        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        popup_theme = {
            "popup_history_text": self.theme.get("popup_history_text", "#00ff00"),
            "popup_history_fg": self.theme.get("popup_history_fg", "#111111"),
            "popup_history_bg": self.theme.get("popup_history_bg", "#0A0A0A"),
            "popup_history_border": self.theme.get("popup_history_border", "#222222"),
            "popup_scrollbar_bg": self.theme.get("popup_history_scrollbar_bg", "#1A1A1A"),
            "popup_scrollbar_thumb": self.theme.get("popup_history_scrollbar_thumb", "#3A3A3A")
        }

        self.history_window = customtkinter.CTkToplevel(self)
        self.history_window.title("History")
        self.history_window.geometry("300x300")
        self.history_window.attributes("-topmost", True)

        self.history_window.configure(
            fg_color=popup_theme["popup_history_bg"],
            border_color=popup_theme["popup_history_border"],
            border_width=2
        )

        # Θέση παραθύρου (κεντραρισμένο πάνω στην αριθμομηχανή)
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        popup_x = parent_x + (self.winfo_width() - 300) // 2
        popup_y = parent_y + 100
        self.history_window.geometry(f"300x300+{popup_x}+{popup_y}")

        scroll_frame = customtkinter.CTkScrollableFrame(
            self.history_window,
            fg_color=popup_theme["popup_history_fg"],
            scrollbar_fg_color=popup_theme["popup_scrollbar_bg"],
            scrollbar_button_color=popup_theme["popup_scrollbar_thumb"]
        )
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        for entry in reversed(self.history_log[-50:]):
            btn = customtkinter.CTkButton(
                scroll_frame,
                text=entry,
                anchor="w",
                height=30,
                font=("Arial", 12),
                fg_color=self.theme["top_button_bg"],
                hover_color=self.theme["top_button_hover"],
                text_color=self.theme["top_button_text"],
                command=lambda e=entry: self.insert_history_expression(e)
            )
            btn.pack(fill="x", pady=2)

    def insert_history_expression(self, entry):
        expr = entry.split('=')[0].strip().replace("×", "*").replace("÷", "/")
        self.display_var.set(expr)




# -------------------------
# ΔΗΜΙΟΥΡΓΙΑ CALCULATOR (για χρήση από main app)
# -------------------------
def create_scientific_calculator(parent, mode="scientific", theme_mode="dark", sound_enabled=True):
    theme = get_theme(theme_mode)
    return ScientificCalcPreview(parent, mode=mode, theme=theme, sound_enabled=sound_enabled)


