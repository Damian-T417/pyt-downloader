
# Importing packages
import os
import tkinter as tk
import moviepy.editor as mp

from tkinter import ttk
from tkinter import S, N, E, W
from tkinter import CENTER
from tkinter import END
from tkinter import messagebox
from pytube import YouTube
from save import Savefile


class Pytdownloader(tk.Tk):

    # Window Constructor
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Configuring the window and grid
        self.title("Youtube Downloader")
        self.geometry("500x415")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.file_title = tk.StringVar()
        self.file_title.set("File name")

        self.create_widgets()
        self.create_table()

    def get_files(self, link, option):

        try:
            yt = YouTube(link)
        except Exception:
            return messagebox.showerror(
                "Syntax error",
                "The link is not supported or misspelled"
            )

        if option == 0:
            streams = yt.streams.filter(only_audio=True)
        elif option == 1:
            streams = yt.streams.filter(only_video=True)

        self.file_title.set(yt.title)
        self.table.delete(*self.table.get_children())
        self.link.delete(0, 'end')

        for file in streams:
            self.table.insert("",END,text=file.itag, values=(file.mime_type, file.resolution, file.codecs))

    def download_file(self, selected):
        itag = self.table.item(selected, 'text')
        print("Downloading: ", itag)

    # Creation the graphic interface
    def create_widgets(self):

        option_download = tk.IntVar()

        # Search bar
        self.link = tk.Entry(self)
        self.link.grid(row=0, column=0, pady=10, padx=10, columnspan=3, sticky=W+E)

        self.search = tk.Button(self, width=10, text="Search", command=lambda: self.get_files(self.link.get(), option_download.get()))
        self.search.grid(row=0, column=3, pady=10, padx=10, sticky=W)

        # Options
        self.audio = tk.Radiobutton(self, text="Audio", variable=option_download, value=0)
        self.audio.grid(row=1, column=0)

        self.video = tk.Radiobutton(self, text="Video", variable=option_download, value=1)
        self.video.grid(row=1, column=1)

        # Title
        self.title = tk.Label(self, font=8, pady=10, textvariable=self.file_title)
        self.title.grid(row=2, column=0, columnspan=3)

        #Download button
        self.download = tk.Button(self, text="Download", command=lambda:self.download_file(self.table.focus()))
        self.download.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)

    def create_table(self):

        table_scroll = ttk.Scrollbar(self)
        table_scroll.grid(row=3, column=3, sticky=N+S+W)

        self.table = ttk.Treeview(self, yscrollcommand=table_scroll.set)

        self.table['columns'] = ("Type", "Resolution", "Codec")

        table_scroll.config(command=self.table.yview)

        self.table.column("#0",width=80, anchor=CENTER, stretch=False)
        self.table.column("Type",width=80, anchor=CENTER)
        self.table.column("Resolution",width=80, anchor=CENTER)
        self.table.column("Codec", width=80, anchor=CENTER)

        self.table.heading("#0", text="ID", anchor=CENTER)
        self.table.heading("Type", text="Type", anchor=CENTER)
        self.table.heading("Resolution", text="Resolution", anchor=CENTER)
        self.table.heading("Codec", text="Codec", anchor=CENTER)

        self.table.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=E+W+N+S)
