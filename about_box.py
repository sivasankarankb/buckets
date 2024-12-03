import tkinter as tk
from tkinter import ttk

class AboutBox:
    def __init__(self, master):
        win = tk.Toplevel(master)
        win.title('About')
        win.transient(master)

        frame = ttk.Frame(win)
        frame.grid(padx=16, pady=16)

        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)
        
        l1 = ttk.Label(frame, text='Buckets')
        l1.grid(pady=(0,8))
        
        l2 = ttk.Label(frame, text='Version v0.1.1')
        l2.grid(pady=(0,8))

        l3 = ttk.Label(frame, text='https://github.com/sivasankarankb/buckets')
        l3.grid(pady=(0,8))

        lcopy = ttk.Label(frame, text='Copyright (C) 2020-2023 Sivasankaran K B')
        lcopy.grid(pady=(0,20))

        license_txt ='''\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation.'''

        llicense = ttk.Label(frame, text=license_txt)
        llicense.grid(pady=(0,20))

        l4 = ttk.Label(frame, text='-- Contributors --')
        l4.grid(pady=(0,20))

        ll = ttk.Label(frame, text='Icons: Sudharsanan K B')
        ll.grid(pady=(0,8))

        frame.columnconfigure(0, weight=1)
