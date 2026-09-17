"""
JARVIS Brain - Central AI Agent Engine & Command Router
Processes voice/text commands in Hindi, English, & Hinglish, and dispatches to appropriate tools.
"""

import re
from tools.auto_meet import AutoMeetTool
from tools.system_tools import SystemTools
from tools.web_tools import WebTools
from tools.ai_brain import AIBrain

class JarvisBrain:
    def __init__(self):
        self.auto_meet = AutoMeetTool()
        self.system = SystemTools()
        self.web = WebTools()
        self.ai = AIBrain()

    def process_command(self, user_command: str) -> dict:
        """
        Interprets natural language command and routes it to the suitable tool.
        Returns structured result with voice response text and execution metadata.
        """
        cmd = user_command.strip()
        cmd_lower = cmd.lower()

        if not cmd:
            return {
                "status": "empty",
                "message": "Sir, I am listening. Please give me a command.",
                "tool": "none"
            }

        # -------------------------------------------------------------
        # 1. AUTO MEET & MEETING AUTOMATION
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["google meet", "auto meet", "meeting", "meet start", "meet kholo", "naya meet", "join meet", "zoom"]):
            if "zoom" in cmd_lower:
                res = self.auto_meet.open_zoom()
                res["tool"] = "auto_meet"
                return res
            elif "schedule" in cmd_lower or "calendar" in cmd_lower:
                # Extract potential title
                title_match = re.search(r'(?:schedule|for|meeting on|title)\s+(.+)', cmd_lower)
                title = title_match.group(1).title() if title_match else "Team Sync"
                res = self.auto_meet.schedule_meet(title)
                res["tool"] = "auto_meet"
                return res
            elif "join" in cmd_lower or "code" in cmd_lower or "link" in cmd_lower:
                # Look for meet code or url
                tokens = cmd.split()
                meet_target = tokens[-1] if len(tokens) > 1 else "new"
                res = self.auto_meet.join_meet(meet_target)
                res["tool"] = "auto_meet"
                return res
            else:
                res = self.auto_meet.create_instant_meet()
                res["tool"] = "auto_meet"
                return res

        # -------------------------------------------------------------
        # 2. SCREENSHOT CAPTURE
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["screenshot", "screen shot", "screen capture", "screen photo"]):
            res = self.system.take_screenshot()
            res["tool"] = "system_tools"
            return res

        # -------------------------------------------------------------
        # 3. YOUTUBE / MUSIC PLAYBACK
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["play", "youtube", "gaana", "song", "chalao", "bajao"]):
            # Clean up query
            clean = re.sub(r'(play|on youtube|youtube pe|youtube par|chalao|bajao|song|gaana|chala do|baja do)', '', cmd_lower, flags=re.IGNORECASE).strip()
            if not clean:
                clean = "Latest Trending Songs"
            res = self.web.play_youtube(clean)
            res["tool"] = "web_tools"
            return res

        # -------------------------------------------------------------
        # 4. WEATHER INFORMATION
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["weather", "mausam", "temperature", "taapman"]):
            # Check for city before "ka/ke/me" (e.g. "Delhi ka mausam") or after "in/of" (e.g. "Weather in Delhi")
            city = "Delhi"
            match_hindi = re.search(r'([a-zA-Z]+)\s+(?:ka|ke|me|ki)\s+(?:mausam|weather|taapman|temperature)', cmd_lower)
            match_eng = re.search(r'(?:weather|temperature|mausam|taapman)\s+(?:in|of|at|for)\s+([a-zA-Z]+)', cmd_lower)
            if match_hindi:
                city = match_hindi.group(1)
            elif match_eng:
                city = match_eng.group(1)
            res = self.web.get_weather(city)
            res["tool"] = "web_tools"
            return res

        # -------------------------------------------------------------
        # 5. VOLUME / SYSTEM AUDIO CONTROL
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["volume", "awaz", "sound", "mute", "unmute"]):
            if any(w in cmd_lower for w in ["up", "badhao", "increase", "tez"]):
                res = self.system.volume_control("up")
            elif any(w in cmd_lower for w in ["down", "kam", "decrease", "slow"]):
                res = self.system.volume_control("down")
            else:
                res = self.system.volume_control("mute")
            res["tool"] = "system_tools"
            return res

        # -------------------------------------------------------------
        # 6. SYSTEM STATUS / BATTERY
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["system status", "battery", "pc info", "laptop info", "status kya hai"]):
            res = self.system.get_system_status()
            res["tool"] = "system_tools"
            return res

        # -------------------------------------------------------------
        # 7. APP LAUNCHER (Notepad, Calculator, VS Code, Chrome, etc.)
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["open", "kholo", "launch", "start", "chalu karo"]):
            # Extract app name
            target_app = re.sub(r'(open|kholo|launch|start|chalu karo|app|application|please)', '', cmd_lower, flags=re.IGNORECASE).strip()
            if target_app:
                res = self.system.open_application(target_app)
                res["tool"] = "system_tools"
                return res

        # -------------------------------------------------------------
        # 8. WIKIPEDIA / GENERAL SEARCH
        # -------------------------------------------------------------
        if any(w in cmd_lower for w in ["who is", "what is", "wikipedia", "kya hota hai", "search", "google"]):
            clean_search = re.sub(r'(who is|what is|search|google|search for|on google|kya hai|batao|kya hota hai)', '', cmd_lower, flags=re.IGNORECASE).strip()
            if "wikipedia" in cmd_lower:
                res = self.web.search_wikipedia(clean_search)
                res["tool"] = "web_tools"
                return res
            elif clean_search:
                res = self.web.google_search(clean_search)
                res["tool"] = "web_tools"
                return res

        # -------------------------------------------------------------
        # 9. AI BRAIN & CONVERSATIONAL INTELLIGENCE FALLBACK
        # -------------------------------------------------------------
        res = self.ai.ask_ai(cmd)
        res["tool"] = "ai_brain"
        return res
