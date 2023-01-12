# Importing packages
import tkinter as tk
import urllib as ur

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
        self.title("Pyt-downloader")
        self.geometry("500x415")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=2)

        # Set global variables
        self.file_title = tk.StringVar()
        self.file_title.set("")

        self.file_link = tk.StringVar()
        self.file_link.set("")

        self.option_selected = tk.IntVar()
        self.option_selected.set(2)

        self.option_download = tk.IntVar()
        self.option_download.set(2)

        # Set a event when return or enter ir clicked
        self.bind("<Return>", self.on_return_click)

        self.create_widgets()
        self.create_table()

    def get_files(self):
        # Check the connection
        conn = self.internet_connection()
        if conn == "ok":
            return self.on_function_finish()

        # on_function_finish return "ok" in these validations, curious i thing
        yt = self.form_validation()
        if yt == "ok":
            return self.on_function_finish()

        # Get the values
        try:
            self.prepare_query(yt.title)
            if self.option_download.get() == 0:
                stream = yt.streams.filter(type="audio", mime_type="audio/mp4").first()
                self.table.insert("",END,text=stream.itag, values=("audio/mp3", stream.resolution, stream.codecs))
            elif self.option_download.get() == 1:
                streams = yt.streams.filter(type="video", progressive=True).order_by("resolution").desc()
                for file in streams:
                    self.table.insert("",END,text=file.itag, values=(file.mime_type, file.resolution, file.codecs))
        except Exception:
            return self.on_function_finish(
                "Error",
                "The program have a unexpected error",
                True
                )
        return self.on_function_finish()

    def get_advanced_files(self):
        # Check the connection
        conn = self.internet_connection()
        if conn == "ok":
            return self.on_function_finish()

        # Notes: on_function_finish return "ok" in form_validation, it curious but functional i guess...
        yt = self.form_validation()
        if yt == "ok":
            return self.on_function_finish()

        if self.option_download.get() == 0:
            audio = messagebox.askokcancel(
                "Search error",
                "Audio haven't more options that mp3, do you want to do a normal search?"
            )
            if audio is True:
                return self.get_files()

        if self.option_download.get() == 1:
            confirm = messagebox.askokcancel(
                "Alert",
                "Do you what to search more videos in diferent codecs and resolutions?" +
                " (Some videos can't work on diferent devices or not have audio)"
            )
            if confirm is True:
                try:
                    self.prepare_query(yt.title)
                    streams = yt.streams.filter(type="video", mime_type="video/mp4").order_by("resolution").desc()
                    for file in streams:
                        self.table.insert("",END,text=file.itag, values=(file.mime_type, file.resolution, file.codecs))
                except Exception:
                    return self.on_function_finish(
                        "Error",
                        "The program have a unexpected error",
                        True
                        )
        return self.on_function_finish()

    def save_file(self):
        if self.table.focus() == "":
            return self.on_function_finish(
                "Table info",
                "Select an option from the table"
            )
        itag = self.table.item(self.table.focus(), 'text')
        Savefile(self, self.file_link.get(), itag, self.option_selected.get())

    # Creation the graphic interface
    def create_widgets(self):
        # Search bar
        self.link = tk.Entry(self)
        self.link.grid(row=0, column=0, pady=10, padx=10, columnspan=3, sticky=W+E)
        self.link.insert(0, "Enter your link")
        self.link['state'] = "disabled"
        self.link.bind("<Button-1>", self.on_link_click)
        self.link.bind("<FocusOut>", self.on_link_focus_out)

        self.search = tk.Button(self, width=14, text="Search", command= lambda:self.get_files())
        self.search.grid(row=0, column=3, pady=10, padx=10, sticky=W)
        self.search.bind("<Button-1>", self.on_button_click)

        self.advanced = tk.Button(self, width=14, text="Advanced search", command=lambda:self.get_advanced_files())
        self.advanced.grid(row=1, column=3, padx=10, sticky=W+S+N)
        self.advanced.bind("<Button-1>", self.on_button_click)

        # Options
        self.audio = tk.Radiobutton(self, text="Audio", variable=self.option_download, value=0)
        self.audio.grid(row=1, column=0, sticky=E+N)

        self.video = tk.Radiobutton(self, text="Video", variable=self.option_download, value=1)
        self.video.grid(row=1, column=1, sticky=N)

        # Title
        self.ftitle = tk.Label(self, font=8, pady=10, textvariable=self.file_title)
        self.ftitle.grid(row=2, column=0, columnspan=4, padx=10, sticky=S)

        #Download button
        self.download = tk.Button(self, text="Download", state="disabled", command=lambda:self.save_file())
        self.download.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)

    def create_table(self):
        # Table
        table_scroll = ttk.Scrollbar(self)
        table_scroll.grid(row=3, column=3, sticky=N+S+W)

        self.table = ttk.Treeview(self, yscrollcommand=table_scroll.set)

        self.table['columns'] = ("Type", "Resolution", "Codec")

        table_scroll.config(command=self.table.yview)

        self.table.column("#0",width=80, minwidth=80, anchor=CENTER)
        self.table.column("Type",width=80, minwidth=80, anchor=CENTER)
        self.table.column("Resolution",width=80, minwidth=80, anchor=CENTER)
        self.table.column("Codec", width=80, minwidth=80, anchor=CENTER)

        self.table.heading("#0", text="ID", anchor=CENTER)
        self.table.heading("Type", text="Type", anchor=CENTER)
        self.table.heading("Resolution", text="Resolution", anchor=CENTER)
        self.table.heading("Codec", text="Codec", anchor=CENTER)

        self.table.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=E+W+N+S)

    # query helpers
    def clean_query(self):
        self.link['state'] = "normal"
        self.file_title.set("")
        self.file_link.set("")
        self.option_selected.set(2)
        self.option_download.set(2)
        self.link.delete(0, END)
        self.link.insert(0, "Enter your link")
        self.table.delete(*self.table.get_children())
        self.link['state'] = "disabled"
        self.download['state'] = "disabled"
    
    def prepare_query(self, title):
        self.file_title.set(title)
        self.file_link.set(self.link.get())
        self.option_selected.set(self.option_download.get())
        self.table.delete(*self.table.get_children())
        self.download['state'] = "active"

    # Validations
    def on_function_finish(self, title = "", message = "", error = False):
        self.config(cursor='')
        if error is True:
            self.clean_query()
            return messagebox.showerror(
                title,
                message
            )
        elif title != "" and message != "":
            return messagebox.showinfo(
                title,
                message
            )

    def internet_connection(self):
        try:
            ur.request.urlopen("https://www.youtube.com/", timeout=4)
        except ur.error.URLError as err:
            return self.on_function_finish(
                "Connection lost",
                "You lost the internet connection, try again later",
                True
            )

    def form_validation(self):
        if self.link.get() == "" or self.link.get() == "Enter your link":
            return self.on_function_finish(
                "Syntax info",
                "Enter the link into the search bar",
            )
        try:
            yt = YouTube(self.link.get())
        except Exception:
            return self.on_function_finish(
                "Syntax error",
                "The link is not supported or is misspelled",
                True
            )
        if self.option_download.get() == 2:
            return self.on_function_finish(
                "Option info",
                "Select one of the options below the search bar",
            )
        return yt

# Events
    def on_link_click(self, event):
        self.link['state'] = "normal"
        if self.link.get() == "Enter your link":
            self.link.delete(0, END)

    def on_link_focus_out(self, event):
        if self.link.get() == "":
            self.link.insert(0, "Enter your link")
        self.link['state'] = "disabled"

    def on_return_click(self, event):
        self.config(cursor='wait')
        self.get_files(self.link.get(), self.option_download.get())

    def on_button_click(self, event):
        self.config(cursor='wait')
