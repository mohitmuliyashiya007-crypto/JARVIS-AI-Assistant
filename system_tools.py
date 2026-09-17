"""
System Tools for JARVIS
Handles Windows applications, screenshots, volume, and system info.
"""

import os
import subprocess
import platform
import datetime
from pathlib import Path

class SystemTools:
    def __init__(self):
        self.name = "system_tools"
        self.description = "Controls Windows OS functions, launches apps, takes screenshots, and monitors system."
        
        # Base screenshot directory
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)

        # Common Windows App mappings
        self.apps = {
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "calc": ["calc.exe"],
            "paint": ["mspaint.exe"],
            "cmd": ["cmd.exe"],
            "command prompt": ["cmd.exe"],
            "powershell": ["powershell.exe"],
            "explorer": ["explorer.exe"],
            "file explorer": ["explorer.exe"],
            "task manager": ["taskmgr.exe"],
            "settings": ["start", "ms-settings:"],
            "chrome": ["start", "chrome"],
            "google chrome": ["start", "chrome"],
            "edge": ["start", "msedge"],
            "microsoft edge": ["start", "msedge"],
            "vscode": ["code"],
            "vs code": ["code"],
            "visual studio code": ["code"],
            "whatsapp": ["start", "whatsapp:"],
            "spotify": ["start", "spotify:"],
            "discord": ["start", "discord:"],
            "telegram": ["start", "tg:"],
        }

    def open_application(self, app_name: str) -> dict:
        """Opens a requested application by name."""
        app_name_lower = app_name.lower().strip()
        
        # Check standard app map
        matched_cmd = None
        for key, cmd in self.apps.items():
            if key in app_name_lower or app_name_lower in key:
                matched_cmd = cmd
                break
                
        try:
            if matched_cmd:
                if matched_cmd[0] == "start":
                    subprocess.Popen(f"start {matched_cmd[1]}", shell=True)
                else:
                    subprocess.Popen(matched_cmd, shell=True)
                return {
                    "action": "open_app",
                    "app": app_name,
                    "status": "success",
                    "message": f"{app_name.capitalize()} open kar diya hai, Sir."
                }
            else:
                # Try generic windows start
                subprocess.Popen(f"start {app_name_lower}", shell=True)
                return {
                    "action": "open_app",
                    "app": app_name,
                    "status": "success",
                    "message": f"{app_name} launch karne ki koshish ki gayi hai, Sir."
                }
        except Exception as e:
            return {
                "action": "open_app",
                "status": "error",
                "message": f"App open karne me error aaya: {str(e)}"
            }

    def take_screenshot(self) -> dict:
        """Captures a screenshot using PowerShell/Windows native utilities."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.screenshot_dir / f"screenshot_{timestamp}.png"
        abs_path = filename.resolve()

        ps_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
        $bitmap.Save('{str(abs_path).replace('\\', '\\\\')}', [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $bitmap.Dispose()
        """
        try:
            subprocess.run(["powershell", "-Command", ps_script], check=True, capture_output=True)
            return {
                "action": "screenshot",
                "status": "success",
                "file_path": str(abs_path),
                "message": f"Screenshot capture kar liya gaya hai aur save ho chuka hai: {filename.name}"
            }
        except Exception as e:
            return {
                "action": "screenshot",
                "status": "error",
                "message": f"Screenshot lene me error aaya: {str(e)}"
            }

    def get_system_status(self) -> dict:
        """Fetches battery, OS, and memory information."""
        info = {
            "os": platform.platform(),
            "processor": platform.processor() or platform.machine(),
            "python_version": platform.python_version(),
            "time": datetime.datetime.now().strftime("%I:%M %p, %d %B %Y")
        }

        # Query battery status via PowerShell
        try:
            ps_cmd = "Get-CimInstance Win32_Battery | Select-Object -Property EstimatedChargeRemaining, BatteryStatus | ConvertTo-Json"
            res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=3)
            if res.stdout.strip():
                import json
                battery_data = json.loads(res.stdout)
                info["battery_percent"] = battery_data.get("EstimatedChargeRemaining", "N/A")
            else:
                info["battery_percent"] = "Desktop/AC Power"
        except Exception:
            info["battery_percent"] = "Normal"

        return {
            "action": "system_status",
            "status": "success",
            "info": info,
            "message": f"System Status: OS {info['os']} par online hai. Time: {info['time']}."
        }

    def volume_control(self, action: str) -> dict:
        """Adjusts volume (up, down, mute) using Windows Virtual Key codes via PowerShell."""
        action = action.lower()
        # VK_VOLUME_MUTE = 0xAD, VK_VOLUME_DOWN = 0xAE, VK_VOLUME_UP = 0xAF
        key_code = None
        if "up" in action or "badhao" in action or "increase" in action:
            key_code = "0xAF"
            msg = "Volume increase kar diya hai, Sir."
        elif "down" in action or "kam" in action or "decrease" in action:
            key_code = "0xAE"
            msg = "Volume decrease kar diya hai, Sir."
        elif "mute" in action or "chup" in action or "unmute" in action:
            key_code = "0xAD"
            msg = "Volume mute/unmute toggle kar diya hai, Sir."
        else:
            return {"status": "error", "message": "Unknown volume command."}

        ps_cmd = f"""
        $wscript = New-Object -ComObject Wscript.Shell
        1..5 | ForEach-Object {{ $wscript.SendKeys([char]{key_code}) }}
        """
        try:
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
            return {"action": "volume_control", "status": "success", "message": msg}
        except Exception as e:
            return {"action": "volume_control", "status": "error", "message": f"Volume control error: {str(e)}"}
