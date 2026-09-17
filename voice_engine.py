"""
Voice Engine for JARVIS: Speech-to-Text (STT) and Text-to-Speech (TTS)
Supports both Hindi and English voice recognition and speech feedback.
"""
import sys
import threading
import subprocess
from typing import Callable, Optional
from jarvis.config import VOICE_RATE, VOICE_VOLUME, VOICE_GENDER, LANGUAGE_CODE

# TTS Engine Initialization
try:
    import pyttsx3
    _tts_available = True
except ImportError:
    _tts_available = False

# Speech Recognition Initialization
try:
    import speech_recognition as sr
    _stt_available = True
except ImportError:
    _stt_available = False


class VoiceEngine:
    def __init__(self, on_status_change: Optional[Callable[[str], None]] = None):
        """
        Initializes the Voice Engine.
        :param on_status_change: Optional callback function to notify UI of status changes
        """
        self.on_status_change = on_status_change
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        self.is_speaking = False
        self.is_listening = False
        self.mic_available = False

        self._init_tts()
        self._init_stt()

    def _set_status(self, status: str):
        if self.on_status_change:
            try:
                self.on_status_change(status)
            except Exception:
                pass

    def _init_tts(self):
        """Initializes the Text-to-Speech engine."""
        if _tts_available:
            try:
                self.tts_engine = pyttsx3.init('sapi5')
                self.tts_engine.setProperty('rate', VOICE_RATE)
                self.tts_engine.setProperty('volume', VOICE_VOLUME)

                # Select Voice (David for Male, Zira for Female if available)
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    if VOICE_GENDER.lower() == "female" and len(voices) > 1:
                        self.tts_engine.setProperty('voice', voices[1].id)
                    else:
                        self.tts_engine.setProperty('voice', voices[0].id)
            except Exception as e:
                print(f"[VoiceEngine] pyttsx3 init error: {e}")
                self.tts_engine = None

    def _init_stt(self):
        """Initializes the Speech Recognition recognizer and microphone."""
        if _stt_available:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                
                # Test microphone access
                try:
                    self.microphone = sr.Microphone()
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.mic_available = True
                except Exception as mic_err:
                    print(f"[VoiceEngine] Microphone not accessible directly (PyAudio or Mic missing): {mic_err}")
                    self.mic_available = False
            except Exception as e:
                print(f"[VoiceEngine] Recognizer init error: {e}")
                self.recognizer = None
                self.mic_available = False

    def speak(self, text: str, block: bool = True):
        """
        Speaks out text using TTS and prints to terminal.
        """
        if not text:
            return

        print(f"\n[JARVIS]: {text}")
        self._set_status("SPEAKING")
        self.is_speaking = True

        def _run_speak():
            try:
                if self.tts_engine:
                    # In some environments, pyttsx3 needs a fresh instance or runAndWait
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                else:
                    # Fallback to Windows PowerShell SAPI Speech
                    escaped_text = text.replace('"', '`"').replace("'", "''")
                    ps_command = f'Add-Type -AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{escaped_text}")'
                    subprocess.run(["powershell", "-NoProfile", "-Command", ps_command], capture_output=True)
            except Exception as e:
                print(f"[VoiceEngine] Speak error: {e}")
            finally:
                self.is_speaking = False
                self._set_status("IDLE")

        if block:
            _run_speak()
        else:
            t = threading.Thread(target=_run_speak, daemon=True)
            t.start()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 8, language: str = LANGUAGE_CODE) -> Optional[str]:
        """
        Listens to user's voice through microphone and returns transcribed text.
        Supports Hindi ('hi-IN') and English ('en-IN', 'en-US').
        """
        if not self.mic_available or not self.recognizer or not self.microphone:
            self._set_status("IDLE")
            return None

        self._set_status("LISTENING")
        self.is_listening = True
        command = None

        try:
            with self.microphone as source:
                print("\n[LISTENING...] Speak now...")
                # Listen to audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
            self._set_status("PROCESSING")
            print("[PROCESSING...] Recognizing speech...")

            # Primary: Recognize using Google Speech (free & highly accurate for Indian English / Hindi)
            try:
                command = self.recognizer.recognize_google(audio, language=language)
            except sr.UnknownValueError:
                # Try fallback language if recognition missed
                fallback_lang = "hi-IN" if language == "en-IN" else "en-IN"
                try:
                    command = self.recognizer.recognize_google(audio, language=fallback_lang)
                except Exception:
                    command = None
            except sr.RequestError as re:
                print(f"[VoiceEngine] Google Speech API request error: {re}")
                command = None

            if command:
                print(f"[USER]: {command}")

        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"[VoiceEngine] Listen error: {e}")
        finally:
            self.is_listening = False
            self._set_status("IDLE")

        return command
