# 🎬 AI Dubbing Studio (Cloud Edition)

A professional, automated workflow manager for dubbing videos. This application uses a **Client-Server architecture** to offload heavy AI processing (Speech Generation & Subtitles) to **Google Colab**, while your local machine handles the UI and final video rendering.

**Key Features:**
* **Zero Local RAM Usage:** Heavy AI models (Kokoro-TTS & Whisper) run on Google's free T4 GPUs.
* **Smart Speed Matching:** Automatically calculates the exact speech speed to match your video's duration.
* **Background Music:** Mixes BGM at 25% volume with auto-trimming.
* **Auto-Subtitles:** Generates frame-perfect `.srt` files.
* **Local Rendering:** Uses FFmpeg locally to merge everything without uploading massive video files.

---

## 🛠️ Architecture

* **Client (Local PC):** Runs the Streamlit Dashboard, Video Player, and FFmpeg Renderer.
* **Server (Google Colab):** Runs Kokoro-TTS (Speech) and OpenAI Whisper (Subtitles).
* **Bridge (Ngrok):** Securely tunnels requests between your PC and Colab.

---

## 🚀 Installation & Setup

### 1. Cloud Server Setup (Google Colab)
1.  Open the provided `google-colab.ipynb` file in [Google Colab](https://colab.research.google.com/).
2.  **Important:** Go to **Runtime > Change runtime type** and select **T4 GPU**.
3.  Get a free Ngrok Authtoken from [dashboard.ngrok.com](https://dashboard.ngrok.com).
4.  Paste your token into the script where it says `YOUR_NGROK_TOKEN_HERE`.
5.  Run the cell. Copy the **public URL** (e.g., `https://xxxx.ngrok-free.app`).

### 2. Local Client Setup (Your PC)

**Prerequisites:**
* Python 3.9+
* [FFmpeg](https://ffmpeg.org/download.html) (The setup script will try to install this for you).

**Installation:**
1.  Clone this repository.
2.  Run the setup script to create folders and install dependencies:
    ```bash
    python setup.py
    ```

---

## 💻 How to Run

1.  **Start the Local App:**
    ```bash
    streamlit run app.py
    ```
2.  **Connect:** Paste the **Ngrok URL** (from Colab) into the sidebar or the "Generate Speech" section.
3.  **Select Video:** Choose your video file (e.g., `1` for `1.mp4`).
4.  **Write Script:** Enter your translation. **Set the "Target Duration"** to match your video length (e.g., 31.0s).
5.  **Generate Speech:** Click **"Generate Speech (Cloud)"**. The audio is created on Colab and downloaded to your `audio/` folder.
6.  **Generate Subtitles:** Click **"Generate SRT (Cloud)"**. Colab transcribes the audio and sends back the `.srt` file.
7.  **Final Render:** Click **"Render Final Video"**. This runs locally to merge Video + Audio + Subs + BGM.

---

## Screenshots
<img width="1917" height="956" alt="image" src="https://github.com/user-attachments/assets/f3c7983f-541f-4ccc-b784-e9eba6e58a9f" />
<img width="1918" height="243" alt="image" src="https://github.com/user-attachments/assets/2c69c652-ebe8-4c9c-8d2d-6eabc1c20098" />
<img width="1288" height="842" alt="image" src="https://github.com/user-attachments/assets/258b3be4-96c6-46aa-8d22-cfd2a2474b9a" />


https://github.com/user-attachments/assets/2e73409b-a701-48cc-a19d-a93294e3804c

---

## 📂 Project Structure

```text
/
├── app.py                # The main Streamlit Dashboard (Client)
├── google-colab.ipynb    # The AI Server code (Run this on Colab)
├── setup.py              # Automated installation script
├── config.json           # Created by setup.py (stores paths)
├── /captions/            # Stores your text scripts
├── /audio/               # Stores generated .wav files
├── /subtitles/           # Stores generated .srt files
├── /bgm/                 # Place background music here (optional)
└── /exports/             # Final rendered videos appear here
