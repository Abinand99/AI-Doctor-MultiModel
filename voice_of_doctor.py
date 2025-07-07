
import os
from gtts import gTTS
import subprocess
from playsound import playsound
from pydub import AudioSegment
import tempfile

def text_to_speech_gtts(input_text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
        tts = gTTS(text=input_text, lang='en', slow=False)
        tts.save(f"./Audio_file/{mp3_file.name}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
        sound = AudioSegment.from_mp3(mp3_file.name)
        sound.export(".Audio_file/{wav_file.name}", format="wav")
        wav_path = wav_file.name

    os.remove(f"./Audio_file/{mp3_file.name}")

    if os.path.getsize(wav_path) == 0:
        raise RuntimeError("Generated audio file is empty!")
    try:
        subprocess.run(['powershell','-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
    except Exception as e:
        print(f"A error occured while trying to play audio{e}")
    return wav_path

