# tooltipMap.py

TooltipMap = {
    # ==========================================================
    # Κοινά στοιχεία για StandardCalculator.py και ScientificCalculator.py
    # ==========================================================
    "self": "background", # Το κύριο frame του calculator (είτε Standard είτε Scientific)
    "self.display_container": "display_bg", # Container για όλα τα display elements
    "self.top_display": "display_bg", # Το πάνω μέρος του display (περιέχει manual/history buttons)
    "self.history_display": ["display_bg", "display_text"], # Εμφάνιση ιστορικού πράξεων
    "self.middle_display": ["display_bg", "display_text"], # Μεσαία εμφάνιση (π.χ. μηνύματα σφάλματος)
    "self.display_entry": ["display_bg", "display_text"], # Κύριο πεδίο εμφάνισης αποτελεσμάτων/εισόδου
    "self.angle_mode_label": ["angle_mode_bg", "angle_mode_text"], # Ένδειξη γωνιακής μονάδας (Deg/Rad)

    "self.manual_button": ["manual_button_bg", "manual_button_text", "hover_manual_button"], # Κουμπί Manual
    "self.history_button": ["manual_button_bg", "manual_button_text", "hover_manual_button"], # Κουμπί History

    "self.bottom_buttons_frame": "bottom_frame_bg", # Το frame που περιέχει όλα τα κάτω κουμπιά
    "self.numeric_buttons": ["num_button_bg", "num_button_text", "num_hover"], # Λίστα αριθμητικών κουμπιών
    "self.operation_buttons": ["op_button_bg", "op_button_text", "op_hover"], # Λίστα τελεστών
    "self.ac_button": ["ac_button_bg", "ac_button_text", "ac_hover"], # Κουμπί AC
    "self.c_button": ["ac_button_bg", "ac_button_text", "ac_hover"], # Κουμπί C

    "self.ac_buttons": ["ac_button_bg", "ac_button_text", "ac_hover"],
    "self.memory_buttons": ["top_button_bg", "top_button_text", "top_button_hover"],
    "self.symbol_buttons": ["op_button_bg", "op_button_text", "op_hover"], # Λίστα συμβολικών κουμπιών (υπάρχει στο ScientificCalculator)


    # ==========================================================
    # Ειδικά στοιχεία ScientificCalculator.py
    # ==========================================================
    "self.top_buttons_frame": "top_frame_bg", # Το frame που περιέχει τα επιστημονικά κουμπιά
    "self.top_button_objects": ["top_button_bg", "top_button_text", "top_button_hover"], # Για τα γενικά top buttons
    "self.top_button_objects[0][0]": ["special_button_fg", "special_button_hover", "special_button_text"],
    "self.top_button_objects[0][1]": ["special_button_fg", "special_button_hover", "special_button_text"],

    # ==========================================================
    # Στοιχεία CurrencyConverter.py
    # ==========================================================
    "self.title_label": "display_text", # Το title_label του CurrencyConverter
    "self.from_label": "label_text",
    "self.to_label": "label_text",
    "self.amount_label": "label_text",
    "self.result_label": "label_text",
    "self.result_value_label": "display_text",
    "self.exchange_rate_label": "placeholder_text",
    "self.from_currency_menu": ["menu_button_bg", "dropdown_fg", "menu_text_color"],
    "self.to_currency_menu": ["menu_button_bg", "dropdown_fg", "menu_text_color"],
    "self.amount_entry": ["entry_fg", "text_input", "placeholder_text"],
    "self.convert_button": ["special_button_fg", "op_button_text", "op_hover"],


    # ==========================================================
    # Στοιχεία NumberConverter.py
    # ==========================================================
    # Σημείωση: Πολλά labels έχουν ίδια ονόματα με CurrencyConverter, αλλά αναφέρονται στο instance του NumberConverter.
    "self.from_base_menu": ["menu_button_bg", "dropdown_fg", "menu_text_color"],
    "self.to_base_menu": ["menu_button_bg", "dropdown_fg", "menu_text_color"],
    "self.swap_button": "special_button_fg",
    "self.allowed_digits_label": "placeholder_text",
    "self.input_label": "label_text",
    "self.input_entry": ["entry_fg", "text_input", "placeholder_text", "menu_button_bg"], # Προστέθηκε menu_button_bg για border_color
    "self.tooltip_label": "error_text",
    "self.result_entry": ["display_bg", "display_text"],
    "self.copy_button": ["special_button_fg", "border_color", "hover_default", "special_button_text"],
}

# ==========================================================
# TopBarTooltipMap (από mainCalcPreview.py)
# ==========================================================
TopBarTooltipMap = {
    "self": "background",
    "self.top_bar_frame": "background",
    "self.menu_button": ["top_frame_bg", "top_button_hover"],
    "self.sound_button": ["top_frame_bg", "top_button_hover"],
    "self.mode_label_display": "menu_text_color",
}

# ==========================================================