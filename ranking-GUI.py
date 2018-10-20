import os
import sys

import tkinter as tk
from tkinter.constants import TOP, BOTTOM, LEFT
from tkinter.messagebox import showinfo, showerror
from PIL import Image, ImageTk

PATH = "training_imgs/"
PHOTO_WIDTH = PHOTO_HEIGHT = 224
MODE = "HEIGHT"
TITLE = "Raking Data Collection"

'''
def exit_processor():
    root.destroy()
    rankingFile.close()
'''


def resize(img_file, mode=MODE):         # WIDTH/HEIGHT MODE sets width/height unchangeable;
    """
    Resize the width or height to make the picture fit our window
    Since the pictures have been cut as 224*224, resize function is not needed actually
    (Keep for the not-standard-picture test and reuse)
    """
    src_width, src_height = img_file.width, img_file.height
    mode_map = {
        "WIDTH":  (PHOTO_WIDTH, int(PHOTO_WIDTH/src_width * src_height)),
        "HEIGHT": (int(PHOTO_HEIGHT/src_height*src_width), PHOTO_HEIGHT),
    }
    return img_file.resize(mode_map[mode])


def rank_it(event):
    """ callback function when click the rank button """
    button_index = rank_button.index(event.widget)
    rank = 50 + button_index*10
    ranking_record.write(img_name + ";" + str(rank))
    ranking_record.write('\n')
    next_img()
    progress_refresh()


def rank_button_generator():
    """ Generate rank_buttons (50,60,70,80,90,100) """
    for i in range(6):
        rank_button[i] = tk.Button(interact_frame, text=str(50+10*i))
        rank_button[i].bind("<Button-1>", rank_it)
        rank_button[i].pack(side=LEFT)


def next_img():
    """ Change img when rank confirmed to create a loop """
    global img_name, img_index, img_label
    if img_label:
        img_label.destroy()
    while True:
        img_index += 1
        if img_index >= len(img_names):
            showinfo(TITLE, "Thank you for the ranking!")
            root.destroy()
            sys.exit()
        img_name = img_names[img_index]
        if img_name not in img_name_records:
            break
        if not os.path.exists(PATH):
            showerror(TITLE, "Training set not found.")
            root.destroy()
            sys.exit()
    img_file = resize(Image.open(PATH + img_name))
    img = ImageTk.PhotoImage(img_file)
    img_label = tk.Label(picture_frame, image=img)
    img_label.pack(side=LEFT)
    storage.append(img)     # This is for avoiding the Garbage-Collection deletes the picture.


def progress_refresh():
    """ Refresh the progress_label """
    progress_text.set("{present_index}/{total}".format(present_index=img_index+1, total=len(img_names)))


""" Initialize """
storage = []
img_index = -1
img_label = {}
img_name = ""

""" Read the file if existed """
if not os.path.exists("ranking_record.txt"):
    f = open("ranking_record.txt", 'w')
    f.close()
ranking_record = open("ranking_record.txt", 'r+')
records = ranking_record.readlines()
img_name_records = [record.split(';')[0] for record in records]
record_num = len(records)
img_names = list(set(os.listdir(PATH)))
if record_num >= len(img_names):
    showinfo(TITLE, "You've already completed the ranking!")
    sys.exit()

""" GUI drawing """
root = tk.Tk()
root.title("Ranking Data Collection")
root.geometry("400x300+450+200")
picture_frame = tk.Frame(root, width=PHOTO_WIDTH, height=PHOTO_HEIGHT)
interact_frame = tk.Frame(root, width=PHOTO_WIDTH, height=50)
picture_frame.pack(side=TOP)
interact_frame.pack(side=TOP)
rank_button = [0]*6
rank_button_generator()
next_img()

""" Generate progress_label and welcomeInfo """
progress_text = tk.StringVar()
progress_text.set("{present_index}/{total}".format(present_index=record_num+1, total=len(img_names)))
progress_label = tk.Label(root, textvariable=progress_text)
progress_label.pack(side=BOTTOM)

if not record_num:
    showinfo(TITLE, "Welcome to face ranking data collection system")
else:
    showinfo(TITLE, "Ranking progress {done}/{total}, keep going!".format(done=record_num, total=len(img_names)))
root.mainloop()
ranking_record.close()
