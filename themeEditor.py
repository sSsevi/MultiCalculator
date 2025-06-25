# themeEditor.py
# ============================================

import customtkinter
import tkinter as tk
import csv
from tkinter import colorchooser
import inspect

from tooltipInjector import inject_tooltips_from_map
from tooltipMap import TooltipMap, TopBarTooltipMap
from frameManager import frame_data
from mainCalcPreview import MainCalcPreview

customtkinter.set_appearance_mode("dark")

CSV_FILE = "themeMatrix.csv"

def load_theme_matrix_from_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        matrix = [row for row in reader]
        return matrix, fieldnames

def save_theme_matrix_to_csv(matrix, fieldnames, path):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matrix)

class ThemeEditor(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎨 Theme Editor")
        self.geometry("1200x850")
        self.configure(padx=20, pady=20)

        self.matrix, self.headers = load_theme_matrix_from_csv(CSV_FILE)
        self.themes = self.headers[1:]
        self.entries = {}
        self.preview_boxes = {}
        self.original_values = {}
        self.previous_values = {}

        self.build_ui()

    def build_ui(self):
        self.top_controls = customtkinter.CTkFrame(self, fg_color="#222222")
        self.top_controls.pack(fill="x", pady=(0, 15))

        self.combo = customtkinter.CTkOptionMenu(
            self.top_controls,
            values=self.themes,
            command=self.display_theme,
            fg_color="#eb7c16",
            button_color="#eb7c16",
            button_hover_color="#d06c11",
            font=("Arial", 14, "bold")  # bold
        )
        self.combo.set(self.themes[0])
        self.combo.pack(side="left", padx=10, pady=10)

        self.mode_names = list(frame_data.keys())

        self.mode_combo = customtkinter.CTkOptionMenu(
            self.top_controls,
            values=self.mode_names,
            command=self.change_mode_preview,
            fg_color="#eb7c16",
            button_color="#eb7c16",
            button_hover_color="#d06c11",
            font=("Arial", 14, "bold")  # bold
        )
        self.mode_combo.set(self.mode_names[0])
        self.mode_combo.pack(side="left", padx=10)

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both")

        self.scroll = customtkinter.CTkScrollableFrame(self.main_frame, width=600)
        self.scroll.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.preview_frame = customtkinter.CTkFrame(self.main_frame)
        self.preview_frame.pack(side="left", fill="both", expand=True)

        for row_index, row in enumerate(self.matrix):
            key = row["key"]

            key_label = customtkinter.CTkLabel(self.scroll, text=key, width=180, anchor="w")
            key_label.grid(row=row_index, column=0, padx=5, pady=2)

            entry = customtkinter.CTkEntry(self.scroll, width=120)
            entry.grid(row=row_index, column=1, padx=5)
            self.entries[key] = entry

            preview = customtkinter.CTkLabel(self.scroll, text="", width=30)
            preview.grid(row=row_index, column=2, padx=5)
            self.preview_boxes[key] = preview

            entry.bind("<Return>", lambda e, k=key: self.update_preview(k))
            entry.bind("<FocusOut>", lambda e, k=key: self.update_preview(k))
            entry.bind("<Button-3>", self.make_context_menu_callback(entry))

            btn = customtkinter.CTkButton(self.scroll, text="🎨", width=30, fg_color="#4f4f4f", text_color="#ff80c0",
                                          command=self.make_picker(entry, preview))
            btn.grid(row=row_index, column=3, padx=2)

            undo_btn = customtkinter.CTkButton(self.scroll, text="↩️", width=0, fg_color="#4f4f4f", text_color="#00ffff",
                                               command=lambda k=key: self.undo_change(k))
            undo_btn.grid(row=row_index, column=4, padx=(2, 0))

            reset_btn = customtkinter.CTkButton(self.scroll, text="♻️", width=30, fg_color="#4f4f4f", text_color="#008000",
                                                command=lambda k=key: self.reset_to_original(k))
            reset_btn.grid(row=row_index, column=5, padx=2)

        self.save_button = customtkinter.CTkButton(self, text="💾 Αποθήκευση", fg_color="#eb7c16", command=self.save_theme)
        self.save_button.pack(pady=(10, 5))

        self.reset_all_button = customtkinter.CTkButton(self, text="♻️ Επαναφορά Όλων", fg_color="#eb7c16", command=self.reset_all)
        self.reset_all_button.pack(pady=(0, 20))

        self.build_preview()

    def build_preview(self, *args):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

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

        self.calc_preview = MainCalcPreview(
            self.fixed_preview_container,
            theme_mode=self.combo.get(),
            sound_enabled=False
        )
        self.calc_preview.pack(expand=True, fill="both")

        self.top_bar = self.calc_preview.top_bar_frame

        #inject_tooltips_from_map(self.top_bar, TopBarTooltipMap)
        inject_tooltips_from_map(self.calc_preview.current_frame, TooltipMap)
        inject_tooltips_from_map(self.calc_preview, TopBarTooltipMap)

        # ✅ Πρώτη εμφάνιση θέματος
        self.display_theme(self.combo.get())

    def change_mode_preview(self, new_mode):
        if not hasattr(self, "calc_preview"):
            return

        if not hasattr(self.calc_preview, "change_mode"):
            return

        self.calc_preview.change_mode(new_mode)
        inject_tooltips_from_map(self.calc_preview.current_frame, TooltipMap)

        # Δυναμικό update του label της πάνω μπάρας στο preview
        if hasattr(self.calc_preview, "mode_label_display"):
            if new_mode.lower() in ("standard", "scientific"):
                label_text = f"{new_mode.title()} Calculator"
            else:
                label_text = new_mode.title()
            self.calc_preview.mode_label_display.configure(
                text=label_text,
                text_color=self.calc_preview.theme.get("menu_text_color", "#ffffff")
        )

    def make_context_menu_callback(self, entry):
        return lambda e: self.show_context_menu(e, entry)

    def show_context_menu(self, event, entry):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Copy", command=lambda: self.copy(entry))
        menu.add_command(label="Paste", command=lambda: self.paste(entry))
        menu.add_command(label="Cut", command=lambda: self.cut(entry))
        menu.tk_popup(event.x_root, event.y_root)

    def copy(self, entry):
        try:
            self.clipboard_clear()
            self.clipboard_append(entry.get())
        except Exception:
            pass

    def paste(self, entry):
        try:
            text = self.clipboard_get()
            self.previous_values[entry] = entry.get()
            entry.delete(0, "end")
            entry.insert(0, text)
        except Exception:
            pass

    def cut(self, entry):
        try:
            self.clipboard_clear()
            self.clipboard_append(entry.get())
            self.previous_values[entry] = entry.get()
            entry.delete(0, "end")
        except Exception:
            pass

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

    def update_preview(self, key):
        entry = self.entries[key]
        value = entry.get()
        if value.startswith("#") and len(value) == 7:
            self.preview_boxes[key].configure(fg_color=value)
            self.update_preview_live()

    def update_preview_live(self):
        theme_dict = {k: self.entries[k].get() for k in self.entries}
        self.calc_preview.apply_theme(theme_dict)

        # ΠΡΟΣΘΗΚΗ ΓΙΑ DEBUGGING: Προσπαθήστε να ρυθμίσετε απευθείας το fg_color της top_bar_frame
        # Χρησιμοποιήστε το κλειδί 'background' όπως διαπιστώσαμε ότι είναι το σωστό χρώμα για τη μπάρα
        if hasattr(self.calc_preview, "top_bar_frame") and self.calc_preview.top_bar_frame:
            self.calc_preview.top_bar_frame.configure(fg_color=theme_dict.get("background", "#222222"))
            # Επίσης, βεβαιωθείτε ότι τα κουμπιά μέσα σε αυτήν παίρνουν το σωστό χρώμα
            #if hasattr(self.calc_preview, "menu_button") and self.calc_preview.menu_button:
                #self.calc_preview.menu_button.configure(fg_color="red")
                #self.calc_preview.menu_button.configure(fg_color=theme_dict.get("top_frame_bg", "#3c3c3c"))
            #if hasattr(self.calc_preview, "sound_button") and self.calc_preview.sound_button:
                #self.calc_preview.sound_button.configure(fg_color=theme_dict.get("top_frame_bg", "#3c3c3c"))
                #self.calc_preview.sound_button.configure(fg_color="blue")

        #inject_tooltips_from_map(self.top_bar, TopBarTooltipMap) # Αυτό αφαιρέθηκε ήδη νωρίτερα και είναι εντάξει
        #inject_tooltips_from_map(self.calc_preview.current_frame, TooltipMap) # Αυτό παραμένει


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

        # ✅ Ενημέρωσε το preview με το νέο theme_name
        self.calc_preview.theme_mode = theme_name
        self.update_preview_live()

    def undo_change(self, key):
        entry = self.entries[key]
        prev_value = self.previous_values.get(entry)
        if prev_value:
            entry.delete(0, "end")
            entry.insert(0, prev_value)
            self.update_preview(key)

    def reset_to_original(self, key):
        value = self.original_values.get(key)
        if value:
            entry = self.entries[key]
            entry.delete(0, "end")
            entry.insert(0, value)
            self.update_preview(key)

    def reset_all(self):
        for key in self.entries:
            self.reset_to_original(key)

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

if __name__ == "__main__":
    app = ThemeEditor()
    app.mainloop()
