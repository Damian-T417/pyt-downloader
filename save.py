# links de prueba: https://www.youtube.com/watch?v=IwzFzUXSE5s
# https://www.youtube.com/watch?v=lwYBVbFVqxg&t=562s
# Importing packages
import os
import time
import json
import shutil
import tkinter as tk
import moviepy.editor as mp

from pytube import YouTube
from tkinter import N, E, W
from tkinter import messagebox
from tkinter import filedialog

class Savefile(tk.Toplevel):

    # Window Constructor
    def __init__(self, parent, link, itag, option, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.link = link
        self.itag = itag
        self.option = option
        self.parent = parent

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

        # Get json data
        with open('data.json', 'r') as f:
            self.data = json.load(f)
            self.location.set(self.data['file_location'])

        # Configuring the window and grid
        self.title("Save File")
        self.geometry("400x115")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.create_widgets()

    def select_dir(self):
        dir_path = filedialog.askdirectory(title="Select a folder")
        with open('data.json', 'r') as f:
            self.data = json.load(f)

        self.data['file_location'] = dir_path

        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)
        self.location.set(dir_path)

    def download_file(self):
        # Debugging
        print(self.link)
        print("Downloading: ", self.itag, self.file_title.get(), " in ", self.location.get(), " with option ", self.option)

        # Get a audio for other options
        audio_video = self.yt.streams.filter(progressive=True).get_highest_resolution()

        # Audio option
        if self.option == 0:
            out_file = audio_video.download(filename=self.file_title.get()+".mp4",output_path=self.location.get())
            base, ext = os.path.splitext(out_file)

            new_file = mp.VideoFileClip(out_file)
            new_file.audio.write_audiofile(base + ".mp3")

            new_file.close()
            os.remove(out_file)

        # Video option
        if self.option == 1:
            out_file = self.file.download(filename=self.file_title.get()+".mp4",output_path=self.location.get())

        # Advanced search
        if self.file.is_progressive == False and self.file.mime_type == "video/mp4":
            confirm = messagebox.askokcancel(
                "Alert",
                "This video doesn't contain audio, the program can add the audio in the video "+
                "but the process take a long moment to complete depending of the quality of the " +
                "video and the duration. In adition the program will take a some resouces of your computer " +
                "for the process. Continue?"
            )
            if confirm == True:
                base, ext = os.path.splitext(out_file)

                # Generate audio
                audio_file = audio_video.download(filename="audio_file.mp4")
                mp.VideoFileClip(audio_file).audio.write_audiofile("audio_file.mp3")
                os.remove(audio_file)

                #Fix video
                new_video = mp.VideoFileClip(out_file)
                audio = mp.AudioFileClip('audio_file.mp3')

                new_audio = mp.CompositeAudioClip([audio])
                new_video.audio = new_audio
                new_video.write_videofile(self.file_title.get() + '.mp4')
                time.sleep(1)

                new_video.close()
                audio.close()
                os.remove(out_file)
                os.remove('audio_file.mp3')
                shutil.move(self.file_title.get() + '.mp4', self.location.get())
            else:
                os.remove(out_file)
                return self.destroy()

        messagebox.showinfo(
            "Success",
            self.file_title.get() + " has been successfully downloaded"
        )

        self.parent.clean_query()
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
