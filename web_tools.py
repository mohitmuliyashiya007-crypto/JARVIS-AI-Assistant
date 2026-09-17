"""
Web Tools for JARVIS
Handles YouTube media playback, Google search, Wikipedia queries, and live weather.
"""

import webbrowser
import urllib.parse
import urllib.request
import json
import re

class WebTools:
    def __init__(self):
        self.name = "web_tools"
        self.description = "Interacts with the web: plays YouTube videos, searches Google, fetches Wikipedia & weather."

    def play_youtube(self, query: str) -> dict:
        """Searches and opens a video or song directly on YouTube."""
        clean_query = query.strip()
        encoded = urllib.parse.quote(clean_query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        return {
            "action": "play_youtube",
            "query": clean_query,
            "url": url,
            "message": f"YouTube par '{clean_query}' play kiya ja raha hai, Sir."
        }

    def google_search(self, query: str) -> dict:
        """Opens a Google search for the query."""
        clean_query = query.strip()
        encoded = urllib.parse.quote(clean_query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return {
            "action": "google_search",
            "query": clean_query,
            "url": url,
            "message": f"Google par '{clean_query}' search kiya ja raha hai, Sir."
        }

    def search_wikipedia(self, query: str) -> dict:
        """Fetches a brief summary from Wikipedia REST API."""
        clean_query = query.strip()
        formatted_title = urllib.parse.quote(clean_query.replace(" ", "_"))
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"

        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": "JarvisAssistant/1.0 (contact@example.com)"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    extract = data.get("extract", "No summary found.")
                    title = data.get("title", clean_query)
                    return {
                        "action": "wikipedia",
                        "status": "success",
                        "title": title,
                        "summary": extract,
                        "message": f"Wikipedia ke anusaar {title}: {extract[:200]}..."
                    }
        except Exception as e:
            # Fallback to Google search
            self.google_search(clean_query)
            return {
                "action": "wikipedia",
                "status": "fallback",
                "message": f"Wikipedia par exact page nahi mila, Google search open kar diya hai: '{clean_query}'."
            }

    def get_weather(self, city: str = "Delhi") -> dict:
        """Fetches live weather from wttr.in in JSON format without any API key requirement."""
        clean_city = city.strip() if city.strip() else "Delhi"
        encoded_city = urllib.parse.quote(clean_city)
        url = f"https://wttr.in/{encoded_city}?format=j1"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "JarvisAssistant/1.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                current = data["current_condition"][0]
                temp_c = current.get("temp_C", "N/A")
                feels_like = current.get("FeelsLikeC", temp_c)
                weather_desc = current.get("weatherDesc", [{}])[0].get("value", "Clear")
                humidity = current.get("humidity", "N/A")

                msg = f"{clean_city.capitalize()} me taapman abhi {temp_c}°C hai ({weather_desc}), humidity {humidity}% hai."
                return {
                    "action": "weather",
                    "status": "success",
                    "city": clean_city,
                    "temp_c": temp_c,
                    "condition": weather_desc,
                    "humidity": humidity,
                    "message": msg
                }
        except Exception:
            # Fallback
            url_web = f"https://www.google.com/search?q=weather+in+{encoded_city}"
            webbrowser.open(url_web)
            return {
                "action": "weather",
                "status": "fallback",
                "city": clean_city,
                "message": f"{clean_city} ka live mausam Google par open kar diya hai, Sir."
            }
