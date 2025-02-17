import os
import moviepy
from moviepy import VideoFileClip, concatenate_videoclips 
import concurrent.futures

global base_dir
base_dir = os.getcwd()

video_dir = f"{base_dir}/cropped_videos"
saving_dir = f"{base_dir}/junks"

# # Text to match
# text = "Hello i am sam"

# output_path = f"{base_dir}/junks/output.mp4"


###########################################################

def text_sign(text, output_path):
    
    import os
    import moviepy
    from moviepy import VideoFileClip, concatenate_videoclips 
    import concurrent.futures
    
    global base_dir
    base_dir = os.getcwd()

    video_dir = f"{base_dir}/cropped_videos"
    saving_dir = f"{base_dir}/junks"

    # Video file extensions
    video_extensions = (".mp4", ".avi", ".mov", ".mkv")  # Add more if needed

    # Get all video filenames (without extensions) in the directory
    videos = {os.path.splitext(f)[0]: os.path.join(video_dir, f) 
            for f in os.listdir(video_dir) if f.endswith(video_extensions)}

    # Video file extensions
    video_extensions = (".mp4", ".avi", ".mov", ".mkv")  # Add more if needed

    # Get all video filenames (without extensions) in the directory
    videos = {os.path.splitext(f)[0].lower(): os.path.splitext(f)[0]  # Store lowercase keys but keep original case
            for f in os.listdir(video_dir) if f.endswith(video_extensions)}

    # Convert labels to lowercase
    labels = [word.lower() for word in text.split()]

    # Find matching video names
    matching_video_names = [videos[word] for word in labels if word in videos]

    # Handle missing words by replacing them with letter videos
    final_results = []
    for word in labels:
        if word in videos:
            final_results.append(videos[word])  # Use full word video if available
        else:
            # Use letter-based video names if word is missing
            final_results.extend([videos[char] for char in word if char in videos])  

    # Convert single characters to uppercase for better clarity
    final_results = [word.upper() if len(word) == 1 else word for word in final_results]

    # Write to vid.txt
    list_file = os.path.join(saving_dir, "vid.txt")
    with open(list_file, "w") as f:
        for video in final_results:
            f.write(f"'{video_dir}/{video}.mp4'\n")

    # Read the file and extract full paths
    with open(list_file, "r") as f:
        video_files = [line.strip().replace("'", "").replace("\\", "/") for line in f]

    # Print the extracted full paths list
    # print(video_files)

    # Print the extracted full paths list
    # print(video_files)

    # Load videos dynamically
    video_clips = [VideoFileClip(video).without_audio() for video in video_files]

    # Concatenate videos (FASTER method)
    final_video = concatenate_videoclips(video_clips, method="chain")

    # Save output video
    final_video.write_videofile(
        output_path, 
        codec="libx264", 
        preset="ultrafast",   # Faster processing
        bitrate="500k",       # Reduce file size
        fps=20,               # Standard frame rate
        threads=3,            # Use multi-threading
    )
    
    # def load_video(video):
    #     return VideoFileClip(video).without_audio()

    # # Use multiple threads to load videos faster
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:  # Adjust workers based on CPU cores
    #     video_clips = list(executor.map(load_video, video_files))


    # # Concatenate videos (FASTER method)
    # final_video = concatenate_videoclips(video_clips, method="chain")

    # # Save output video
    # final_video.write_videofile(
    #     output_path, 
    #     codec="libx264", 
    #     preset="ultrafast",   # Faster processing
    #     bitrate="500k",       # Reduce file size
    #     fps=18,               # Standard frame rate
    #     threads=3,            # Use multi-threading
    # )

    
