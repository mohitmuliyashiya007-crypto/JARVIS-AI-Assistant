"""
AI Brain & Intent Processor for JARVIS:
- Parses spoken or typed commands in Hindi, English, and Hinglish.
- Dispatches tool actions to PCController and WebTools.
- Supports Google Gemini API for free-form intelligent conversations and reasoning.
"""
import re
import os
import random
from typing import Dict, Any, Tuple
from jarvis.config import USER_NAME, ASSISTANT_NAME, GEMINI_API_KEY
from jarvis.pc_controller import PCController
from jarvis.web_tools import WebTools

# Optional Gemini API SDK
_gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[AIBrain] Gemini API init note: {e}")


class AIBrain:
    def __init__(self, pc_controller: PCController, web_tools: WebTools):
        self.pc = pc_controller
        self.web = web_tools
        self.user_name = USER_NAME
        self.assistant_name = ASSISTANT_NAME

    def process_command(self, query: str) -> Tuple[str, str]:
        """
        Interprets the query and executes corresponding PC or Web tool, or answers conversationally.
        Returns: (response_text, action_type)
        """
        if not query or not query.strip():
            return "", "NONE"

        orig_q = query.lower().strip()

        # Remove assistant wake names from query start/end
        q = re.sub(r'^(jarvis|hey jarvis|ok jarvis|hello jarvis|sun jarvis|namaste jarvis)\s*', '', orig_q).strip()
        q = re.sub(r'\s*(jarvis|bhai|yaar)$', '', q).strip()

        # If query only consisted of wake word or simple greeting
        is_pure_greeting = not q or q in ["hello", "hi", "hey", "namaste", "kem cho", "suno", "wake up", "hello jarvis", "hey jarvis"]
        if is_pure_greeting:
            if any(term in orig_q for term in ["who are you", "kaun ho", "tumhara naam", "what is your name"]):
                return (
                    f"I am {self.assistant_name}, your personal AI desktop agent. "
                    f"I can control your PC, launch applications, play videos, automate tasks, and assist you with anything."
                ), "INFO"
            
            responses = [
                f"Hello {self.user_name}! How can I assist you with your computer today?",
                f"Yes {self.user_name}, I am online and listening. What would you like me to do?",
                f"Namaste {self.user_name}! All systems are operational. Tell me your command."
            ]
            return random.choice(responses), "GREETING"


        if "who are you" in q or "kaun ho" in q or "tumhara naam" in q or "what is your name" in q:
            return (
                f"I am {self.assistant_name}, your personal AI desktop agent. "
                f"I can control your PC, launch applications, play videos, automate tasks, and assist you with anything."
            ), "INFO"


        if "how are you" in q or "kaise ho" in q or "kya hal chal" in q:
            return f"I am running at optimal performance, {self.user_name}! How are you doing today?", "CONVERSATION"

        # -------------------------------------------------------------
        # 2. YouTube & Music Playback
        # -------------------------------------------------------------
        if any(phrase in q for phrase in ["play on youtube", "youtube pe", "youtube par", "gaana bajao", "song play karo", "play song", "play "]):
            # Extract song/video title
            song_query = q
            for trigger in ["play on youtube", "youtube pe chalao", "youtube par chalao", "youtube pe", "youtube par", "gaana bajao", "song bajao", "play "]:
                song_query = song_query.replace(trigger, "")
            song_query = song_query.replace("chalao", "").replace("bajao", "").replace("play", "").strip()
            if not song_query:
                song_query = "latest songs"
            return self.web.play_youtube(song_query), "YOUTUBE"

        # -------------------------------------------------------------
        # 3. Screenshot Capture
        # -------------------------------------------------------------
        if "screenshot" in q or "screen shot" in q:
            return self.pc.take_screenshot(), "SCREENSHOT"

        # -------------------------------------------------------------
        # 4. System Diagnostics (Battery, CPU, RAM)
        # -------------------------------------------------------------
        if any(term in q for term in ["battery", "charge", "charging", "cpu", "ram", "system status", "pc condition", "performance"]):
            return self.pc.get_system_status(), "SYSTEM_STATUS"

        # -------------------------------------------------------------
        # 5. Volume Controls
        # -------------------------------------------------------------
        if "volume" in q or "aawaz" in q or "sound" in q:
            if any(term in q for term in ["up", "badhao", "increase", "tez", "unmute"]):
                return self.pc.adjust_volume("up"), "VOLUME"
            elif any(term in q for term in ["down", "kam", "decrease", "dheemi"]):
                return self.pc.adjust_volume("down"), "VOLUME"
            elif any(term in q for term in ["mute", "silent", "chup"]):
                return self.pc.adjust_volume("mute"), "VOLUME"
            else:
                return self.pc.adjust_volume("up"), "VOLUME"

        # -------------------------------------------------------------
        # 6. Google Search & Web Browsing
        # -------------------------------------------------------------
        if any(term in q for term in ["search google for", "google pe search karo", "google search", "search on google", "search karo"]):
            search_query = q
            for trigger in ["search google for", "google pe search karo", "google search", "search on google", "search karo", "search"]:
                search_query = search_query.replace(trigger, "")
            search_query = search_query.strip()
            if not search_query:
                search_query = "Python programming"
            return self.web.search_google(search_query), "GOOGLE_SEARCH"

        # -------------------------------------------------------------
        # 7. Wikipedia & Knowledge
        # -------------------------------------------------------------
        if "wikipedia" in q or "who is " in q or "what is " in q or "tell me about " in q or "ke baare me" in q:
            wiki_query = q
            for trigger in ["search wikipedia for", "wikipedia pe search karo", "wikipedia", "tell me about", "who is", "what is", "ke baare me batao", "ke baare me"]:
                wiki_query = wiki_query.replace(trigger, "")
            wiki_query = wiki_query.strip()
            if wiki_query:
                return self.web.search_wikipedia(wiki_query), "WIKIPEDIA"

        # -------------------------------------------------------------
        # 8. Date, Time & Weather
        # -------------------------------------------------------------
        if any(term in q for term in ["time kya hua", "current time", "what time", "samay kya hai", "time"]):
            return self.web.get_time_date(), "TIME"

        if any(term in q for term in ["date kya hai", "what is the date", "today date", "aaj konsi date"]):
            return self.web.get_time_date(), "DATE"

        if any(term in q for term in ["weather", "mausam", "temperature", "tapman", "barish"]):
            city = "Junagadh"
            # Check if city name is mentioned
            words = q.split()
            if "in" in words:
                idx = words.index("in")
                if idx + 1 < len(words):
                    city = words[idx + 1]
            elif "me" in words:
                idx = words.index("me")
                if idx > 0:
                    city = words[idx - 1]
            return self.web.get_weather(city), "WEATHER"

        # -------------------------------------------------------------
        # 9. Folder Navigation
        # -------------------------------------------------------------
        if any(folder in q for folder in ["downloads", "documents", "desktop", "pictures", "music", "folder", "c drive", "d drive"]):
            return self.pc.open_folder(q), "FOLDER_OPEN"

        # -------------------------------------------------------------
        # 10. App Launching & Closing
        # -------------------------------------------------------------
        if any(term in q for term in ["open", "kholo", "start", "launch", "chalu karo", "khol do"]):
            app_target = q
            for trigger in ["open", "kholo", "start", "launch", "chalu karo", "chalu", "khol do"]:
                app_target = app_target.replace(trigger, "")
            app_target = app_target.strip()
            if app_target:
                # Check if it's a popular website
                from jarvis.config import POPULAR_WEBSITES
                for site in POPULAR_WEBSITES:
                    if site in app_target:
                        return self.web.open_website(site), "WEBSITE"
                # Otherwise open application
                return self.pc.open_app(app_target), "APP_LAUNCH"

        if any(term in q for term in ["close", "band karo", "stop", "exit", "band kar do"]):
            app_target = q
            for trigger in ["close", "band karo", "stop", "exit", "band kar do", "band"]:
                app_target = app_target.replace(trigger, "")
            app_target = app_target.strip()
            if app_target:
                return self.pc.close_app(app_target), "APP_CLOSE"


        # -------------------------------------------------------------
        # 11. Typing & Notes Taking
        # -------------------------------------------------------------
        if any(term in q for term in ["type karo", "write note", "note likho", "note banao", "type "]):
            content = q
            for trigger in ["type karo", "write note", "note likho", "note banao", "type"]:
                content = content.replace(trigger, "")
            content = content.strip()
            if not content:
                content = "Note created by JARVIS voice command."
            return self.pc.create_note(content), "NOTE"

        # -------------------------------------------------------------
        # 12. Windows Shortcuts & Lock
        # -------------------------------------------------------------
        if any(term in q for term in ["lock pc", "lock screen", "computer lock karo", "screen lock"]):
            return self.pc.lock_pc(), "LOCK"

        if any(term in q for term in ["minimize", "desktop dikhao", "show desktop"]):
            return self.pc.press_shortcut("win+d"), "SHORTCUT"

        if any(term in q for term in ["switch window", "window badlo", "alt tab"]):
            return self.pc.press_shortcut("alt+tab"), "SHORTCUT"

        # -------------------------------------------------------------
        # 13. Conversational AI / Gemini / Fallback
        # -------------------------------------------------------------
        if _gemini_client:
            try:
                prompt = (
                    f"You are JARVIS, a highly capable, polite, and witty AI desktop assistant created for {self.user_name}. "
                    f"Respond concisely in 1-2 friendly sentences. The user said: '{query}'"
                )
                response = _gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip(), "GEMINI_AI"
            except Exception as e:
                print(f"[AIBrain] Gemini call error: {e}")

        # Intelligent Fallback Responses
        smart_responses = [
            f"I have received your command: '{query}', {self.user_name}. I am checking the best action for this.",
            f"Understood {self.user_name}. Let me know if you would like me to search Google or open a related tool for '{query}'.",
            f"Command acknowledged, {self.user_name}. I am ready for your next instruction."
        ]
        return random.choice(smart_responses), "DEFAULT"
