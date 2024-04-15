import tkinter as tk
from tkinter import ttk, messagebox
from Q4_Objects import RightTriangle


def calculate():  # handles the error and performs the calculation
    try:
        A = int(Side_A.get())
        B = int(Side_B.get())
        if A == 0 or B == 0:
            messagebox.showerror(title='Error', message='Value must be greater than 0')
        else:
            triangle = RightTriangle(A, B)
            Side_C.set(f'{triangle.c:.3f}')  # uses the triangle class property to output the calculation
    except ValueError:
        messagebox.showerror("Error", "Please enter an integer")


# initializes the gui
root = tk.Tk()
root.geometry('450x200')
root.title('Right Triangle Calculator')

# sets the ui frame
window = ttk.Frame(root, padding='5 5 5 5')
window.pack(fill='both', expand=True)

# A label
A_label = ttk.Label(window, text='Side A: ')
A_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

# Side A input field
Side_A = tk.StringVar()
A_entry = ttk.Entry(window, width=50, textvariable=Side_A)
A_entry.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10, columnspan=5)

# B Label
B_label = ttk.Label(window, text='Side B: ')
B_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

# Side B input field
Side_B = tk.StringVar()
B_entry = ttk.Entry(window, width=50, textvariable=Side_B)
B_entry.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10, columnspan=5)

# C label
C_label = ttk.Label(window, text='Side C: ')
C_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

# Side C output field
Side_C = tk.StringVar()
C_output = ttk.Entry(window, width=50, textvariable=Side_C, state='readonly')
C_output.grid(row=2, column=1, sticky=tk.E, padx=10, pady=10, columnspan=5)

# calculate button
calculate = ttk.Button(window, width=10, text='Calculate', command=calculate)
calculate.grid(row=3, column=4, sticky=tk.W, padx=0, pady=0)

# exit button
exit = ttk.Button(window, width=10, text='Exit', command=window.quit)
exit.grid(row=3, column=5, sticky=tk.E, padx=0, pady=0)

# starts the GUI loop
root.mainloop()
