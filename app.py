import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import numpy as np
from matplotlib.patches import Rectangle
from keras.models import load_model

NeuralNetwork = load_model('PneuClass(90%).h5')
img_size = 150
  

def predict(name):
    image = st.file_uploader("Загрузите фотографию " + name, type=["png", "jpg", "jpeg"], )
    if image:
        st.image(image=image)
        im = Image.open(image)
        im.filename = image.name
        SamplePhoto = np.asarray(im)
        resized_arr = cv2.resize(SamplePhoto, (img_size, img_size))

        data = []
        data.append([resized_arr, 0])
        data = np.array(data, dtype = object)
        SamplePhotoXTrain = []
        SamplePhotoYTrain = []
        for feature, label in data:
            SamplePhotoXTrain.append(np.array(feature))
            SamplePhotoYTrain.append(np.array(label))

        SamplePhotoXTrain = np.array(SamplePhotoXTrain) / 255
        SamplePhotoXTrain = SamplePhotoXTrain.reshape(-1, img_size, img_size, 1)
        Prediction = NeuralNetwork.predict(SamplePhotoXTrain)
        FloatNumber = (1.0 - Prediction[0][0]) * 100
        ANS = str("%.2f" % FloatNumber)
        # ANS = str("%.2f" % (1.0 - Prediction[0][0], 3) * 100)   
        if FloatNumber > 60:
          st.markdown("<h4 style='text-align: center; color: white;'>Обнаружены признаки пневмонии.</h4>", unsafe_allow_html=True)
          st.markdown(f"<h5 style='text-align: center; color: white;'>Вероятность наличия составляет {ANS}%</h5>", unsafe_allow_html=True)
        else:
          st.markdown("<h4 style='text-align: center; color: white;'>Признаков заболевания не обнаружено.</h4>", unsafe_allow_html=True)
          st.markdown(f"<h5 style='text-align: center; color: white;'>Вероятность наличия составляет {ANS}%</h5>", unsafe_allow_html=True)
      
        

def main():
  st.markdown("<h2 style='text-align: center; color: white;'>Модель машинного обучения для диагностирования бактериальной и вирусной пневмонии</h2>", unsafe_allow_html=True)
  st.image('https://th.bing.com/th/id/OIG.N.VeSzaC2cX.4Lmg.8Rm?w=1024&h=1024&rs=1&pid=ImgDetMain', caption='“Здоровье до того перевешивает все остальные блага жизни, что поистине здоровый нищий счастливее больного короля. —Артур Шопенгауэр”', use_column_width=True)
  st.markdown("<h3 style='text-align: center; color: white;'>Как работает модель?</h3>", unsafe_allow_html=True)
  st.markdown("<h6 style='text-align: center; color: white;'>Пользователь должен ввести в качестве входных данных снимок рентгена (на практике - dicom-файл), программа обрабатывает полученную фотографию и выводит результат в виде диагноза: положительный диагноз либо отрицательный.</h6>", unsafe_allow_html=True)
  st.markdown("<h6 style='text-align: center; color: white;'>Загрузите фотографию, чтобы передать её модели искусственного интеллекта</h6>", unsafe_allow_html=True)
  # Отображение изображений в две колонки
  col1, col2 = st.columns(2)
  col1.image('Healthy.jpg', caption='Снимок грудной клетки здорового пациента')
  col2.image('Pneumonia.jpeg', caption='Снимок грудной клетки, пораженной болезнью')
  st.markdown("<h5 style='text-align: center; color: white;'>Загрузите снимок</h5>", unsafe_allow_html=True)
  predict('image')  # Передаем имя загруженного файла  

if __name__ == "__main__":
  main()
