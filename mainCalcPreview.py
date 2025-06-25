# mainCalcPreview.py
# ============================================
# Preview αριθμομηχανής για το Theme Editor.
# Πλήρης εμφάνιση top bar και calculator frame.
# Τα κουμπιά δεν έχουν λειτουργία (μόνο εμφάνιση).
# ============================================

import customtkinter
from PIL import Image
from themeLoader import get_theme
from frameManager import frame_data
from standardCalc import StandardCalculator
import os


class MainCalcPreview(customtkinter.CTkFrame):
    def __init__(self, parent, theme_mode="dark", sound_enabled=True):
        super().__init__(parent)
        self.pack_propagate(False)

        self.theme_mode = theme_mode
        self.sound_enabled = sound_enabled
        self.current_mode = "standard"
        self.display_value = ""

        # Αρχικοποιούμε το theme εδώ, αλλά θα εφαρμοστεί πλήρως στην set_theme
        self.theme = get_theme(self.theme_mode)

        # ==================== Φόρτωση εικόνων ====================
        sound_on_path = "images/sound_on.png"
        if os.path.exists(sound_on_path):
            self.sound_on_img = customtkinter.CTkImage(light_image=Image.open(sound_on_path), size=(24, 24))
        else:
            self.sound_on_img = None

        sound_off_path = "images/sound_off.png"
        if os.path.exists(sound_off_path):
            self.sound_off_img = customtkinter.CTkImage(light_image=Image.open(sound_off_path), size=(24, 24))
        else:
            self.sound_off_img = None

        menu_icon_path = "images/menu_icon.png"
        if os.path.exists(menu_icon_path):
            self.menu_icon_img = customtkinter.CTkImage(light_image=Image.open(menu_icon_path), size=(24, 24))
        else:
            self.menu_icon_img = None

        # ==================== Δημιουργία Top Bar (ΜΟΝΟ ΜΙΑ ΦΟΡΑ) ====================
        self.top_bar_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0)
        self.top_bar_frame.pack(fill="x")

        self.menu_button = customtkinter.CTkButton(
            self.top_bar_frame,
            text="",
            width=40,
            height=40,
            image=self.menu_icon_img,
            corner_radius=6,
            fg_color=self.theme.get("top_frame_bg", "#3c3c3c"), # Χρησιμοποιούμε top_frame_bg για τα κουμπιά
            #command=self.dummy_command
        )
        self.menu_button.pack(side="left", padx=5)



        self.mode_label_display = customtkinter.CTkLabel(
            self.top_bar_frame,
            text="Standard Calculator",
            font=("Arial", 16),
            text_color=self.theme.get("menu_text_color", "#ffffff")
        )
        self.mode_label_display.pack(side="left", padx=10)

        self.sound_button = customtkinter.CTkButton(
            self.top_bar_frame,
            image=self.sound_on_img if self.sound_enabled else self.sound_off_img,
            text="",
            width=40,
            height=40,
            fg_color=self.theme.get("top_frame_bg", "#3c3c3c"), # Χρησιμοποιούμε top_frame_bg για τα κουμπιά
            #command=self.dummy_command
        )
        self.sound_button.pack(side="right", padx=5)

        # ==================== Εμφάνιση Calculator Frame ====================
        self.calculator_frame = None
        self.current_frame = None
        self.show_calculator_frame()

        # Εφαρμογή αρχικού theme
        self.set_theme(self.theme)



    def show_calculator_frame(self):
        if self.calculator_frame:
            try:
                self.display_value = self.calculator_frame.get_display_value()
            except Exception:
                self.display_value = ""
            self.calculator_frame.destroy()

        FrameClass = frame_data.get(self.current_mode, {}).get("frame", StandardCalculator)

        try:
            # Προσπαθούμε να περάσουμε το theme και sound_enabled
            self.calculator_frame = FrameClass(self, theme=self.theme, sound_enabled=self.sound_enabled)
        except TypeError:
            try:
                # Αν αποτύχει, δοκιμάζουμε μόνο με theme
                self.calculator_frame = FrameClass(self, theme=self.theme)
            except TypeError:
                # Αν αποτύχει, τότε χωρίς ορίσματα (τελευταία λύση)
                self.calculator_frame = FrameClass(self)

        self.calculator_frame.pack(fill="both", expand=True)

        try:
            self.calculator_frame.set_display_value(self.display_value)
        except Exception:
            pass


        self.current_frame = self.calculator_frame
        self.menu_button.configure(
            fg_color=self.theme.get("top_frame_bg", "#333333"),
            hover_color=self.theme.get("top_button_hover", "#555555"))

    def set_theme(self, theme_dict): # Μετονομάστηκε σε theme_dict για σαφήνεια
        if isinstance(theme_dict, str):
            self.theme_mode = theme_dict
            self.theme = get_theme(theme_dict)
        else:
            self.theme_mode = theme_dict.get("name", "custom")
            self.theme = theme_dict # Εδώ το theme_dict είναι ήδη το λεξικό

        self.configure(fg_color=self.theme.get("background", "#222222"))


        if self.top_bar_frame: # Έλεγχος αν υπάρχει το widget
            self.top_bar_frame.configure(
                fg_color=self.theme.get("background", "#222222")
            )

        # Τα κουμπιά μέσα στο top_bar_frame πρέπει να παίρνουν το top_frame_bg
        if self.menu_button: # Έλεγχος αν υπάρχει το widget
            self.menu_button.configure(
                fg_color=self.theme.get("top_frame_bg", "#3c3c3c"),
                hover_color=self.theme.get("top_button_hover", "#555555")
            )


        if self.sound_button: # Έλεγχος αν υπάρχει το widget
            self.sound_button.configure(
                fg_color=self.theme.get("top_frame_bg", "#3c3c3c"),
                hover_color=self.theme.get("top_button_hover", "#555555"),
                image=self.sound_on_img if self.sound_enabled else self.sound_off_img
            )
        if self.mode_label_display: # Έλεγχος αν υπάρχει το widget
            self.mode_label_display.configure(
                text_color=self.theme.get("menu_text_color", "#ffffff")
            )

        if hasattr(self.calculator_frame, "apply_theme"):
            self.calculator_frame.apply_theme(self.theme)

    # Η apply_theme καλεί απλώς την set_theme
    def apply_theme(self, theme):
        self.set_theme(theme)

    def change_mode(self, new_mode):
        self.current_mode = new_mode
        self.show_calculator_frame()

        if hasattr(self, "current_frame") and hasattr(self.current_frame, "apply_theme"):
            self.current_frame.apply_theme(self.theme)