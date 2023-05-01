import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import face_recognition
import os
import datetime
import hashlib
import json
import mysql.connector
import mysql.connector.plugins
from web3 import Web3
import json
import pickle

#Database Connection
mydb = mysql.connector.connect(
  host='localhost',
  user='SDB',
  password='73T)U//Fjq_[cK6C',
  database="stu_dbms"
)

mycursor = mydb.cursor()
print(mydb)

mycursor.execute("SELECT * FROM students")

result = mycursor.fetchall()

for row in result:
  print(row)

#Blockchain Code
# Connect to Ganache local blockchain
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract ABI and contract address
with open('StudentAttendanceABI.json', 'r') as f:
    contract_abi = json.load(f)

contract_address = "0x95961b4bDAED4544044b58b76C8D77E5BEF48791"

# Instantiate contract object
contract = web3.eth.contract(address=contract_address, abi=contract_abi)




#Face Recognition
def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def attendance(PID):

    IdList = []
    IdList.append(PID)
    if PID not in IdList:
        namequery = "SELECT Name FROM students WHERE PID = %s"
        mycursor.execute(namequery, (PID,))
        name = mycursor.fetchone()[0]
        if name is not None:
            print(f"The name of the student with PID {PID} is {name[0]}")
            # Append a block to the blockchain
            tx_hash = contract.functions.markAttendance(name, int(PID), 2).transact({'from': web3.eth.accounts[0]})

            # Wait for transaction confirmation
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            print("Block added to the blockchain with transaction hash:", tx_receipt.transactionHash.hex())
        else:
            print(f"No student found with PID {PID}")


def recognize_faces():
    path = 'images'
    images = []
    PID = []
    myList = os.listdir(path)
    print(myList)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        PID.append(os.path.splitext(cu_img)[0])
    print(PID)

    with open('encodings.pkl', 'rb') as f:
        encodeListKnown = pickle.load(f)

    print('All Encodings Complete!!!')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                ID = PID[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, ID, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(ID)

        cv2.imshow('VideoFrame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Define the functions for the buttons
def view_student_details():
    # Code for the functionality
    pass

def mark_attendance():
    # Code for the functionality
    recognize_faces()


def view_attendance():
    # Code for the functionality
    pass

def train_data():
    # Code for the functionality
    path = 'images'
    images = []
    PID = []
    myList = os.listdir(path)
    print(myList)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        PID.append(os.path.splitext(cu_img)[0])
    print(PID)
    encodeList = faceEncodings(images)
    with open('encodings.pkl', 'wb') as f:
        pickle.dump(encodeList, f)

def view_photo_data():
    # Code for the functionality
    pass

def exit_program():
    root.destroy()

# Create the main window
root = tk.Tk()

# Set the window title
root.title("Student Attendance System")

# Set the window size
root.geometry("400x300")

# Create the buttons
btn_view_student_details = tk.Button(root, text="View Student Details", command=view_student_details)
btn_mark_attendance = tk.Button(root, text="Mark Attendance", command=mark_attendance)
btn_view_attendance = tk.Button(root, text="View Attendance", command=view_attendance)
btn_train_data = tk.Button(root, text="Train Data", command=train_data)
btn_view_photo_data = tk.Button(root, text="View Photo Data", command=view_photo_data)
btn_exit = tk.Button(root, text="Exit", command=exit_program)

# Add the buttons to the window
btn_view_student_details.pack(pady=10)
btn_mark_attendance.pack(pady=10)
btn_view_attendance.pack(pady=10)
btn_train_data.pack(pady=10)
btn_view_photo_data.pack(pady=10)
btn_exit.pack(pady=10)

# Start the main loop
root.mainloop()
