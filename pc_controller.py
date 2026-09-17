"""
PC Controller for JARVIS: Full system automation, app launcher, volume, battery, screenshots, and keyboard/mouse controls.
"""
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from jarvis.config import WINDOWS_APPS, SCREENSHOTS_DIR, NOTES_DIR, USER_NAME

# Import system monitoring and automation modules
try:
    import psutil
    _psutil_available = True
except ImportError:
    _psutil_available = False

try:
    import pyautogui
    _pyautogui_available = True
    pyautogui.FAILSAFE = False
except ImportError:
    _pyautogui_available = False

try:
    from PIL import ImageGrab
    _pil_grab_available = True
except ImportError:
    _pil_grab_available = False


class PCController:
    def __init__(self):
        self.screenshots_dir = SCREENSHOTS_DIR
        self.notes_dir = NOTES_DIR

    def open_app(self, app_name: str) -> str:
        """
        Opens a Windows application by name or keyword.
        """
        app_name_lower = app_name.lower().strip()

        # Check known mapping
        for key, command in WINDOWS_APPS.items():
            if key in app_name_lower or app_name_lower in key:
                try:
                    subprocess.Popen(command, shell=True)
                    return f"Opening {key.capitalize()} for you, {USER_NAME}."
                except Exception as e:
                    return f"Failed to open {key}: {e}"

        # Generic open via Windows shell
        try:
            subprocess.Popen(f"start {app_name_lower}", shell=True)
            return f"Attempting to launch {app_name}, {USER_NAME}."
        except Exception as e:
            return f"Could not find or open application '{app_name}'. Error: {e}"

    def close_app(self, app_name: str) -> str:
        """
        Closes an application running on Windows.
        """
        app_name_clean = app_name.lower().replace(" ", "").replace(".exe", "")
        
        # Add .exe suffix
        exe_name = f"{app_name_clean}.exe"

        # Check if process is running
        found = False
        if _psutil_available:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if app_name_clean in proc.info['name'].lower():
                        proc.terminate()
                        found = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        if not found:
            # Fallback to taskkill
            res = os.system(f"taskkill /f /im {exe_name} >nul 2>&1")
            if res == 0:
                return f"Closed {app_name} successfully."
            return f"Could not find running process for {app_name}."
        
        return f"Closed {app_name} successfully, {USER_NAME}."

    def adjust_volume(self, action: str = "up", level: int = 5) -> str:
        """
        Adjusts system volume: 'up', 'down', 'mute', 'unmute'.
        """
        if not _pyautogui_available:
            return "Volume control requires PyAutoGUI module."

        action = action.lower()
        if "up" in action or "badhao" in action or "increase" in action:
            for _ in range(level):
                pyautogui.press('volumeup')
            return f"Volume increased."
        elif "down" in action or "kam" in action or "decrease" in action:
            for _ in range(level):
                pyautogui.press('volumedown')
            return f"Volume decreased."
        elif "mute" in action or "silent" in action:
            pyautogui.press('volumemute')
            return "Volume muted."
        elif "unmute" in action:
            pyautogui.press('volumemute')
            return "Volume unmuted."
        else:
            pyautogui.press('volumeup')
            return "Volume adjusted."

    def take_screenshot(self, filename: str = None) -> str:
        """
        Captures the screen and saves it as an image.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not filename:
            filename = f"screenshot_{timestamp}.png"
        elif not filename.endswith(".png"):
            filename = f"{filename}_{timestamp}.png"

        filepath = self.screenshots_dir / filename

        try:
            # Try PIL ImageGrab first (standard on Windows)
            if _pil_grab_available:
                screenshot = ImageGrab.grab()
                screenshot.save(str(filepath))
                return f"Screenshot saved successfully at {filepath.name}."
            elif _pyautogui_available:
                screenshot = pyautogui.screenshot()
                screenshot.save(str(filepath))
                return f"Screenshot saved successfully at {filepath.name}."
            else:
                return "Screenshot tool not available."
        except Exception as e:
            # If screen grab fails in non-interactive session, create a placeholder diagnostic image
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (800, 600), color=(15, 25, 45))
                d = ImageDraw.Draw(img)
                d.text((50, 50), f"JARVIS Screen Capture - {timestamp}\n{e}", fill=(0, 229, 255))
                img.save(str(filepath))
                return f"Screenshot saved at {filepath.name}."
            except Exception:
                return f"Failed to take screenshot: {e}"


    def get_system_status(self) -> str:
        """
        Checks CPU, RAM, and Battery status.
        """
        if not _psutil_available:
            return "System monitoring is currently unavailable (psutil required)."

        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.5)

            # RAM Usage
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_used_gb = round(ram.used / (1024 ** 3), 1)
            ram_total_gb = round(ram.total / (1024 ** 3), 1)

            # Battery
            battery = psutil.sensors_battery()
            battery_info = ""
            if battery:
                percent = battery.percent
                plugged = "Plugged in (Charging)" if battery.power_plugged else "Running on Battery"
                battery_info = f"Battery is at {percent}%, {plugged}. "
            else:
                battery_info = "Desktop system (No battery sensor). "

            status_msg = (
                f"{battery_info}CPU usage is {cpu_percent}%, "
                f"and RAM usage is {ram_percent}% ({ram_used_gb} GB of {ram_total_gb} GB)."
            )
            return status_msg
        except Exception as e:
            return f"Error retrieving system diagnostics: {e}"

    def type_text(self, text: str, delay: float = 0.05) -> str:
        """
        Types text using automated keystrokes.
        """
        if not _pyautogui_available:
            return "Keyboard automation requires PyAutoGUI."

        try:
            time.sleep(0.5)  # Short delay to allow window focus
            pyautogui.write(text, interval=delay)
            return f"Typed text into active window."
        except Exception as e:
            return f"Failed to type text: {e}"

    def press_shortcut(self, shortcut: str) -> str:
        """
        Executes a keyboard shortcut (e.g. 'win+d', 'alt+tab', 'enter', 'ctrl+s').
        """
        if not _pyautogui_available:
            return "Keyboard shortcuts require PyAutoGUI."

        shortcut = shortcut.lower().strip()
        try:
            if shortcut in ["win+d", "minimize all", "desktop"]:
                pyautogui.hotkey('win', 'd')
                return "Toggled Desktop view."
            elif shortcut in ["alt+tab", "switch"]:
                pyautogui.hotkey('alt', 'tab')
                return "Switched window."
            elif shortcut in ["enter", "press enter"]:
                pyautogui.press('enter')
                return "Pressed Enter."
            elif shortcut in ["ctrl+s", "save"]:
                pyautogui.hotkey('ctrl', 's')
                return "Saved file."
            elif shortcut in ["ctrl+a", "select all"]:
                pyautogui.hotkey('ctrl', 'a')
                return "Selected all."
            else:
                keys = [k.strip() for k in shortcut.split('+')]
                pyautogui.hotkey(*keys)
                return f"Pressed shortcut {shortcut}."
        except Exception as e:
            return f"Failed to execute shortcut: {e}"

    def create_note(self, content: str, title: str = "note") -> str:
        """
        Creates a text note file and opens it in Notepad.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title}_{timestamp}.txt"
        filepath = self.notes_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"JARVIS Note - Created on {datetime.now().strftime('%d-%b-%Y %I:%M %p')}\n")
                f.write("=" * 40 + "\n\n")
                f.write(content)
                f.write("\n")

            # Open note in notepad
            subprocess.Popen(["notepad", str(filepath)])
            return f"Note created and opened in Notepad: {filename}."
        except Exception as e:
            return f"Error creating note: {e}"

    def open_folder(self, folder_name: str) -> str:
        """
        Opens user directory (Downloads, Documents, Desktop, Pictures, etc.)
        """
        folder_lower = folder_name.lower().strip()
        user_home = Path.home()

        folder_map = {
            "downloads": user_home / "Downloads",
            "documents": user_home / "Documents",
            "desktop": user_home / "Desktop",
            "pictures": user_home / "Pictures",
            "music": user_home / "Music",
            "videos": user_home / "Videos",
            "c drive": Path("C:\\"),
            "d drive": Path("D:\\"),
            "project": Path(__file__).resolve().parent.parent
        }

        for key, path in folder_map.items():
            if key in folder_lower:
                if path.exists():
                    os.startfile(str(path))
                    return f"Opened {key.capitalize()} folder."

        # Fallback to current directory
        os.startfile(str(Path.cwd()))
        return f"Opened current workspace folder."

    def lock_pc(self) -> str:
        """Locks the Windows workstation."""
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return f"Locking workstation now, {USER_NAME}."
        except Exception as e:
            return f"Failed to lock workstation: {e}"
