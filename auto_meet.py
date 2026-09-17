"""
Auto Meet Tool for JARVIS
Handles Google Meet, Zoom, and meeting scheduling automation.
"""

import webbrowser
import urllib.parse
import re

class AutoMeetTool:
    def __init__(self):
        self.name = "auto_meet"
        self.description = "Automates Google Meet sessions, joins meetings via code/URL, and opens meeting schedulers."

    def create_instant_meet(self) -> dict:
        """Starts a brand new Google Meet session."""
        url = "https://meet.google.com/new"
        webbrowser.open(url)
        return {
            "action": "create_meet",
            "url": url,
            "message": "Naya Google Meet start kar diya hai, Sir. Room is ready!"
        }

    def join_meet(self, meet_code_or_url: str) -> dict:
        """Joins an existing Google Meet session using code or URL."""
        meet_code_or_url = meet_code_or_url.strip()
        
        # Check if full URL or just code
        if "meet.google.com" in meet_code_or_url or "http" in meet_code_or_url:
            url = meet_code_or_url
        else:
            # Clean up meet code format (e.g. abc-defg-hij)
            code_clean = re.sub(r'[^a-zA-Z0-9-]', '', meet_code_or_url)
            url = f"https://meet.google.com/{code_clean}"
            
        webbrowser.open(url)
        return {
            "action": "join_meet",
            "url": url,
            "message": f"Google Meet join kar raha hoon: {url}"
        }

    def schedule_meet(self, title: str = "JARVIS Scheduled Meeting") -> dict:
        """Opens Google Calendar with pre-configured Google Meet conference."""
        encoded_title = urllib.parse.quote(title)
        url = f"https://calendar.google.com/calendar/r/eventedit?text={encoded_title}&add=meet"
        webbrowser.open(url)
        return {
            "action": "schedule_meet",
            "url": url,
            "message": f"Google Calendar me '{title}' ke liye meeting schedule page open kar diya hai, Sir."
        }

    def open_zoom(self) -> dict:
        """Opens Zoom Web / App."""
        url = "https://zoom.us/join"
        webbrowser.open(url)
        return {
            "action": "open_zoom",
            "url": url,
            "message": "Zoom meeting portal open kar diya hai, Sir."
        }
