import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from pytube import YouTube


def ui(master):
    master.title("Youtube Downloader")
    master.geometry("800x500")
    title_label = Label(master, text='Youtube Downloader', font=("Arial", 30, 'bold'))
    title_label.pack()

def widgets(master):
    global url_name
    url_name = StringVar()
    url_label = Label(master, text="Enter youtube url: ")
    url_txtbox = Entry(master, textvariable=url_name, width=50)
    url_label.pack(pady=30)
    url_txtbox.pack()

    btn_download = Button(master, text="Download Video", command=open_file_dialog)
    btn_download.pack(pady=10)

def download_video(url, path):
    try:
        yt = YouTube(url)

        streams = yt.streams.filter(progressive=True, file_extension="mp4")

        hr_stream = streams.get_highest_resolution()

        hr_stream.download(output_path=path)
        messagebox.showinfo("Yay!!", "Video downloaded successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"{e}")

def open_file_dialog():
    url = url_name.get()
    folder = filedialog.askdirectory()

    if folder:
        print(f"Selected folder: {folder}")
        download_video(url, folder)

    return folder


def main(master):
    ui(master)
    widgets(master)


if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()
