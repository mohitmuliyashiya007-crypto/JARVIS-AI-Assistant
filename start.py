"""
J.A.R.V.I.S. Launcher
Starts the backend server and automatically opens the Stark Holographic HUD in the default browser.
"""

import sys
import time
import webbrowser
import threading
from server import run_server, PORT

def open_browser():
    time.sleep(1.2)
    url = f"http://localhost:{PORT}"
    print(f"🚀 Opening JARVIS HUD in browser: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run server
    try:
        run_server(PORT)
    except Exception as e:
        print(f"Error starting JARVIS: {e}")
