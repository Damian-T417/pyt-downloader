'''PytDownloader v0.1 using pytube library and tkinter, Made By Damian-T417'''

# Importing packages
import tkinter as tk

from tkinter import ttk
from tkinter import S, N, E, W
from tkinter import messagebox


class YoutubeDownloader(tk.Tk):

    # Window Constructor
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Configuring the window and grid (final desing)
        self.geometry("500x425")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title("Youtube Downloader")
        self.resizable(False, False)
        self.createWidgets()

    def downloadFile(self, itag):
        print("Yes, it's that a function? ", itag)

    # Functionality of the program
    def printList(self):

        # Title
        self.title = tk.Label(self, font=12, pady=10, text="James Smith - Tell Me That You Love Me")
        self.title.grid(row=2, column=0, columnspan=5)

        for i in range(10):

            # itag
            itagVar = tk.IntVar()
            itagVar.set(256 + i)
            self.itag = tk.Entry(self, font=5, state="disabled", textvariable=itagVar)
            self.itag.grid(row=9 + i, column=0, sticky=E+W)

            # mime_type
            self.mime = tk.Label(self, font=1, anchor=W, padx=10, text="audio/webm")
            self.mime.grid(row=9 + i, column=1, sticky=E+W)

            # res (resolution)
            # If this is audio, don't show
            self.res = tk.Label(self, font=5, text="720p")
            self.res.grid(row=9 + i, column=2, sticky=E+W)

            # download
            self.download = tk.Button(self, width=5, text="Download", command=lambda: self.downloadFile(self.itag.get()))
            self.download.grid(row=9 + i, column=3, padx=10, sticky=E+W)


    # Creation the graphic interface
    def createWidgets(self):

        option_download = tk.IntVar()

        # Search bar
        self.link = tk.Entry(self)
        self.link.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky=W+E)

        self.search = tk.Button(self, width=10, text="Search", command=lambda: self.printList())
        self.search.grid(row=0, column=3, pady=10, padx=10, sticky=W+E)

        # Options
        self.audio = tk.Radiobutton(self, text="Audio", variable=option_download, value=0)
        self.audio.grid(row=1, column=0)

        self.video = tk.Radiobutton(self, text="Video", variable=option_download, value=1)
        self.video.grid(row=1, column=1)



        # Table
        


        '''
        option_download = tk.IntVar()

        self.title = tk.Label(self, font=12, text="Youtube Video downloader")
        self.title.grid(row=0, column=0, columnspan=2, padx=1, ipady=6)

        self.link = tk.Entry(self)
        self.link.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=5, sticky=W+E)

        self.audio = tk.Radiobutton(self, text="Audio", variable=option_download, value=0)
        self.audio.grid(row=3, column=0)

        self.video = tk.Radiobutton(self, text="Video", variable=option_download, value=1)
        self.video.grid(row=3, column=1)

        self.download = tk.Button(self, height=2, text="Download", command=lambda: self.functionality())
        self.download.grid(row=4, column=0, columnspan=2, rowspan=5, padx=10, pady=5, sticky=S+N+E+W)
        '''


if __name__ == "__main__":

    root = YoutubeDownloader()
    root.mainloop()
