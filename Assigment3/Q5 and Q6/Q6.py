import Question5 as q5
import tkinter as tk
from tkinter import ttk,messagebox

padding = '5 5 5 5'
EditSalesData = tk.Tk()
EditSalesData.title('Edit Sales Data')
EditSalesData.geometry('400x300')

frame = ttk.Frame(EditSalesData, padding=padding)
frame.pack(fill='both',expand=True)

instruction = ttk.Label(frame, text='Enter date and region to get sales amount.')
instruction.grid(row=0, column=0, columnspan=4, sticky=tk.N)

date_label = ttk.Label(frame, width = 10, text='Date: ',padding=padding,)
date_label.grid(row =1, column=0, sticky=tk.W)


date = tk.StringVar(value='')
dateEntry = tk.Entry(frame,width=25, textvariable=date)
dateEntry.grid(row =1, column=1, columnspan=2, sticky=tk.W)

region_label = ttk.Label(frame, width = 10, text='Region: ',padding=padding)
region_label.grid(row =2, column=0, sticky=tk.W)

region = tk.StringVar(value='')
regionEntry = tk.Entry(frame,width=25, textvariable=region)
regionEntry.grid(row =2, column=1, columnspan=2, sticky=tk.W)

amount_label = ttk.Label(frame, width = 10, text='Amount: ',padding=padding)
amount_label.grid(row =3, column=0, sticky=tk.W)

amount = tk.IntVar(value=0)
amountEntry = tk.Entry(frame,width=25, textvariable=amount)
amountEntry.grid(row =3, column=1)

id_label = ttk.Label(frame, width=10, text='ID: ',padding=padding)
id_label.grid(row=4, column=0, sticky=tk.E)

id = tk.IntVar(value=0)
idEntry = tk.Entry(frame,width=25, textvariable=id, state="readonly")
idEntry.grid(row =4, column=1)

EditSalesData.mainloop()