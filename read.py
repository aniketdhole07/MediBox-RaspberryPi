import firebase_admin
from firebase_admin import credentials, firestore
import json
import datetime

# For text to speech
import pyttsx3
engine = pyttsx3.init()

#for servo controlling
import RPi.GPIO as GPIO
import time

#steeing up pinmode
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
servo1 = GPIO.PWM(23,50)
servo2 = GPIO.PWM(18,50)

#initialize servo
servo1.start(0)
servo2.start(0)

#Add Servo Duty Cycle Angles to Box ID
#(Duty Cycle 2 to 12  -> 0 Degree to 180 Degrees)
servo_duty={"A":2,"B":4,"C":6,"D":9,"E":12}

# Add Firebase Admin Credentials, you will get at 
# Firebase Project->Project Settings->Service Account->Generate New Private Key , Paste the key in creds.json file
cred = credentials.Certificate("./creds.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#Interval Time to check data in firestore
time_int=2
#to read only once for that minute
f=0
col_ref=[]
all_data=[]
update_done={
    u'done': True
}
#Infinite Loop
while True:
    #Get Current Date
    datetime_object = datetime.datetime.now()
    t = datetime_object.strftime("%M")
    #Get current Time
    t_hr_min = datetime_object.strftime("%H:%M")
    t_date= datetime_object.strftime("%Y-%m-%d")
    #print(t_hr_min)
    #Read Every 2 Minutes
    if(int(t)%time_int==0 and f==0):
        col_ref = db.collection(u'med').document(u'lvwsKOTcE1X6jTaiRUOBHlNiElZ2').collection(u'med').get()
        print("Reading From Database Every 2 Minutes")
        f=1
        all_data.clear()
        #Store All Data in new List
        for doc in col_ref:
            #print(u'{} => {}'.format(doc.id, doc.to_dict()))
            temp_data=doc.to_dict()
            if(temp_data["done"]==False):
                single_med_data=[]
                date_med,time_med=temp_data["date"].split(" ")
                single_med_data.append(date_med)
                single_med_data.append(temp_data["content"])
                single_med_data.append(temp_data["dose"])
                single_med_data.append(temp_data["box"])
                single_med_data.append(time_med)
                single_med_data.append(doc.id)
                all_data.append(single_med_data)
        print(all_data)
    #Update FLag to avoid Reading Data Multiple TImes    
    elif(int(t)%time_int!=0):
        f=0
    rem_list=[]
    #Traverse Data from List and Check the Time
    for i in all_data:
        if(i[0]==t_date and i[4]==t_hr_min):
            print("Take Medicine")
            engine.setProperty('rate', 100)
            #Text to Speech
            say_text="Hello,  Please take the Medicine "+ i[1] + " With " + i[2] + " doses. And The Box will Open Now" 
            engine.say(say_text)
            engine.runAndWait()
            #Rotate the Base Servo Accoording to Box ID and Duty Cycle
            servo2.ChangeDutyCycle(servo_duty[i[3]])
            time.sleep(2)
            servo2.ChangeDutyCycle(0)
            #Change Angle of Door Servo Motor
            servo1.ChangeDutyCycle(4)
            time.sleep(2)
            servo1.ChangeDutyCycle(11)
            time.sleep(5)
            servo1.ChangeDutyCycle(4)
            time.sleep(2)
            servo1.ChangeDutyCycle(0)
            #Update in Database that Medicine is Taken
            db.collection(u'med').document(u'lvwsKOTcE1X6jTaiRUOBHlNiElZ2').collection(u'med').document(i[5]).set(update_done, merge=True)
            rem_list.append(i[5])
    for value in all_data[:]:
        if value[5] in rem_list:
            all_data.remove(value)
    



    

