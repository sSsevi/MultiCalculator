import ast

def get_args(node):
    args = []
    for arg in node.args.args:
        args.append(arg.arg)
    # Προσθήκη default τιμών (αν υπάρχουν)
    defaults = [None] * (len(args) - len(node.args.defaults)) + node.args.defaults
    arg_list = []
    for name, default in zip(args, defaults):
        if default is not None:
            if isinstance(default, ast.Constant):
                arg_list.append(f"{name}={repr(default.value)}")
            else:
                arg_list.append(f"{name}=...")
        else:
            arg_list.append(name)
    return ", ".join(arg_list)

def print_outline(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, ast.ClassDef):
        print(f"{prefix}Class: {node.name}")
        # Εμφάνιση attributes κλάσης
        for child in node.body:
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        print(f"{prefix}  Attribute: {target.id}")
        # Εμφάνιση μεθόδων και nested στοιχείων
        for child in node.body:
            print_outline(child, indent + 1)
    elif isinstance(node, ast.FunctionDef):
        args = get_args(node)
        print(f"{prefix}Function: {node.name}({args})")
        # Εμφάνιση attributes στιγμιοτύπου (self.x)
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if (isinstance(target, ast.Attribute) and
                        isinstance(target.value, ast.Name) and
                        target.value.id == "self"):
                        print(f"{prefix}  Attribute: {target.attr}")
            # Εμφάνιση nested functions
            if isinstance(stmt, ast.FunctionDef):
                print_outline(stmt, indent + 1)

with open("mainCalc.py", "r", encoding="utf-8") as f:
    tree = ast.parse(f.read())

for node in tree.body:
    print_outline(node)