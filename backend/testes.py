from GetKnownWords import GetKnownWords
from CropHandService import CropHandService
from SignService import SignService
import cv2
import numpy as np
from PIL import Image
import io

model_path = r'C:\Users\jv_ca\TCC\backend\ia\files\a3.h5'
img = r'C:\Users\jv_ca\TCC\backend\ia\collectedimages\cropped\A\A.jpg'
with open(img, 'rb') as f:
    image_bytes = f.read()
img = io.BytesIO(image_bytes)
img_array = np.frombuffer(img.getvalue(), dtype=np.uint8)
image = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
model_service = SignService(image, model_path)
predicted_word = model_service.process_image()
print(predicted_word)