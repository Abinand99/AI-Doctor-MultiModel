
import os
from gtts import gTTS
import subprocess
from pydub import AudioSegment
import tempfile

def text_to_speech_gtts(input_text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
        tts = gTTS(text=input_text, lang='en', slow=False)
        mp3_path = f"./Audio_file/{os.path.basename(mp3_file.name)}"
        tts.save(mp3_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
        wav_path = f"./Audio_file/{os.path.basename(wav_file.name)}"
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")

    os.remove(mp3_path)

    if os.path.getsize(wav_path) == 0:
        raise RuntimeError("Generated audio file is empty!")
    try:
        subprocess.run(['powershell','-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
    except Exception as e:
        print(f"A error occured while trying to play audio{e}")
    return wav_path

