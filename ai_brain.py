"""
AI Brain for JARVIS
Handles Gemini API queries or built-in intelligent responses.
"""

import os
import json
import urllib.request
import urllib.parse

class AIBrain:
    def __init__(self):
        self.name = "ai_brain"
        self.api_key = os.environ.get("GEMINI_API_KEY", "")

    def ask_ai(self, query: str) -> dict:
        """Asks Gemini API if available, else responds with high-tech JARVIS smart intelligence."""
        if self.api_key:
            try:
                # Gemini 2.5 Flash / Flash-lite REST endpoint
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
                system_instruction = (
                    "You are JARVIS, Tony Stark's advanced AI assistant. You speak courteously, calling the user 'Sir' or 'Boss'. "
                    "You can reply in Hindi, English, or Hinglish depending on what the user speaks. "
                    "Keep answers concise, direct, helpful, and high-tech."
                )
                payload = {
                    "contents": [{
                        "parts": [{"text": query}]
                    }],
                    "systemInstruction": {
                        "parts": [{"text": system_instruction}]
                    }
                }
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_data = json.loads(response.read().decode())
                    text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "action": "ai_response",
                        "status": "success",
                        "provider": "gemini",
                        "message": text.strip()
                    }
            except Exception as e:
                pass

        # Smart Heuristic Responses for JARVIS Persona
        q_lower = query.lower()
        if any(w in q_lower for w in ["who are you", "kaun ho", "tum kaun ho", "introduce"]):
            msg = "I am J.A.R.V.I.S. (Just A Rather Very Intelligent System), your personal AI assistant. Main aapke voice commands par auto meet, system automation aur web actions execute kar sakta hoon, Sir!"
        elif any(w in q_lower for w in ["hello", "namaste", "hey jarvis", "hi jarvis", "kya haal"]):
            msg = "Greetings, Sir. JARVIS systems are 100% online and operational. Main aapki kya madad kar sakta hoon?"
        elif any(w in q_lower for w in ["joke", "chutkula", "hasao"]):
            msg = "Sir, kyu ek programmer hamesha dark mode use karta hai? Kyunki light attracts bugs! Haha."
        elif any(w in q_lower for w in ["who made you", "kisne banaya", "creator"]):
            msg = "I was inspired by Tony Stark's Stark Industries AI protocol and crafted as your ultimate personal assistant, Sir."
        elif any(w in q_lower for w in ["thank you", "thanks", "dhanyawad", "shukriya"]):
            msg = "Always at your service, Sir. Glad to be of assistance!"
        else:
            msg = f"Aapka command '{query}' process ho gaya hai, Sir. Tool executions ready hain."

        return {
            "action": "ai_response",
            "status": "success",
            "provider": "local_brain",
            "message": msg
        }
