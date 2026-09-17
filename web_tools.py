"""
Web and Media Automation Tools for JARVIS:
- YouTube player & search
- Google search
- Wikipedia summaries
- Real-time weather & time/date
- Website browser launcher
"""
import urllib.parse
import urllib.request
import json
import webbrowser
from datetime import datetime
from jarvis.config import POPULAR_WEBSITES, USER_NAME

try:
    import requests
    _requests_available = True
except ImportError:
    _requests_available = False



class WebTools:
    def __init__(self):
        pass

    def play_youtube(self, query: str) -> str:
        """
        Searches and plays songs/videos on YouTube.
        """
        clean_query = query.strip()
        encoded = urllib.parse.quote_plus(clean_query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        
        webbrowser.open(url)
        return f"Playing '{clean_query}' on YouTube, {USER_NAME}."

    def search_google(self, query: str) -> str:
        """
        Searches Google for any query and opens results in default browser.
        """
        clean_query = query.strip()
        encoded = urllib.parse.quote_plus(clean_query)
        url = f"https://www.google.com/search?q={encoded}"

        webbrowser.open(url)
        return f"Here is what I found on Google for '{clean_query}', {USER_NAME}."

    def search_wikipedia(self, query: str) -> str:
        """
        Fetches a summary from Wikipedia API for the given topic.
        """
        clean_query = query.strip()
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_query)}"
            headers = {'User-Agent': 'JarvisAI/1.0 (Python)'}
            
            data = None
            if _requests_available:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    data = response.json()
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))

            if data:
                extract = data.get('extract')
                if extract:
                    sentences = extract.split(". ")
                    summary = ". ".join(sentences[:2])
                    if not summary.endswith("."):
                        summary += "."
                    return f"According to Wikipedia: {summary}"
        except Exception as e:
            print(f"[WebTools] Wikipedia API error: {e}")

        # Fallback to Google Search
        self.search_google(clean_query)
        return f"I couldn't fetch a direct Wikipedia summary, so I have opened Google search for '{clean_query}'."

    def get_weather(self, city: str = "Junagadh") -> str:
        """
        Fetches current weather for the specified city using wttr.in JSON API (no API key required).
        """
        city_clean = city.strip() if city else "Junagadh"
        try:
            url = f"https://wttr.in/{urllib.parse.quote(city_clean)}?format=j1"
            headers = {'User-Agent': 'JarvisAI/1.0'}
            
            data = None
            if _requests_available:
                resp = requests.get(url, headers=headers, timeout=6)
                if resp.status_code == 200:
                    data = resp.json()
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=6) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))

            if data:
                current = data['current_condition'][0]
                temp_c = current['temp_C']
                desc = current['weatherDesc'][0]['value']
                humidity = current['humidity']
                wind = current['windspeedKmph']

                return (
                    f"The current weather in {city_clean.capitalize()} is {desc} with a temperature of {temp_c}°C. "
                    f"Humidity is {humidity}% and wind speed is {wind} kilometers per hour."
                )
        except Exception as e:
            print(f"[WebTools] Weather API error: {e}")

        return f"Sorry {USER_NAME}, I could not retrieve weather information for {city_clean} at the moment."


    def get_time_date(self) -> str:
        """
        Returns the current time, day, and date.
        """
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        day_str = now.strftime("%A")
        date_str = now.strftime("%d %B %Y")
        return f"It is currently {time_str} on {day_str}, {date_str}."

    def open_website(self, site_query: str) -> str:
        """
        Opens a website based on name or direct URL.
        """
        site_clean = site_query.lower().strip()

        # Check known website list
        for key, url in POPULAR_WEBSITES.items():
            if key in site_clean:
                webbrowser.open(url)
                return f"Opening {key.capitalize()} in your browser."

        # If it looks like a URL
        if "." in site_clean and not site_clean.startswith("http"):
            url = f"https://{site_clean}"
            webbrowser.open(url)
            return f"Opening {url}."
        elif site_clean.startswith("http://") or site_clean.startswith("https://"):
            webbrowser.open(site_clean)
            return f"Opening requested webpage."

        # Otherwise search Google
        return self.search_google(site_query)
