"""
themeManager.py

Αυτό το module διαχειρίζεται τα θέματα χρωμάτων για την Επιστημονική Αριθμομηχανή.
Ορίζονται τα θέματα για dark, light, purple, oceanic, mondrian, goth, μαζί με τις παραμέτρους τους.
"""

# ---------------------------------------------------------------------------
# Ορισμοί για το Dark Theme
# ---------------------------------------------------------------------------
DARK_THEME = {
    "background":       "#222222",  # Γενικό background
    "top_frame_bg":     "#222222",  # Background του top frame
    "bottom_frame_bg":  "#222222",  # Background του bottom frame
    "slide_menu_bg":    "#222222",  # Background του slide menu
    "inner_frame_bg":   "#222222",  # Background του inner frame του slide menu
    "display_bg":       "#000000",  # Background του display
    "angle_mode_bg":    "#000000",  # Background του angle mode (εντός τού display)
    "dropdown_fg":      "#4f4f4f",  # Background του dropdown menu
    "entry_fg":         "#ffffff",  # Background του entry field (π.χ. για το Currency Converter)

    "top_button_bg":    "#4f4f4f",  # Background των top buttons
    "num_button_bg":    "#a6a6a6",  # Background των num buttons
    "op_button_bg":     "#7c7c7c",  # Background των op buttons
    "ac_button_bg":     "#eb7c16",  # Background των ac και c buttons
    "menu_button_bg":   "#eb7c16",  # Background του menu button
    "manual_button_bg": "#000000",  # Χρώμα background του manual button
    "special_button_fg":"#eb7c16",  # Χρώμα background για τα ειδικά κουμπιά, 2nd, Rad, Deg

    #χρώμα των κειμένων
    "top_button_text":      "#ffffff",  # Χρώμα κειμένου των top buttons
    "num_button_text":      "#ffffff",  # Χρώμα κειμένου των num buttons
    "op_button_text":       "#ffffff",  # Χρώμα κειμένου των op buttons
    "ac_button_text":       "#ffffff",  # Χρώμα κειμένου των ac και c buttons
    "display_text":         "#00ff00",  # Χρώμα κειμένου του display
    "angle_mode_text":      "#00ff00",  # Χρώμα κειμένου για τη γωνία (πχ Rad, Deg)
    "manual_button_text":   "#eb7c16",  # Χρώμα κειμένου του manual button
    "menu_text_color":      "#ffffff",  # Χρώμα κειμένου του menu button
    "special_button_text":  "#ffffff",  # Χρώμα κειμένου για τα ειδικά κουμπιά, 2nd, Rad, Deg
    "label_text":           "#ffffff",  # Χρώμα κειμένου για τις ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",  # Χρώμα κειμένου για τα placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",  # Χρώμα κειμένου για το input field (π.χ. για το Currency Converter)

    # Hover χρώματα
    "hover_default":        "#6e6e6e",  # Χρώμα hover για τα κουμπιά γενικά
    "top_button_hover":     "#6e6e6e",  # Χρώμα hover για τα top buttons
    "hover_special":        "#f39c12",  # Χρώμα hover για τα ειδικά κουμπιά
    "num_hover":            "#b6b6b6",  # Χρώμα hover για τα num buttons
    "op_hover":             "#8c8c8c",  # Χρώμα hover για τα op buttons
    "ac_hover":             "#f39c12",  # Χρώμα hover για τα ac και c buttons
    "hover_manual_button":  "#000000",  # Χρώμα hover για το manual button
    "menu_button_hover":    "#d06c11",  # Χρώμα hover του menu button
    "special_button_hover": "#f39c12",  # Χρώμα hover για τα ειδικά κουμπιά, 2nd, Rad, Deg

    # Pop-up History
    "popup_history_bg":                 "#222222",  # Φόντο παραθύρου ιστορικού
    "popup_history_border":             "#4f4f4f",  # Χρώμα περιγράμματος (border) παραθύρου
    "popup_history_border_width": 1,  # Πάχος περιγράμματος (border width)
    "popup_history_fg":                 "#333333",  # Φόντο scrollable περιοχής
    "popup_history_scrollbar_bg":       "#222222",  # Χρώμα φόντου scrollbar
    "popup_history_scrollbar_thumb":    "#4f4f4f",  # Χρώμα "χειρολαβής" (thumb) του scrollbar
    "popup_history_line_bg":            "#333333",  # Φόντο κουμπιού για κάθε entry
    "popup_history_hover":              "#4f4f4f",  # Hover χρώμα κάθε κουμπιού ιστορικού
    "popup_history_text":               "#ffffff",  # Χρώμα κειμένου στα κουμπιά ιστορικού

    #testing colors
    "red4test":     "red",  # Χρώμα για δοκιμές
    "blue4test":    "blue"  # Χρώμα για δοκιμές

}

# ---------------------------------------------------------------------------
# Ορισμοί για το Light Theme
# ---------------------------------------------------------------------------
LIGHT_THEME = {
    "background":       "#e3e3e3",  # Γενικό background
    "top_frame_bg":     "#e3e3e3",  # Background του top frame
    "bottom_frame_bg":  "#e3e3e3",  # Background του bottom frame
    "display_bg":       "#ffffff",  # Background του display
    "angle_mode_bg":    "#ffffff",  # Background του angle mode (εντός του display)
    "slide_menu_bg":    "#929292",  # Background του slide menu
    "inner_frame_bg":   "#929292",  # Background του inner frame του slide menu
    "dropdown_fg":      "#929292",  # Background του dropdown menu
    "entry_fg":         "#ffffff",  # Background του entry field (π.χ. για το Currency Converter)

    "top_button_bg":    "#929292",  # Background των top buttons
    "num_button_bg":    "#ffffff",  # Background των num buttons
    "op_button_bg":     "#bebebe",  # Background των op buttons
    "ac_button_bg":     "#ff6f00",  # Background των ac και c buttons
    "manual_button_bg": "#ffffff",  # Χρώμα background του manual button
    "menu_button_bg":   "#bebebe",  # Background του menu button

    "top_button_text":      "#ffffff",  # Χρώμα κειμένου των top buttons
    "num_button_text":      "#000000",  # Χρώμα κειμένου των num buttons
    "op_button_text":       "#333333",  # Χρώμα κειμένου των op buttons
    "ac_button_text":       "#ffffff",  # Χρώμα κειμένου των ac και c buttons
    "display_text":         "#212121",  # Χρώμα κειμένου του display
    "angle_mode_text":      "#333333",  # Χρώμα κειμένου για τη γωνία (πχ Rad, Deg)
    "manual_button_text":   "#ff6f00",  # Χρώμα κειμένου του manual button
    "special_button_text":  "#ffffff",  # Χρώμα κειμένου για τα ειδικά κουμπιά, 2nd, Rad, Deg
    "menu_text_color":      "#ffffff",  # Χρώμα κειμένου του menu button
    "label_text":           "#222222",  # Χρώμα κειμένου για τις ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",  # Χρώμα κειμένου για τα placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",  # Χρώμα κειμένου για το input field (π.χ. για το Currency Converter)

    "hover_default":        "#e6e6e6",  # Χρώμα hover για τα κουμπιά γενικά
    "top_button_hover":     "#dcdcdc",  # Χρώμα hover για τα top buttons
    "hover_special":        "#ff8f00",  # Χρώμα hover για τα ειδικά κουμπιά
    "num_hover":            "#f2f2f2",  # Χρώμα hover για τα num buttons
    "op_hover":             "#d6d6d6",  # Χρώμα hover για τα op buttons
    "ac_hover":             "#ff8f00",  # Χρώμα hover για τα ac και c buttons
    "hover_manual_button":  "#f5f5f5",  # Χρώμα hover για το manual button
    "menu_button_hover":    "#ff8f00",  # Χρώμα hover του menu button

    "special_button_fg":    "#ff6f00",  # Χρώμα background για τα ειδικά κουμπιά, 2nd, Rad, Deg
    "special_button_hover": "#ff8f00",  # Χρώμα hover για τα ειδικά κουμπιά, 2nd, Rad, Deg
}

# ---------------------------------------------------------------------------
# Ορισμοί για το purple Theme
# ---------------------------------------------------------------------------
PURPLE_THEME = {
    # Πλαίσια και Οθόνες
    "background":           "#a87aff",   # Γενικό φόντο εφαρμογής
    "top_frame_bg":         "#a87aff",   # Φόντο του πάνω πλαισίου
    "slide_menu_bg":        "#9761ff",   # Φόντο του slide menu
    "inner_frame_bg":       "#9761ff",   # Φόντο του εσωτερικού πλαισίου του slide menu
    "bottom_frame_bg":      "#a87aff",   # Φόντο του κάτω πλαισίου
    "display_bg":           "#421699",   # Φόντο της οθόνης
    "display_text":         "#00ff00",   # Χρώμα κειμένου της οθόνης
    "angle_mode_bg":        "#421699",   # Φόντο για το angle mode (εντός οθόνης)
    "angle_mode_text":      "#00ff00",   # Χρώμα κειμένου για το angle mode

    # Κουμπιά αριθμών (π.χ. 1, 2, 3...)
    "num_button_bg":        "#c3a8f6",   # Φόντο κουμπιών αριθμών
    "num_button_text":      "#000000",   # Χρώμα κειμένου κουμπιών αριθμών
    "num_hover":            "#e1d0ff",   # Χρώμα hover κουμπιών αριθμών

    # Κουμπιά πράξεων (π.χ. +, -, x, ÷)
    "op_button_bg":         "#9761ff",   # Φόντο κουμπιών πράξεων
    "op_button_text":       "#000000",   # Χρώμα κειμένου κουμπιών πράξεων
    "op_hover":             "#c3a8f6",   # Χρώμα hover κουμπιών πράξεων

    # Κουμπιά AC / C
    "ac_button_bg":         "#d413d8",   # Φόντο κουμπιών AC/C
    "ac_button_text":       "#ffffff",   # Χρώμα κειμένου κουμπιών AC/C
    "ac_hover":             "#9c119f",   # Χρώμα hover κουμπιών AC/C

    # Κουμπιά στο πάνω μέρος (π.χ. mc, mr, m+, m-)
    "top_button_bg":        "#763ee4",   # Φόντο top κουμπιών
    "top_button_text":      "#ffffff",   # Χρώμα κειμένου top κουμπιών
    "top_button_hover":     "#5c30b4",   # Χρώμα hover top κουμπιών

    # Ειδικά κουμπιά (π.χ. 2nd, Rad, Deg)
    "special_button_fg":    "#d413d8",   # Φόντο ειδικών κουμπιών
    "special_button_hover": "#9c119f",   # Χρώμα hover ειδικών κουμπιών
    "special_button_text":  "#ffffff",   # Χρώμα κειμένου ειδικών κουμπιών

    # Κουμπί Manual
    "manual_button_bg":     "#421699",   # Φόντο κουμπιού manual
    "manual_button_text":   "#00ff00",   # Χρώμα κειμένου κουμπιού manual
    "hover_manual_button":  "#421699",   # Χρώμα hover κουμπιού manual

    # Hover γενικής χρήσης (fallback)
    "hover_default":        "#5c30b4",   # Γενικό χρώμα hover
    "hover_special":        "#5c30b4",   # Χρώμα hover για ειδικά κουμπιά

    # Μενού (κουμπί + χρώματα κειμένου)
    "menu_button_bg":       "#d413d8",   # Φόντο κουμπιού μενού
    "menu_button_hover":    "#9c119f",   # Χρώμα hover κουμπιού μενού
    "menu_text_color":      "#ffffff",   # Χρώμα κειμένου κουμπιού μενού

    "dropdown_fg":          "#763ee4",   # Φόντο dropdown menu
    "label_text":           "#ffffff",   # Χρώμα κειμένου για ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",   # Χρώμα placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",   # Χρώμα κειμένου input field (π.χ. για το Currency Converter)
    "entry_fg":             "#ffffff",   # Φόντο entry field (π.χ. για το Currency Converter)
}


# ---------------------------------------------------------------------------
# Ορισμοί για το Oceanic Theme
# ---------------------------------------------------------------------------
OCEANIC_THEME = {
    "background":           "#1b2b34",  # Σκούρο γαλάζιο-γκρί (φόντο εφαρμογής)
    "display_bg":           "#0f1c22",  # Πολύ σκούρο μπλε (οθόνη)
    "angle_mode_bg":        "#0f1c22",  # Φόντο για το angle mode (εντός οθόνης)
    "top_frame_bg":         "#1b2b34",  # Φόντο του πάνω πλαισίου
    "slide_menu_bg":        "#1b2b34",  # Φόντο του slide menu
    "inner_frame_bg":       "#1b2b34",  # Φόντο του εσωτερικού πλαισίου του slide menu
    "bottom_frame_bg":      "#1b2b34",  # Φόντο του κάτω πλαισίου
    "dropdown_fg":          "#4c6473",  # Φόντο του dropdown menu
    "entry_fg":             "#ffffff",  # Φόντο του entry field (π.χ. για το Currency Converter)

    "top_button_bg":        "#4c6473",  # Ψυχρό μπλε για λειτουργίες
    "num_button_bg":        "#78a0b4",  # Πιο φωτεινό μπλε για αριθμούς
    "op_button_bg":         "#3d5c69",  # Ήπιο γκρίζο-μπλέ για πράξεις
    "ac_button_bg":         "#00bcd4",  # Έντονο κυανό για AC/C

    "top_button_text":      "#ffffff",  # Χρώμα κειμένου των top buttons
    "num_button_text":      "#ffffff",  # Χρώμα κειμένου των num buttons
    "op_button_text":       "#ffffff",  # Χρώμα κειμένου των op buttons
    "ac_button_text":       "#ffffff",  # Χρώμα κειμένου των ac/c buttons
    "display_text":         "#00ffff",  # Φωτεινό κυανό για οθόνη
    "special_button_text":  "#ffffff",  # Χρώμα κειμένου ειδικών κουμπιών
    "label_text":           "#ffffff",  # Χρώμα κειμένου για τις ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",  # Χρώμα placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",  # Χρώμα κειμένου input field (π.χ. για το Currency Converter)

    # Hover Χρώματα
    "hover_default":        "#5e7b8b",  # Γενικό χρώμα hover
    "top_button_hover":     "#5e7b8b",  # Χρώμα hover για τα top buttons
    "hover_special":        "#00e5ff",  # Hover ειδικών κουμπιών (γαλάζιο)
    "num_hover":            "#91b7c8",  # Hover για num buttons
    "op_hover":             "#527682",  # Hover για op buttons
    "ac_hover":             "#00e5ff",  # Hover για ac/c buttons
    "hover_manual_button":  "#0f1c22",  # Hover για manual button

    # Άλλα στοιχεία
    "angle_mode_text":      "#00ffff",  # Χρώμα κειμένου για το angle mode
    "switch_text":          "#ffffff",  # Χρώμα κειμένου switch
    "switch_fg":            "#00bcd4",  # Χρώμα switch foreground
    "switch_progress":      "#00bcd4",  # Χρώμα switch progress
    "manual_button_text":   "#00bcd4",  # Χρώμα κειμένου manual button
    "manual_button_bg":     "#0f1c22",  # Φόντο manual button

    # Ειδικά κουμπιά
    "special_button_fg":    "#00bcd4",  # Φόντο ειδικών κουμπιών
    "special_button_hover": "#00e5ff",  # Hover ειδικών κουμπιών

    "menu_button_bg":       "#1b2b34",  # Φόντο κουμπιού μενού
    "menu_button_hover":    "#cc0000",  # Hover κουμπιού μενού
    "menu_text_color":      "#ffffff"   # Χρώμα κειμένου κουμπιού μενού
}

# ---------------------------------------------------------------------------
# Ορισμοί για το Goth Theme
# ---------------------------------------------------------------------------
GOTH_THEME = {
    "background":         "#1a1a1a",  # Γενικό background
    "top_frame_bg":       "#1a1a1a",  # Background του top frame
    "bottom_frame_bg":    "#1a1a1a",  # Background του bottom frame
    "display_bg":         "#000000",  # Background του display
    "angle_mode_bg":      "#000000",  # Background του angle mode (εντός του display)
    "dropdown_fg":        "#330000",  # Background του dropdown menu
    "entry_fg":           "#ffffff",  # Background του entry field (π.χ. για το Currency Converter)

    "top_button_bg":      "#330000",  # Background των top buttons
    "num_button_bg":      "#4d0000",  # Background των num buttons
    "op_button_bg":       "#660000",  # Background των op buttons
    "slide_menu_bg":      "#1a1a1a",  # Background του slide menu
    "inner_frame_bg":     "#1a1a1a",  # Background του inner frame του slide menu
    "ac_button_bg":       "#990000",  # Background των ac και c buttons
    "manual_button_bg":   "#000000",  # Χρώμα background του manual button

    "top_button_text":    "#ff0000",  # Χρώμα κειμένου των top buttons
    "num_button_text":    "#ffffff",  # Χρώμα κειμένου των num buttons
    "op_button_text":     "#ff6666",  # Χρώμα κειμένου των op buttons
    "ac_button_text":     "#ffffff",  # Χρώμα κειμένου των ac και c buttons
    "display_text":       "#ff1a1a",  # Χρώμα κειμένου του display
    "angle_mode_text":    "#ff1a1a",  # Χρώμα κειμένου για τη γωνία (πχ Rad, Deg)
    "manual_button_text": "#ff0000",  # Χρώμα κειμένου του manual button
    "special_button_text":"#ffffff",  # Χρώμα κειμένου για τα ειδικά κουμπιά, 2nd, Rad, Deg
    "label_text":         "#ffffff",  # Χρώμα κειμένου για τις ετικέτες (labels)
    "placeholder_text":   "#BEBEBE",  # Χρώμα κειμένου για τα placeholder (π.χ. για το Currency Converter)
    "text_input":         "#000000",  # Χρώμα κειμένου για το input field (π.χ. για το Currency Converter)

    "hover_default":         "#800000",  # Χρώμα hover για τα κουμπιά γενικά
    "top_button_hover":      "#800000",  # Χρώμα hover για τα top buttons
    "hover_special":         "#b30000",  # Χρώμα hover για τα ειδικά κουμπιά
    "num_hover":             "#661111",  # Χρώμα hover για τα num buttons
    "op_hover":              "#990000",  # Χρώμα hover για τα op buttons
    "ac_hover":              "#b30000",  # Χρώμα hover για τα ac και c buttons
    "hover_manual_button":   "#1a1a1a",  # Χρώμα hover για το manual button

    "special_button_fg":     "#990000",  # Χρώμα background για τα ειδικά κουμπιά, 2nd, Rad, Deg
    "special_button_hover":  "#cc0000",  # Χρώμα hover για τα ειδικά κουμπιά, 2nd, Rad, Deg

    "menu_button_bg":        "#990000",  # Background του menu button
    "menu_button_hover":     "#cc0000",  # Χρώμα hover του menu button
    "menu_text_color":       "#ffffff"   # Χρώμα κειμένου του menu button
}

# ---------------------------------------------------------------------------
# Ορισμοί για το Mondrian Theme
# ---------------------------------------------------------------------------
MONDRIAN_THEME = {
    # ---------------------------------------------------------------------------
    # Backgrounds (εμφάνιση πλαισίων)
    # ---------------------------------------------------------------------------
    "background":           "#000000",  # Μαύρο φόντο εφαρμογής
    "display_bg":           "#f0f0f0",  # Ανοιχτό γκρι φόντο οθόνης
    "angle_mode_bg":        "#f0f0f0",  # Ανοιχτό γκρι φόντο angle mode
    "top_frame_bg":         "#000000",  # Μαύρο φόντο πάνω πλαισίου
    "slide_menu_bg":        "#999999",  # Γκρι φόντο slide menu
    "inner_frame_bg":       "#999999",  # Γκρι φόντο εσωτερικού πλαισίου slide menu
    "bottom_frame_bg":      "#000000",  # Μαύρο φόντο κάτω πλαισίου

    # ---------------------------------------------------------------------------
    # Button Backgrounds
    # ---------------------------------------------------------------------------
    "top_button_bg":        "#ff0000",  # Έντονο κόκκινο για top buttons
    "num_button_bg":        "#ffffff",  # Λευκά κουμπιά αριθμών
    "op_button_bg":         "#0000ff",  # Έντονο μπλε για κουμπιά πράξεων
    "ac_button_bg":         "#ffcc00",  # Κίτρινο για AC/C κουμπιά
    "manual_button_bg":     "#f0f0f0",  # Ανοιχτό γκρι για manual button
    "special_button_fg":    "#ffcc00",  # Κίτρινο για ειδικά κουμπιά
    "menu_button_bg":       "#ffffff",  # Λευκό για menu button
    "entry_fg":             "#ffffff",  # Λευκό φόντο entry field (π.χ. Currency Converter)

    # ---------------------------------------------------------------------------
    # Text Colors
    # ---------------------------------------------------------------------------
    "top_button_text":      "#ffffff",  # Λευκό κείμενο στα top buttons
    "num_button_text":      "#000000",  # Μαύρο κείμενο στα κουμπιά αριθμών
    "op_button_text":       "#ffffff",  # Λευκό κείμενο στα κουμπιά πράξεων
    "ac_button_text":       "#000000",  # Μαύρο κείμενο στα κουμπιά AC/C
    "display_text":         "#000000",  # Μαύρο κείμενο στην οθόνη
    "angle_mode_text":      "#000000",  # Μαύρο κείμενο στο angle mode
    "manual_button_text":   "#000000",  # Μαύρο κείμενο στο manual button
    "menu_text_color":      "#000000",  # Μαύρο κείμενο στο menu button
    "special_button_text":  "#000000",  # Μαύρο κείμενο στα ειδικά κουμπιά
    "label_text":           "#ffffff",  # Λευκό κείμενο για ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",  # Γκρι placeholder (π.χ. Currency Converter)
    "text_input":           "#000000",  # Μαύρο κείμενο input field (π.χ. Currency Converter)

    # ---------------------------------------------------------------------------
    # Hover Colors
    # ---------------------------------------------------------------------------
    "hover_default":        "#d9d9d9",  # Ανοιχτό γκρι hover γενικά
    "top_button_hover":     "#ff4d4d",  # Ανοιχτό κόκκινο hover για top buttons
    "hover_special":        "#ffa500",  # Πορτοκαλί hover για ειδικά κουμπιά
    "num_hover":            "#e6e6e6",  # Ανοιχτό γκρι hover για αριθμούς
    "op_hover":             "#4d4dff",  # Ανοιχτό μπλε hover για πράξεις
    "ac_hover":             "#ffd633",  # Ανοιχτό κίτρινο hover για AC/C
    "hover_manual_button":  "#f0f0f0",  # Ανοιχτό γκρι hover για manual button
    "menu_button_hover":    "#e0e0e0",  # Ανοιχτό γκρι hover για menu button
    "special_button_hover": "#ffd633",  # Ανοιχτό κίτρινο hover για ειδικά κουμπιά
}

RAINBOW_THEME = {
    # ---------------------------------------------------------------------------
    # Backgrounds (εμφάνιση πλαισίων)
    # ---------------------------------------------------------------------------
    "background":           "#FFD63A",   # Κίτρινο φόντο εφαρμογής
    "top_frame_bg":         "#FFD63A",   # Κίτρινο φόντο πάνω πλαισίου
    "bottom_frame_bg":      "#FFD63A",   # Κίτρινο φόντο κάτω πλαισίου
    "display_bg":           "#6DE1D2",   # Τιρκουάζ φόντο οθόνης
    "angle_mode_bg":        "#6DE1D2",   # Τιρκουάζ φόντο angle mode
    "manual_button_bg":     "#6DE1D2",   # Τιρκουάζ φόντο κουμπιού manual
    "slide_menu_bg":        "#FFA955",   # Πορτοκαλί φόντο slide menu
    "inner_frame_bg":       "#FFA955",   # Πορτοκαλί φόντο εσωτερικού πλαισίου slide menu

    # ---------------------------------------------------------------------------
    # Button Backgrounds
    # ---------------------------------------------------------------------------
    "top_button_bg":        "#FFA955",   # Πορτοκαλί φόντο top buttons
    "num_button_bg":        "#ffffff",   # Λευκό φόντο κουμπιών αριθμών
    "op_button_bg":         "#FFA955",   # Πορτοκαλί φόντο κουμπιών πράξεων
    "ac_button_bg":         "#F75A5A",   # Κόκκινο φόντο κουμπιών AC/C
    "menu_button_bg":       "#FFD63A",   # Κίτρινο φόντο κουμπιού μενού
    "entry_fg":             "#ffffff",   # Λευκό φόντο entry field (π.χ. για το Currency Converter)

    # ---------------------------------------------------------------------------
    # Text Colors
    # ---------------------------------------------------------------------------
    "top_button_text":      "#ffffff",   # Λευκό κείμενο στα top buttons
    "num_button_text":      "#000000",   # Μαύρο κείμενο στα κουμπιά αριθμών
    "op_button_text":       "#ffffff",   # Λευκό κείμενο στα κουμπιά πράξεων
    "ac_button_text":       "#ffffff",   # Λευκό κείμενο στα κουμπιά AC/C
    "display_text":         "#000000",   # Μαύρο κείμενο στην οθόνη
    "angle_mode_text":      "#000000",   # Μαύρο κείμενο στο angle mode
    "manual_button_text":   "#000000",   # Μαύρο κείμενο στο manual button
    "menu_text_color":      "#ffffff",   # Λευκό κείμενο στο κουμπί μενού
    "special_button_fg":    "#F75A5A",   # Κόκκινο φόντο ειδικών κουμπιών
    "special_button_text":  "#FFFFFF",   # Λευκό κείμενο ειδικών κουμπιών
    "label_text":           "#ffffff",   # Λευκό κείμενο για ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",   # Γκρι placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",   # Μαύρο κείμενο input field (π.χ. για το Currency Converter)

    # ---------------------------------------------------------------------------
    # Hover Colors
    # ---------------------------------------------------------------------------
    "hover_default":        "#e0e0e0",   # Ανοιχτό γκρι hover γενικά
    "top_button_hover":     "#F75A5A",   # Κόκκινο hover για top buttons
    "hover_special":        "#FFA955",   # Πορτοκαλί hover για ειδικά κουμπιά
    "num_hover":            "#e0e0e0",   # Ανοιχτό γκρι hover για αριθμούς
    "op_hover":             "#F75A5A",   # Κόκκινο hover για πράξεις
    "ac_hover":             "#FFA955",   # Πορτοκαλί hover για AC/C
    "hover_manual_button":  "#b3f0e6",   # Ανοιχτό τιρκουάζ hover για manual button
    "menu_button_hover":    "#FFA955",   # Πορτοκαλί hover για κουμπί μενού
    "special_button_hover": "#FFA955",   # Πορτοκαλί hover για ειδικά κουμπιά
}

EXCEL_2003_THEME = {
    "background":           "#C0DCC0",  # Νεκροζώντανο πράσινο γραφείου
    "top_frame_bg":         "#C0DCC0",  # Λίγο πιο σκούρο για διαχωρισμό
    "bottom_frame_bg":      "#C0DCC0",  # Ίδιο με το background
    "display_bg":           "#FFFFFF",  # Οθόνη = ξύλινο λευκό
    "slide_menu_bg":        "#A0C0A0",  # Πράσινο slide menu
    "inner_frame_bg":       "#A0C0A0",  # Πράσινο εσωτερικό frame
    "angle_mode_bg":        "#FFFFFF",  # Λευκό angle mode
    "manual_button_bg":     "#FFFFFF",  # Λευκό κουμπί manual

    # Buttons
    "top_button_bg":        "#E0E0E0",  # Κουμπί toolbar
    "num_button_bg":        "#FFFFFF",  # Λευκό κουμπί αριθμών
    "op_button_bg":         "#B0B0B0",  # Γκρι κουμπί πράξεων
    "ac_button_bg":         "#808080",  # Σκούρο γκρι AC/C
    "menu_button_bg":       "#C0DCC0",  # Πράσινο κουμπί μενού
    "entry_fg":             "#ffffff",  # Λευκό entry field (π.χ. για το Currency Converter)

    # Text
    "top_button_text":      "#000000",  # Μαύρο κείμενο top buttons
    "num_button_text":      "#000000",  # Μαύρο κείμενο αριθμών
    "op_button_text":       "#000000",  # Μαύρο κείμενο πράξεων
    "ac_button_text":       "#FFFFFF",  # Λευκό κείμενο AC/C
    "display_text":         "#000080",  # Βαθύ μπλε στην οθόνη
    "angle_mode_text":      "#000080",  # Βαθύ μπλε angle mode
    "manual_button_text":   "#000080",  # Βαθύ μπλε manual button
    "menu_text_color":      "#000000",  # Μαύρο κείμενο μενού
    "special_button_fg":    "#808080",  # Σκούρο γκρι ειδικά κουμπιά
    "special_button_text":  "#FFFFFF",  # Λευκό κείμενο ειδικών κουμπιών
    "label_text":           "#ffffff",  # Λευκό κείμενο για ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",  # Γκρι placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",  # Μαύρο κείμενο input field (π.χ. για το Currency Converter)

    # Hover
    "hover_default":        "#D0E0D0",  # Απαλό πράσινο hover γενικά
    "top_button_hover":     "#C0D0C0",  # Πράσινο hover top button
    "hover_special":        "#A0B0A0",  # Πιο σκούρο πράσινο hover ειδικών
    "num_hover":            "#F0F0F0",  # Ανοιχτό γκρι hover αριθμών
    "op_hover":             "#C0C0C0",  # Γκρι hover πράξεων
    "ac_hover":             "#A0A0A0",  # Ανοιχτό γκρι hover AC/C
    "hover_manual_button":  "#C0DCC0",  # Πράσινο hover manual button
    "menu_button_hover":    "#A0A0A0",  # Ανοιχτό γκρι hover μενού
    "special_button_hover": "#B0B000",  # Κίτρινο-χακί hover ειδικών κουμπιών
}
WIN95_ERROR_THEME = {
    "background":           "#C3C3C3",  # Κλασικό γκρι
    "top_frame_bg":         "#C3C3C3",  # Γκρι πάνω πλαίσιο
    "slide_menu_bg":        "#A9A9A9",  # Σκούρο γκρι slide menu
    "inner_frame_bg":       "#A9A9A9",  # Σκούρο γκρι εσωτερικό frame
    "bottom_frame_bg":      "#C3C3C3",  # Γκρι κάτω πλαίσιο
    "display_bg":           "#FFFFFF",  # Λευκή οθόνη
    "angle_mode_bg":        "#FFFFFF",  # Λευκό angle mode
    "manual_button_bg":     "#FFFFFF",  # Λευκό κουμπί manual

    # Buttons με σκιές θλίψης
    "top_button_bg":        "#D4D0C8",  # Ανοιχτό γκρι top buttons
    "num_button_bg":        "#FFFFFF",  # Λευκά κουμπιά αριθμών
    "op_button_bg":         "#D4D0C8",  # Ανοιχτό γκρι κουμπιά πράξεων
    "ac_button_bg":         "#000080",  # Classic μπλε BSOD για AC/C
    "menu_button_bg":       "#C3C3C3",  # Γκρι κουμπί μενού
    "entry_fg":             "#ffffff",  # Λευκό entry field (π.χ. για το Currency Converter)

    # Text colors
    "top_button_text":      "#000000",  # Μαύρο κείμενο top buttons
    "num_button_text":      "#000000",  # Μαύρο κείμενο αριθμών
    "op_button_text":       "#000000",  # Μαύρο κείμενο πράξεων
    "ac_button_text":       "#FFFFFF",  # Λευκό κείμενο AC/C
    "display_text":         "#000000",  # Μαύρο κείμενο οθόνης
    "angle_mode_text":      "#000000",  # Μαύρο κείμενο angle mode
    "manual_button_text":   "#000000",  # Μαύρο κείμενο manual button
    "menu_text_color":      "#FFFFFF",  # Λευκό κείμενο μενού
    "special_button_fg":    "#000080",  # Μπλε φόντο ειδικών κουμπιών
    "special_button_text":  "#FFFFFF",  # Λευκό κείμενο ειδικών κουμπιών
    "label_text":           "#ffffff",  # Λευκό κείμενο για ετικέτες (labels)
    "placeholder_text":     "#BEBEBE",  # Γκρι placeholder (π.χ. για το Currency Converter)
    "text_input":           "#000000",  # Μαύρο κείμενο input field (π.χ. για το Currency Converter)

    # Hover 
    "hover_default":        "#D9D9D9",  # Ανοιχτό γκρι hover γενικά
    "top_button_hover":     "#E0E0E0",  # Ανοιχτότερο γκρι hover top button
    "hover_special":        "#1E90FF",  # Electric blue hover ειδικών
    "num_hover":            "#EEEEEE",  # Πολύ ανοιχτό γκρι hover αριθμών
    "op_hover":             "#B0B0B0",  # Γκρι hover πράξεων
    "ac_hover":             "#1E90FF",  # Electric blue hover AC/C
    "hover_manual_button":  "#FFFFFF",  # Λευκό hover manual button
    "menu_button_hover":    "#1E90FF",  # Electric blue hover μενού
    "special_button_hover": "#A52A2A",  # Καφέ hover ειδικών κουμπιών
}




# ---------------------------------------------------------------------------
# Λεξικό που αντιστοιχίζει τα ονόματα θεμάτων στα αντίστοιχα λεξικά χρωμάτων
# καθολικά προσβάσιμο.
# ---------------------------------------------------------------------------
THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "purple": PURPLE_THEME,
    "oceanic": OCEANIC_THEME,
    "goth": GOTH_THEME,
    "mondrian": MONDRIAN_THEME,
    "rainbow": RAINBOW_THEME,
    "windows95": WIN95_ERROR_THEME,
    "excel2003": EXCEL_2003_THEME,
}


def get_theme(mode="dark"):
    """
    Επιστρέφει το αντίστοιχο λεξικό θέματος.

    :param mode: Το όνομα του θέματος (π.χ. "dark", "light").
    :return: Λεξικό με τους ορισμούς χρωμάτων για το θέμα.
             Επιστρέφει το DARK_THEME ως default αν το `mode` δε βρεθεί.
    """
    return THEMES.get(mode.lower(), DARK_THEME)


def get_all_theme_names():
    """
    Επιστρέφει μια λίστα με όλα τα διαθέσιμα ονόματα θεμάτων.
    Διαβάζει τα ονόματα δυναμικά από το λεξικό THEMES.

    :return: Μια λίστα με τα ονόματα των θεμάτων (strings).
    """
    return list(THEMES.keys())

