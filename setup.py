import os
import sys
import subprocess
import json
import urllib.request
import zipfile
import shutil

print("--- AI Dubbing Studio (Cloud Edition) Setup ---\n")

# 1. Install LIGHTWEIGHT Python Packages
print("Installing Client dependencies...")
dependencies = ["streamlit", "requests", "soundfile", "numpy", "watchdog"] 
subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)

# 2. Check for FFmpeg (Required for local rendering)
print("\nChecking for FFmpeg...")
ffmpeg_exe = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"

if sys.platform == "win32":
    if not os.path.exists(ffmpeg_exe) and not shutil.which("ffmpeg"):
        print("Downloading FFmpeg for Windows...")
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        zip_name = "ffmpeg.zip"
        
        try:
            urllib.request.urlretrieve(url, zip_name)
            print("Extracting...")
            with zipfile.ZipFile(zip_name, 'r') as z:
                for file in z.namelist():
                    if file.endswith("ffmpeg.exe"):
                        with z.open(file) as zf, open("ffmpeg.exe", 'wb') as f:
                            shutil.copyfileobj(zf, f)
                        break
            os.remove(zip_name)
            print("✅ FFmpeg installed successfully.")
        except Exception as e:
            print(f"❌ Failed to download FFmpeg: {e}")
            print("Please download it manually from ffmpeg.org")
    else:
        print("✅ FFmpeg found.")

elif sys.platform == "darwin":
    if not shutil.which("ffmpeg"):
        print("Attempting to install FFmpeg via Brew...")
        subprocess.run(["brew", "install", "ffmpeg"])

elif sys.platform == "linux":
    if not shutil.which("ffmpeg"):
        print("Attempting to install FFmpeg via Apt...")
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"])

# 3. Setup Project Directories (HARDCODED TO 'video' FOLDER)
print("\n--- Project Configuration ---")
project_root = os.getcwd()
video_dir = os.path.join(project_root, "video")

print(f"Project Root: {project_root}")
print(f"Target Video Directory: {video_dir}")

# Ensure the 'video' folder exists
if not os.path.exists(video_dir):
    os.makedirs(video_dir)
    print(f"✅ Created missing 'video' folder at: {video_dir}")
    print("⚠️  REMINDER: Please move your .mp4 files into this 'video' folder before continuing!")
else:
    print(f"✅ Found 'video' folder.")

# We set base_dir to the 'video' folder so app.py finds the mp4s there
base_dir = video_dir 

# Create required subfolders INSIDE the video folder
# This keeps everything together: /video/captions, /video/audio, etc.
folders = ["captions", "subtitles", "exports", "audio", "bgm"]
for folder in folders:
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
    print(f"Checked/Created: {path}")

# 4. Rename Videos
print("\nRenaming videos in 'video' folder sequentially...")
# Check if dir is empty
if len(os.listdir(base_dir)) == 0:
    print("⚠️  No files found in 'video' folder. Skipping rename.")
else:
    existing_mp4s = [f for f in os.listdir(base_dir) if f.lower().endswith(".mp4")]

    highest_num = 0
    for f in existing_mp4s:
        name = os.path.splitext(f)[0]
        if name.isdigit():
            highest_num = max(highest_num, int(name))

    to_rename = [f for f in existing_mp4s if not os.path.splitext(f)[0].isdigit()]

    current_index = highest_num + 1
    for video in to_rename:
        old_path = os.path.join(base_dir, video)
        new_path = os.path.join(base_dir, f"{current_index}.mp4")
        os.rename(old_path, new_path)
        print(f"Renamed: {video} -> {current_index}.mp4")
        current_index += 1

# 5. Generate Blank Scripts (1-100)
print("\nGenerating blank script files (1-100)...")
captions_dir = os.path.join(base_dir, "captions")
for i in range(1, 101):
    f_path = os.path.join(captions_dir, f"{i}.txt")
    if not os.path.exists(f_path):
        open(f_path, 'a').close()

# 6. Save Configuration
# This tells app.py to look inside the 'video' folder for everything
config_data = {"base_dir": base_dir}
with open("config.json", "w") as f:
    json.dump(config_data, f)
print(f"\nSaved config.json pointing to: {base_dir}")

print("\n✅ Setup Complete!")
print("Make sure your .mp4 files are in the 'video' folder.")
print("Run the app with: streamlit run app.py")
