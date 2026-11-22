
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pathlib import Path
from datetime import datetime, date
import json
import urllib.parse

from sakhi_core import ask_sakhi


# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Sakhi AI",
    page_icon="🌸",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

JOURNAL_FILE = DATA_DIR / "journal.json"
REMINDER_FILE = DATA_DIR / "reminders.json"


# =====================================================
# 2. STORAGE
# =====================================================

def load_data(path):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
    except Exception as error:
        print("Storage error:", error)

    return []


def save_data(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        print("Save error:", error)
        return False


# =====================================================
# 3. SESSION STATE
# =====================================================

defaults = {
    "messages": [],
    "language": "Auto",
    "speak_answers": True,
    "last_audio": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# 4. UI DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #101426, #202342);
    color: white;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #171827;
}

div.stButton > button {
    border-radius: 12px;
    min-height: 42px;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: #292d4d;
    border-radius: 14px;
    padding: 15px;
}

.hero {
    background: linear-gradient(120deg, #393568, #743d70);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.hero h1 {
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 5. LANGUAGE AND AUDIO
# =====================================================

def get_voice_language(text=""):

    selected = st.session_state.language

    if selected == "Hindi":
        return "hi"

    if selected == "English":
        return "en"

    if selected == "Hinglish":
        return "en"

    if any("\u0900" <= c <= "\u097F" for c in text):
        return "hi"

    return "en"


def make_audio(text):

    try:
        buffer = BytesIO()

        speech = gTTS(
            text=text,
            lang=get_voice_language(text),
            slow=False
        )

        speech.write_to_fp(buffer)
        buffer.seek(0)

        return buffer.getvalue()

    except Exception as error:
        print("Audio error:", error)
        return None


def speak_answer(answer):

    if not st.session_state.speak_answers:
        return

    audio = make_audio(answer)

    if audio:
        st.audio(audio, format="audio/mp3")


# =====================================================
# 6. GEMINI CONNECTION
# =====================================================

def ask_ai(message, history=None, extra_instruction=None):

    if extra_instruction:
        message = (
            extra_instruction
            + "\n\nUser request:\n"
            + message
        )

    return ask_sakhi(
        message,
        history=history or [],
        language=st.session_state.language
    )


# =====================================================
# 7. DIRECT ACTIONS
# =====================================================

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chatgpt.com",
    "instagram": "https://www.instagram.com"
}


def detect_action(message):

    text = message.lower().strip()

    # Open websites
    for name, url in WEBSITES.items():

        if text in [
            f"open {name}",
            f"{name} kholo",
            f"{name} khol do"
        ]:
            return {
                "type": "website",
                "name": name,
                "url": url
            }

    # Google search
    prefixes = [
        "search for ",
        "search ",
        "google "
    ]

    for prefix in prefixes:
        if text.startswith(prefix):
            query = message[len(prefix):].strip()

            if query:
                return {
                    "type": "search",
                    "query": query,
                    "url": (
                        "https://www.google.com/search?q="
                        + urllib.parse.quote(query)
                    )
                }

    # Music search
    music_phrases = [
        "play music",
        "play a song",
        "gaana chalao",
        "music chalao"
    ]

    for phrase in music_phrases:
        if phrase in text:

            query = text.replace(phrase, "").strip()
            if not query:
                query = "music"

            return {
                "type": "music",
                "query": query,
                "url": (
                    "https://www.youtube.com/results?search_query="
                    + urllib.parse.quote(query)
                )
            }

    # Time
    if any(word in text for word in [
        "what time",
        "current time",
        "time now",
        "kitne baje",
        "samay kya"
    ]):
        return {"type": "time"}

    # Date
    if any(word in text for word in [
        "today's date",
        "what is the date",
        "aaj ki date"
    ]):
        return {"type": "date"}

    # Journal
    journal_phrases = [
        "save in journal",
        "save to journal",
        "journal mein save",
        "meri diary mein likho"
    ]

    for phrase in journal_phrases:
        if phrase in text:
            content = message.lower().replace(phrase, "").strip()
            return {
                "type": "journal",
                "content": content
            }

    # Reminder
    reminder_phrases = [
        "remind me to",
        "save reminder",
        "reminder lagao",
        "yaad dilana"
    ]

    for phrase in reminder_phrases:
        if phrase in text:
            task = message.lower().replace(phrase, "").strip()
            return {
                "type": "reminder",
                "task": task
            }

    return None


# =====================================================
# 8. MESSAGE PROCESSOR
# =====================================================

def process_message(message):

    if not message or not message.strip():
        return

    message = message.strip()

    # Save previous conversation for Gemini
    history = st.session_state.messages[-8:]

    action = detect_action(message)

    answer = ""

    # Direct actions do not need Gemini
    if action:

        if action["type"] == "website":

            answer = (
                f"Sure! Open {action['name']} using the link below."
            )

            st.markdown(
                f"[Open {action['name'].title()}]({action['url']})"
            )

        elif action["type"] == "search":

            answer = "I found your search request. Open the search link below."

            st.markdown(
                f"[Search Google for {action['query']}]({action['url']})"
            )

        elif action["type"] == "music":

            answer = "I found music for you. Open YouTube using the link below."

            st.markdown(
                f"[Find {action['query']} on YouTube]({action['url']})"
            )

        elif action["type"] == "time":

            answer = (
                "The current time is "
                + datetime.now().strftime("%I:%M %p")
            )

        elif action["type"] == "date":

            answer = (
                "Today is "
                + datetime.now().strftime("%d %B %Y")
            )

        elif action["type"] == "journal":

            content = action["content"]

            if not content:
                answer = "Please tell me what you want to save in your journal."
            else:
                entries = load_data(JOURNAL_FILE)

                entries.append({
                    "date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                    "text": content
                })

                if save_data(JOURNAL_FILE, entries):
                    answer = "Your journal entry has been saved successfully."
                else:
                    answer = "I could not save your journal entry."

        elif action["type"] == "reminder":

            task = action["task"]

            if not task:
                answer = "Please tell me the task you want to remember."
            else:
                reminders = load_data(REMINDER_FILE)

                reminders.append({
                    "task": task,
                    "date": "",
                    "time": "",
                    "done": False
                })

                if save_data(REMINDER_FILE, reminders):
                    answer = "Your reminder task has been saved."
                else:
                    answer = "I could not save your reminder."

    else:

        # Normal conversation with Gemini
        with st.spinner("🌸 Sakhi is thinking..."):

            try:
                answer = ask_ai(
                    message,
                    history=history
                )

            except Exception as error:

                print("Gemini error:", error)

                st.error(
                    "Gemini is temporarily unavailable. "
                    "Please try again in a moment."
                )

                return

    # Store conversation
    st.session_state.messages.extend([
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer}
    ])

    st.session_state.messages = st.session_state.messages[-20:]

    # Display answer
    with st.chat_message("user"):
        st.write(message)

    with st.chat_message("assistant"):
        st.write(answer)
        speak_answer(answer)


# =====================================================
# 9. VOICE RECOGNITION
# =====================================================

def recognise_voice(audio_file, language):

    recognizer = sr.Recognizer()

    with sr.AudioFile(
        BytesIO(audio_file.getvalue())
    ) as source:

        audio = recognizer.record(source)

    code = "hi-IN" if language == "Hindi" else "en-IN"

    return recognizer.recognize_google(
        audio,
        language=code
    )


# =====================================================
# 10. SIDEBAR
# =====================================================

st.sidebar.title("🌸 Sakhi AI")
st.sidebar.caption("Your Everyday AI Companion")

page = st.sidebar.radio(
    "EXPLORE",
    [
        "Dashboard",
        "AI Assistant",
        "Digital Safety",
        "Study Assistant",
        "My Journal",
        "Smart Reminders",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.selectbox(
    "Response language",
    ["Auto", "English", "Hindi", "Hinglish"],
    key="language"
)

st.sidebar.checkbox(
    "Speak answers",
    key="speak_answers"
)

st.sidebar.divider()

st.sidebar.subheader("Quick Access")

for name, url in WEBSITES.items():

    st.sidebar.markdown(
        f"[Open {name.title()}]({url})"
    )

st.sidebar.divider()
st.sidebar.caption("Powered by Google Gemini AI")


# =====================================================
# 11. DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🌸 Welcome to Sakhi AI</h1>
        <p>Your intelligent companion for learning,
        safety, productivity and daily conversations.</p>
    </div>
    """, unsafe_allow_html=True)

    journal = load_data(JOURNAL_FILE)
    reminders = load_data(REMINDER_FILE)

    c1, c2, c3 = st.columns(3)

    c1.metric("Journal Entries", len(journal))
    c2.metric("Reminders", len(reminders))
    c3.metric("Messages", len(st.session_state.messages))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.info("🤖 AI Conversation\n\nAsk questions naturally.")
        st.info("📚 Study Assistant\n\nLearn coding and prepare for exams.")
        st.info("📖 Journal\n\nSave your thoughts.")

    with right:
        st.info("🛡️ Digital Safety\n\nAnalyse suspicious messages.")
        st.info("⏰ Reminders\n\nOrganise daily tasks.")
        st.info("🎙️ Voice Interaction\n\nSpeak and hear Sakhi.")

    st.divider()

    quick_question = st.text_input(
        "Ask Sakhi",
        placeholder="What can you help me with today?"
    )

    if st.button("Send to Sakhi", type="primary"):

        if quick_question.strip():
            process_message(quick_question)


# =====================================================
# 12. AI ASSISTANT
# =====================================================

elif page == "AI Assistant":

    st.title("🤖 Sakhi AI Assistant")
    st.caption("Your personal multilingual AI companion.")

    for item in st.session_state.messages:

        with st.chat_message(item["role"]):
            st.write(item["content"])

    message = st.chat_input("Message Sakhi...")

    if message:
        process_message(message)

    st.divider()

    st.subheader("🎙️ Voice Conversation")

    voice_language = st.selectbox(
        "Select your speaking language",
        ["English", "Hindi"],
        key="voice_language"
    )

    audio_file = st.audio_input("Record your question")

    if st.button("Understand My Voice", type="primary"):

        if audio_file is None:

            st.warning("Please record your voice first.")

        else:

            try:

                with st.spinner("Understanding your voice..."):

                    spoken_text = recognise_voice(
                        audio_file,
                        voice_language
                    )

                st.success("You said: " + spoken_text)

                process_message(spoken_text)

            except sr.UnknownValueError:

                st.error("I could not understand your voice.")

            except Exception as error:

                st.error("Voice recognition failed.")
                st.caption(str(error))

    if st.button("Clear Conversation"):

        st.session_state.messages = []
        st.rerun()


# =====================================================
# 13. DIGITAL SAFETY
# =====================================================

elif page == "Digital Safety":

    st.title("🛡️ Digital Safety Center")

    category = st.selectbox(
        "Choose what to analyse",
        [
            "Suspicious message",
            "Job offer",
            "Website or link",
            "Payment request",
            "Other"
        ]
    )

    content = st.text_area(
        "Paste the message or offer",
        height=170
    )

    if st.button("Analyse with Sakhi", type="primary"):

        if not content.strip():

            st.warning("Please enter the content.")

        else:

            instruction = (
                f"Act as a digital safety assistant. Analyse this "
                f"{category}. Explain warning signs, possible risks "
                "and safe next steps. Do not claim a link is safe "
                "without verification."
            )

            with st.spinner("Analysing..."):

                try:

                    answer = ask_ai(
                        content,
                        extra_instruction=instruction
                    )

                    st.subheader("Safety Report")
                    st.write(answer)
                    speak_answer(answer)

                except Exception as error:

                    st.error("Analysis failed.")
                    st.caption(str(error))

    st.divider()

    st.subheader("Safety Tips")

    st.write("🔒 Never share OTPs, passwords or PINs.")
    st.write("🔗 Avoid unknown links.")
    st.write("💼 Verify job offers before paying.")
    st.write("🏦 Use official banking websites.")


# =====================================================
# 14. STUDY ASSISTANT
# =====================================================

elif page == "Study Assistant":

    st.title("📚 Study Assistant")

    subject = st.selectbox(
        "Select subject",
        [
            "Artificial Intelligence",
            "Computer Networks",
            "Python",
            "Java",
            "Web Development",
            "Database Management",
            "Other"
        ]
    )

    style = st.selectbox(
        "Choose answer format",
        [
            "Simple explanation",
            "Exam answer - 5 to 6 marks",
            "Step-by-step coding",
            "Short revision notes",
            "MCQs with answers"
        ]
    )

    question = st.text_area(
        "Enter your question",
        height=140
    )

    if st.button("Generate Answer", type="primary"):

        if not question.strip():

            st.warning("Enter a question first.")

        else:

            instruction = (
                f"You are a friendly tutor. Subject: {subject}. "
                f"Format: {style}. Use simple English, keywords "
                "and examples where useful."
            )

            with st.spinner("Preparing your answer..."):

                try:

                    answer = ask_ai(
                        question,
                        extra_instruction=instruction
                    )

                    st.subheader("Your Answer")
                    st.write(answer)
                    speak_answer(answer)

                except Exception as error:

                    st.error("Could not generate answer.")
                    st.caption(str(error))


# =====================================================
# 15. JOURNAL
# =====================================================

elif page == "My Journal":

    st.title("📖 My Personal Journal")

    journal = load_data(JOURNAL_FILE)

    note = st.text_area(
        "Write your thoughts",
        height=150
    )

    if st.button("Save Journal Entry", type="primary"):

        if note.strip():

            journal.append({
                "date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                "text": note
            })

            if save_data(JOURNAL_FILE, journal):

                st.success("Journal entry saved.")
                st.rerun()

        else:

            st.warning("Write something first.")

    st.divider()

    st.subheader("Saved Entries")

    for entry in reversed(journal):

        with st.expander(entry.get("date", "Journal entry")):
            st.write(entry.get("text", ""))


# =====================================================
# 16. SMART REMINDERS
# =====================================================

elif page == "Smart Reminders":

    st.title("⏰ Smart Reminders")

    reminders = load_data(REMINDER_FILE)

    task = st.text_input("What should I remind you about?")

    reminder_date = st.date_input(
        "Date",
        value=date.today()
    )

    reminder_time = st.time_input("Time")

    if st.button("Add Reminder", type="primary"):

        if task.strip():

            reminders.append({
                "task": task,
                "date": str(reminder_date),
                "time": reminder_time.strftime("%I:%M %p"),
                "done": False
            })

            if save_data(REMINDER_FILE, reminders):

                st.success("Reminder saved.")
                st.rerun()

        else:

            st.warning("Enter a reminder task.")

    st.divider()

    st.subheader("Your Reminders")

    for index, item in enumerate(reminders):

        col1, col2 = st.columns([5, 1])

        with col1:

            done = st.checkbox(
                f"{item.get('task', 'Task')} | "
                f"{item.get('date', '')} | "
                f"{item.get('time', '')}",
                value=item.get("done", False),
                key=f"reminder_{index}"
            )

            if done != item.get("done", False):

                reminders[index]["done"] = done
                save_data(REMINDER_FILE, reminders)

        with col2:

            if st.button("Delete", key=f"delete_{index}"):

                reminders.pop(index)
                save_data(REMINDER_FILE, reminders)
                st.rerun()


# =====================================================
# 17. ABOUT
# =====================================================

elif page == "About":

    st.title("🌸 About Sakhi AI")

    st.write("""
    Sakhi AI is a multilingual personal AI assistant.

    FEATURES

    - Gemini AI conversation
    - English, Hindi and Hinglish interaction
    - Voice input and spoken answers
    - Digital safety analysis
    - Study and coding assistant
    - Personal journal
    - Smart reminders
    - Website shortcuts

    TECHNOLOGY

    - Python
    - Streamlit
    - Google Gemini API
    - SpeechRecognition
    - Google Text-to-Speech
    - JSON storage

    SAFETY

    Never enter passwords, OTPs, PINs or confidential
    banking information into this prototype.
    """)

    st.info(
        "Sakhi AI is a prototype. Safety analysis is educational "
        "and does not replace professional security advice."
    )


# =====================================================
# 18. FOOTER
# =====================================================

st.sidebar.divider()
st.sidebar.caption("🌸 Sakhi AI | Your Everyday AI Companion")
