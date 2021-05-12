# Benjamin Ugaz
# AM CLASS OF 2021
# 4-27-2021
# Final ver 5/7/2021
from tkinter import *
import pyaudio
import pyttsx3
import speech_recognition as sr
import threading
import time
import os
import datetime
import wikipedia
import subprocess
import webbrowser
from selenium import webdriver
import cv2
import imageio
from PIL import Image, ImageTk
from playsound import playsound

sttime = datetime.datetime.now().strftime("%D")
starttime = open("runtime.txt","a")
starttime.write("Started: " + sttime +"\n")
starttime.write("______________\n" )
starttime.close()
root = Tk()
root.configure(bg='black')
root.title("JRVA")
root.protocol("WM_DELETE_WINDOW", root.iconify)
print(root.protocol)

# make Esc exit the program

root.bind('<Escape>', lambda e: root.destroy())

photo = PhotoImage(file = "Icons/logo.png")
cl = PhotoImage(file = "Icons/classlogo.png")
#frames of the animation
frames = [PhotoImage(file='Icons/Background.gif',format = 'gif -index %i' %(i)) for i in range(60)]


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
introduction = 'Im Jrva. Your virtual assistant.'

#mic on image
mic_status_on = [PhotoImage(file='Icons/mic_1.png')]

#mic off image
mic_status_off = [PhotoImage(file='Icons/mic_0.png')]

#a function that tells jrva what to say
def say(audio):
    write("Jrva said: " + audio)
    label.configure(text=audio,compound='center')
    JRVA.say(audio)
    JRVA.runAndWait()

def write(say):
    time = datetime.datetime.now().strftime("%H:%M:%S\n")
    runtime = open("runtime.txt","a")
    runtime.write('\n')
    runtime.write('Time: ' + time)
    runtime.write(str(say) + '\n')

    runtime.close()

#gets the current time of day 
def saytime():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        label.configure(text="Good morning, " + introduction)
        say("Good morning, " + introduction)
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
        write('User said: ' + query)
        if 'who are you' in query:
            say(introduction)

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
            say("Great, Thanks for asking.")

        elif 'spotify' in query:
            say("Opening Spotify")
            subprocess.call('Apps/Spotify/Spotify.exe')

        elif 'grades' in query:
            say("Opening Gradebook")
            webbrowser.open('https://igradeplus.com/index.jsp')
        
        elif 'career' in query:
            say("Opening Career Center")
            webbrowser.open('http://mcc.jamesrumsey.com/')

        elif 'resources' in query:
             say("Opening Student Resources")
             webbrowser.open('https://www.jamesrumsey.com/knowledge-base/electronic-resources/')
        
        elif 'calender' in query:
            say('Opening Calender')
            webbrowser.open('https://www.jamesrumsey.com/calendars/')

        elif query == 'none':
            say("Sorry, i didnt get that. please try again.")
            write('Microphone didnt Hear anything')
            readon()

        else:
            say('Here is a Google search for, ' + query + '.' )
            webbrowser.open('https://www.google.com/search?q=' + query)
    except Exception as e:
        write(e)
        readoff()


#listens for a command
def takeCommand():
    try:
        r=sr.Recognizer()
        with sr.Microphone() as source:
            try:
                r.pause_threshold=1
                say("Listening..")
                r.dynamic_energy_threshold = False   
                audio=r.listen(source,timeout=5.0,phrase_time_limit=5)
            except Exception as e:
                write(e)
                audio = ''
        try:
            readoff()
            say("One second")
            query=r.recognize_google(audio,language='en-in')
        except Exception as e:
            write(e)
            return "None"
        return query
    except Exception as e:
        write(e)
        readoff()
        say('No Microphone was Detected')

    
video_name = "Videos/jriv.mp4" #This is your video file path
video = imageio.get_reader(video_name)
#activates the mic and updates the image
def readon():
    write('Mic On Activated')
    button.config(image=mic_status_on,command=lambda: threading.Thread(target=readoff, daemon=True).start())
    threading.Thread(target=results, daemon=True).start()


def playsounds():
    playsound('Videos/jriv.mp3')
    
def video():
    video_name = "Videos/jriv.mp4" #This is your video file path
    video = imageio.get_reader(video_name)

    videowin = Toplevel(root)
  
    # sets the title of the
    # Toplevel widget
    videowin.title("INTRO")
  

    videowin.resizable(False, False)
    
    re = Label(videowin,background="black")
    re.pack()
    threading.Thread(target=playsounds, daemon=True).start()
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        re.config(image=frame_image)
        re.image = frame_image
    p.terminate()



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
    newWindow.geometry("350x350")

    newWindow.resizable(False, False)
    # A Label widget to show in toplevel
    Label(newWindow,text =data,relief=RIDGE,justify=LEFT,bd=2,font=('Bookman',8)).pack()


#turns off the mic
def readoff():
    write('Mic Off Activated')
    button.config(image=mic_status_off,command=lambda: threading.Thread(target=readon, daemon=True).start())

#updates the animation
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == 60:
        ind = 0
    label.configure(image=frame,compound='center',font='impact',foreground="orange")
    root.after(speed, update, ind)

button= Button(root,activebackground="black",borderwidth=0,background="black", width=50, height=50,image=mic_status_off,command=lambda: threading.Thread(target=readon, daemon=True).start())
c = Button(root,background='#DCAE96', text="Commands",command = openNewWindow, width=9, )
tag = Button(root,image=cl,activebackground="black",borderwidth=0,bg='black',height=100,relief=SUNKEN, state=ACTIVE,pady=50,command=lambda: threading.Thread(target=video, daemon=True).start())
text= Label(root)
label = Label(root,background="black")
label.pack()

button.pack()
tag.pack(side=RIGHT)
root.iconphoto(False, photo)
root.resizable(False, False)
c.pack(side=LEFT)
root.geometry('600x485')
root.after(0, update, 0)
threading.Thread(target=saytime, daemon=True).start()

root.mainloop()
sttime = datetime.datetime.now().strftime("%D")
starttime = open("runtime.txt","a")
starttime.write('\n')
starttime.write("closed: "+ sttime + '\n')
starttime.write("______________\n" )
starttime.close()