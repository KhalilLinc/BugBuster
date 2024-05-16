import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from options.beautify import beautify_code
import autopep8
bButton = True
def attempt_auto_fix(file_path):
    # Attempt automatic code fixing
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            compile(code, file_path, 'exec')
        messagebox.showinfo("Success", "Automatic code fixing successful.")
        return True
    except SyntaxError:
        return False

def load_option(option_name):
    option_file_path = os.path.join("options", option_name)
    if os.path.exists(option_file_path):
        try:
            with open(option_file_path, 'r') as option_file:
                option_code = option_file.read()
                return option_code
        except Exception as e:
            messagebox.showerror("Error", f"Error loading option '{option_name}': {e}")
    else:
        messagebox.showerror("Error", f"Option '{option_name}' not found.")
    return None

def fix_code_with_option(file_path, option_name, line_number):
    global bButton
    try:
        if option_name == "beautify.py":
            # If the option is to beautify the code, call the beautify_code function
            formatted_code = beautify_code(file_path)
            if isinstance(formatted_code, str):
                with open(file_path, 'w') as file:
                    file.write(formatted_code)
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, f"\n $-/ The code has been beautified.")
                text_area.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Beautify Error", formatted_code)
        else:
            with open(file_path, 'r') as file:
                code = file.read()
            option_code = load_option(option_name)
            if option_code is not None:
                exec(option_code, globals())
                fixed_code = fix_code(code, line_number)
                with open(file_path, 'w') as file:
                    file.write(fixed_code)
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, f"\n $-/Changes saved to {file_path}.")
                text_area.config(state=tk.DISABLED)
                if bButton :
                    fix_button = tk.Button(root, text="Beautify", command=lambda: attempt_fix(file_path, "beautify.py", 0))
                    fix_button.pack(side=tk.LEFT, padx=5, pady=10)
                bButton = False
            else:
                messagebox.showerror("Error", "Option code not loaded.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def select_option(error_message):
    # Check the error message to determine which option to use
    if "expected ':'" in error_message:
        return "semicolon.py"  # Option for adding a semicolon
    else:
        return None  # No applicable option found

def check_syntax(file_path):
    global bButton
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            compile(code, file_path, 'exec')
            text_area.delete(1.0, tk.END)  # Clear previous content
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "$-/ No syntax errors found.\n")
            text_area.config(state=tk.DISABLED)
            if bButton :
                fix_button = tk.Button(root, text="Beautify", command=lambda: attempt_fix(file_path, "beautify.py", 0))
                fix_button.pack(side=tk.LEFT, padx=5, pady=10)
                bButton = False
    except FileNotFoundError:
            text_area.delete(1.0, tk.END)  # Clear previous content
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"$-/ File '{file_path}' not found.")
            text_area.config(state=tk.DISABLED)
    except SyntaxError as e:
        # Extracting line number and error message from the exception
        line_number, error_message = e.lineno, e.msg
        text_area.delete(1.0, tk.END)
        text_area.config(state=tk.NORMAL)
        # text_area.insert(tk.END, f"$-/ Syntax error at line {line_number}: {error_message}")
        text_area.insert(tk.END, f" $-/ Syntax error detected")
        text_area.config(state=tk.DISABLED)
        guess = "missing colon" if "expected ':'" in error_message else "other"
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"\n $-/ script guess : {guess}")
        text_area.config(state=tk.DISABLED)
        fix_button = tk.Button(root, text="Attempt to Fix", command=lambda: attempt_fix(file_path, error_message, line_number))
        fix_button.pack(side=tk.LEFT, padx=5, pady=10)

def attempt_fix(file_path, error_message, line_number):
    # if not attempt_auto_fix(file_path) or error_message == "Beautify":
        # print(error_message)
        if error_message == "beautify.py":
            fix_code_with_option(file_path, "beautify.py", line_number)
        else:
            option_name = select_option(error_message)
            if option_name:
                fix_code_with_option(file_path, option_name, line_number)
            else:
                messagebox.showinfo("Option Not Found", "No suitable option found for this error.")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        check_syntax(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Python Code Checker")
    
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.pack(pady=10)

    text_area = tk.Text(root, height=20, width=50, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10)

    root.mainloop()
