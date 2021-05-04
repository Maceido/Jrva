# Benjamin Ugaz
# AM CLASS OF 2021
# 4-27-2021
from tkinter import *
import pyaudio
import pyttsx3
import speech_recognition as sr
import threading
import time
import random
import requests
import json
import pyowm
import os
import datetime
import wikipedia
import webbrowser
from selenium import webdriver


root = Tk()
root.title("JRVA")
photo = PhotoImage(file = "Icons/logo.png")
#frames of the animation
frames = [PhotoImage(file='Icons/Background.gif',format = 'gif -index %i' %(i)) for i in range(60)]


bottom = Frame(root)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)


#speed of the animation
speed = 50
with open('Commands.txt', 'r') as file:
    data = file.read()
#speed rate of the voice
newVoiceRate = 175

#speach engine properties
JRVA = pyttsx3.init()
voices =JRVA.getProperty('voices')
JRVA.setProperty('voice',voices[0].id)
JRVA.setProperty('rate',newVoiceRate)

#How jrva will intorduce himself
introduction = 'Im Jrva, Your virtual assistant.'

#mic on image
mic_status_on = [PhotoImage(file='Icons/mic_1.png')]

#mic off image
mic_status_off = [PhotoImage(file='Icons/mic_0.png')]

#a function that tells jrva what to say
def say(audio):
    label.configure(text=audio,compound='center')
    JRVA.say(audio)
    JRVA.runAndWait()
    
#gets the current time of day 
def saytime():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        label.configure(text="Good morning. " + introduction)
        say("Good morning. " + introduction)
    elif hour>=12 and hour<18:
        say("Good afternoon. " + introduction)
        label.configure(text="Good afternoon. " + introduction)
    else:
        say("Good Evenning. " + introduction)
        label.configure(text="Good Evenning. " + introduction)

#gets the command and activates it
def results():
    try:
        query=takeCommand().lower()
        if 'who are you' in query:
            say('I am Jrva.')
        elif 'james' in query:
            say('opening James Rumsey home page')
            webbrowser.open('jamesrumsey.com')
        elif 'adult programs' in query:
            say('opening James Rumsey adult programs')
            webbrowser.open('https://www.jamesrumsey.com/category/adult-programs/')
        elif 'high school progrmas' in query:
            say('opening James Rumsey high school programs')
            webbrowser.open('https://www.jamesrumsey.com/category/high-school-programs/')
        elif 'nursing' in query:
            say('opening James Rumsey nursing program')
            webbrowser.open('https://www.jamesrumsey.com/academics/adult-programs/practical-nursing/')

        elif 'adult education' in query:
           say('opening adult education')
           webbrowser.open('https://www.jamesrumsey.com/academics/adult-basic-education/')

        elif 'youtube' in query:
            say('Opening Youtube')
            webbrowser.open("youtube.com")

        elif 'google' in query:
            say('Opening Google')
            webbrowser.open("google.com")

        elif 'time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            say(f"the time is {strTime}")

        elif 'how are you' in query:
            say("I am good. What about you..")

        elif query == 'none':
            say("Sorry, i didnt get that. please try again.")
            readon()

        else:
            say("Not sure what " + query + ' is')
    except:
        readoff()

#listens for a command
def takeCommand():
    try:
        r=sr.Recognizer()
        with sr.Microphone() as source:
            try:
                say("Listening..")
                r.pause_threshold=1
                r.dynamic_energy_threshold = False  
                r.listen(source,timeout=5.0)      
                audio=r.listen(source)
            except:
                audio = ''
        try:
            readoff()
            say("One second")
            query=r.recognize_google(audio,language='en-in')
            print(f"User said:{query}\n")
        except Exception as e:
            return "None"
        return query
    except:
        say('No Microphone was Detected')
        readoff()
    

#activates the mic and updates the image
def readon():
    button.config(image=mic_status_on,command=lambda: threading.Thread(target=readoff, daemon=True).start())
    threading.Thread(target=results, daemon=True).start()
    

# function to open a new window 
# on a button click
def openNewWindow():
      
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(root)
  
    # sets the title of the
    # Toplevel widget
    newWindow.title("Jrva")
  
    # sets the geometry of toplevel
    newWindow.geometry("355x250")
  
    # A Label widget to show in toplevel
    Label(newWindow,text =data,relief=RIDGE,justify=LEFT).pack()

#turns off the mic
def readoff():
    button.config(image=mic_status_off,command=lambda: threading.Thread(target=readon, daemon=True).start())

#updates the animation
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == 60:
        ind = 0
    label.configure(image=frame,compound='center',font='impact',foreground="orange")
    root.after(speed, update, ind)
    


button= Button(root, image=mic_status_off,command=lambda: threading.Thread(target=readon, daemon=True).start())
c = Button(root, text="Commands",command = openNewWindow, width=9, height=2)
text= Label(root)
label = Label(root)
label.pack()
button.pack()
root.iconphoto(False, photo)
root.resizable(False, False)
c.pack(in_=bottom, side=LEFT)
root.after(0, update, 0)
threading.Thread(target=saytime, daemon=True).start()

root.mainloop()

