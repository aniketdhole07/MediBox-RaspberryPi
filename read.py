import firebase_admin
from firebase_admin import credentials, firestore
import json
import datetime

import pyttsx3
engine = pyttsx3.init()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
servo2 = GPIO.PWM(18,50)
GPIO.setup(23,GPIO.OUT)
servo1 = GPIO.PWM(23,50)
servo1.start(0)
servo2.start(0)

servo_duty={"A":2,"B":4,"C":6,"D":9,"E":12}
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
while True:
    datetime_object = datetime.datetime.now()
    t = datetime_object.strftime("%M")
    t_hr_min = datetime_object.strftime("%H:%M")
    t_date= datetime_object.strftime("%Y-%m-%d")
    #print(t_hr_min)
    if(int(t)%time_int==0 and f==0):
        col_ref = db.collection(u'med').document(u'lvwsKOTcE1X6jTaiRUOBHlNiElZ2').collection(u'med').get()
        print("Reading From Database Every 2 Minutes")
        f=1
        all_data.clear()
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
    elif(int(t)%time_int!=0):
        f=0
    rem_list=[]
    for i in all_data:
        if(i[0]==t_date and i[4]==t_hr_min):
            print("Take Medicine")
            engine.setProperty('rate', 100)
            
            say_text="Hello,  Please take the Medicine "+ i[1] + " With " + i[2] + " doses. And The Box will Open Now" 
            engine.say(say_text)
            engine.runAndWait()
            servo2.ChangeDutyCycle(servo_duty[i[3]])
            time.sleep(2)
            servo2.ChangeDutyCycle(0)
            servo1.ChangeDutyCycle(4)
            time.sleep(2)
            servo1.ChangeDutyCycle(11)
            time.sleep(5)
            servo1.ChangeDutyCycle(4)
            time.sleep(2)
            servo1.ChangeDutyCycle(0)
            db.collection(u'med').document(u'lvwsKOTcE1X6jTaiRUOBHlNiElZ2').collection(u'med').document(i[5]).set(update_done, merge=True)
            rem_list.append(i[5])
    for value in all_data[:]:
        if value[5] in rem_list:
            all_data.remove(value)
    



    

