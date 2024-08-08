import tkinter
import customtkinter
from pytubefix import YouTube  # Import pytubefix for YouTube download functionality

def startDownload():
    try:
        yt_link = link.get()
        yt_object = YouTube(yt_link, on_progress_callback=on_progress)

        # Handle potential errors during stream selection (common issue with pytubefix)
        try:
            video = yt_object.streams.get_audio_only()
        except (AttributeError, KeyError):
            available_streams = yt_object.streams.filter(progressive=True).order_by('resolution').desc()
            video = available_streams.first()  # Select the first available stream

        video.download()

        title.configure(text=yt_object.title, text_color="black")
        finsishLabel.configure(text="Download Completed!!")
    except Exception as e:
        # Provide more informative error handling
        error_message = f"An error occurred: {str(e)}"
        finsishLabel.configure(text=error_message, text_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percent_of_completion))

    pPercentage.configure(text=per + " %")
    pPercentage.update()

    # Update the progress bar
    progressBar.set(float(percent_of_completion / 100))  # Needs float value between 0 and 1

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()  # Initialization
app.geometry("720x480")  # Dimensions
app.title("Youtube Downloader")

# UI elements
title = customtkinter.CTkLabel(app, text="Insert a Youtube Link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Download finished label
finsishLabel = customtkinter.CTkLabel(app, text="")
finsishLabel.pack()

# Progress percentage label
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

# Progress bar
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)  # Progress bar goes from 0-1
progressBar.pack(padx=10, pady=10)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run the app
app.mainloop()