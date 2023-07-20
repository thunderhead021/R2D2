import os.path
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import json
import random
import speech_recognition as sr
import pyttsx3
import time
import math 
#import serial

startlog = time.time()
slowMove = ['amble', 'limp', 'saunter', 'stagger', 'swagger', 'tiptoe', 'traipse', 'sway', 'slow']
normalMove = ['move', 'go', 'walk', 'lope', 'strut', 'come']
fastMove = ['run', 'jog', 'dart', 'scamper', 'scurry', 'bounce']
spinMove = ['turn', 'spin', 'roll', 'clockwise', 'counterclockwise']

def SpinCall(movestring):
    if('counterclockwise' in movestring or 'left' in movestring):
        SpinCallHelper("left", movestring)
    else:
        SpinCallHelper("right", movestring)
    
def SpinCallHelper(movetype, movestring):
    res = [int(i) for i in movestring.split() if i.isdigit()]
    if len(res) == 1:
        if 'degree' in movestring:
            movewithtime(movetype, convertAngleToSeconds(res[0]), 0)
        else:
            movewithtime(movetype, convertTimeToSeconds(movestring, res[0]), 0)
    else:
        movewithtime(movetype, 1, 0)
    
def MoveCall(movestring, speed):
    res = [int(i) for i in movestring.split() if i.isdigit()]
    if len(res) == 1:
        movewithtime(movestring, convertTimeToSeconds(movestring, res[0]), speed)
    else:
        movewithtime(movestring, 1, speed)

def convertAngleToSeconds(angle):
    #need actual speed
    return math.ceil(angle*2/45)
              
def convertTimeToSeconds(movestring, timeInput):
    if ('second' in movestring):
        return timeInput
    elif('minute' in movestring):
        return timeInput*60
    elif('hour' in movestring):
        return timeInput*60*60
    else:
        return 0
             
def movewithtime(movestring, exetime, speed):
    global startlog
    tm = 0
    move(movestring)
    for x in range(speed):
        move(movestring)
    while (startlog + tm < startlog + exetime):
        tm += 1
        print(str(tm))
        time.sleep(1)
    move("stop")   
    
def move(movestring):
    if ('left' in movestring):
        print("move left")
        #ser.write(b"left")
    elif ('right' in movestring):
        print("move right") 
        #ser.write(b"right") 
    elif ('forward' in movestring):
        print("move forward") 
        #ser.write(b"forward")
    elif ('backward' in movestring):
        print("move backward")  
        #ser.write(b"backward")
    elif ('stop' in movestring):
        print("Stop")
        #ser.write(b"stop")
        
# Initialize the recognizer
r = sr.Recognizer()
 
# Function to convert text to
# speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
     
     
# Loop infinitely for user to
# speak
 
while(1):   
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source2:
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input
            audio2 = r.listen(source2)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print("Did you say " + MyText)
            if any(text in MyText for text in spinMove):
                SpinCall(MyText)
            elif any(text in MyText for text in slowMove):
                MoveCall(MyText, 0)
            elif any(text in MyText for text in normalMove):
                MoveCall(MyText, 1)
            elif any(text in MyText for text in fastMove):
                MoveCall(MyText, 2)
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occured")