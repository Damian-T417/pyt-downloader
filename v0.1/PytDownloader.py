'''PytDownloader v0.1 using pytube library and tkinter, Made By Damian-T417'''

# Importing packages
import os
import moviepy.editor as mp

from tkinter import *
from tkinter import messagebox
from pytube import YouTube


class YoutubeDownloader(Tk):

    # Window Constructor
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Configuring the window and grid (final desing)
        # self.geometry("651x424")

        self.geometry("300x150")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title("Youtube Downloader")
        self.resizable(False, False)
        self.createWidgets()

    # Functionality of the program
    def downloadLink(self, option):
        try:
            yt = YouTube(self.link.get())
        except Exception:
            return messagebox.showerror(
                "Syntax error",
                "The link is not supported or is misspelled"
                )

        file = yt.streams.filter(res="720p").first()

        if (file is None):
            file = yt.streams.first()

        '''
        For the moment the destination will save in the current directory

        Error 'Label' object is not callable (why?)
        destination = askstring(
            'Save file',
            'Enter the destination for save (leave blank for current directory)'
            )

        #destination = "."
        if (destination == ""):
            destination = '.'
        out_file = file.download(output_path=destination)
        '''

        out_file = file.download()
        base, ext = os.path.splitext(out_file)

        if (option == 0):
            new_file = mp.VideoFileClip(out_file)
            new_file.audio.write_audiofile(base + '.mp3')
            new_file.close()
            os.remove(out_file)

        if (option == 1):
            new_file = base + '.mp4'
            os.rename(out_file, new_file)

        self.link.delete(0, 'end')

        messagebox.showinfo(
            "Success", 
            "The" + yt.title + " has been successfully downloaded")

    # Creation the graphic interface
    def createWidgets(self):
        option_download = IntVar()

        self.title = Label(self, font=12, text="Youtube Video downloader")
        self.title.grid(row=0, column=0, columnspan=2, padx=1, ipady=6)

        self.link = Entry(self)
        self.link.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=5, sticky=W+E)

        self.audio = Radiobutton(self, text="Audio", variable=option_download, value=0)
        self.audio.grid(row=3, column=0)

        self.video = Radiobutton(self, text="Video", variable=option_download, value=1)
        self.video.grid(row=3, column=1)

        self.download = Button(self, height=2, text="Download", command=lambda: self.downloadLink(option_download.get()))
        self.download.grid(row=4, column=0, columnspan=2, rowspan=6, padx=10, pady=5, sticky=S+N+E+W)


root = YoutubeDownloader()
root.mainloop()