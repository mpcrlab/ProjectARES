import subprocess

NUM_LOOPS = 5

for _ in range(NUM_LOOPS):
    print("Recording...")
    subprocess.call(["python", "receive_proc.py"])
    print("Recognizing...")
    subprocess.call(["python", "projectares_recognize.py"])
    subprocess.call(["ffmpeg", "-y", "-i", "response0.mp3", "response0.wav"])
    print("Responding...")
    subprocess.call(["python", "transmit_proc.py"])

print("Done!")
