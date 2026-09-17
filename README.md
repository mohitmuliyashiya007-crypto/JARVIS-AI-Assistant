# ⚡ J.A.R.V.I.S. AI Agent (Stark Industries Protocol)

An advanced **Voice-Controlled AI Assistant** built in Python with **Auto Meet**, **System Automation**, **Web Intelligence**, and a futuristic **Iron Man Stark Holographic HUD**.

---

## 🚀 Quick Start (1-Click Run)

### Option 1: Double click `run_jarvis.bat`
OR run in terminal:
```bash
python start.py
```
> This will start the JARVIS server and automatically open the **Futuristic Arc Reactor HUD** in your browser at `http://localhost:7860`.

### Option 2: Run in Terminal (CLI Mode)
```bash
python cli_jarvis.py
```

---

## 🛠️ Integrated Tools & Capabilities

### 1. 📹 Auto Meet Tool (`tools/auto_meet.py`)
- **Instant Google Meet**: Automatically launches a brand new Google Meet session.
- **Join Meeting**: Join any Google Meet via code or link.
- **Schedule Meeting**: Opens Google Calendar pre-configured with Google Meet conference.
- **Zoom Meeting**: Launches Zoom portal / app.

### 2. ⚡ System Automation Tool (`tools/system_tools.py`)
- **App Launcher**: Opens Notepad, Calculator, VS Code, WhatsApp, Chrome, MS Edge, Paint, Command Prompt, File Explorer, Task Manager, Settings, Spotify, Discord, etc.
- **Screenshots**: Automatically captures full-screen screenshots and saves them with timestamps in the `screenshots/` directory.
- **System Telemetry**: Reports battery percentage, OS info, system time, and diagnostics.
- **Audio Control**: Increases volume, decreases volume, and toggles mute.

### 3. 🌐 Web & Media Tools (`tools/web_tools.py`)
- **YouTube Music / Video**: Plays any song or video on YouTube.
- **Live Weather**: Fetches real-time temperature, condition, and humidity for any city (e.g. Delhi, Mumbai, New York).
- **Wikipedia Search**: Summarizes any topic directly from Wikipedia.
- **Google Search**: Instant searches for queries.

### 4. 🧠 AI Reasoning Brain (`tools/ai_brain.py`)
- Conversational AI in Hindi, English, and Hinglish.
- Supports Google Gemini API (optional: set `set GEMINI_API_KEY=your_key`) with built-in intelligent fallback when offline.

---

## 🗣️ Voice Commands (Hindi & English Examples)

| Task | What You Can Say ("Jo Bolu Vo Kare") |
| :--- | :--- |
| **Google Meet** | *"Google Meet start karo"*, *"Auto meet kholo"*, *"Create instant meeting"*, *"Meet join karo abc-defg-hij"* |
| **YouTube Music** | *"Play Believer on YouTube"*, *"Arijit Singh ke gaane chalao"*, *"YouTube pe trending gaana bajao"* |
| **Open Apps** | *"Notepad kholo"*, *"Open Calculator"*, *"VS Code chalu karo"*, *"WhatsApp open karo"*, *"Chrome kholo"* |
| **Screenshot** | *"Take a screenshot"*, *"Screenshot lo"*, *"Screen capture karo"* |
| **Live Weather** | *"Delhi ka mausam kaisa hai"*, *"What's the weather in Mumbai"*, *"Temperature batao"* |
| **System Info** | *"System status kya hai"*, *"Battery kitni hai"*, *"Laptop diagnostics"* |
| **Volume Control** | *"Awaz badhao"*, *"Volume up"*, *"Awaz kam karo"*, *"Mute karo"* |
| **AI Conversation** | *"Tum kaun ho?"*, *"Who is Tony Stark?"*, *"Ek joke sunao"*, *"What is Quantum Computing?"* |

---

## 🖥️ Stark Holographic HUD Features
- **Central Arc Reactor Core**: Click or press **Spacebar** to speak.
- **Real-time Audio Waveform**: Reactive animated sine wave visualizer.
- **Multilingual Support**: Supports Hindi (`hi-IN`), Indian English (`en-IN`), and Global English (`en-US`).
- **Interactive Quick Action Chips**: Instant single-click command triggers.
- **Live Activity Feed**: Real-time log of user prompts and JARVIS tool executions.
- **Voice Feedback (TTS)**: Realistic speech synthesis replying as JARVIS.
