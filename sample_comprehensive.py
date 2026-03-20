# Comprehensive Tkinter Sample
# This includes features that the converter supports

import tkinter as tk
from tkinter import ttk

# Global variables
counter = 0
name = "Guest"

# --- Functions ---

def increment():
    global counter
    counter = counter + 1
    label.config(text="Count: " + str(counter))
    if counter < 10:
        root.after(500, increment)

def decrement():
    global counter
    counter = counter - 1
    label.config(text="Count: " + str(counter))

def reset():
    global counter
    counter = 0
    label.config(text="Count: 0")

def show_name():
    global name
    name = entry.get()
    result_label.config(text="Hello, " + name + "!")

def toggle_feature():
    if var.get() == "on":
        status_label.config(text="Feature: ON")
    else:
        status_label.config(text="Feature: OFF")

def start_timer():
    timer_label.config(text="Timer started!")
    root.after(2000, timer_done)

def timer_done():
    timer_label.config(text="Timer done!")

# --- Main Window ---
root = tk.Tk()
root.title("Comprehensive App")
root.geometry("400x500")

# --- Label ---
label = tk.Label(root, text="Count: 0", font=("Arial", 20), bg="#eee")
label.pack(pady=10)

# --- Buttons with different colors ---
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

inc_btn = tk.Button(btn_frame, text="+1", command=increment, bg="#4CAF50", fg="white")
inc_btn.pack(side=tk.LEFT, padx=5)

dec_btn = tk.Button(btn_frame, text="-1", command=decrement, bg="#f44336", fg="white")
dec_btn.pack(side=tk.LEFT, padx=5)

reset_btn = tk.Button(btn_frame, text="Reset", command=reset, bg="#FF9800", fg="white")
reset_btn.pack(side=tk.LEFT, padx=5)

# --- Entry with label ---
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry_label = tk.Label(entry_frame, text="Enter name:")
entry_label.pack(side=tk.LEFT)

entry = tk.Entry(entry_frame, width=15)
entry.pack(side=tk.LEFT, padx=5)

submit_btn = tk.Button(entry_frame, text="Submit", command=show_name)
submit_btn.pack(side=tk.LEFT)

# --- Result label ---
result_label = tk.Label(root, text="Hello, Guest!", font=("Arial", 14))
result_label.pack(pady=10)

# --- Checkbutton ---
var = tk.StringVar(value="off")
check = tk.Checkbutton(root, text="Enable Feature", variable=var, onvalue="on", offvalue="off", command=toggle_feature)
check.pack(pady=5)

status_label = tk.Label(root, text="Feature: OFF")
status_label.pack()

# --- Another button with timer ---
timer_btn = tk.Button(root, text="Start Timer (2s)", command=start_timer, bg="#2196F3", fg="white")
timer_btn.pack(pady=10)

timer_label = tk.Label(root, text="")
timer_label.pack()

# --- Frame example ---
info_frame = tk.Frame(root, bg="#ddd", bd=2, relief=tk.RIDGE)
info_frame.pack(pady=10, padx=20, fill=tk.BOTH)

info_label = tk.Label(info_frame, text="This is a Frame with info", bg="#ddd")
info_label.pack(pady=10)

# --- Main loop ---
root.mainloop()
