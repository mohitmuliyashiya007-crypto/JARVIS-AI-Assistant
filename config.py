"""
Configuration settings for JARVIS AI Agent
"""
import os
from pathlib import Path

# Assistant & User Identity
ASSISTANT_NAME = "Jarvis"
USER_NAME = "Mohit"
WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis", "hello jarvis", "sun jarvis", "namaste jarvis"]

# Voice Settings
VOICE_RATE = 185       # Speed of speech (words per minute)
VOICE_VOLUME = 1.0     # Volume level (0.0 to 1.0)
VOICE_GENDER = "male"  # Preferred voice ("male" or "female")
LANGUAGE_CODE = "en-IN" # Speech recognition language ('en-IN', 'hi-IN', 'en-US')

# AI API Configuration (Optional: can set GEMINI_API_KEY environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Workspace Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
NOTES_DIR = BASE_DIR / "notes"

# Ensure essential directories exist
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
NOTES_DIR.mkdir(parents=True, exist_ok=True)

# Common Windows Applications Map
WINDOWS_APPS = {
    "chrome": "start chrome",
    "google chrome": "start chrome",
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "vs code": "code",
    "vscode": "code",
    "code": "code",
    "file explorer": "explorer",
    "explorer": "explorer",
    "files": "explorer",
    "cmd": "start cmd",
    "command prompt": "start cmd",
    "terminal": "start wt",
    "powershell": "start powershell",
    "task manager": "taskmgr",
    "taskmgr": "taskmgr",
    "settings": "start ms-settings:",
    "paint": "mspaint",
    "camera": "start microsoft.windows.camera:",
    "spotify": "start spotify:",
    "whatsapp": "start whatsapp:",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "edge": "start msedge",
    "microsoft edge": "start msedge"
}

# Common Websites
POPULAR_WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "x": "https://www.x.com",
    "chatgpt": "https://chat.openai.com",
    "linkedin": "https://www.linkedin.com",
    "netflix": "https://www.netflix.com",
    "whatsapp web": "https://web.whatsapp.com",
    "reddit": "https://www.reddit.com",
    "wikipedia": "https://www.wikipedia.org"
}
