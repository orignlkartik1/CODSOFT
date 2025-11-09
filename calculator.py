import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculator")
        self.root.geometry("320x470")
        self.root.config(bg="#2e2e2e")

        self.expression = ""

        # --- Display ---
        self.display = tk.Entry(
            root,
            font=("Arial", 24),
            borderwidth=5,
            relief="flat",
            justify="right",
            bg="#3b3b3b",
            fg="white"
        )
        self.display.pack(fill="both", ipadx=8, ipady=15, pady=(20, 10), padx=10)

        # --- Button Frame ---
        btn_frame = tk.Frame(root, bg="#2e2e2e")
        btn_frame.pack()

        # --- Buttons Layout ---
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # --- Create Buttons Dynamically ---
        for row in buttons:
            frame = tk.Frame(btn_frame, bg="#2e2e2e")
            frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 20),
                    bg="#4a4a4a" if char not in ['C', '⌫', '='] else "#f57c00" if char == '=' else "#d32f2f" if char == 'C' else "#616161",
                    fg="white",
                    relief="flat",
                    height=2,
                    width=5,
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both", padx=3, pady=3)

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '⌫':
            self.expression = self.expression[:-1]
        elif char == '=':
            try:
                # Safely evaluate expression
                result = str(eval(self.expression))
                self.expression = result
            except Exception:
                self.expression = "Error"
        else:
            self.expression += str(char)
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

# --- Run Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
