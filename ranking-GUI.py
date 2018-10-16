# coding:utf-8

from __future__ import division
from tkinter import *
from tkinter.constants import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import os
# from scipy import stats

PATH = "1849968224/"
storage = []
imgIndex = -1
imgLabel = {}
imgName = ""
PHOTO_WIDTH = 224
PHOTO_HEIGHT = 224
TITLE = "Raking Data Collection"

'''
Map the input ranking range to normal distribution
'''
'''
def rankMap(rankings,k):
    x = np.random.uniform(0, 1, 1000)
    x_norm, lbda = stats.boxcox(x)
    print(x_norm, lbda)
    return (x_norm, lbda)
'''
'''
def exitProcessor():
    root.destroy()
    rankingFile.close()
'''

'''
resize the width or height to make the picture fit our window
Since the pictures have been cut as 224*224, resize function is not needed actually
'''
def resize(imgFile, MODE="HEIGHT"):         # WIDTH/HEIGHT MODE sets width/height unchangeable;
    src_width, src_height = imgFile.width, imgFile.height
    resizeTuple = (PHOTO_WIDTH, int(PHOTO_WIDTH/src_width * src_height)) if MODE == "WIDTH" else (int(PHOTO_HEIGHT/src_height*src_width), PHOTO_HEIGHT)
    return imgFile.resize(resizeTuple)


'''
callback function when click the rank button
'''
def rankit(event):
    buttonIndex = rankButton.index(event.widget)
    rank = 50 + buttonIndex*10
    ranking_record.write(imgName + ";" + str(rank))
    ranking_record.write('\n')
    nextImg()
    progressRefresh()


'''
Generate rankButtons in range(50,101,10)
'''
def rankButtonGenerator():
    for i in range(6):
        rankButton[i] = Button(interactFrame, text=str(50+10*i))
        rankButton[i].bind("<Button-1>", rankit)
        rankButton[i].pack(side=LEFT)

'''
change img when rank confirmed to create a loop
'''
def nextImg():
    global imgName, imgIndex, imgLabel
    if imgLabel:
        imgLabel.destroy()
    while True:
        imgIndex += 1
        if imgIndex>=len(imgNames):
            showinfo(TITLE, "Thank you for the ranking!")
            exit()
        imgName = imgNames[imgIndex]
        if not imgName in imgNameRecords:
            break
    imgFile = resize(Image.open(PATH + imgName))
    img = ImageTk.PhotoImage(imgFile)
    imgLabel = Label(pictureFrame, image=img)
    imgLabel.pack(side=LEFT)
    storage.append(img)

'''
Refresh the progressLabel
'''
def progressRefresh():
    progressText.set("{0}/{1}".format(imgIndex+1, len(imgNames)))


'''
Read the file if existed
'''
if not os.path.exists("ranking_record.txt"):
    f = open("ranking_record.txt", 'w')
    f.close()
ranking_record = open("ranking_record.txt", 'r+')
records = ranking_record.readlines()
imgNameRecords = [record.split(';')[0] for record in records]
recordNum = len(records)
imgNames = os.listdir(PATH)

if recordNum>=len(imgNames):
    showinfo(TITLE, "You've completed the ranking!")
    exit()

'''
GUI drawing
'''
root = Tk()
root.title("Ranking Data Collection")
root.geometry("400x300+450+200")
pictureFrame = Frame(root, width=PHOTO_WIDTH, height=PHOTO_HEIGHT)
interactFrame = Frame(root, width=PHOTO_WIDTH, height=50)
pictureFrame.pack(side=TOP)
interactFrame.pack(side=TOP)
rankButton = [0]*6
rankButtonGenerator()
nextImg()


'''
Generate progressLabel and welcomeInfo
'''
progressText = StringVar()
progressText.set("{0}/{1}".format(recordNum+1, len(imgNames)))
progressLabel = Label(root, textvariable=progressText)
progressLabel.pack(side=BOTTOM)

if not recordNum:
    showinfo(TITLE, "Welcome to face ranking data collection system")
else:
    showinfo(TITLE, "Ranking progress {0}/{1}, keep going!".format(recordNum,len(imgNames)))
root.mainloop()
ranking_record.close()