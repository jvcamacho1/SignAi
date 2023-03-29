import cv2
import mediapipe as mp
import os
import io
import numpy as np
from PIL import Image
import cv2

class CropHandService:
    def __init__(self, image,label,flag):
        self.image = image
        self.label = label
        self.flag = flag

    def crop_hand(self):
        img = io.BytesIO(self.image)
        img_array = np.frombuffer(img.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
        
        #if self.flag == str(1):
        #    os.chdir('C:\\Users\\jv_ca\\TCC\\backend')
        #    save_dir = '.\\ia\\collectedimages\\raw\\'+ self.label
        #    if not os.path.exists(save_dir):
        #        os.makedirs(save_dir)
        #        os.chdir(save_dir)
        #        file_name = self.label+'.'+'1'+'.jpg'
        #        img_resized = hand_image.resize((50, 50), resample=Image.LANCZOS)
        #        cv2.imwrite(file_name, img_resized)
        #        print('imagem'+file_name+'salva com sucesso')
        #    else:
        #        os.chdir(save_dir)
        #        size_folder = len([name for name in os.listdir('.') if os.path.isfile(name)])
        #        file_name = self.label+'.'+str(size_folder+1)+'.jpg'
        #        img_resized = hand_image.resize((50, 50), resample=Image.LANCZOS)
        #        cv2.imwrite(file_name, img_resized)
        #        print('imagem'+file_name+'salva com sucesso')
        #        
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_hands = mp.solutions.hands.Hands()

        results = mp_hands.process(image)

        if not results.multi_hand_landmarks:
            print(("No hands detected in the image"))
            raise Exception("No hands detected in the image")

        xmin, ymin, xmax, ymax = image.shape[1], image.shape[0], 0, 0
        for hand_idx in range(min(2, len(results.multi_hand_landmarks))):
            landmarks = results.multi_hand_landmarks[hand_idx].landmark

            x1, y1, z1 = landmarks[0].x, landmarks[0].y, landmarks[0].z
            x2, y2, z2 = landmarks[-1].x, landmarks[-1].y, landmarks[-1].z

            h, w, _ = image.shape
            x1, y1 = int(x1 * w), int(y1 * h)
            x2, y2 = int(x2 * w), int(y2 * h)

            xmin = min(xmin, x1, x2)
            ymin = min(ymin, y1, y2)
            xmax = max(xmax, x1, x2)
            ymax = max(ymax, y1, y2)

        margin = 75
        xmin = max(0, xmin - margin)
        ymin = max(0, ymin - margin)
        xmax = min(image.shape[1], xmax + margin)
        ymax = min(image.shape[0], ymax + margin)

        hand_image = image[ymin:ymax, xmin:xmax]

        hand_image = cv2.cvtColor(hand_image, cv2.COLOR_RGB2BGR)
        
        if self.flag == str(1):
            os.chdir('C:\\Users\\jv_ca\\TCC\\backend')
            save_dir = '.\\ia\\collectedimages\\cropped\\'+ self.label
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                os.chdir(save_dir)
                file_name = self.label+'.1'+'.jpg'
                img_resized = cv2.resize(hand_image, (50, 50), interpolation=cv2.INTER_LANCZOS4)
                cv2.imwrite(file_name, img_resized)
                print('imagem '+file_name+' salva com sucesso')
            else:
                os.chdir(save_dir)
                size_folder = len([name for name in os.listdir('.') if os.path.isfile(name)])
                file_name = self.label+'.'+str(size_folder+1)+'.jpg'
                img_resized = cv2.resize(hand_image, (50, 50), interpolation=cv2.INTER_LANCZOS4)
                cv2.imwrite(file_name, img_resized)
                print('imagem '+file_name+' salva com sucesso')
            return hand_image
        else:
            return hand_image