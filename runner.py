from interface0 import run_inference

# Call the function
run_inference(
    checkpoint_path='checkpoints/wav2lip_gan.pth',
    face_path='inputs/black_man.mp4',
    audio_path='inputs/input.wav',
    output_path='results/res1.mp4',
    resize_factor=2,
    fps=20,
)
