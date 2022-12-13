# links de prueba: https://www.youtube.com/watch?v=IwzFzUXSE5s
# https://www.youtube.com/watch?v=lwYBVbFVqxg&t=562s
# Importing packages
import os
import tkinter as tk
import moviepy.editor as mp

from pytube import YouTube
from tkinter import S, N, E, W
from tkinter import messagebox
from tkinter import filedialog


class Savefile(tk.Toplevel):

    # Window Constructor
    def __init__(self, parent, link, itag, option, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.link = link
        self.itag = itag
        self.option = option

        # Get the file
        try:
            self.yt = YouTube(link)
            self.file = self.yt.streams.get_by_itag(itag)
        except Exception:
            return messagebox.showerror(
                "Error",
                "The program have a unexpected error"
                )

        # Set Variables
        self.file_title = tk.StringVar()
        self.location = tk.StringVar()
        self.file_title.set(self.yt.title)

        # Configuring the window and grid
        self.geometry("400x115")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.title("Save File")
        self.resizable(False, False)
        self.create_widgets()

    def select_dir(self):
        dir_path = filedialog.askdirectory(title="Select a folder")
        self.location.set(dir_path)

    def download_file(self):
        # Debugging
        print(self.link)
        print("Downloading: ", self.itag, self.file_title.get(), " in ", self.location.get(), " with option ", self.option)

        # Get the ext
        file_type = self.file.mime_type
        mtype = file_type.split('/')

        # Audio
        if (self.option == 0):
            file_audio = self.yt.streams.filter(progressive=True).get_highest_resolution()
            out_file = file_audio.download(filename=self.file_title.get()+"."+mtype[1],output_path=self.location.get())

            if(mtype[1] == "mp4"):
                mtype[1] = "mp3"

            base, ext = os.path.splitext(out_file)

            new_file = mp.VideoFileClip(out_file)
            new_file.audio.write_audiofile(base +"."+ mtype[1])
            new_file.close()
            os.remove(out_file)

        # Video
        if (self.option == 1):
            out_file = self.file.download(filename=self.file_title.get()+"."+mtype[1],output_path=self.location.get())

            # Only if i add the advanced options
            # base, ext = os.path.splitext(out_file)
            # new_file = base + mtype[1]
            # os.rename(out_file, new_file)

        messagebox.showinfo(
            "Success",
            self.file_title.get() + " has been successfully downloaded"
        )
        return self.destroy()


    # Creation the graphic interface
    def create_widgets(self):

        # File Title
        self.lab_filetitle = tk.Label(self, anchor=E, text="Title: ")
        self.lab_filetitle.grid(row=0, column=0, pady=10, padx=10, sticky=E+N)

        self.f_title = tk.Entry(self, textvariable=self.file_title)
        self.f_title.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky=W+E)

        # File Location
        self.lab_filelocation = tk.Label(self, anchor=E, text="Location: ")
        self.lab_filelocation.grid(row=1, column=0, pady=5, padx=10, sticky=N+W+E)

        self.f_location = tk.Entry(self, textvariable=self.location, state="disabled")
        self.f_location.grid(row=1, column=1, columnspan=2, padx=10, ipadx=10, pady=5, sticky=N+W+E)

        self.search_loc = tk.Button(self, text="...", command=lambda: self.select_dir())
        self.search_loc.grid(row=1, column=2, padx=5, sticky=E)

        # Buttons
        self.cancel_button = tk.Button(self, text="Cancel", relief="raised", width=10, command=lambda: self.destroy())
        self.cancel_button.grid(row=2, column=1, pady=5, sticky=E)

        self.save_button = tk.Button(self, text="Save", width=10, command=lambda: self.download_file())
        self.save_button.grid(row=2, column=2, pady=5, padx=10, sticky=W)
