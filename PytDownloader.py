# Importing packages
from tkinter import *
# from tkinter import messagebox


class YoutubeDownloader(Frame):

    # Constructor
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.parent = master
        self.grid()
        self.createWidgets()

    # Functionality of the program
    def downloadLink(self, option):
        print(self.link.get(), option)

    # Creation the graphic interface
    def createWidgets(self):
        option_download = IntVar()

        self.title = Label(self, text="Youtube Video downloader", justify=CENTER)
        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.link = Entry(self, justify=LEFT)
        self.link.grid(row=1, column=0, sticky="nsew", columnspan=2)

        self.audio = Radiobutton(self, text="Audio", justify=CENTER, variable=option_download, value=0)
        self.audio.grid(row=2, column=0, sticky="nsew")

        self.video = Radiobutton(self, text="Video", justify=CENTER, variable=option_download, value=1)
        self.video.grid(row=2, column=1, sticky="nsew")

        self.download = Button(self, text="Download", justify=CENTER, command=lambda: self.downloadLink(option_download.get()))
        self.download.grid(row=3, column=0, sticky="nsew", columnspan=2)

downloader = Tk()
downloader.title("Youtube Downloader")
downloader.resizable(False, False)
root = YoutubeDownloader(downloader)
downloader.mainloop()