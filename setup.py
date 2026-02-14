import os
import sys
import subprocess
import json
import urllib.request
import zipfile
import shutil

print("--- AI Dubbing Studio (Cloud Edition) Setup ---\n")

# 1. Install LIGHTWEIGHT Python Packages
# Removed: torch, kokoro, openai-whisper (These run on Cloud now)
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
                # Find the bin/ffmpeg.exe in the zip
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

# 3. Setup Project Directories
print("\n--- Project Configuration ---")
default_path = os.getcwd()
print(f"Current folder: {default_path}")

use_current = input("Use current folder for videos? (y/n): ").lower().strip()
if use_current == 'y':
    base_dir = default_path
else:
    base_dir = input(r"Enter the full path to your video folder: ").strip()

# Create required subfolders
folders = ["captions", "subtitles", "exports", "audio", "bgm"]
for folder in folders:
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
    print(f"Checked/Created: {path}")

# 4. Rename Videos (ADDED BACK)
print("\nRenaming videos sequentially...")
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

# 5. Generate Blank Scripts (INCREASED TO 100)
print("\nGenerating blank script files (1-100)...")
captions_dir = os.path.join(base_dir, "captions")
for i in range(1, 101):
    f_path = os.path.join(captions_dir, f"{i}.txt")
    if not os.path.exists(f_path):
        open(f_path, 'a').close()

# 6. Save Configuration
config_data = {"base_dir": base_dir}
with open("config.json", "w") as f:
    json.dump(config_data, f)
print(f"\nSaved config.json pointing to: {base_dir}")

print("\n✅ Setup Complete!")
print("Run the app with: streamlit run app.py")
