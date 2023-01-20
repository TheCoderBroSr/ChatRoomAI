import tkinter as tk
from tkinter import ttk
from connection import start_client, username_exists

def on_submit():
    username = name_entry.get()
    
    if username_exists(username):
        ttk.Label(mainframe, text="Username already exists. Try another one").grid(column=1, row=4, sticky=tk.W)
    else:
        root.destroy()
        start_client(username)
    

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chat Client - Enter User Name")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    name = tk.StringVar()

    name_entry = ttk.Entry(mainframe, width=7, textvariable=name)
    name_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

    ttk.Label(mainframe, text="User Name").grid(column=1, row=1, sticky=tk.W)
    ttk.Button(mainframe, text="Submit", command=on_submit).grid(column=3, row=3, sticky=tk.W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    name_entry.focus()
    root.bind('<Return>', lambda event: on_submit())
    root.mainloop()
