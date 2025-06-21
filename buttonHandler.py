# buttonHandler.py
# ==========================================================
# Αυτό το αρχείο υλοποιεί τη λογική χειρισμού κουμπιών για την αριθμομηχανή.
# Περιλαμβάνει λειτουργίες όπως:
# - Αναπαραγωγή ήχου κατά το πάτημα κουμπιών.
# - Επεξεργασία και αξιολόγηση μαθηματικών εκφράσεων.
# - Υποστήριξη επιστημονικών συναρτήσεων (π.χ. sin, cos, log).
# - Διαχείριση ειδικών κουμπιών όπως "AC", "C", "Rand", "EE".
# - Έλεγχος ορίων για συναρτήσεις (π.χ. domain checks).
# - Μορφοποίηση αποτελεσμάτων με ακρίβεια.
# ==========================================================

#==================== ΕΙΣΑΓΩΓΗ ΒΙΒΛΙΟΘΗΚΩΝ ====================
import os  # Για έλεγχο ύπαρξης αρχείων
import pygame  # Για αναπαραγωγή ήχου
pygame.mixer.init()  # Αρχικοποίηση του mixer για ήχο

#==================== ΑΝΑΠΑΡΑΓΩΓΗ ΗΧΟΥ ====================
sound_path = "sounds/space_sound4.mp3"  # Διαδρομή αρχείου ήχου
if os.path.exists(sound_path):  # Έλεγχος αν υπάρχει το αρχείο ήχου
    click_sound = pygame.mixer.Sound(sound_path)  # Φόρτωση ήχου
else:
    click_sound = None  # Αν δεν υπάρχει, ορίζεται ως None
    print(f"Warning: Sound file '{sound_path}' not found.")  # Εμφάνιση προειδοποίησης

def play_click_sound(calculator):
    """Αναπαραγωγή ήχου αν είναι ενεργοποιημένος."""
    if hasattr(calculator, "sound_enabled") and calculator.sound_enabled and click_sound:
        click_sound.play()  # Παίζει τον ήχο

#==================== ΕΙΣΑΓΩΓΗ ΕΠΙΣΤΗΜΟΝΙΚΩΝ ΣΥΝΑΡΤΗΣΕΩΝ ====================
import re  # Για επεξεργασία εκφράσεων με κανονικές εκφράσεις
from mpmath import mp, mpf, sin, cos, tan, asin, acos, atan, asinh, acosh, atanh, sqrt, log, factorial, pi, e, sinh, cosh, tanh
mp.dps = 28  # Ορισμός ακρίβειας δεκαδικών ψηφίων

#==================== ΜΟΡΦΟΠΟΙΗΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ====================
def format_result(result):
    """Μορφοποίηση αποτελέσματος με σταθερή ακρίβεια και αφαίρεση περιττών μηδενικών."""
    try:
        num = float(result)  # Μετατροπή σε float
        formatted = "{:.10f}".format(num).rstrip("0").rstrip(".")  # Μορφοποίηση με 10 δεκαδικά ψηφία
        return formatted if formatted else "0"  # Επιστροφή μορφοποιημένου αποτελέσματος
    except:
        return str(result)  # Επιστροφή του αποτελέσματος ως string αν υπάρχει σφάλμα

#==================== ΧΕΙΡΙΣΜΟΣ ΚΟΥΜΠΙΩΝ ====================
def on_button_click(calculator, value):
    """Χειρισμός πατήματος κουμπιών."""
    play_click_sound(calculator)  # Αναπαραγωγή ήχου

    # Εναλλαγή λειτουργίας "2nd"
    if value == "2nd":
        calculator.toggle_second_function()
        return

    # Εναλλαγή γωνιακής μονάδας (Rad/Deg)
    if value in ["Rad", "Deg"]:
        calculator.toggle_angle_mode()
        return

    # Διαγραφή τελευταίου χαρακτήρα (C)
    if value == "C":
        backspace(calculator)
        calculator.middle_display.configure(text="")
        return

    # Εκκαθάριση όλων (AC)
    if value == "AC":
        calculator.display_var.set("0")  # Επαναφορά display
        calculator.middle_display.configure(text="")  # Επαναφορά ενδιάμεσης οθόνης
        calculator.history_display_var.set("")  # Επαναφορά ιστορικού
        calculator.memory = mpf("0")  # Επαναφορά μνήμης
        calculator.just_evaluated = False  # Επαναφορά κατάστασης αξιολόγησης
        return

    # Αξιολόγηση μαθηματικής έκφρασης (=)
    if value == "=":    # Έλεγχος αν το κουμπί είναι το κουμπί αξιολόγησης
        expr = calculator.display_var.get()  # Λήψη έκφρασης από το display
        try:        
            result = evaluate_expression(calculator, prepare_expression(calculator, expr))  # Αξιολόγηση έκφρασης

            if result == mpf(int(result)):  # Έλεγχος αν το αποτέλεσμα είναι ακέραιο
                result = int(result)    # Μετατροπή σε ακέραιο αν είναι δυνατόν

            entry = f"{expr.replace('*', '×').replace('/', '÷')} = {format_result(result)}"  # Δημιουργία εγγραφής ιστορικού
            calculator.history_display_var.set(entry)  # Ενημέρωση ιστορικού
            calculator.display_var.set(format_result(result))  # Ενημέρωση display
            calculator.history_log.append(entry)  # Προσθήκη στο ιστορικό

            calculator.middle_display.configure(text="")  # Επαναφορά ενδιάμεσης οθόνης
            calculator.just_evaluated = True  # Ενημέρωση κατάστασης αξιολόγησης

        except ZeroDivisionError:   # Διαχείριση διαίρεσης με το μηδέν
            msg = "Cannot divide by zero"  # Μήνυμα σφάλματος διαίρεσης με μηδέν
            calculator.middle_display.configure(text=msg)   # Ενημέρωση ενδιάμεσης οθόνης με μήνυμα σφάλματος
            calculator.display_var.set("Error") # Ενημέρωση display με "Error"

        except Exception as e:  # Γενική διαχείριση εξαιρέσεων
            if hasattr(e, 'args') and e.args and isinstance(e.args[0], str):    # Έλεγχος αν το σφάλμα έχει μήνυμα
                msg = e.args[0] # Λήψη του μηνύματος σφάλματος
            else:   # Αν δεν υπάρχει μήνυμα, ορίζουμε γενικό μήνυμα σφάλματος
                msg = "Error"       # Γενικό μήνυμα σφάλματος

            calculator.middle_display.configure(text=msg)  # Ενημέρωση ενδιάμεσης οθόνης με μήνυμα σφάλματος
            calculator.display_var.set("Error")  # Ενημέρωση display με "Error"

        return

    #==================== ΕΙΔΙΚΑ ΚΟΥΜΠΙΑ ====================
    # Αλλαγή πρόσημου (+/-)
    if value == "+/-":
        current = calculator.display_var.get()
        if current.startswith("-"):
            calculator.display_var.set(current[1:])  # Αφαίρεση αρνητικού πρόσημου
        else:
            calculator.display_var.set("-" + current)  # Προσθήκη αρνητικού πρόσημου
        return

    # Διαχείριση μνήμης (mc, m+, m-, mr)
    if value == "mc":   # Εκκαθάριση μνήμης
        calculator.memory = mpf("0")  # Εκκαθάριση μνήμης
        return          
    if value == "m+":   # Προσθήκη στην μνήμη
        try:            
            calculator.memory += evaluate_expression(calculator, prepare_expression(calculator, calculator.display_var.get()))  # Προσθήκη στη μνήμη
        except:     
            pass
        return
    if value == "m-":   # Αφαίρεση από τη μνήμη
        try:
            calculator.memory -= evaluate_expression(calculator, prepare_expression(calculator, calculator.display_var.get()))  # Αφαίρεση από τη μνήμη
        except:
            pass
        return
    if value == "mr":   # Ανάκτηση από τη μνήμη
        calculator.display_var.set(format_result(calculator.memory))  # Εμφάνιση μνήμης στο display
        return

    #==================== ΤΥΧΑΙΟΣ ΑΡΙΘΜΟΣ ====================
    if value == "Rand": # Δημιουργία τυχαίου αριθμού
        import random   # Εισαγωγή βιβλιοθήκης για τυχαίους αριθμούς
        rand_num = mpf(str(random.random()))  # Δημιουργία τυχαίου αριθμού
        calculator.display_var.set(format_result(rand_num))  # Ενημέρωση display
        return

    #==================== ΕΚΘΕΤΗΣ (EE) ====================
    if value == "EE":   # Έλεγχος αν το κουμπί είναι ο εκθέτης
        current = calculator.display_var.get()  # Λήψη της τρέχουσας τιμής από το display
        if current in ["0", "Error"]:           # Έλεγχος αν το display είναι κενό ή έχει σφάλμα
            calculator.display_var.set("e")  # Εισαγωγή εκθέτη
        else:
            calculator.display_var.set(current + "e")  # Προσθήκη εκθέτη στην τρέχουσα τιμή
        calculator.just_evaluated = False   # Ενημέρωση κατάστασης αξιολόγησης
        return

    #==================== ΠΟΣΟΣΤΟ (%) ====================
    if value == "%":    # Έλεγχος αν το κουμπί είναι το ποσοστό
        expr = calculator.display_var.get() # Λήψη της τρέχουσας έκφρασης από το display
        # Κανονική έκφραση για αναγνώριση μαθηματικών εκφράσεων (αριθμός, τελεστής, αριθμός)
        pattern = r'(-?\d+(?:\.\d+)?)([+\-x÷])(-?\d+(?:\.\d+)?)$'   
        m_obj = re.search(pattern, expr)    # Αναζήτηση για αριθμούς και τελεστές
        if m_obj:                           # Αν βρεθεί αντιστοίχιση
            try:    # Εξαγωγή των αριθμών και του τελεστή
                A = mpf(m_obj.group(1))                     # Πρώτος αριθμός
                op = m_obj.group(2)                         # Τελεστής
                B = mpf(m_obj.group(3))                     # Δεύτερος αριθμός
                newB = A * (B / mpf("100")) if op in ['+', '-'] else B / mpf("100") # Υπολογισμός νέου B ως ποσοστό του A
                new_expr = m_obj.group(1) + op + str(newB)  # Δημιουργία νέας έκφρασης
                calculator.display_var.set(new_expr)        # Ενημέρωση display με νέα έκφραση
            except Exception:               # Αν υπάρξει σφάλμα κατά την αξιολόγηση
                calculator.display_var.set("Error") # Ενημέρωση display με "Error"
        else:   # Αν δε βρεθεί αντιστοίχιση
            try:    # Προσπάθεια αξιολόγησης της τρέχουσας έκφρασης ως ποσοστό
                num = evaluate_expression(calculator, prepare_expression(calculator, expr)) # Αξιολόγηση της τρέχουσας έκφρασης
                result = num / mpf("100")   # Υπολογισμός του ποσοστού
                calculator.display_var.set(format_result(result))   # Ενημέρωση display με το αποτέλεσμα
            except Exception:   # Αν υπάρξει σφάλμα κατά την αξιολόγηση
                calculator.display_var.set("Error") # Ενημέρωση display με "Error"
        return

    #==================== ΕΠΙΣΤΗΜΟΝΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ====================
    # Έλεγχος αν το κουμπί είναι επιστημονική συνάρτηση
    if value in ["x²", "x³", "1/x", "√", "2ʸ", "sin", "cos", "tan", "sinh", "cosh", "tanh", "log₁₀", "log₂", "log_b", "x!"]:    
        if calculator.is_second_function and value in calculator.second_map:    # Έλεγχος αν είναι ενεργοποιημένη η δεύτερη λειτουργία  
            value = calculator.second_map[value]    # Αν ναι, αντικατάσταση με τη δεύτερη λειτουργία
        current = calculator.display_var.get()      # Λήψη της τρέχουσας τιμής από το display
        transformations = {  # Λεξικό μετασχηματισμών για τις επιστημονικές συναρτήσεις
            "sin"    : lambda operand: f"sin({operand})",
            "sin⁻¹"  : lambda operand: f"asin({operand})",
            "cos"    : lambda operand: f"cos({operand})",
            "cos⁻¹"  : lambda operand: f"acos({operand})",
            "tan"    : lambda operand: f"tan({operand})",
            "tan⁻¹"  : lambda operand: f"atan({operand})",
            "sinh"   : lambda operand: f"sinh({operand})",
            "sinh⁻¹" : lambda operand: f"asinh({operand})",
            "cosh"   : lambda operand: f"cosh({operand})",
            "cosh⁻¹" : lambda operand: f"acosh({operand})",
            "tanh"   : lambda operand: f"tanh({operand})",
            "tanh⁻¹" : lambda operand: f"atanh({operand})",
            "log₁₀"  : lambda operand: f"log({operand})",
            "log₂"   : lambda operand: f"log2({operand})",
            "log_b"  : lambda operand: operand,
            "x²"     : lambda operand: f"(({operand})**2)",
            "x³"     : lambda operand: f"(({operand})**3)",
            "1/x"    : lambda operand: f"(1/({operand}))",
            "√"      : lambda operand: f"sqrt({operand})",
            "2ʸ"     : lambda operand: f"((2)**({operand}))",
            "x!"     : lambda operand: f"factorial({operand})"
        }
        transform = transformations.get(value)  # Λήψη της συνάρτησης μετασχηματισμού από το λεξικό
        m = re.search(r'(.*?)(-?(?:\d*\.\d+|\d+))$', current)   # Κανονική έκφραση για αναγνώριση αριθμού στο τέλος της τρέχουσας τιμής
        if m and transform:     # Αν βρεθεί αριθμός και υπάρχει μετασχηματισμός
            prefix = m.group(1) # Λήψη του προθέματος (ό,τι υπάρχει πριν τον αριθμό)
            operand = m.group(2)    # Λήψη του αριθμού
            new_expr = f"{prefix}{transform(operand)}"  # Δημιουργία νέας έκφρασης με τον μετασχηματισμό
        else:   # Αν δεν βρεθεί αριθμός ή δεν υπάρχει μετασχηματισμός
            new_expr = f"{value}(" if current in ["0", "Error"] else f"{current}{value}("   # Δημιουργία νέας έκφρασης με την επιστημονική συνάρτηση
        calculator.display_var.set(new_expr)    # Ενημέρωση display με τη νέα έκφραση
        calculator.just_evaluated = False   # Ενημέρωση κατάστασης αξιολόγησης
        return

    #==================== ΕΚΘΕΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ====================
    if value == "yˣ":   # Έλεγχος αν είναι εκθετική συνάρτηση
        current = calculator.display_var.get()  # Λήψη της τρέχουσας τιμής από το display
        calculator.display_var.set("**" if current in ["0", "Error"] else current + "**")   # Προσθήκη εκθετικής συνάρτησης στο τέλος της τρέχουσας τιμής
        return      

    if value == "ⁿ√x":  # Έλεγχος αν είναι ριζική συνάρτηση
        current = calculator.display_var.get()  # Λήψη της τρέχουσας τιμής από το display
        calculator.display_var.set("r" if current in ["0", "Error"] else current + "r") # Προσθήκη ριζικής συνάρτησης στο τέλος της τρέχουσας τιμής
        return

    #==================== ΕΙΣΑΓΩΓΗ ΨΗΦΙΩΝ ====================
    if calculator.just_evaluated and value in "0123456789.":    # Έλεγχος αν έχει γίνει πρόσφατα αξιολόγηση και αν το κουμπί είναι ψηφίο ή τελεστή
        calculator.display_var.set("0." if value == "." else value)     # Επαναφορά display με το νέο ψηφίο ή τελεστή
        calculator.just_evaluated = False   # Ενημέρωση κατάστασης αξιολόγησης
    else:   # Αν δεν έχει γίνει πρόσφατα αξιολόγηση ή το κουμπί δεν είναι ψηφίο ή τελεστής
        current = calculator.display_var.get()  # Λήψη της τρέχουσας τιμής από το display
        if current in ["0", "Error"]:   # Έλεγχος αν το display είναι κενό ή έχει σφάλμα
            calculator.display_var.set("0." if value == "." else value) # Επαναφορά display με το νέο ψηφίο ή τελεστή
        else:   # Αν το display έχει ήδη τιμή
            calculator.display_var.set(current + value) # Προσθήκη του νέου ψηφίου ή τελεστή στο τέλος της τρέχουσας τιμής
        calculator.just_evaluated = False   # Ενημέρωση κατάστασης αξιολόγησης
        calculator.middle_display.configure(text="")    # Επαναφορά ενδιάμεσης οθόνης




def backspace(calculator):
    # Παίρνει την τρέχουσα έκφραση από το display
    expr = calculator.display_var.get() 
    # Αφαιρεί το τελευταίο συνεχόμενο τμήμα αριθμών ή δεκαδικών ψηφίων
    new_expr = re.sub(r'[\d.]+$', '', expr)
    # Αν το αποτέλεσμα είναι κενό, το θέτει σε "0"
    if new_expr == "":  # Έλεγχος αν το νέο expr είναι κενό
        new_expr = "0"  # Αν είναι κενό, επαναφορά σε "0"
    # Ενημερώνει το display με τη νέα έκφραση
    calculator.display_var.set(new_expr)

def prepare_expression(calculator, expr):
    expr = re.sub(r'\b(sin|cos|tan)(\d+(\.\d+)?)\b', r'\1(\2)', expr)   # Αντικατάσταση sin, cos, tan με sin(x), cos(x), tan(x)
    expr = expr.replace("x", "*")       # Αντικατάσταση x με *
    expr = expr.replace("÷", "/")       # Αντικατάσταση ÷ με /
    expr = expr.replace("π", "pi")      # Αντικατάσταση π με pi
    expr = expr.replace("√", "sqrt")    # Αντικατάσταση √ με sqrt
    expr = expr.replace("log₂", "log2") # Αντικατάσταση log₂ με log2
    expr = expr.replace("log₁₀", "log") # Αντικατάσταση log₁₀ με log
    expr = re.sub(r'(\d+(\.\d+)?)r(\d+(\.\d+)?)', r'nth_root(\3,\1)', expr) # Αντικατάσταση n√x με nth_root(x, n)
    expr = re.sub(                      # Αντικατάσταση log_b με log_b(x)
        r"mpf\('(\d+(\.\d+)?)'\)\s*log_b\s*mpf\('(\d+(\.\d+)?)'\)", 
        r"(log(mpf('\3'))/log(mpf('\1')))",     # log_b(x) = log(x) / log(b)
        expr                                    
    )
    expr = re.sub(r'(?<!\d)\.(\d+)', r'0.\1', expr) # Αντικατάσταση .123 με 0.123
    expr = re.sub(      # Αντικατάσταση αριθμών με mpf για ακρίβεια
        r'(?<![\w)])(-?\d+(?:\.\d+)?(?:e-?\d+)?)(?![\w(])',     # Αντικατάσταση αριθμών με mpf για ακρίβεια
        r"mpf('\1')",   # Αντικατάσταση αριθμών με mpf για ακρίβεια
        expr
    )

    return expr

def evaluate_expression(calculator, expr):  # Αξιολόγηση μαθηματικής έκφρασης
    def check_domain_issues(expr):          # Έλεγχος για προβλήματα ορίων συναρτήσεων
        try:    
            def get_val(val):       # Επιστρέφει την τιμή ως float
                return float(val)   # Αν δεν είναι έγκυρη τιμή, θα προκαλέσει σφάλμα

            # Trig domain checks
            if "asin" in expr or "acos" in expr:    # Έλεγχος για asin(x) και acos(x)
                matches = re.findall(r'(asin|acos)\(mpf\(\'([^\']+)\'\)\)', expr)   # Αναζήτηση για asin(x) και acos(x)
                for func, val in matches:   # Αναζήτηση για asin(x) και acos(x)
                    x = get_val(val)        # Επιστρέφει την τιμή ως float
                    if not -1 <= x <= 1:    # Αν η τιμή είναι μη έγκυρη
                        return f"Invalid input: {func} domain is [-1, 1]"   # Έλεγχος για asin(x) και acos(x)
            if "acosh" in expr:             # Έλεγχος για acosh(x)
                matches = re.findall(r'acosh\(mpf\(\'([^\']+)\'\)\)', expr) # Αναζήτηση για acosh(x)
                for val in matches:     # Αναζήτηση για acosh(x)
                    x = get_val(val)    # Επιστρέφει την τιμή ως float
                    if x < 1:           # Αν η τιμή είναι μικρότερη από 1
                        return "Invalid input: acosh domain is [1, ∞)"  # Έλεγχος για acosh(x)
            if "atanh" in expr:         # Έλεγχος για atanh(x)
                matches = re.findall(r'atanh\(mpf\(\'([^\']+)\'\)\)', expr) # Αναζήτηση για atanh(x)
                for val in matches:     # Αναζήτηση για atanh(x)
                    x = get_val(val)    # Επιστρέφει την τιμή ως float
                    if not -1 < x < 1:  # Αν η τιμή είναι εκτός του έγκυρου πεδίου
                        return "Invalid input: atanh domain is (-1, 1)" # Έλεγχος για atanh(x)

            # log(x), log2(x)   
            if "log" in expr:           # Έλεγχος για log(x)
                matches = re.findall(r'log\(mpf\(\'([^\']+)\'\)\)', expr)   # Αναζήτηση για log(x)
                for val in matches:     # Αναζήτηση για log(x)
                    x = get_val(val)    # Επιστρέφει την τιμή ως float
                    if x <= 0:          # Αν η τιμή είναι μη έγκυρη
                        return "Invalid input: log(x) domain is (0, ∞)"   # Έλεγχος για log(x)
            if "log2" in expr:          # Έλεγχος για log2(x)
                matches = re.findall(r'log2\(mpf\(\'([^\']+)\'\)\)', expr)  # Αναζήτηση για log2(x)
                for val in matches:     # Αναζήτηση για log2(x)
                    x = get_val(val)    # Επιστρέφει την τιμή ως float
                    if x <= 0:          # Αν η τιμή είναι μη έγκυρη
                        return "Invalid input: log2(x) domain is (0, ∞)"    # Έλεγχος για log2(x)

            # sqrt(x)
            if "sqrt" in expr:          # Έλεγχος για sqrt(x)
                matches = re.findall(r'sqrt\(mpf\(\'([^\']+)\'\)\)', expr)  # Αναζήτηση για sqrt(x)
                for val in matches:     # Αναζήτηση για sqrt(x)
                    x = get_val(val)    # Επιστρέφει την τιμή ως float
                    if x < 0:           # Αν η τιμή είναι αρνητική
                        return "Invalid input: sqrt(x) domain is [0, ∞)"    # Έλεγχος για αρνητική τιμή

            # 1/x
            if "1/(" in expr:           # Έλεγχος για διαίρεση με το μηδέν
                matches = re.findall(r'1/\(mpf\(\'([^\']+)\'\)\)', expr)    # Αναζήτηση για 1/(x)
                for val in matches:     # Για κάθε τιμή που βρέθηκε
                    x = get_val(val)    # Έλεγχος αν είναι έγκυρη τιμή
                    if x == 0:          # Αν η τιμή είναι μηδέν
                        return "Cannot divide by zero"  # Έλεγχος διαίρεσης με το μηδέν

        except:
            pass
        return None

    domain_msg = check_domain_issues(expr)  # Έλεγχος για προβλήματα ορίων συναρτήσεων
    if domain_msg:                          # Αν υπάρχει πρόβλημα ορίων
        raise ValueError(domain_msg)        # Αν υπάρχει πρόβλημα ορίων, ρίχνει εξαίρεση με το μήνυμα

    def format_result(result, precision=10):    # Μορφοποίηση αποτελέσματος με ακρίβεια
        try:    
            result = float(result)              # Μετατροπή σε float για μορφοποίηση
        except: 
            return str(result)                  # αν είναι Error κτλ.

        # Αν είναι πολύ κοντά σε ακέραιο (π.χ. 0.9999999999999999 → 1)
        if abs(result - round(result)) < 1e-12: # πολύ μικρή διαφορά    
            return str(int(round(result)))      # Επιστροφή ως ακέραιος

        # Εμφάνιση: αν πολύ μικρό ή πολύ μεγάλο → επιστημονική μορφή
        if abs(result) < 1e-4 or abs(result) > 1e+6:
            return f"{result:.{precision}e}"  # επιστημονική μορφή
        else:
            return f"{result:.{precision}g}"  # κανονική μορφή

    funcs = {
        'mpf'      : mpf,
        'sqrt'     : sqrt,
        'nth_root' : lambda x, n: n ** (mpf("1") / x),
        'sinh'     : sinh,
        'cosh'     : cosh,
        'tanh'     : tanh,
        'asinh'    : asinh,
        'acosh'    : acosh,
        'atanh'    : atanh,
        'log'      : lambda x: log(x) / log(10),    # log base 10
        'log2'     : lambda x: log(x) / log(2),     # log base 2
        'factorial': factorial,
        'pi'       : pi,
        'e'        : e,
        'EE'       : lambda x, y: x * (10 ** y)     # Εκθετική συνάρτηση EE
    }

    if calculator.is_degree:    # Αν είμαστε σε μοίρες
        funcs.update({          # Προσθήκη συναρτήσεων με γωνίες σε μοίρες
            'sin' : lambda x: sin(x * pi / 180),    
            'cos' : lambda x: cos(x * pi / 180),
            'tan' : lambda x: tan(x * pi / 180),
            'asin': lambda x: (asin(x) * 180 / pi),
            'acos': lambda x: (acos(x) * 180 / pi),
            'atan': lambda x: (atan(x) * 180 / pi),
        })
    else:   # Αν είμαστε σε ακτίνια
        funcs.update({  # Προσθήκη συναρτήσεων με γωνίες σε ακτίνια
            'sin' : sin,    
            'cos' : cos,
            'tan' : tan,
            'asin': asin,
            'acos': acos,
            'atan': atan,
        })

    return eval(expr, {"__builtins__": None}, funcs)    # Αξιολόγηση της έκφρασης με ασφαλή περιβάλλον
    # Επιστρέφει το αποτέλεσμα της αξιολόγησης