# links de prueba: https://www.youtube.com/watch?v=IwzFzUXSE5s
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

        # Configuring the window and grid
        self.title("Save File")
        self.geometry("400x115")
        # Only in production mode add _internal/ in the path
        self.iconbitmap("favicon.ico")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        x = parent.winfo_x()
        y = parent.winfo_y()
        self.geometry("+%d+%d" % (x+50, y+150))

        # Get the file
        try:
            self.yt = YouTube(link)
        except Exception:
            return self.on_function_finish(
                "Error",
                "The program have a unexpected error",
                True
            )

        # Set Variables
        self.file_title = tk.StringVar()
        self.file_title.set(self.yt.title)

        self.file = tk.StringVar()
        if option == 0:
            self.file.set(self.yt.title + ".mp3")
        if option == 1:
            self.file.set(self.yt.title + ".mp4")

        self.location = tk.StringVar()
        # Get json data
        with open('data.json', 'r') as f:
            self.data = json.load(f)
            self.location.set(self.data['file_location'])

        # Set a event when return or enter ir clicked
        self.bind("<Return>", self.on_return_click)

        self.create_widgets()
        self.wm_transient(parent)
        self.grab_set()
        self.focus_set()

    def select_dir(self):
        # Ask for a new path
        dir_path = filedialog.askdirectory(title="Select a folder")
        if dir_path == "":
            return

        # Set the new location in the json file
        with open('data.json', 'w') as f:
            self.data['file_location'] = dir_path
            json.dump(self.data, f, indent=4, sort_keys=True)

        # Set the location in the input
        return self.location.set(dir_path)

    def download_file(self):
        if self.file_title != self.yt.title:
            self.on_change_name()

        # Check the file exist
        if os.path.exists(self.location.get()+"/"+self.file.get()):
            overwrite = messagebox.askokcancel(
                'Alert',
                'File already exists in this directory, overwrite?'
            )
            if not overwrite:
                self.on_cancel()
                return
            if overwrite:
                os.remove(self.location.get()+"/"+self.file.get())

        # Get a stream video for audio and advanced search options
        file = self.yt.streams.get_by_itag(self.itag)
        audio_video = self.yt.streams.filter(
            progressive=True
            ).get_highest_resolution()

        # Audio option
        if self.option == 0:
            out_file = audio_video.download(
                filename="audio_in_process.mp4",
                output_path=self.location.get()
                )

            new_file = mp.VideoFileClip(out_file)
            new_file.audio.write_audiofile(self.file.get())

            new_file.close()
            os.remove(out_file)
            shutil.move(self.file.get(), self.location.get())

        # Video option
        if self.option == 1:
            out_file = file.download(
                filename=self.file.get(),
                output_path=self.location.get()
                )

        # Advanced search
        if file.is_progressive is False and file.mime_type == "video/mp4":
            confirm = messagebox.askokcancel(
                "Alert",
                "This video doesn't contain audio, " +
                "PytDownloader can add the audio in the video " +
                "but the process take a long moment to complete " +
                "depending of the quality of the video and the duration. " +
                "This process will take a some resouces of your computer. " +
                "Continue?"
            )
            if not confirm:
                os.remove(out_file)
                self.on_cancel()
                return self.on_function_finish()

            try:
                # Generate audio
                audio_file = audio_video.download(filename="audio_file.mp4")
                mp.VideoFileClip(
                    audio_file
                    ).audio.write_audiofile("audio_file.mp3")
                os.remove(audio_file)

                # Fix video
                new_video = mp.VideoFileClip(out_file)
                audio = mp.AudioFileClip('audio_file.mp3')

                new_audio = mp.CompositeAudioClip([audio])
                new_video.audio = new_audio
                new_video.write_videofile(self.file.get())
                time.sleep(1)

                new_video.close()
                os.remove(out_file)
                os.remove('audio_file.mp3')
                audio.close()
                shutil.move(self.file.get(), self.location.get())
            except Exception:
                os.remove(out_file)
                os.remove('audio_file.mp3')
                return self.on_function_finish(
                    "Conversion error",
                    "Something has happened in the conversion process, " +
                    "please try again later.",
                    True
                )

        return self.on_function_finish(
            "Success",
            self.file.get() + " has been successfully downloaded"
        )

    # Creation the graphic interface
    def create_widgets(self):

        # File Title
        self.lab_filetitle = tk.Label(
            self,
            anchor=E,
            text="Title: "
            )
        self.lab_filetitle.grid(
            row=0,
            column=0,
            pady=10,
            padx=10,
            sticky=E + N
            )

        self.f_title = tk.Entry(
            self,
            textvariable=self.file_title
            )
        self.f_title.grid(
            row=0,
            column=1,
            columnspan=2,
            pady=10,
            padx=10,
            sticky=W + E
            )

        # File Location
        self.lab_filelocation = tk.Label(
            self,
            anchor=E,
            text="Location: "
            )
        self.lab_filelocation.grid(
            row=1,
            column=0,
            pady=5,
            padx=10,
            sticky=N + W + E
            )

        self.f_location = tk.Entry(
            self,
            textvariable=self.location,
            state="disabled"
            )
        self.f_location.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=10,
            ipadx=10,
            pady=5,
            sticky=N + W + E
            )

        self.search_loc = tk.Button(
            self,
            text="...",
            command=lambda: self.select_dir()
            )
        self.search_loc.grid(
            row=1,
            column=2,
            padx=5,
            sticky=E
            )

        # Buttons
        self.cancel_button = tk.Button(
            self,
            text="Cancel",
            relief="raised",
            width=10,
            command=lambda: self.destroy()
            )
        self.cancel_button.grid(
            row=2,
            column=1,
            pady=5,
            sticky=E
            )

        self.save_button = tk.Button(
            self,
            text="Save",
            width=10,
            command=lambda: self.download_file()
            )
        self.save_button.grid(
            row=2,
            column=2,
            pady=5,
            padx=10,
            sticky=W
            )
        self.save_button.bind('<Button-1>', self.on_button_click)

    # Validations
    def on_function_finish(self, title="", message="", error=False):
        self.config(cursor='')
        self.title("Save File")
        if error is True:
            messagebox.showerror(
                title,
                message
            )
            return self.destroy()
        elif title != "" and message != "":
            messagebox.showinfo(
                title,
                message
            )
            self.parent.clean_query()
        return self.destroy()

    def on_cancel(self):
        self.config(cursor='')

    def on_change_name(self):
        if self.option == 0:
            self.file.set(self.file_title.get() + ".mp3")
        if self.option == 1:
            self.file.set(self.file_title.get() + ".mp4")

    # Events
    def on_return_click(self, event):
        self.config(cursor='wait')
        self.title("Save File (Downloading)")
        self.download_file()

    def on_button_click(self, event):
        self.config(cursor='wait')
        self.title("Save File (Downloading)")
