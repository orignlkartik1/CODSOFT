import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List")
        self.root.geometry("400x500")
        self.root.config(bg="#f7f7f7")

        # --- Title ---
        tk.Label(
            root,
            text="My To-Do List",
            font=("Arial", 18, "bold"),
            bg="#f7f7f7",
            fg="#333"
        ).pack(pady=10)

        # --- Frame for Entry and Add Button ---
        frame = tk.Frame(root, bg="#f7f7f7")
        frame.pack(pady=10)

        self.task_entry = tk.Entry(
            frame,
            font=("Arial", 14),
            width=22,
            bd=2,
            relief="groove"
        )
        self.task_entry.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(
            frame,
            text="Add Task",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            command=self.add_task
        )
        add_btn.pack(side=tk.LEFT)

        # --- Listbox for Tasks ---
        self.listbox = tk.Listbox(
            root,
            font=("Arial", 13),
            width=35,
            height=15,
            selectbackground="#a6a6a6",
            bg="white",
            activestyle="none"
        )
        self.listbox.pack(pady=10)

        # --- Scrollbar ---
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # --- Buttons ---
        button_frame = tk.Frame(root, bg="#f7f7f7")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Delete Task",
            font=("Arial", 12),
            bg="#e53935",
            fg="white",
            padx=10,
            command=self.delete_task
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Clear All",
            font=("Arial", 12),
            bg="#757575",
            fg="white",
            padx=10,
            command=self.clear_all
        ).grid(row=0, column=1, padx=5)

    # --- Add Task ---
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task before adding.")

    # --- Delete Selected Task ---
    def delete_task(self):
        try:
            selected_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    # --- Clear All Tasks ---
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
            self.listbox.delete(0, tk.END)

# --- Run Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
