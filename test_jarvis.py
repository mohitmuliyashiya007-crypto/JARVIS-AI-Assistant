"""
Automated Verification for JARVIS
"""

from jarvis_brain import JarvisBrain

def test():
    brain = JarvisBrain()
    test_queries = [
        "Google meet start karo",
        "Play Believer on YouTube",
        "Open Notepad",
        "Take a screenshot",
        "Delhi ka mausam kaisa hai",
        "System status kya hai",
        "Tum kaun ho"
    ]

    print("\n--- RUNNING JARVIS TEST SUITE ---")
    for q in test_queries:
        res = brain.process_command(q)
        print(f"Query: '{q}'\n  -> Tool: [{res.get('tool')}]\n  -> Output: {res.get('message')}\n")
    print("--- ALL TESTS COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    test()
