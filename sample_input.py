# Sample Python Tkinter Code
# Copy this into the converter

import tkinter as tk
from tkinter import ttk

# Counter variable
counter = 0

def increment():
    global counter
    counter = counter + 1
    label.config(text="Count: " + str(counter))
    if counter < 10:
        root.after(500, increment)

def on_reset():
    global counter
    counter = 0
    label.config(text="Count: 0")

# Create main window
root = tk.Tk()
root.title("Counter App")
root.geometry("300x200")

# Create label
label = tk.Label(root, text="Count: 0", font=("Arial", 24))
label.pack(pady=20)

# Create increment button
inc_button = tk.Button(root, text="Start Counting", command=increment, bg="#4CAF50", fg="white")
inc_button.pack(side=tk.LEFT, padx=5)

# Create reset button
reset_button = tk.Button(root, text="Reset", command=on_reset, bg="#f44336", fg="white")
reset_button.pack(side=tk.LEFT, padx=5)

# Start the application
root.mainloop()
