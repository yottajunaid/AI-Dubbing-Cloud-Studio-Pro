import os
import sys
import subprocess
import json
import urllib.request
import zipfile
import shutil

print("--- AI Dubbing Studio (Cloud Edition) Setup ---\n")

# 1. Install LIGHTWEIGHT Python Packages
# Removed: torch, kokoro, openai-whisper (These now run on Cloud)
print("Installing Client dependencies...")
dependencies = ["streamlit", "requests", "soundfile", "numpy", "watchdog"] 
subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)

# 2. Check for FFmpeg (Still needed for local rendering)
print("\nChecking for FFmpeg (Required for rendering)...")
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
    print(f"Created: {path}")

# 4. Save Configuration
config_data = {"base_dir": base_dir}
with open("config.json", "w") as f:
    json.dump(config_data, f)
print(f"\nSaved config.json pointing to: {base_dir}")

# 5. Generate Blank Scripts (Optional helper)
print("\nGenerating blank script files (1-10)...")
for i in range(1, 11):
    f_path = os.path.join(base_dir, "captions", f"{i}.txt")
    if not os.path.exists(f_path):
        open(f_path, 'a').close()

print("\n✅ Setup Complete!")
print("Run the app with: streamlit run app.py")