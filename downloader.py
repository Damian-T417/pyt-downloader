# Importing packages
import tkinter as tk

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
        self.file_title.set("")

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

        self.file_title.set(yt.title)
        self.table.delete(*self.table.get_children())
        self.download['state'] = "active"

        if option == 0:
            stream = yt.streams.filter(type="audio", mime_type="audio/mp4").first()
            self.table.insert("",END,text=stream.itag, values=("audio/mp3", stream.resolution, stream.codecs))
        elif option == 1:
            streams = yt.streams.filter(type="video", mime_type="video/mp4", progressive=True).order_by("resolution").desc()
            for file in streams:
                self.table.insert("",END,text=file.itag, values=(file.mime_type, file.resolution, file.codecs))


    def save_file(self, link, selected, option):
        itag = self.table.item(selected, 'text')
        save = Savefile(self, link, itag, option)
        save.grab_set()

    def clean_query(self):
        self.link.delete(0, 'end')
        self.table.delete(*self.table.get_children())

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
        self.audio.grid(row=1, column=0, sticky=E)

        self.video = tk.Radiobutton(self, text="Video", variable=option_download, value=1)
        self.video.grid(row=1, column=1, sticky=N)

        # Title
        self.ftitle = tk.Label(self, font=8, pady=10, textvariable=self.file_title)
        self.ftitle.grid(row=2, column=0, columnspan=4, padx=10, sticky=S)

        #Download button
        self.download = tk.Button(self, text="Download", state="disabled", command=lambda:self.save_file(self.link.get(), self.table.focus(), option_download.get()))
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
