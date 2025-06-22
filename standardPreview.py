# scientificPreview.py
# Πιστό UI preview του scientific calculator για χρήση στον themeEditor
import customtkinter

class StandardPreview(customtkinter.CTkFrame):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.theme = theme
        self.build_ui()

    def build_ui(self):
        self.configure(fg_color=self.theme["background"])