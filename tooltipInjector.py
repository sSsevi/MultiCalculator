# tooltipInjector.py

from tooltip import Tooltip

def inject_tooltips_from_map(obj, theme_map: dict):
    """
    Κάνει inject τα Tooltips με βάση το theme_map.
    Υποστηρίζει:
    - Μοναδικά widgets (π.χ. self.manual_button)
    - Λίστες από widgets (π.χ. self.numeric_buttons)
    - Λίστες από λίστες από widgets (π.χ. self.top_button_objects)
    """
    for attr_name, theme_key in theme_map.items():
        try:
            widget = eval(attr_name, {}, {"self": obj})

            if widget is None:
                continue  # Αγνοούμε None

            if isinstance(widget, list):
                for item in widget:
                    if isinstance(item, list):
                        for sub_item in item:
                            if sub_item:
                                Tooltip(sub_item, theme_key)
                    else:
                        if item:
                            Tooltip(item, theme_key)
            else:
                Tooltip(widget, theme_key)

        except Exception as e:
            print(f"[TooltipInjector] Δεν μπόρεσα να κάνω inject στο '{attr_name}': {e}")
