import os
import json
from tkinter import messagebox
from downloader import Pytdownloader

if not os.path.exists('data.json'):
    data = {
        'show_welcome': 1,
        'file_location': ""
    }
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    with open('data.json', 'r') as f:
        data = json.load(f)

    root = Pytdownloader()

    if data['show_welcome'] == 1:
        messagebox.showinfo(
            "Welcome!",
            "Welcome to Pyt-downloader, put a youtube link in the first entry and push"+
            " search to find your audio/video in diferent quality and download, "+
            "try in advanced search to more if you need a more options."
        )
        data['show_welcome'] = 0
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    root.mainloop()
