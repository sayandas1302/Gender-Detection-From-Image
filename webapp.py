from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2
import os
import math

# calling the gender model 
gen_model = load_model('./artifacts/gen_model.h5')

# function to detect faces from the input image
def face_detect(img):
    '''function detects faces from the image and mark those faces in the image also save the cropped version of the faces'''
    folder_path = "./static/input_output/faces/"
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.09, minNeighbors=10)

    count = 0
    if len(faces)>0:
        for (x, y, w, h) in faces:
            cv2.imwrite(f'{folder_path}face{count}.jpg', cv2.resize(img[y:(y+h), x:(x+w)], (100,100)))
            count += 1
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0, 0, 255), 2)
            
    cv2.imwrite('./static/input_output/outputImg.jpg', img)

    return count

def detect_gender_and_age():
    '''detect the gender of a given face using the pretrained model'''
    gen_dict = {
        0: 'Male',
        1: 'Female'
    }
    folder_path = './static/input_output/faces/'
    files = os.listdir(folder_path)
    X = []
    for file in files:
        img = cv2.imread(folder_path+file)
        X.append(np.array(img))
    X = np.array(X)/255
    gen = [gen_dict[np.argmax(x)] for x in gen_model.predict(X)]
    return (gen)

## The flask app functionality
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    nface = None
    facepaths = None
    gender_list = None
    file_path = "./static/input_output/inputImg.jpg"
    if os.path.isfile(file_path):
        os.remove(file_path)

    if request.method == 'POST':
        img = request.files.get('imageInput')
        img.save('./static/input_output/inputImg.jpg')
    uploadImg_url = 'static/images/uploadImg.png'
    inputimg = cv2.imread('./static/input_output/inputImg.jpg')
    if inputimg is None:
        inputindicate = False
    else:
        inputindicate = True
        nface = face_detect(inputimg)
        if nface >= 1:
            folderpath = './static/input_output/faces/'
            facepaths = [folderpath+x for x in os.listdir(folderpath)]
            gender_list= detect_gender_and_age()

    return render_template('index.html', 
                           uploadImg_url=uploadImg_url,
                           inputindicate=inputindicate,
                           nface=nface,
                           facepaths=facepaths,
                           gender_list = gender_list)

if __name__ == '__main__':
    app.run(debug=True)