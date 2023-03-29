import cv2
import os
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from GetKnownWords import GetKnownWords

class SignService:

    def __init__(self, image_path, model_path):
        self.image = image_path
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        return tf.keras.models.load_model(model_path)
    
    def preprocess_image(self, image):
        resized_image = cv2.resize(image, (100, 100))
        img_array = np.reshape(resized_image,(1,resized_image.shape[0],resized_image.shape[1],3))
        return img_array

    def process_image(self):
        known_words = GetKnownWords()
        preprocessed_image = self.preprocess_image(self.image)
        prediction = self.model.predict(preprocessed_image)
        dict_palavras_conhecidas = known_words.get_dict()
        label = dict_palavras_conhecidas[str(np.argmax(prediction))]
        return label