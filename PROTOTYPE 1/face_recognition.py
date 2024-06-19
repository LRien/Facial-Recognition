import os
import cv2 as cv
import numpy as np
from datetime import datetime

# Function to get the list of people (folders) from the Faces directory
def get_people_list(directory):
    return [person for person in os.listdir(directory) if os.path.isdir(os.path.join(directory, person))]

DIR = r'C:\Users\Leon\Desktop\CASESTUDY\Faces'
haar_cascade = cv.CascadeClassifier('haar_face.xml')

# Get the list of people
people = get_people_list(DIR)
print("People found:", people)

# Variables to hold features and labels
features = []
labels = []

# Function to create training data
def create_train():
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            face_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in face_rect:
                faces_roi = gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)

create_train()
print('Training Done -----------------------------')

features = np.array(features, dtype='object')
labels = np.array(labels)

# Creating the recognizer
face_recognizer = cv.face.LBPHFaceRecognizer_create()

# Training the recognizer on the feature list and label list
face_recognizer.train(features, labels)

# Save the trained recognizer and people list
face_recognizer.save('face_trained.yml')
np.save('features.npy', features)
np.save('labels.npy', labels)
np.save('people.npy', np.array(people))  # Save the people list

# Load the people list
people = np.load('people.npy').tolist()
print("People loaded:", people)

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 9)

    for (x, y, w, h) in faces_rect:
        faces_roi = gray[y:y+h, x:x+w]

        label, confidence = face_recognizer.predict(faces_roi)

        if confidence < 100:  # Confidence threshold to consider a match
            cv.putText(frame, str(people[label]), (x, y-10), cv.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), thickness=2)
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} - {people[label]}: Is present")

    frame = cv.resize(frame, (min(frame.shape[1], 800), min(frame.shape[0], 600)))

    cv.imshow("Face Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
