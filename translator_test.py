import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time
from pathlib import Path
from openai import OpenAI
import re
import time
import threading
import queue
import os
import streamlit as st

key = "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"

client = OpenAI(api_key=key)

# Initialize a queue to hold filenames for processing
file_queue = queue.Queue()
stop_flag = False

def record(duration, output_path):
    """
    Records audio for a given duration and saves it to the specified path.
    """
    time_in_seconds = int(duration)
    sample_rate = 16000  # Hz

    # Record audio
    audio_data = sd.rec(int(time_in_seconds * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is complete

    # Save audio to specified path
    write(output_path, sample_rate, audio_data)
    
    

# def continuous_recording(record_duration, save_dir):
#     global counter
#     """
#     Continuously records audio and enqueues filenames for processing.
#     """
#     save_dir = Path(save_dir)
#     save_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

#     counter = 0  # Initialize counter for filenames
#     while True:
#         output_path = save_dir / f"input{counter}.wav"  # Incremental filename
#         # print(f"Recording audio: {output_path}")

#         # Record and save audio
#         record(record_duration, str(output_path))
        
#         # Enqueue the file path for processing
#         file_queue.put(str(output_path))
#         # print(f"Saved and enqueued: {output_path}")

#         counter += 1  # Increment counter for the next recording

def clean_saved_files(directory, max_files, remove_count):
    
    directory = Path(directory)
    if not directory.exists():
        print(f"Directory {directory} does not exist.")
        return

    # Get only files, excluding directories
    files = [f for f in directory.iterdir() if f.is_file()]

    # Sort files by modification time (oldest first)
    files = sorted(files, key=lambda f: f.stat().st_mtime)

    # If the number of files exceeds the limit, remove the oldest files
    if len(files) > max_files:
        files_to_remove = files[:remove_count]
        for file in files_to_remove:
            try:
                file.unlink()  # Remove the file
                # print(f"Removed file: {file}")
            except Exception as e:
                print(f"Error removing file {file}: {e}")
                
def clear_directory(directory):
    
    directory = Path(directory)
    if not directory.exists():
        print(f"Directory {directory} does not exist. Creating it.")
        directory.mkdir(parents=True, exist_ok=True)
        return

    # Remove all files in the directory
    for file in directory.iterdir():
        if file.is_file():  # Ensure only files are deleted
            try:
                file.unlink()
                # print(f"Deleted file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

def speech_to_speech(file_path, input_language, output_language, gen_sub, sign_):
    """
    Process a single audio file: transcribe, translate, and save results.
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Speech-to-Text
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=input_language
            )

        transcriptxt = transcription.text

        # Text-to-Text Translation
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a translation assistant."},
                {"role": "user", "content": f"Translate the following text into {output_language}: {transcriptxt}"}
            ]
        )

        translated_text = response.choices[0].message.content
        match = re.search(r'\"(.*?)\"', translated_text)
        translatext = match.group(1) if match else translated_text
        
        # Text to Speech
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=translatext,
        )

        # Generate output file paths
        transcript_output_path = file_path.parent / f"{file_path.stem}_transcription.txt"
        translation_output_path = file_path.parent / f"{file_path.stem}_translation.txt"
        transvoice_output_path = file_path.parent / f"{file_path.stem}_transvoice.mp3"

        # Save transcription
        with open(transcript_output_path, "w", encoding="utf-8") as file:
            file.write(transcriptxt)

        # Save translated text
        with open(translation_output_path, "w", encoding="utf-8") as file:
            file.write(translatext)

        response.stream_to_file(transvoice_output_path)
        
        # print(transcriptxt)
        # print(f"Processing completed for {file_path}. Transcription saved to: {transcript_output_path}")
        # print(f"Translation saved to: {translation_output_path}")
        
        return transcriptxt, translatext

    except Exception as e:
        print(f"Error in speech_to_speech: {e}")
        return None, None

def process_audio(input_language, output_language, gen_sub, sign_):
    
    while True:
        file_path = file_queue.get()
        if file_path is None:  # Exit signal
            break

        # print(f"Processing audio file: {file_path}")
        speech_to_speech(
            file_path=file_path,
            input_language=input_language,
            output_language=output_language,
            gen_sub=gen_sub,
            sign_=sign_
        )
        file_queue.task_done()

def continuous_recording(record_duration, save_dir):
    
    global counter
    counter = 0
    
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    clear_directory(save_dir)

    while True:
        output_path = save_dir / f"input{counter}.wav"
        # print(f"Recording audio: {output_path}")
        record(record_duration, str(output_path))
        file_queue.put(output_path)
        counter += 1

        # Clean up the directory if the file limit is reached
        clean_saved_files(save_dir, max_files=90, remove_count=10)
        

############ Run #############

# # Start recording and processing threads
# try:
#     # Start the processing thread
#     processing_thread = threading.Thread(target=process_audio, daemon=True)
#     processing_thread.start()
    
#     # Start the continuous recording
#     continuous_recording(record_duration=5, save_dir="D:/Work/Stramlit/junks")
# except KeyboardInterrupt:
#     print("Stopping recording and processing.")
#     file_queue.put(None)  # Signal processing thread to exit
#     processing_thread.join()

##############################




        
    