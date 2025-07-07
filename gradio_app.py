from brain_of_the_doctor import encode_image,image_query
from voice_of_patient import record_audio,transcribe
from voice_of_doctor import text_to_speech_gtts
import gradio as gr
import subprocess

stt_model ='whisper-large-v3'
model = "meta-llama/llama-4-scout-17b-16e-instruct"

system_prompt="""You have to act as a professional doctor. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_input(audio_file_path,image_file_path,stt_model=stt_model,model = model):
    speech_to_text = transcribe(stt_model=stt_model,audio_file_path=audio_file_path)
    if image_file_path:
        doctor_reponse = image_query(query=system_prompt+speech_to_text,encoded_image=encode_image(image_path=image_file_path),model=model)
    else:
        doctor_reponse = "No image Provided to Analyze"
    
    voice = text_to_speech_gtts(doctor_reponse)

    return speech_to_text,doctor_reponse, voice


iface = gr.Interface(
    fn = process_input,
    inputs=[
        gr.Audio(sources=["microphone"],type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs= [
        gr.Textbox(label="Speech to text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Doctor's Voice")
    ],
    title="AI Doctor"
)
iface.launch(debug=True)

# http://127.0.0.1:7860