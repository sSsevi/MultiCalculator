# mainCalcPreview.py

import customtkinter
from PIL import Image
from themeLoader import get_theme


class MainCalcPreview(customtkinter.CTkFrame):
    def __init__(self, parent, theme_mode="dark", sound_enabled=True):
        super().__init__(parent, height=40, corner_radius=0)
        self.pack_propagate(False)

        self.theme_mode = theme_mode
        self.sound_enabled = sound_enabled

        # Εικόνες
        self.sound_on_img = customtkinter.CTkImage(light_image=Image.open("images/sound_on.png"), size=(24, 24))
        self.sound_off_img = customtkinter.CTkImage(light_image=Image.open("images/sound_off.png"), size=(24, 24))
        self.menu_icon_img = customtkinter.CTkImage(light_image=Image.open("images/menu_icon.png"), size=(24, 24))

        # Κουμπί μενού
        self.menu_button = customtkinter.CTkButton(self, text="", width=40, height=40, image=self.menu_icon_img, corner_radius=6)
        self.menu_button.pack(side="left", padx=5)

        # Ετικέτα λειτουργίας
        self.mode_label_display = customtkinter.CTkLabel(self, text="Standard Calculator", font=("Arial", 16))
        self.mode_label_display.pack(side="left", padx=10)

        # Κουμπί ήχου
        self.sound_button = customtkinter.CTkButton(self, text="", width=40, height=40)
        self.sound_button.pack(side="right", padx=5)

        # Εφαρμογή αρχικού theme
        self.set_theme(theme_mode)

    def set_theme(self, theme):
        if isinstance(theme, str):
            self.theme_mode = theme
            theme = get_theme(theme)
        else:
            self.theme_mode = theme.get("name", "custom")

        # ✅ Χρησιμοποιούμε το ίδιο dict παντού
        self.configure(fg_color=theme.get("background", "#222222"))

        self.menu_button.configure(
            fg_color=theme.get("top_frame_bg", "#333333"),
            hover_color=theme.get("top_button_hover", "#555555")
        )
        self.sound_button.configure(
            fg_color=theme.get("top_frame_bg", "#333333"),
            hover_color=theme.get("top_button_hover", "#555555"),
            image=self.sound_on_img if self.sound_enabled else self.sound_off_img
        )
        self.mode_label_display.configure(
            text_color=theme.get("menu_text_color", "#ffffff")
        )


