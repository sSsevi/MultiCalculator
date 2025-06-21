# zodiacIconWidget.py

import tkinter as tk
import customtkinter
from PIL import Image, ImageTk, ImageEnhance
import os

from themeManager import get_theme
from customtkinter import CTkFont

class ZoomingZodiac(customtkinter.CTkFrame):
    def __init__(self, master, slug, name, mode="dark"):
        super().__init__(master)

        self.theme = get_theme(mode)
        self.bg_color = self.theme["background"]
        self.hover_color = self.theme["animation_hover"]
        self.configure(fg_color=self.bg_color, cursor="hand2")

        self.slug = slug
        self.name = name
        self.img_folder = "assets/zodiac_images"
        self.default_img = "default.png"

        self.canvas_size = 75

        self.load_images()

        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size,
                                highlightthickness=0, bg=self.bg_color, cursor="hand2")
        self.canvas.pack()
        self.show_image(dark=False)

        self.name_label = customtkinter.CTkLabel(
            self,
            text=self.name,
            font=CTkFont(family="Arial", size=12),
            text_color="white",
            fg_color="transparent"
        )
        self.name_label.pack(pady=(0, 2))

        self.bind("<Enter>", self.on_hover_in)
        self.bind("<Leave>", self.on_hover_out)
        self.canvas.bind("<Enter>", self.on_hover_in)
        self.canvas.bind("<Leave>", self.on_hover_out)
        self.name_label.bind("<Enter>", self.on_hover_in)
        self.name_label.bind("<Leave>", self.on_hover_out)

    def load_images(self):
        img_path = os.path.join(self.img_folder, f"{self.slug}.png")
        if not os.path.exists(img_path):
            img_path = os.path.join(self.img_folder, self.default_img)

        self.original_image = Image.open(img_path)
        self.dark_image = ImageEnhance.Brightness(self.original_image).enhance(0.6)
        self.update_image()

    def update_image(self):
        resized = self.original_image.resize((self.canvas_size, self.canvas_size), Image.Resampling.LANCZOS)
        dark_resized = self.dark_image.resize((self.canvas_size, self.canvas_size), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)
        self.tk_img_dark = ImageTk.PhotoImage(dark_resized)

    def show_image(self, dark=False):
        img = self.tk_img_dark if dark else self.tk_img
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=img)

    def on_hover_in(self, event=None):
        self.show_image(dark=True)

    def on_hover_out(self, event=None):
        self.show_image(dark=False)
