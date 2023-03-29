from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware
import random
from GetKnownWords import GetKnownWords
from CropHandService import CropHandService
from SignService import SignService
import traceback
model_path = '.\\ia\\files\\SignAi.h5'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/palavras-conhecidas-ai')
async def PalavrasConhecidas():
    try:
        translator = Translator()
        resposta_api = open('.\\ia\\PalavrasConhecidas\\palavras_conhecidas_pela_ai.txt','r').read().split(';')[0:-1]
        resposta_api = [translator.translate(i,src='pt',dest='en').text for i in resposta_api]
        return resposta_api
    except Exception as e:
        raise HTTPException(status_code=500, detail='Erro ao buscar o arquivo: {}'.format(str(e)))

@app.get('/palavra-aleatoria')
async def PalavraAleatoria():
    try:
        translator = Translator()
        PalavraAleatoria = random.choice(open('.\\ia\\PalavrasConhecidas\\palavras_conhecidas_pela_ai.txt','r').read().split(';')[0:-1])
        resposta_api = {'Palavra em portugues':PalavraAleatoria,
                        'Palavra em ingles':translator.translate(PalavraAleatoria,src='pt',dest='en').text
                        }
        return resposta_api
    except Exception as e:
        raise HTTPException(status_code=500, detail='Erro ao buscar o arquivo: {}'.format(str(e)))

@app.post("/Sign-Verify/")
async def SignVerify(file: bytes = File(...), label: str = Form(...), flag: str = Form(True)):
    try:
        crop = CropHandService(file,label,flag)
        model_service = SignService(crop.crop_hand(), 'C:\\Users\\jv_ca\\TCC\\backend\\ia\\files\\SignAi.h5')
        predicted_word = model_service.process_image()
        return {"status": "success", "message": predicted_word}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")


#testing
#crop = CropHandService('C:\\Users\jv_ca\\TCC\RealTimeObjectDetection\\Tensorflow\\workspace\\images\\test\\Casa.13.jpg', 'Casa', '1')
#cropped_image = crop.crop_hand()
