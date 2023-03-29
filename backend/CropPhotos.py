from CropHandService import CropHandService
import os
from PIL import Image

raw = r'C:\Users\jv_ca\TCC\backend\ia\collectedimages\raw'



for folder in os.listdir(raw):
    sub_folder = os.path.join(raw,folder)
    for image in os.listdir(sub_folder):
        image_file = os.path.join(sub_folder, image)
        with open(image_file, 'rb') as f:
            image_bytes = f.read()
        crop_service = CropHandService(image_bytes, image.split('.')[0], '1')
        try:
            c = crop_service.crop_hand()
        except :
            continue
