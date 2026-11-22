# 🌸 Sakhi AI — Your Personal AI Voice Assistant

<p align="center">
  <strong>Your friendly AI companion for everyday life.</strong><br/>
  Talk naturally. Learn smarter. Stay organized. Feel supported.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/AI-Gemini-orange" alt="Gemini AI"/>
  <img src="https://img.shields.io/badge/Interface-Streamlit-red?logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Status-MVP-purple" alt="MVP"/>
</p>

---

## ✨ What is Sakhi AI?

**Sakhi AI** is a multilingual, voice-first personal AI assistant designed to make everyday digital tasks easier and more accessible.

It allows users to interact with an AI assistant using natural language and get help with learning, writing, productivity, digital safety, and everyday questions.

Instead of being just another chatbot, Sakhi AI aims to provide a friendly and useful experience through AI-powered conversations, voice interaction, and personal productivity tools.

**Our vision:** Make AI feel more accessible, helpful, and comfortable for everyone.

## 🎯 Problem We Are Solving

Many people find digital tools difficult to use, especially when they need quick assistance, personalized learning support, or help organizing daily activities.

Sakhi AI addresses this by bringing multiple everyday assistance features into one simple interface.

### 👥 Who Can Use Sakhi AI?

- Students who need study assistance and explanations.
- People who want help with everyday questions and writing.
- Users who prefer voice interaction.
- Individuals who want simple journaling and reminder management.
- Beginners who need guidance about digital safety.

## 🚀 MVP Features

| Feature | What it does |
|---|---|
| 🤖 AI Assistant | Answers questions and helps with everyday tasks using Gemini AI. |
| 🗣️ Voice Interaction | Supports voice input and spoken responses. |
| 🌐 Multilingual Conversations | Designed for Hindi, English, and Hinglish interactions. |
| 📚 Study Assistant | Helps with learning, explanations, and study-related questions. |
| 🛡️ Digital Safety | Provides educational guidance about online safety and suspicious digital activity. |
| 📝 Personal Journal | Allows users to write and save personal journal entries locally. |
| ⏰ Smart Reminders | Allows users to create and manage reminder entries. |
| 💬 Conversation Experience | Provides a friendly conversational interface. |

*Note: Features are part of the current MVP. Some capabilities depend on an internet connection and configured API services.*

## 🖥️ How Sakhi AI Works

1. The user enters a question or provides voice input.
2. The application processes the input.
3. The AI Assistant sends the request to Google's Gemini API.
4. Gemini generates a response based on the user's request and application instructions.
5. The response is displayed and, where supported, converted into speech.
6. Journal entries and reminder data can be stored locally.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Google Gemini API | AI-powered responses |
| Google Gen AI SDK | Gemini integration |
| SpeechRecognition | Speech input |
| gTTS | Text-to-speech generation |
| Pygame | Audio playback |
| Python-dotenv | Secure environment configuration |
| JSON | Local storage for journal and reminder data |

## 📂 Project Structure

```text
Jarvis-personal-ai-assistant/
│
├── app.py                  # Streamlit web application
├── sakhi_core.py           # Gemini AI integration
├── voice_assistant.py      # Continuous voice assistant
├── voice_engine.py         # Text-to-speech and audio engine
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes private and temporary files
├── .env                    # Private API key (create locally)
│
└── data/                   # Local journal and reminder data
```

## ⚙️ Installation & Setup

Follow these steps to run Sakhi AI on your computer.

### 1. Clone the Repository

Open PowerShell or the VS Code terminal:

```bash
git clone https://github.com/Jyoti33-kri/Jarvis-personal-ai-assistant.git
```

Move into the project folder:

```bash
cd Jarvis-personal-ai-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Gemini API Key

Sakhi AI uses the Google Gemini API for AI-powered responses.

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Create a file named `.env` in the project root.
3. Add the following line:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the example value with your own API key.

**Important:** Never upload your real API key or `.env` file to GitHub. Keep it private.

### 5. Run the Web Application

```bash
python -m streamlit run app.py
```

The application will open in your browser. If it does not open automatically, use the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 🎤 How to Use Sakhi AI

### A. AI Assistant

1. Open the Sakhi AI web application.
2. Navigate to the AI Assistant section.
3. Enter your question or message.
4. Submit it to receive an AI-generated response.
5. Use the available audio controls to listen to supported responses.

Example prompts:

- "Hi Sakhi, help me plan my day."
- "Explain artificial intelligence in simple English."
- "Mujhe Python loops samjhao."
- "Help me prepare a study timetable."
- "Write a professional email for me."

### B. Voice Interaction

The web application provides audio input through its available recording control.

For the continuous desktop voice assistant, open another terminal in the project directory, activate the virtual environment, and run:

```bash
python voice_assistant.py
```

Allow microphone access when prompted. Speak your command and follow the assistant's response.

### C. Study Assistant

1. Open the Study Assistant section.
2. Ask a study-related question.
3. Request a simple explanation, examples, or learning support.

Example:

```text
Explain the OSI model in simple language with examples.
```

### D. Digital Safety

1. Open the Digital Safety section.
2. Describe your online safety concern.
3. Ask for guidance about suspicious messages, links, or online behavior.

Sakhi AI provides educational guidance. It is not a live malware scanner or a replacement for professional cybersecurity services.

### E. My Journal

1. Open My Journal.
2. Write your personal entry.
3. Save it using the available application controls.
4. Your journal data is stored locally.

### F. Smart Reminders

1. Open Smart Reminders.
2. Enter a reminder.
3. Select the available date and time.
4. Save and manage your reminder entries.

**Reminder note:** The current MVP stores reminder information. It does not guarantee automatic notifications or alarms.

## 🧠 AI / ML Implementation

Sakhi AI integrates Google's Gemini generative AI model through the Google Gen AI SDK.

The AI component is designed to:
- Understand natural-language questions.
- Generate conversational responses.
- Support study, writing, productivity, and everyday assistance.
- Follow application-level instructions for a friendly multilingual experience.

The application uses a configured Gemini model in `sakhi_core.py`. AI responses require a valid API key and an internet connection.

## 🔐 Privacy & Safety

We believe personal assistance should be designed with privacy in mind.

- API keys are stored in a local `.env` file.
- The `.gitignore` file excludes private configuration and local JSON data.
- Journal and reminder data are stored locally by the current MVP.
- Users should avoid entering passwords, financial details, or highly sensitive personal information.
- AI-generated responses may contain mistakes. Users should verify important information.
- Digital Safety provides guidance, not guaranteed threat detection.

## 🧪 Testing & Validation

The following development checks have been performed:

| Check | Status |
|---|---|
| Python syntax compilation | Passed |
| Dependency installation | Completed |
| Streamlit application launch | Tested |
| Audio response interface | Tested |
| Gemini API response | Requires successful live verification |

The Gemini API connection should be verified with a valid key and working internet connection before treating the AI functionality as fully validated.

### Basic Manual Test Cases

| Test | Expected behavior |
|---|---|
| Normal text question | AI response is displayed |
| Hindi question | Assistant attempts a Hindi response |
| English question | Assistant attempts an English response |
| Hinglish question | Assistant attempts a Hinglish response |
| Empty input | User should provide a question |
| Missing or invalid API key | Application should handle the service error |
| Journal entry | Entry should be saved locally |
| Reminder entry | Reminder details should be stored |

## ⚠️ Current MVP Limitations

Sakhi AI is an early-stage MVP. Some limitations are:

- Gemini-powered responses require internet access.
- Speech recognition and text-to-speech may require internet access.
- Microphone performance depends on device permissions and audio quality.
- Reminder entries are stored but automatic scheduled alerts are not guaranteed.
- Digital Safety does not perform real-time website or malware scanning.
- AI-generated information may occasionally be inaccurate.
- The web and desktop voice experiences may not share all application data.

## 🔮 Future Scope

We plan to improve Sakhi AI with:

- More reliable multilingual voice conversations.
- Faster speech recognition and response generation.
- Automatic reminder notifications.
- Improved personalization and conversation memory controls.
- Better accessibility and user interface design.
- Real-time digital safety checks with appropriate security integrations.
- More extensive automated testing.
- Offline support for selected basic features.

## ▶️ Demo & Screenshots

Add your actual project screenshots and demo video link here before final submission.

Suggested screenshots:
1. Sakhi AI home/dashboard.
2. AI Assistant conversation.
3. Voice interaction.
4. Study Assistant.
5. Digital Safety.
6. Journal and Smart Reminders.

**Demo Video:** Add your public demo video link here.

## 📌 Hackathon Project Information

| Detail | Information |
|---|---|
| Project Name | Sakhi AI |
| Category | AI for Everyday Life |
| Project Type | AI-powered personal assistant |
| Development Stage | Minimum Viable Product (MVP) |
| Primary Language | Python |
| AI Integration | Google Gemini API |
| Interface | Streamlit |

## 🙌 Acknowledgements & Attribution

- Google Gemini API and Google Gen AI SDK for generative AI capabilities.
- Streamlit for the web application framework.
- Python community and the open-source libraries used in this project.

No external training dataset is claimed for this MVP. The project uses an external generative AI service for responses.

## 👩‍💻 Developer

**Jyoti Kumari**

GitHub: [@Jyoti33-kri](https://github.com/Jyoti33-kri)

Project Repository: [Sakhi AI — Jarvis Personal AI Assistant](https://github.com/Jyoti33-kri/Jarvis-personal-ai-assistant)

---

<p align="center">
  <strong>🌸 Sakhi AI — A smarter, friendlier companion for everyday life.</strong><br/>
  <em>Built with Python, AI, and the vision of making technology more accessible.</em>
</p>