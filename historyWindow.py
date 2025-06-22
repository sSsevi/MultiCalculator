# historyWindow.py
# ----------------------------------------------------------
# Αυτή η μονάδα περιέχει την υλοποίηση του παραθύρου ιστορικού (history)
# που χρησιμοποιείται σε Standard και Scientific Calculator

import customtkinter

class HistoryWindowModule:
    def __init__(self, parent, theme, history_log, insert_callback):
        self.parent = parent
        self.theme = theme
        self.history_log = history_log
        self.insert_callback = insert_callback
        self.history_window = None
        self.scroll_frame = None

    def open(self):
        print("HistoryWindowModule open() running")

        if not self.history_log:
            print("History log is empty – returning")
            return

        if self.history_window and self.history_window.winfo_exists():
            print("Window already open – lifting")
            self.history_window.lift()
            return

        print("Creating new history window...")

        self.history_window = customtkinter.CTkToplevel(self.parent)
        self.history_window.title("History")
        self.history_window.attributes("-topmost", True)

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        popup_x = parent_x + (self.parent.winfo_width() - 300) // 2
        popup_y = parent_y + 100
        self.history_window.geometry(f"300x300+{popup_x}+{popup_y}")

        # Apply theme immediately
        self.history_window.configure(
            fg_color=self.theme["popup_history_bg"],
            border_color=self.theme["popup_history_border"],
            border_width=20
        )

        self.scroll_frame = customtkinter.CTkScrollableFrame(
            self.history_window,
            fg_color=self.theme["popup_history_fg"],
            scrollbar_fg_color=self.theme["popup_history_scrollbar_bg"],
            scrollbar_button_color=self.theme["popup_history_scrollbar_thumb"]
        )
        self.scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Δημιουργούμε τα κουμπιά αμέσως με το σωστό θέμα
        for entry in reversed(self.history_log[-50:]):
            btn = customtkinter.CTkButton(
                self.scroll_frame,
                text=entry,
                anchor="w",
                height=30,
                font=("Arial", 12),
                fg_color=self.theme["popup_history_line_bg"],
                hover_color=self.theme["popup_history_hover"],
                text_color=self.theme["popup_history_text"],
                command=lambda e=entry: self.insert_callback(e)
            )
            btn.pack(fill="x", pady=2)

    def apply_theme(self, theme):
        self.theme = theme
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.configure(
                fg_color=self.theme["popup_history_bg"],
                border_color=self.theme["popup_history_border"],
                border_width=0
            )
            if self.scroll_frame:
                self.scroll_frame.configure(
                    fg_color=self.theme["popup_history_fg"],
                    scrollbar_fg_color=self.theme["popup_history_scrollbar_bg"],
                    scrollbar_button_color=self.theme["popup_history_scrollbar_thumb"]
                )

                # Διαγράφουμε τα παλιά widgets για να ανανεώσουμε
                for child in self.scroll_frame.winfo_children():
                    child.destroy()

                # Δημιουργούμε εκ νέου τα κουμπιά του ιστορικού με το νέο θέμα
                for entry in reversed(self.history_log[-50:]):
                    btn = customtkinter.CTkButton(
                        self.scroll_frame,
                        text=entry,
                        anchor="w",
                        height=30,
                        font=("Arial", 12),
                        fg_color=self.theme["popup_history_fg"],
                        hover_color=self.theme["popup_history_hover"],
                        text_color=self.theme["popup_history_text"],
                        command=lambda e=entry: self.insert_callback(e)
                    )
                    btn.pack(fill="x", pady=2)
