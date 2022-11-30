
# Importing packages
import tkinter as tk

from tkinter import ttk
from tkinter import S, N, E, W
from tkinter import messagebox


class Savefile(tk.Tk):

    # Window Constructor
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Configuring the window and grid
        self.geometry("400x115")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.title("Save File")
        self.resizable(False, False)
        self.create_widgets()

    def cancel_save(self):
        print("ok")

    def save_file(self):
        print("Saved")

    # Creation the graphic interface
    def create_widgets(self):

        title = tk.IntVar()
        location = tk.IntVar()
        # Debugging
        title.set(" HOlamundo")
        location.set("Holamundo")


        # File Title
        self.lab_filetitle = tk.Label(self, anchor=E, text="Title: ")
        self.lab_filetitle.grid(row=0, column=0, pady=10, padx=10, sticky=W+E)

        self.file_title = tk.Entry(self, textvariable=title)
        self.file_title.grid(row=0, column=1, pady=10, padx=10, columnspan=2, sticky=W+E)

        # File Location
        self.lab_filelocation = tk.Label(self, anchor=E, text="Location: ")
        self.lab_filelocation.grid(row=1, column=0, pady=5, padx=10, sticky=N+W+E)

        self.file_location = tk.Entry(self, textvariable=location)
        self.file_location.grid(row=1, column=1, pady=5, padx=10, columnspan=2, sticky=N+W+E)

        # Buttons
        self.cancel_button = tk.Button(self, text="Cancel", width=10, command=lambda: self.cancel_save())
        self.cancel_button.grid(row=2, column=1, pady=5, sticky=E)

        self.save_button = tk.Button(self, text="Save", width=10, command=lambda: self.save_file())
        self.save_button.grid(row=2, column=2, pady=5, padx=10, sticky=W)
