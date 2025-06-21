# keyboardInputHandler.py
from buttonHandler import on_button_click

def handle_keyboard_input(char, calculator):
    key_map = {
        '\r': '=',        # Enter or =
        '\n': '=',        # Alternate newline
        '\x08': 'C',      # Backspace
        '*': '*',
        '/': '÷',
        '+': '+',
        '-': '-',
        '.': '.',
        '%': '%',
        '=': '=',
        'x': '*',
        '(': '(',
        ')': ')',
        'C': 'AC',          # C key to All Clear
        'E': '+/-',         #  Toggle Sign
        'R': '1/x' ,        #  Reciprocal
        'Q': 'x²' ,         #  Square
        'S': '√',           #  Square Root
        'T': 'mc',          # Memory Clear
        'Y': 'm+',          # Memory Add
        'U': 'm-',          # Memory Subtract
        'I': 'mr',          # Memory Recall
        'H' : 'sin',        #sine trigonometric function
        'J' : 'cos',        #trigonometric function that relates an angle of a right-angled triangle
        'K' : 'tan',        #tangent' function
        'L' : 'sinh',       #Hyperbolic sine function
        'Z' : 'cosh',       #hyperbolic cosine function
        'X' : 'tanh',       #hyperbolic tangent function
        'V' : 'π',          #3,14
        'B' : 'x!',         #factorial function
        'W' : 'x³',         # cube
        'N' : 'Rand',       #generate random number
        'M' : 'EE',
        'P' : '2ʸ',         #calculate the square of a value
        'G' : 'log2',       #calculates the power to which 2 must be raised to get a specified number
        'F' :  'log10',     #calculates the power to which 10 must be raised to get a specified number.




    }

    mapped = key_map.get(char, char if char.isdigit() or char == '.' else None)

    if mapped:
        on_button_click(calculator, mapped)






