import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube
import customtkinter as ck
from customtkinter import *


def main():
    root = CTk()
    root.title("Youtube Downloader")
    root.geometry("800x500")

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=3)

    root.grid_columnconfigure(0, weight=1)

    title_frame = CTkFrame(root)
    title_frame.grid(row=0, column=0, columnspan=2, stick="nsew")
    title_label = CTkLabel(title_frame, text='Youtube Downloader', font=("Arial", 36, 'bold'))
    title_label.pack()

    form_frame = CTkFrame(root)
    form_frame.grid(row=1, column=0, sticky='nsew')

    video_title_str = StringVar()
    video_title_str.set("After uploading link, press 'Enter' to view details")
    video_title = CTkLabel(form_frame, textvariable=video_title_str, font=("Arial", 16, 'bold'))
    video_title.pack(pady=30)

    def download_video():
        url = url_name.get()
        try:
            yt = YouTube(url, on_progress_callback=on_progress)

            fileType = file_type_txt.get()

            if (fileType == "Video"):
                type_message_txt.configure(text="")
                streams = yt.streams.filter(progressive=True, file_extension="mp4")
                hr_stream = streams.get_highest_resolution()
                path = open_file_dialog()
                hr_stream.download(output_path=path)
            elif (fileType == "Audio"):
                type_message_txt.configure(text="")
                streams = yt.streams.filter(only_audio=True).first()
                path = open_file_dialog()
                streams.download(path)
            else:
                type_message_txt.configure(text="Please select file type.", text_color="Red")

        except Exception as e:
            url_message_txt.configure(text="Invalid URL", text_color="Red")
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        per = str(int(percentage_of_completion))

        progress_lbl.configure(text=per + "%")
        progress_lbl.update()

        progressBar.set(float(percentage_of_completion) / 100)
        if per == "100%":
            download_message_txt.configure(text="Download successful", text_color="Blue")

    def open_file_dialog():
        folder = filedialog.askdirectory()

        if folder:
            print(f"Selected folder: {folder}")

        return folder

    def on_link_upload(event=None):
        try:
            url = url_name.get()
            yt = YouTube(url)
            url_title = yt.title
            video_title_str.set(url_title)
            url_message_txt.configure(text="")
        except Exception as e:
            url_message_txt.configure(text="Unable to get url details.", text_color="Red")


    url_name = StringVar()
    url_label = CTkLabel(form_frame, text="Enter Youtube URL: ")
    url_txtbox = CTkEntry(form_frame, textvariable=url_name, width=400)
    url_txtbox.bind("<Return>", on_link_upload)
    url_message_txt = CTkLabel(form_frame, text="")
    url_label.pack()
    url_txtbox.pack()
    url_message_txt.pack()

    file_type_frame = CTkFrame(form_frame, fg_color="transparent")
    file_type_lbl = CTkLabel(file_type_frame, text="Choose File Type: ")
    file_type_txt = ck.StringVar()
    file_type_mode = ck.CTkComboBox(file_type_frame, values=["Video", "Audio"], variable=file_type_txt)
    type_message_txt = CTkLabel(file_type_frame, text="")
    file_type_frame.pack(pady=20)
    file_type_lbl.pack()
    file_type_mode.pack()
    type_message_txt.pack()


    btn_download = CTkButton(form_frame, text="Download", command=download_video)
    btn_download.pack()

    # Progress widgets
    progress_frame = CTkFrame(form_frame, height=50)
    progress_frame.pack(pady=40)

    progress_lbl = CTkLabel(progress_frame, text="0%")
    progress_lbl.pack()

    progressBar = CTkProgressBar(progress_frame, width=400)
    progressBar.set(0)
    progressBar.pack()

    download_message_txt  = CTkLabel(progress_frame, text="")
    download_message_txt.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
