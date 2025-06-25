# =========================
# previewFrameManager.py
# =========================
# Δημιουργεί δυναμικά preview frames χωρίς να απαιτούνται ξεχωριστά αρχεία preview.

from frameManager import frame_data

# Δημιουργούμε preview frames αυτόματα
preview_frame_data = {}

for mode_name, frame_info in frame_data.items():
    original_class = frame_info["frame"]

    # Δημιουργούμε νέα κλάση με όνομα: FunctionalClassPreview
    preview_class = type(
        original_class.__name__ + "Preview",  # Το όνομα της νέας κλάσης
        (original_class,),                   # Κληρονομεί από την functional κλάση
        {}                                    # Δεν προσθέτουμε νέα χαρακτηριστικά
    )

    # Καταχωρούμε στο λεξικό preview frames
    preview_frame_data[mode_name] = {"frame": preview_class}

    print(f"Δημιουργήθηκε δυναμικό preview για: {mode_name} -> {preview_class.__name__}")
