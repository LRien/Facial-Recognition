import os
import cv2 as cv
import numpy as np

people =['Leonardo','Christine']

# For variable use later
# p = []
# for i in os.listdir(r'C:\Users\Leon\Desktop\CASESTUDY\Faces'):
    # p.append(i)

DIR = r'C:\Users\Leon\Desktop\CASESTUDY\Faces'
haar_cascade = cv.CascadeClassifier('haar_face.xml')


# this function is used to train the model
features = []
labels = []

def create_train():
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path,img)

            img_array =cv.imread(img_path)
            gray =cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            face_rect = haar_cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=4)

            for(x,y,w,h) in face_rect:
                faces_roi=gray[y:y+h,x:x+w]
                features.append(faces_roi)
                labels.append(label)

create_train()
print('Training Done -----------------------------')

features = np.array(features, dtype='object')
labels = np.array(labels)
#creating the recognizer

face_recognizer =cv.face.LBPHFaceRecognizer_create()

#Training the Recognizer on the feature list and label list

face_recognizer.train(features,labels)

face_recognizer.save('face_trained.yml')
np.save('features.npy', features)
np.save('labels.npy', labels)


