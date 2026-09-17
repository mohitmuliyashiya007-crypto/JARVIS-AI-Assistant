"""
J.A.R.V.I.S. Command Line & Console Interface
Run JARVIS directly in your terminal with text/voice commands.
"""

from jarvis_brain import JarvisBrain

def main():
    brain = JarvisBrain()
    print("=" * 60)
    print("⚡ J.A.R.V.I.S. (Just A Rather Very Intelligent System) ⚡")
    print("Type your commands in Hindi, English, or Hinglish.")
    print("Examples:")
    print("  - 'Google meet start karo' / 'Open Google Meet'")
    print("  - 'Play Believer on YouTube'")
    print("  - 'Open Notepad' / 'Open Calculator'")
    print("  - 'Take screenshot'")
    print("  - 'Mausam kaisa hai'")
    print("  - 'Exit' to quit")
    print("=" * 60 + "\n")

    while True:
        try:
            cmd = input("You > ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["exit", "quit", "bye", "band karo"]:
                print("JARVIS > Goodbye Sir! Shutting down systems.")
                break

            result = brain.process_command(cmd)
            msg = result.get("message", "Action completed, Sir.")
            tool = result.get("tool", "none")
            print(f"JARVIS [{tool}] > {msg}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nJARVIS > Systems shutting down. Have a good day, Sir!")
            break

if __name__ == "__main__":
    main()
