from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import librosa
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import soundfile
import tensorflow as tf
from PIL import Image
from pathlib import Path

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_MEDIA_DIR = PROJECT_ROOT / "frontend" / "media"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
MODELS_PATH = PROJECT_ROOT / "models" / "model_9982.h5"


app.mount("/media", StaticFiles(directory=str(FRONTEND_MEDIA_DIR)), name="media")
app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

labels = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise", "surprised"]
model = tf.keras.models.load_model(str(MODELS_PATH))

def audio_to_spectrogram(bytes_file):
  
  audio_data, sample_rate = soundfile.read(bytes_file)
  print("Audio shape:", audio_data.shape)
  print("Sample rate:", sample_rate)

  if audio_data.ndim > 1:
    audio_data = librosa.to_mono(audio_data.T)

  Spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128, fmax=8000)

  Spectrogram_dB = librosa.power_to_db(Spectrogram, ref=np.max)

  plt.figure(figsize=(12, 12))
  librosa.display.specshow(Spectrogram_dB, sr=sample_rate,fmax=8000,cmap="magma")

  buf = BytesIO()
  plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
  buf.seek(0)
  plt.close()

  return buf


@app.get("/")
def home():
    return({"message":"for docs visit /docs route"})


@app.post("/predict")
async def predict(uploaded_file: UploadFile):
    try:
        audio_bytes = await uploaded_file.read()
        audio_file = BytesIO(audio_bytes)
        img_buf = audio_to_spectrogram(audio_file)

        img = Image.open(img_buf).convert("RGB")
        img_resized = img.resize((224,224))
        np_img = np.array(img_resized)/255.0
        np_img = np_img.reshape((1,224,224,3))

        output = model.predict(np_img)
        pred_index = int(np.argmax(output))
        prediction = labels[pred_index]

        return JSONResponse({
            "prediction": prediction,
            "probabilities": output.tolist()
        })

    except Exception as e:
        return JSONResponse({"error": str(e)})