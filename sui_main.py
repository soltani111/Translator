import os
import time
from pathlib import Path
from interface0 import run_inference

global base_dir
base_dir = Path(os.getcwd()).as_posix()  # Converts to a forward-slash path
# Define the directory containing input audio files
input0_dir = f"{base_dir}/junks"  # Folder where your input .wav files are stored
output0_dir = f"{base_dir}/results/resjunk" # Folder where output .mp4 files will be saved
checkpoint_path = f"{base_dir}/checkpoints/wav2lip_gan.pth" # Path to the model checkpoint

# Checkbox to open the popup
def lipsync(input0_dir, output0_dir, face_path):

    # face_path = st.session_state["selected_image"]

    # Ensure the output directory exists
    os.makedirs(output0_dir, exist_ok=True)

    # Set to track processed files
    processed_files = set()

    while True:
        # Get all .wav files in the directory, sorted by modification time
        audio_files = sorted(Path(input0_dir).glob("*_transvoice.mp3"), key=lambda f: f.stat().st_mtime)

        for audio_file in audio_files:
            if audio_file not in processed_files:  # Process only new files
                input_path = str(audio_file)
                output_path = os.path.join(output0_dir, f"res_{audio_file.stem}.mp4").replace("\\", "/")

                # Process the file
                run_inference(
                    checkpoint_path=checkpoint_path,
                    face_path=face_path,
                    audio_path=input_path,
                    output_path=output_path,
                    resize_factor=2,
                    fps=20,
                )

                processed_files.add(audio_file)  # Mark as processed

        # Wait 0.1 seconds before checking for new files again
        time.sleep(0.1)
