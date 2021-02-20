# MediBox-RaspberryPi
Codes for Raspberry Pi of MediBox and CAD STL files

##  For Flutter App Code Go to https://github.com/aniketdhole07/MediBox

<img src="https://i.ibb.co/kKzZ1v1/Screenshot-17.png" alt="Screenshot-17" border="0">
<img src="https://i.ibb.co/wMYgx2J/rpii.png" alt="rpii" border="0">

## To Generate  creds.json 
1. Go To Firebase Project -> Project Settings
2. Then Open Service Accounts
3. In that open Firebase Admin SDK
4. Below Click on `Generate Private Key`
5. Paste that key in `creds.json` file

<img src="https://i.ibb.co/XxYzVcb/image-19.png" alt="image-19" border="0">

## To Run on RaspberryPi
1. Follow the Circuit and Attach the Speaker AUX cable to Audio Jack of Raspberry Pi or Update the Code According to Your Servo Pinout

<img src="https://i.ibb.co/5nQ9LQY/image-13.png" alt="image-13" border="0">

2. Install the Required Libraries
```
pip install pytts3x
pip install firebase-admin
```

3. And then Run the Python File

`python3 read.py`
