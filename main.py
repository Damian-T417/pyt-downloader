import os
import json
import urllib as ur

from tkinter import messagebox
from downloader import Pytdownloader

if not os.path.exists('data.json'):
    new_data = {
        'show_welcome': 1,
        'file_location': ""
    }
    with open('data.json', 'w') as f:
        json.dump(new_data, f, indent=4, sort_keys=True)


def internet_connection():
    try:
        ur.request.urlopen('https://www.youtube.com/', timeout=1)
        return True
    except ur.error.URLError:
        return False


if __name__ == "__main__":

    connection = internet_connection()
    if connection is False:
        messagebox.showerror(
            "Connection error",
            "You need internet to use PytDownloader, " +
            "or maybe your connection is so slow. " +
            "If this is the case, PytDownloader won't work properly."
        )

    with open('data.json', 'r') as f:
        data = json.load(f)

    root = Pytdownloader()

    if data['show_welcome'] == 1:
        messagebox.showinfo(
            "Welcome!",
            "Welcome to Pyt-downloader, " +
            "put a youtube link in the first entry and push" +
            " search to find your audio/video in " +
            "diferent quality and download, " +
            "try in advanced search to more if you need a more options."
        )
        data['show_welcome'] = 0
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    root.mainloop()
