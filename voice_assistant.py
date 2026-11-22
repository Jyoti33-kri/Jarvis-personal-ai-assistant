
import time
import datetime
import urllib.parse
import webbrowser
import json
from pathlib import Path

import speech_recognition as sr

from sakhi_core import ask_sakhi
from voice_engine import speak


# ---------------- CONFIGURATION ----------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

JOURNAL_FILE = DATA_DIR / "journal.json"
REMINDER_FILE = DATA_DIR / "reminders.json"

LANGUAGE = "auto"

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.65
recognizer.non_speaking_duration = 0.4

history = []
pending_reminder = False


# ---------------- STORAGE ----------------

def load_data(file_path):

    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

    except Exception as error:
        print("Storage error:", error)

    return []


def save_data(file_path, data):

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True

    except Exception as error:
        print("Save error:", error)
        return False


def save_journal(text):

    entries = load_data(JOURNAL_FILE)

    entries.append({
        "text": text,
        "date": datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })

    return save_data(JOURNAL_FILE, entries)


def save_reminder(text):

    reminders = load_data(REMINDER_FILE)

    reminders.append({
        "task": text,
        "date": "",
        "time": "",
        "done": False
    })

    return save_data(REMINDER_FILE, reminders)


# ---------------- VOICE INPUT ----------------

def listen():

    try:

        with sr.Microphone() as source:

            print("\nListening... Speak naturally.")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=12
            )

        # Try English recognition first.
        try:

            return recognizer.recognize_google(
                audio,
                language="en-IN"
            ).strip()

        except sr.UnknownValueError:

            return recognizer.recognize_google(
                audio,
                language="hi-IN"
            ).strip()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        print("I couldn't understand. Please speak again.")
        return ""

    except Exception as error:
        print("Microphone error:", error)
        return ""


# ---------------- WEBSITE ACTIONS ----------------

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chatgpt.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com"
}


def open_website(name):

    url = WEBSITES.get(name)

    if url:
        webbrowser.open(url)
        speak(f"Opening {name}.")
        return True

    return False


# ---------------- QUICK ACTIONS ----------------

def handle_quick_action(message):

    global pending_reminder

    text = message.lower().strip()

    # Stop assistant
    stop_words = [
        "stop assistant",
        "stop sakhi",
        "exit assistant",
        "goodbye",
        "band ho jao",
        "shutdown sakhi"
    ]

    if any(word in text for word in stop_words):

        speak("Goodbye! Have a wonderful day.")
        return False, True

    # Pending reminder
    if pending_reminder:

        if save_reminder(message):

            speak("Your reminder has been saved.")

        else:

            speak("Sorry, I could not save your reminder.")

        pending_reminder = False
        return True, True

    # Open websites
    for name in WEBSITES:

        if (
            f"open {name}" in text
            or f"{name} kholo" in text
            or f"{name} khol do" in text
        ):

            open_website(name)
            return True, True

    # Time
    if any(word in text for word in [
        "what time",
        "current time",
        "time now",
        "samay kya",
        "kitne baje"
    ]):

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak("The current time is " + current_time)
        return True, True

    # Date
    if any(word in text for word in [
        "today's date",
        "what is the date",
        "current date",
        "aaj ki date",
        "aaj kya date"
    ]):

        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak("Today is " + today)
        return True, True

    # Google search
    search_prefixes = [
        "search for ",
        "search ",
        "google ",
        "find "
    ]

    for prefix in search_prefixes:

        if text.startswith(prefix):

            query = message[len(prefix):].strip()

            if query:

                speak("Searching Google.")

                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(query)
                )

                webbrowser.open(url)

            return True, True

    # Play music
    if any(word in text for word in [
        "play music",
        "play a song",
        "gaana chalao",
        "music chalao"
    ]):

        query = message.lower()

        for word in [
            "play music",
            "play a song",
            "gaana chalao",
            "music chalao"
        ]:
            query = query.replace(word, "")

        query = query.strip()

        if not query:
            query = "music"

        url = (
            "https://www.youtube.com/results?search_query="
            + urllib.parse.quote(query)
        )

        speak("Finding music for you.")
        webbrowser.open(url)

        return True, True

    # Save journal
    journal_triggers = [
        "save in journal",
        "save to journal",
        "save my thought",
        "journal mein save",
        "meri diary mein likho",
        "diary mein save"
    ]

    for trigger in journal_triggers:

        if trigger in text:

            content = text.replace(trigger, "").strip()

            if content and save_journal(content):

                speak("I have saved your thought in your journal.")

            else:

                speak("Please tell me what you want to save.")

            return True, True

    # Save reminder
    reminder_triggers = [
        "remind me to",
        "remind me",
        "set a reminder",
        "reminder lagao",
        "yaad dilana",
        "mujhe yaad dilana"
    ]

    for trigger in reminder_triggers:

        if trigger in text:

            task = text.replace(trigger, "").strip()

            if task:

                if save_reminder(task):
                    speak("Your reminder task has been saved.")

                else:
                    speak("I could not save your reminder.")

            else:

                pending_reminder = True
                speak("What should I remind you about?")

            return True, True

    return True, False


# ---------------- AI CONVERSATION ----------------

def talk_to_sakhi(message):

    global history

    start_time = time.time()

    try:

        answer = ask_sakhi(
            message,
            history=history,
            language=LANGUAGE
        )

        history.append({
            "role": "user",
            "content": message
        })

        history.append({
            "role": "model",
            "content": answer
        })

        history = history[-10:]

        elapsed = time.time() - start_time

        print("\nSakhi:", answer)
        print(f"\nResponse generated in {elapsed:.2f} seconds")

        speak(answer)

    except Exception as error:

        print("AI error:", error)
        speak("Sorry, I am having trouble right now. Please try again.")


# ---------------- MAIN ASSISTANT ----------------

def main():

    speak(
        "Hello! I am Sakhi, your personal AI assistant. "
        "You can speak to me naturally in English, Hindi or Hinglish. "
        "How can I help you today?"
    )

    print("\n===================================")
    print("       SAKHI AI ASSISTANT")
    print("===================================")
    print("Speak naturally.")
    print("Say stop Sakhi to exit.")
    print("===================================")

    running = True

    while running:

        message = listen()

        if not message:
            continue

        print("\nYou:", message)

        running, handled = handle_quick_action(message)

        if not running:
            break

        if not handled:
            talk_to_sakhi(message)


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nSakhi stopped.")
