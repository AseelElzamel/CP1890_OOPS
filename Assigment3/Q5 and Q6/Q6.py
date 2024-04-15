import Question5 as q5
import tkinter as tk
from tkinter import ttk,messagebox
from dataclasses import dataclass
padding = '5 5 5 5'
EditSalesData = tk.Tk()
EditSalesData.title('Edit Sales Data')
EditSalesData.geometry('400x300')

window = ttk.Frame(EditSalesData, padding=padding)
window.pack(fill='both',expand=True)

instruction = ttk.Label(window, text='Enter date and region to get sales amount.')
instruction.grid(row=0)

date_label = ttk.Label(window, width = 5, text='Date: ',padding=padding)
date_label.grid(row =1, column=0, sticky=tk.W)


date = tk.StringVar(value='')
dateEntry = tk.Entry(window,width=25, textvariable=date)
dateEntry.grid(row =1, column=1, sticky=tk.W)

region_label = ttk.Label(window, width = 5, text='Region: ',padding=padding)
region_label.grid(row =2, column=0, sticky=tk.W)

region = tk.StringVar(value='')
regionEntry = tk.Entry(window,width=25, textvariable=region)
regionEntry.grid(row =2, column=1, sticky=tk.W)

amount_label = ttk.Label(window, width = 5, text='Amount: ',padding=padding)
amount_label.grid(row =3, column=0, sticky=tk.W)

amount = tk.IntVar(value=0)
amountEntry = tk.Entry(window,width=25, textvariable=amount)
amountEntry.grid(row =3, column=1, sticky=tk.W)

id_label = ttk.Label(window, width = 5, text='ID: ',padding=padding)
id_label.grid(row =4, column=0, sticky=tk.W)

id = tk.IntVar(value=0)
idEntry = tk.Entry(window,width=25, textvariable=id)
idEntry.grid(row =4, column=1, sticky=tk.W)

EditSalesData.mainloop()