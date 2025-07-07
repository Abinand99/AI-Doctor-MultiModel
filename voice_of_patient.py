# 1. setup audio Recoder
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# stt_model ='whisper-large-v3'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20 , phrase_time_limit = None): # phrse time limit - maximum time for phrase to be rocorded
    recognizer = sr.Recognizer() # process and stores
    try:
        with sr.Microphone() as source:
            logging.info("Adjesting for ambient noise..")
            recognizer.adjust_for_ambient_noise(source=source,duration= 1)
            logging.info("Start speaking now..")

            # record Audio
            audio_data = recognizer.listen(source=source,timeout= timeout,phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete")

            # convert the recorded audio to mp3 file
            wav_data =audio_data.get_wav_data()
            audio_segment= AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format ="mp3",bitrate ="128k")
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occured: {e}")




def transcribe(stt_model,audio_file_path):
    client = Groq()
    audio_file =open(audio_file_path,'rb')
    transcription = client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language='en'

    )
    return transcription.text