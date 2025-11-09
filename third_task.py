import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import math

# ---------------------------
# Secure Password Generator
# ---------------------------

AMBIGUOUS = 'Il1O0'  # characters many people find confusing

def build_alphabet(use_lower, use_upper, use_digits, use_symbols, avoid_ambiguous):
    alphabet = ''
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        # Using a conservative set of symbols
        alphabet += '!@#$%^&*()-_=+[]{};:,.<>/?'
    if avoid_ambiguous:
        alphabet = ''.join(ch for ch in alphabet if ch not in AMBIGUOUS)
    return alphabet

def estimate_entropy(length, pool_size):
    # entropy in bits = length * log2(pool_size)
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)

def strength_label(entropy_bits):
    # crude mapping of entropy to a textual label
    if entropy_bits < 28:
        return "Very Weak"
    if entropy_bits < 36:
        return "Weak"
    if entropy_bits < 60:
        return "Reasonable"
    if entropy_bits < 80:
        return "Strong"
    return "Very Strong"

def generate_password(length, alphabet):
    if not alphabet:
        return ''
    # securely choose characters
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ---------------------------
# Tkinter GUI
# ---------------------------

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("🔐 Password Generator")
        root.geometry("520x360")
        root.resizable(False, False)

        pad = {'padx': 10, 'pady': 6}

        main = ttk.Frame(root)
        main.pack(fill="both", expand=True, **pad)

        # Title
        title = ttk.Label(main, text="Secure Password Generator", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(6, 12))

        # Length
        ttk.Label(main, text="Length:").grid(row=1, column=0, sticky="w", **pad)
        self.length_var = tk.IntVar(value=16)
        length_spin = ttk.Spinbox(main, from_=4, to=128, textvariable=self.length_var, width=6)
        length_spin.grid(row=1, column=1, sticky="w")

        # Checkbuttons for character sets
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambig_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(main, text="Lowercase (a-z)", variable=self.lower_var).grid(row=2, column=0, sticky="w", **pad)
        ttk.Checkbutton(main, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=2, column=1, sticky="w", **pad)
        ttk.Checkbutton(main, text="Digits (0-9)", variable=self.digits_var).grid(row=3, column=0, sticky="w", **pad)
        ttk.Checkbutton(main, text="Symbols (!@#...)", variable=self.symbols_var).grid(row=3, column=1, sticky="w", **pad)
        ttk.Checkbutton(main, text="Avoid ambiguous (Il1O0)", variable=self.ambig_var).grid(row=4, column=0, sticky="w", **pad)

        # Generate button
        gen_btn = ttk.Button(main, text="Generate Password", command=self.on_generate)
        gen_btn.grid(row=4, column=1, sticky="ew", **pad)

        # Password display
        ttk.Label(main, text="Password:").grid(row=5, column=0, sticky="w", **pad)
        self.pw_var = tk.StringVar()
        pw_entry = ttk.Entry(main, textvariable=self.pw_var, font=("Courier", 14), width=36)
        pw_entry.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10)

        # Buttons: copy & save
        copy_btn = ttk.Button(main, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.grid(row=7, column=0, sticky="ew", **pad)
        save_btn = ttk.Button(main, text="Save to File...", command=self.save_to_file)
        save_btn.grid(row=7, column=1, sticky="ew", **pad)

        # Strength indicator
        self.entropy_var = tk.StringVar(value="Entropy: 0 bits — Strength: N/A")
        ttk.Label(main, textvariable=self.entropy_var, foreground="#007700").grid(row=8, column=0, columnspan=3, sticky="w", padx=10, pady=(8,0))

        # Quick presets
        ttk.Label(main, text="Quick presets:").grid(row=9, column=0, sticky="w", **pad)
        presets = ttk.Frame(main)
        presets.grid(row=9, column=1, columnspan=2)
        ttk.Button(presets, text="8 (Easy)", command=lambda: self.set_preset(8)).pack(side="left", padx=4)
        ttk.Button(presets, text="12 (Normal)", command=lambda: self.set_preset(12)).pack(side="left", padx=4)
        ttk.Button(presets, text="16 (Secure)", command=lambda: self.set_preset(16)).pack(side="left", padx=4)
        ttk.Button(presets, text="24 (Very Secure)", command=lambda: self.set_preset(24)).pack(side="left", padx=4)

        # Keyboard binding: Enter -> generate
        root.bind('<Return>', lambda e: self.on_generate())

        # Initialize with a password
        self.on_generate()

    def set_preset(self, length):
        self.length_var.set(length)
        self.on_generate()

    def on_generate(self):
        length = int(self.length_var.get())
        use_lower = self.lower_var.get()
        use_upper = self.upper_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()
        avoid_ambiguous = self.ambig_var.get()

        alphabet = build_alphabet(use_lower, use_upper, use_digits, use_symbols, avoid_ambiguous)
        if not alphabet:
            messagebox.showwarning("No characters selected", "Please select at least one character set (lower, upper, digits or symbols).")
            return

        password = generate_password(length, alphabet)
        self.pw_var.set(password)

        entropy = estimate_entropy(length, len(alphabet))
        label = strength_label(entropy)
        # format entropy to one decimal place
        self.entropy_var.set(f"Entropy: {entropy:.1f} bits — Strength: {label}")

    def copy_to_clipboard(self):
        pwd = self.pw_var.get()
        if not pwd:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def save_to_file(self):
        pwd = self.pw_var.get()
        if not pwd:
            messagebox.showinfo("Nothing to save", "Generate a password first.")
            return
        fpath = filedialog.asksaveasfilename(
            title="Save password",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not fpath:
            return
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(pwd + "\n")
            messagebox.showinfo("Saved", f"Password saved to:\n{fpath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

# ---------------------------
# Run
# ---------------------------

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    # optional: use a platform-appropriate theme
    try:
        style.theme_use('clam')
    except Exception:
        pass
    app = PasswordGeneratorApp(root)
    root.mainloop()
