"""
J.A.R.V.I.S. Main Entry Point
Boots the AI Brain, PC Controller, Voice Engine, and Futuristic HUD GUI.
"""
import sys
import time
import threading
from jarvis.config import USER_NAME, ASSISTANT_NAME
from jarvis.voice_engine import VoiceEngine
from jarvis.pc_controller import PCController
from jarvis.web_tools import WebTools
from jarvis.ai_brain import AIBrain
from jarvis.gui_hud import JarvisHUD


class JarvisAgent:
    def __init__(self):
        print("=" * 60)
        print("[*] INITIALIZING J.A.R.V.I.S. AUTONOMOUS DESKTOP AGENT")
        print("=" * 60)


        # 1. Initialize Tools & Controllers
        self.pc = PCController()
        self.web = WebTools()
        self.brain = AIBrain(self.pc, self.web)

        # 2. Initialize HUD Interface
        self.hud = JarvisHUD(
            on_command_callback=self.handle_command,
            get_status_callback=lambda: "READY"
        )

        # 3. Initialize Voice Engine with HUD status hook
        self.voice = VoiceEngine(on_status_change=self.on_voice_status)

        # 4. Flags
        self.is_running = True
        self.is_processing = False

    def on_voice_status(self, status: str):
        """Callback to update HUD badge when voice state changes."""
        if hasattr(self, 'hud'):
            try:
                self.hud.update_status(status)
            except Exception:
                pass

    def handle_command(self, query: str):
        """
        Processes a command string (from Voice or Text Input).
        """
        if not query or not query.strip() or self.is_processing:
            return

        self.is_processing = True
        try:
            self.hud.update_status("PROCESSING")
            
            # AI Brain interpretation and execution
            response_text, action_type = self.brain.process_command(query)

            # Update HUD Console
            if response_text:
                self.hud.log_jarvis(response_text, action_type)
                
                # Speak out response
                self.voice.speak(response_text, block=True)

        except Exception as e:
            err_msg = f"An error occurred while executing command: {e}"
            self.hud.log_system(err_msg)
            self.voice.speak(err_msg, block=False)
        finally:
            self.is_processing = False
            self.hud.update_status("SYSTEM ONLINE")

    def voice_listener_loop(self):
        """
        Continuous background thread for speech recognition.
        """
        time.sleep(1.5)  # Wait for GUI and startup speech to complete

        while self.is_running:
            # Only listen if mic toggle is active in HUD and not already speaking/processing
            if self.hud.mic_active_var.get() and self.voice.mic_available and not self.is_processing and not self.voice.is_speaking:
                try:
                    speech_text = self.voice.listen(timeout=4, phrase_time_limit=7)
                    if speech_text:
                        self.hud.log_user(speech_text)
                        self.handle_command(speech_text)
                except Exception as e:
                    time.sleep(0.5)
            else:
                time.sleep(0.5)

    def startup_sequence(self):
        """Plays startup greeting."""
        time.sleep(0.8)
        greeting = f"Hello {USER_NAME}! Jarvis is online and ready for your commands."
        self.voice.speak(greeting, block=False)

    def start(self):
        """
        Starts the JARVIS Agent: boots background listener and runs GUI HUD.
        """
        # Start Voice Listening Background Thread
        listener_thread = threading.Thread(target=self.voice_listener_loop, daemon=True)
        listener_thread.start()

        # Start Greeting Sequence
        startup_thread = threading.Thread(target=self.startup_sequence, daemon=True)
        startup_thread.start()

        # Run HUD GUI Loop (blocking)
        try:
            self.hud.run()
        finally:
            self.is_running = False
            print("\n[JARVIS]: System shutting down. Goodbye!")


if __name__ == "__main__":
    agent = JarvisAgent()
    agent.start()
