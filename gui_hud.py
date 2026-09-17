"""
JARVIS Futuristic Arc Reactor Desktop GUI HUD
Built with high-performance animated Tkinter Canvas and Cyberpunk styling.
"""
import math
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

# Color Palette (Futuristic Neon Cyan & Dark Sci-Fi)
BG_DARK = "#050b14"
BG_CARD = "#0d1b2a"
BG_CARD_BORDER = "#1b3a5b"
ACCENT_CYAN = "#00e5ff"
ACCENT_BLUE = "#0077b6"
ACCENT_GLOW = "#48cae4"
ACCENT_GREEN = "#00f5d4"
ACCENT_AMBER = "#ffb703"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#8da9c4"
TEXT_CYAN = "#90e0ef"


class JarvisHUD:
    def __init__(self, on_command_callback: Callable[[str], None], get_status_callback: Optional[Callable[[], str]] = None):
        """
        Initializes the JARVIS Desktop HUD.
        :param on_command_callback: Function called when user submits a text/voice command
        """
        self.on_command = on_command_callback
        self.get_status = get_status_callback
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S. - Advanced AI System")
        self.root.geometry("900x650")
        self.root.minsize(800, 580)
        self.root.configure(bg=BG_DARK)

        # State Variables
        self.status_var = tk.StringVar(value="SYSTEM ONLINE")
        self.mic_active_var = tk.BooleanVar(value=True)
        self.angle = 0
        self.pulse_radius = 50
        self.pulse_direction = 1

        self._build_ui()
        self._start_arc_reactor_animation()

    def _build_ui(self):
        # -------------------------------------------------------------
        # 1. Top Header Bar
        # -------------------------------------------------------------
        header_frame = tk.Frame(self.root, bg=BG_CARD, height=60, highlightbackground=BG_CARD_BORDER, highlightthickness=1)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        # Title & Subtitle
        title_label = tk.Label(
            header_frame, 
            text="J.A.R.V.I.S.", 
            font=("Consolas", 20, "bold"), 
            fg=ACCENT_CYAN, 
            bg=BG_CARD
        )
        title_label.pack(side="left", padx=(20, 10), pady=10)

        sub_label = tk.Label(
            header_frame, 
            text="// AUTONOMOUS DESKTOP INTELLIGENCE", 
            font=("Consolas", 10), 
            fg=TEXT_MUTED, 
            bg=BG_CARD
        )
        sub_label.pack(side="left", pady=10)

        # Status Badge
        self.status_badge = tk.Label(
            header_frame, 
            textvariable=self.status_var, 
            font=("Consolas", 11, "bold"), 
            fg=ACCENT_GREEN, 
            bg="#0b2923", 
            padx=12, 
            pady=4,
            relief="solid",
            bd=1
        )
        self.status_badge.pack(side="right", padx=20, pady=12)

        # -------------------------------------------------------------
        # 2. Main Middle Container (Arc Reactor + Console)
        # -------------------------------------------------------------
        main_container = tk.Frame(self.root, bg=BG_DARK)
        main_container.pack(fill="both", expand=True, padx=15, pady=5)

        # Left Column: Arc Reactor Visualizer & Quick Actions
        left_frame = tk.Frame(main_container, bg=BG_CARD, width=320, highlightbackground=BG_CARD_BORDER, highlightthickness=1)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)

        # Arc Reactor Canvas
        self.canvas = tk.Canvas(left_frame, width=280, height=260, bg=BG_CARD, highlightthickness=0)
        self.canvas.pack(pady=10)

        # Quick Control Buttons Title
        quick_title = tk.Label(
            left_frame, 
            text="QUICK CONTROLS", 
            font=("Consolas", 10, "bold"), 
            fg=TEXT_MUTED, 
            bg=BG_CARD
        )
        quick_title.pack(anchor="w", padx=20, pady=(5, 5))

        # Quick Buttons Grid
        btn_grid = tk.Frame(left_frame, bg=BG_CARD)
        btn_grid.pack(fill="x", padx=15, pady=5)

        self._create_tool_btn(btn_grid, "📸 Screenshot", lambda: self.on_command("take a screenshot"), 0, 0)
        self._create_tool_btn(btn_grid, "🔋 System Info", lambda: self.on_command("battery check"), 0, 1)
        self._create_tool_btn(btn_grid, "🎵 YouTube Lofi", lambda: self.on_command("play lofi songs on youtube"), 1, 0)
        self._create_tool_btn(btn_grid, "📝 New Note", lambda: self.on_command("write note: Jarvis session started"), 1, 1)
        self._create_tool_btn(btn_grid, "🔊 Volume Up", lambda: self.on_command("increase volume"), 2, 0)
        self._create_tool_btn(btn_grid, "🔉 Volume Down", lambda: self.on_command("decrease volume"), 2, 1)

        # Mic Toggle Button
        self.mic_btn = tk.Button(
            left_frame, 
            text="🎙️ VOICE LISTENING: ON", 
            font=("Consolas", 11, "bold"), 
            bg="#004d40", 
            fg=ACCENT_GREEN, 
            activebackground=ACCENT_GREEN, 
            activeforeground=BG_DARK,
            bd=0, 
            padx=10, 
            pady=8, 
            cursor="hand2",
            command=self._toggle_mic
        )
        self.mic_btn.pack(fill="x", padx=20, pady=(15, 10))

        # Right Column: Terminal Console Log & Chat
        right_frame = tk.Frame(main_container, bg=BG_CARD, highlightbackground=BG_CARD_BORDER, highlightthickness=1)
        right_frame.pack(side="right", fill="both", expand=True)

        console_header = tk.Frame(right_frame, bg="#081426", height=32)
        console_header.pack(fill="x")

        console_title = tk.Label(
            console_header, 
            text=">_ LIVE TERMINAL & CONVERSATION LOG", 
            font=("Consolas", 9, "bold"), 
            fg=ACCENT_CYAN, 
            bg="#081426"
        )
        console_title.pack(side="left", padx=15, pady=6)

        # Text Console with Scrollbar
        console_frame = tk.Frame(right_frame, bg=BG_CARD)
        console_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.console_text = tk.Text(
            console_frame, 
            bg="#060e1a", 
            fg=TEXT_PRIMARY, 
            font=("Consolas", 10), 
            wrap="word", 
            bd=0, 
            padx=12, 
            pady=12,
            insertbackground=ACCENT_CYAN
        )
        scrollbar = tk.Scrollbar(console_frame, command=self.console_text.yview, bg=BG_CARD)
        self.console_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.console_text.pack(side="left", fill="both", expand=True)

        # Configure Text Tags for Coloring
        self.console_text.tag_config("user", foreground=ACCENT_AMBER, font=("Consolas", 10, "bold"))
        self.console_text.tag_config("jarvis", foreground=ACCENT_CYAN, font=("Consolas", 10))
        self.console_text.tag_config("system", foreground=TEXT_MUTED, font=("Consolas", 9, "italic"))
        self.console_text.tag_config("action", foreground=ACCENT_GREEN, font=("Consolas", 9, "bold"))

        # -------------------------------------------------------------
        # 3. Bottom Prompt Input Bar
        # -------------------------------------------------------------
        input_frame = tk.Frame(self.root, bg=BG_CARD, height=55, highlightbackground=BG_CARD_BORDER, highlightthickness=1)
        input_frame.pack(fill="x", padx=15, pady=(10, 15))

        prompt_icon = tk.Label(input_frame, text="⚡", font=("Segoe UI", 14), fg=ACCENT_CYAN, bg=BG_CARD)
        prompt_icon.pack(side="left", padx=(15, 5), pady=8)

        self.entry_box = tk.Entry(
            input_frame, 
            font=("Consolas", 11), 
            bg="#060e1a", 
            fg=TEXT_PRIMARY, 
            insertbackground=ACCENT_CYAN, 
            bd=0,
            highlightthickness=1,
            highlightcolor=ACCENT_CYAN,
            highlightbackground="#1b3a5b"
        )
        self.entry_box.pack(side="left", fill="x", expand=True, padx=10, pady=10, ipady=5)
        self.entry_box.bind("<Return>", lambda e: self._on_send())

        send_btn = tk.Button(
            input_frame, 
            text="EXECUTE", 
            font=("Consolas", 10, "bold"), 
            bg=ACCENT_BLUE, 
            fg=TEXT_PRIMARY, 
            activebackground=ACCENT_CYAN, 
            activeforeground=BG_DARK,
            bd=0, 
            padx=18, 
            pady=6, 
            cursor="hand2",
            command=self._on_send
        )
        send_btn.pack(side="right", padx=(5, 15), pady=10)

        # Welcome message in console
        self.log_system("J.A.R.V.I.S. Core Intelligence loaded successfully.")
        self.log_system("All subroutines, PC tools, and voice links operational.")
        self.log_jarvis("Greetings Sir! How may I assist you today?")

    def _create_tool_btn(self, parent, text, command, row, col):
        btn = tk.Button(
            parent, 
            text=text, 
            font=("Consolas", 9), 
            bg="#10253f", 
            fg=TEXT_CYAN, 
            activebackground=ACCENT_BLUE, 
            activeforeground=TEXT_PRIMARY,
            bd=0, 
            padx=6, 
            pady=6, 
            cursor="hand2",
            command=command
        )
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
        parent.columnconfigure(col, weight=1)

    def _toggle_mic(self):
        new_state = not self.mic_active_var.get()
        self.mic_active_var.set(new_state)
        if new_state:
            self.mic_btn.config(text="🎙️ VOICE LISTENING: ON", bg="#004d40", fg=ACCENT_GREEN)
            self.log_system("Voice recognition activated.")
        else:
            self.mic_btn.config(text="🔇 VOICE MUTED (MANUAL)", bg="#3e1b1b", fg="#ff6b6b")
            self.log_system("Voice recognition paused. Use text input below.")

    def _on_send(self):
        text = self.entry_box.get().strip()
        if text:
            self.entry_box.delete(0, tk.END)
            self.log_user(text)
            threading.Thread(target=self.on_command, args=(text,), daemon=True).start()

    def update_status(self, status: str):
        """Updates the status badge (LISTENING, THINKING, SPEAKING, IDLE)"""
        status_upper = status.upper()
        self.status_var.set(status_upper)

        if "LISTEN" in status_upper:
            self.status_badge.config(fg=ACCENT_CYAN, bg="#08304b")
        elif "PROCESS" in status_upper or "THINK" in status_upper:
            self.status_badge.config(fg=ACCENT_AMBER, bg="#3d2c00")
        elif "SPEAK" in status_upper:
            self.status_badge.config(fg=ACCENT_GREEN, bg="#073b32")
        else:
            self.status_badge.config(fg=ACCENT_CYAN, bg="#0b2923")

    def log_user(self, text: str):
        self.console_text.insert(tk.END, f"\n[USER]: {text}\n", "user")
        self.console_text.see(tk.END)

    def log_jarvis(self, text: str, action_type: str = ""):
        self.console_text.insert(tk.END, f"[JARVIS]: {text}\n", "jarvis")
        if action_type and action_type not in ["NONE", "GREETING", "CONVERSATION", "DEFAULT"]:
            self.console_text.insert(tk.END, f"  └─ Action Executed: [{action_type}]\n", "action")
        self.console_text.see(tk.END)

    def log_system(self, text: str):
        self.console_text.insert(tk.END, f"[SYSTEM]: {text}\n", "system")
        self.console_text.see(tk.END)

    def _start_arc_reactor_animation(self):
        """Draws dynamic rotating holographic rings and pulsing core."""
        cx, cy = 140, 130
        self.canvas.delete("all")

        # Outer Pulsing Glow
        self.pulse_radius += 0.5 * self.pulse_direction
        if self.pulse_radius > 65:
            self.pulse_direction = -1
        elif self.pulse_radius < 45:
            self.pulse_direction = 1

        self.canvas.create_oval(
            cx - self.pulse_radius, cy - self.pulse_radius,
            cx + self.pulse_radius, cy + self.pulse_radius,
            outline="#0c3b5e", width=2
        )

        # Outer Fixed Ring
        self.canvas.create_oval(cx - 75, cy - 75, cx + 75, cy + 75, outline=ACCENT_BLUE, width=2)
        self.canvas.create_oval(cx - 82, cy - 82, cx + 82, cy + 82, outline="#112d4e", width=1)

        # Rotating Segmented Arc
        self.angle = (self.angle + 3) % 360
        for i in range(8):
            start_a = self.angle + (i * 45)
            self.canvas.create_arc(
                cx - 68, cy - 68, cx + 68, cy + 68,
                start=start_a, extent=25, outline=ACCENT_CYAN, width=3, style="arc"
            )

        # Inner Counter-Rotating Ring
        inner_angle = (360 - (self.angle * 2)) % 360
        for j in range(4):
            start_ia = inner_angle + (j * 90)
            self.canvas.create_arc(
                cx - 40, cy - 40, cx + 40, cy + 40,
                start=start_ia, extent=45, outline=ACCENT_GREEN, width=2, style="arc"
            )

        # Core Glowing Center
        self.canvas.create_oval(cx - 22, cy - 22, cx + 22, cy + 22, fill="#04324f", outline=ACCENT_CYAN, width=2)
        self.canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill=ACCENT_CYAN, outline=TEXT_PRIMARY, width=1)

        # Schedule next animation frame (30 FPS)
        self.root.after(33, self._start_arc_reactor_animation)

    def run(self):
        """Starts GUI main loop."""
        self.root.mainloop()
