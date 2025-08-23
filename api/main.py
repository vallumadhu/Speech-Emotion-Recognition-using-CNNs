from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import librosa
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import soundfile
import tensorflow as tf
from PIL import Image

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model("../models/model_9982.h5")

def audio_to_spectrogram(bytes_file):
  
  audio_data, sample_rate = soundfile.read(bytes_file)

  Spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128, fmax=8000)

  Spectrogram_dB = librosa.power_to_db(Spectrogram, ref=np.max)

  plt.figure(figsize=(12, 12))
  librosa.display.specshow(Spectrogram_dB, sr=sample_rate,fmax=8000,cmap="magma")

  buf = BytesIO()

  plt.savefig(buf, format="png")

  buf.seek(0)

  plt.close()

  return buf



@app.get("/")
def home():
    return({"message":"for docs visit /docs route"})


@app.post("/predict")
async def predict(uploaded_file:UploadFile):

    audio = await uploaded_file.read()

    audio = BytesIO(audio)

    img_buf = audio_to_spectrogram(audio)

    img = Image.open(img_buf).convert("RGB")
    resized_img = img.resize((224,224))
    np_img = np.array(resized_img)/255.0
    np_img.reshape((1,224,224,3))
    

    output = model.predict(np_img)

    return StreamingResponse(img, media_type="image/png")

