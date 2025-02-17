import streamlit as st
import threading
import queue
from pathlib import Path
from time import sleep
import time
import os
import moviepy
from moviepy import VideoFileClip, concatenate_videoclips 

# Import your functions (or paste them here directly)
from translator_test import process_audio, clear_directory, continuous_recording
from sui_main import lipsync
from asl_rec import asl_rec
from text_main import text_to_sign

record_duration = int(7)

# Shared Queue for communication
file_queue = queue.Queue()

global base_dir
base_dir = Path(os.getcwd()).as_posix()  # Converts to a forward-slash path

save_dir = f"{base_dir}/junks"
# Define the directory containing input audio files
input0_dir = f"{base_dir}/junks"  # Folder where your input .wav files are stored
output0_dir = f"{base_dir}/results/resjunk" # Folder where output .mp4 files will be saved
checkpoint_path = f"{base_dir}/checkpoints/wav2lip_gan.pth" # Path to the model checkpoint

# Language mapping
language_codes = {
    "English": "en",
    "Hebrew": "he",
    "French": "fr",
    "Italian": "it",
    "Arabic": "ar",
    "Hindi": "hi",
    "Spanish": "es",
    # Add more languages as needed
}
selections = "_"

# Define a stop event for thread management
# stop_event = threading.Event()

# App UI
def main():
    st.title("Audio Recording and Processing")
    
    global base_dir
    base_dir = os.getcwd()

    save_dir = f"{base_dir}/junks"
    # Define the directory containing input audio files
    input0_dir = f"{base_dir}/junks"  # Folder where your input .wav files are stored
    output0_dir = f"{base_dir}/results/resjunk" # Folder where output .mp4 files will be saved
    checkpoint_path = f"{base_dir}/checkpoints/wav2lip_gan.pth" # Path to the model checkpoint
    
    # Selectors
    input_language = st.selectbox("Choose an Input Language", ["English","Hebrew","French","Italian","Arabic","Hindi","Spanish"])
    output_language = st.selectbox("Choose an Output Language", ["English","Hebrew","French","Italian","Arabic","Hindi","Spanish"])
        
    input_language = language_codes[input_language]
    output_language = language_codes[output_language]

    subtitle = st.checkbox("Translation")
    lip_sync = st.checkbox("Lip Sync")
    sign_language = st.checkbox("Sign Language Detection")
    textsign = st.checkbox("Sign Language Avatar")
    
    ###
    if lip_sync:
        st.subheader("Select an Avatar")
        col1, col2, col3, col4 = st.columns(4)

        # Image URLs or file paths
        black_man = f"{base_dir}/inputs/picvatar/Black_man_enhanced.png"
        black_woman = f"{base_dir}/inputs/picvatar/Black_woman_enhanced.png"
        white_man = f"{base_dir}/inputs/picvatar/White_man_enhanced.png"
        white_woman = f"{base_dir}/inputs/picvatar/White_woman_enhanced.png"
        
        # Ensure session state exists
        if "selected_image" not in st.session_state:
            st.session_state["selected_image"] = None

        # Selection options
        with col1:
            if st.button("black_man"):
                st.session_state["selected_image"] = black_man
            st.image(black_man, caption="Black Man", width=200)
        with col2:
            if st.button("black_woman"):
                st.session_state["selected_image"] = black_woman
            st.image(black_woman, caption="Black Woman", width=200)
        with col3:
            if st.button("white_man"):
                st.session_state["selected_image"] = white_man
            st.image(white_man, caption="White Man", width=200)
        with col4:
            if st.button("white_woman"):
                st.session_state["selected_image"] = white_woman
            st.image(white_woman, caption="White Woman", width=200)
        
    # Start and stop buttons
    if st.button("Start Recording"):
        if not Path(save_dir).exists():
            st.warning("Creating save directory.")
            Path(save_dir).mkdir(parents=True, exist_ok=True)

        # st.write("Starting continuous recording...")
        clear_directory(save_dir)
        clear_directory(output0_dir)
        
        # Start threads
        if subtitle:
            print("True")
            processing_thread = threading.Thread(target=process_audio, args=(input_language, output_language, subtitle, sign_language), daemon=True)
            recording_thread = threading.Thread(target=continuous_recording,args=(record_duration, save_dir), daemon=True)
            processing_thread.start()
            recording_thread.start()

        if lip_sync and "selected_image" in st.session_state and st.session_state["selected_image"]:
            lipsync_thread = threading.Thread(target=lipsync, args=(input0_dir, output0_dir, st.session_state["selected_image"]), daemon=True)
            lipsync_thread.start()

        if sign_language:
            asl_rec_thread = threading.Thread(target=asl_rec, args=(), daemon=True)
            asl_rec_thread.start()
            
        if textsign:
            textsign_thread = threading.Thread(target=text_to_sign, args=(), daemon=True)
            textsign_thread.start()
        
        st.session_state["recording"] = True

    if st.button("Stop Recording"):
        os._exit(0)
        # stop_event.set()  # Signal all threads to stop
        # file_queue.put(None)  # Signal processing thread to exit
        # st.write("Stopped recording and processing.")
        st.session_state["recording"] = False
        
    # Continuously check for updates
    placeholder = st.empty()
    while "recording" in st.session_state and st.session_state["recording"]:
        
        # transcription_files = sorted(Path(save_dir).glob("*_transcription.txt"))
        # translatext_files = sorted(Path(save_dir).glob("*_translation.txt"))
        transcription_files = sorted(Path(save_dir).glob("*_transcription.txt"), key=lambda x: x.stat().st_mtime)
        translatext_files = sorted(Path(save_dir).glob("*_translation.txt"), key=lambda x: x.stat().st_mtime)
        audio_files = sorted(Path(save_dir).glob("*_transvoice.mp3"), key=lambda f: f.stat().st_mtime)
        lipsync_files = sorted(Path(output0_dir).glob("*.mp4"), key=lambda f: f.stat().st_mtime)
        
        sign_files = sorted(Path(save_dir).glob("*res.mp4"), key=lambda f: f.stat().st_mtime)

        with placeholder.container():
            # Display subtitles
            if subtitle and transcription_files:
                st.subheader("Text Transcriptions")
                lastwo_transcipt = transcription_files[-2:]  # Slicing to get the last two files
                for file in lastwo_transcipt:
                    with open(file, "r", encoding="utf-8") as f:
                        # st.text(f.read())
                        st.markdown(f"```\n{f.read()}\n```")
                        
            # Display subtitles
            if subtitle and translatext_files:
                st.subheader("Text Translations")
                lastwo_translit = translatext_files[-2:]  # Slicing to get the last two files
                for file in lastwo_translit:
                    with open(file, "r", encoding="utf-8") as f:
                        # st.text(f.read())
                        st.markdown(f"```\n{f.read()}\n```")

            # Display the last audio file
            if audio_files and audio_files:
                last_audio_file = audio_files[-1]
                st.subheader("Last Processed Audio")
                with open(last_audio_file, "rb") as f:
                    audio_data = f.read()
                    st.audio(audio_data, format="audio/mp3")
                    
            # Display the last processed video file
            if lipsync_files and lipsync_files:
                last_lipsync_file = lipsync_files[-1]
                video_file = open(last_lipsync_file, "rb")
                video_file = video_file.read()
                st.video(video_file)
                
            if sign_language:
                detected_text_file = f"{base_dir}/detected_letters.txt"  # Path to detected letters file
                if os.path.exists(detected_text_file):
                    with open(detected_text_file, "r", encoding="utf-8") as f:
                        detected_text = f.read().strip()  # Read detected letters
                    # Display detected text
                    if detected_text:
                        st.markdown(f"**Detected Text:** `{detected_text}`")
                
            if textsign and sign_files:  # Check if textsign is True and sign_files is not empty
                last_sign_file = sign_files[-1]  # Get the last file in the list
                with open(last_sign_file, "rb") as sign_video:  # Open the video file safely
                    sign_video_data = sign_video.read()
                    st.video(sign_video_data)
                                            

        time.sleep(0.15)  # Check for updates every second

if __name__ == "__main__":
    main()
