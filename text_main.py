import os
from text_sign import text_sign
from pathlib import Path
import time
import re

global base_dir
base_dir = Path(os.getcwd()).as_posix()


video_dir = f"{base_dir}/cropped_videos"
saving_dir = f"{base_dir}/junks"
input0_dir = f"{base_dir}/junks"
output0_dir = f"{base_dir}/junks"  


def text_to_sign():
    
    import os
    from text_sign import text_sign
    from pathlib import Path
    import time
    import re

    global base_dir
    base_dir = Path(os.getcwd()).as_posix()


    video_dir = f"{base_dir}/cropped_videos"
    saving_dir = f"{base_dir}/junks"
    input0_dir = f"{base_dir}/junks"
    output0_dir = f"{base_dir}/junks" 

    # Ensure the output directory exists
    os.makedirs(output0_dir, exist_ok=True)

    # Set to track processed files
    processed_files = set()

    while True:
        # Get all .txt files in the directory, sorted by modification time
        text_files = sorted(Path(input0_dir).glob("*_transcription.txt"), key=lambda f: f.stat().st_mtime)

        for text_file in text_files:
            if text_file not in processed_files:  # Process only new files
                
                with open(text_file, "r", encoding="utf-8") as f:
                    text = f.read().strip() 
                    # print(text)
                
                output_path = os.path.join(output0_dir, f"{text_file.stem}_res.mp4").replace("\\", "/")

                # Process the file
                text_sign(text, output_path)

                processed_files.add(text_file)  # Mark as processed

        # Wait 0.1 seconds before checking for new files again
        time.sleep(0.15)

