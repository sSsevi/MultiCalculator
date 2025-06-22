import customtkinter

class Tooltip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = "\n".join(text) if isinstance(text, list) else text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def schedule_show(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self):
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tooltip_window = customtkinter.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.configure(fg_color="#333333", corner_radius=10)

        label = customtkinter.CTkLabel(
            self.tooltip_window,
            text=self.text,
            font=("Arial", 12),
            text_color="#FFFFFF",
            fg_color="#333333",
            corner_radius=6,
            padx=10,
            pady=6
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
