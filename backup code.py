from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title ("MP3 Player")
root.iconbitmap()
root.geometry("500x450")

# Initialize Pygame Mixer
pygame.mixer.init()

# Grab Song length time info
def play_time():
    # grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    # convert to time format
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

    # Get currently playing song
    # current_song = song_box.curselection()
    # Grab song title from playlist
    song = song_box.get(ACTIVE)
    # add directory structure and mp3 to song title
    song = f'C:/Users/mozam/PycharmProjects/MP3 Player/media/{song}.mp3'
    # Load Song Length with Mutagen
    song_mut = MP3(song)
    # Get song Length
    song_length = song_mut.info.length
    # Convert to time format
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))

    # output time to status bar
    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
    # update time
    status_bar.after(1000, play_time)

# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir= "C:/Users/mozam/PycharmProjects/MP3 Player/media", title= "Choose A Song", filetype=(("mp3 Files", ".mp3"), ))
    # strip out the directory info and .mp3 extension from the ....
    song = song.replace("C:/Users/mozam/PycharmProjects/MP3 Player/media/", "")
    song = song.replace(".mp3", "")

    song_box.insert(END, song)

# Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="C:/Users/mozam/PycharmProjects/MP3 Player/media/",
                                      title="Choose A Song", filetype=(("mp3 Files", ".mp3"),))
    # Loop thru song list and replace directory info and mp3
    for song in songs:
        song = song.replace("C:/Users/mozam/PycharmProjects/MP3 Player/media/", "")
        song = song.replace(".mp3", "")
        # Insert into Playlist
        song_box.insert(END, song)
def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/mozam/PycharmProjects/MP3 Player/media/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # call the play time function tp get song length
    play_time()

# Stop playing current song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    # Clear the status bar
    status_bar.config(text="")

# Play the next song in the playlist
def next_song():
    # Get the current song tuple number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Grab song title from playlist
    song= song_box.get(next_one)
    # add directory structure and mp3 to song title
    song = f'C:/Users/mozam/PycharmProjects/MP3 Player/media/{song}.mp3'
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Move active bar in playlist listbox
    song_box.selection_clear(0, END)
    # Activate new song bar
    song_box.activate(next_one)
    # Set active bar to next song
    song_box.selection_set(next_one, last=None)

# Play previous song in playlist
def previous_song():
    # Get the current song tuple number
    next_one = song_box.curselection()
    # Reduce one to the current song number
    next_one = next_one[0] - 1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # reduce directory structure and mp3 to song title
    song = f'C:/Users/mozam/PycharmProjects/MP3 Player/media/{song}.mp3'
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Move active bar in playlist listbox
    song_box.selection_clear(0, END)
    # Activate new song bar
    song_box.activate(next_one)
    # Set active bar to next song
    song_box.selection_set(next_one, last=None)

# Delete A song
def delete_song():
    # Delete Currently selected song
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Delete All song
def delete_all_song():
    song_box.delete(0, END)
    # Stop Music if its playing
    pygame.mixer.music.stop()

# Create Global Pause Variable
global paused
paused = False

def pause(is_paused):
    global paused               # calling this global variable for predefined value False means do nothing initially
    paused = is_paused
    if paused:                  # It will run while paused is true
        pygame.mixer.music.unpause()   # unpaused : now its unpaused
        paused = False          # changing paused initial value
    else:
        # paused
        pygame.mixer.music.pause()
        paused = True

# Create slider function
def slide(x):
	#slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
	song = song_box.get(ACTIVE)
	song = f'C:/gui/audio/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Create Playlist Box
song_box = Listbox(root, bg = "black", fg = "green", width = 60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# Define Player Control Button Images
back_btn = PhotoImage(file="C:/Users/mozam/PycharmProjects/MP3 Player/images/back50.png")
forward_btn = PhotoImage(file="C:/Users/mozam/PycharmProjects/MP3 Player/images/forward50.png")
play_btn = PhotoImage(file="C:/Users/mozam/PycharmProjects/MP3 Player/images/play50.png")
pause_btn = PhotoImage(file="C:/Users/mozam/PycharmProjects/MP3 Player/images/pause50.png")
stop_btn = PhotoImage(file="C:/Users/mozam/PycharmProjects/MP3 Player/images/stop50.png")


controls_frame = Frame(root)
controls_frame.pack()

back_button = Button(controls_frame, image= back_btn, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image= forward_btn, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn, borderwidth=0, command= lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu = add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
# Add Many Song to playlist
add_song_menu.add_command(label="Add Many SOng  To Playlist", command=add_many_songs)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Sing From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Sing From Playlist", command=delete_all_song)

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

root.mainloop()