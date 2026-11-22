
import os
import re
import time
import tempfile
import pygame
from gtts import gTTS


def detect_language(text):

    # Devanagari script
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"

    # Bengali
    if re.search(r"[\u0980-\u09FF]", text):
        return "bn"

    # Gujarati
    if re.search(r"[\u0A80-\u0AFF]", text):
        return "gu"

    # Tamil
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "ta"

    # Telugu
    if re.search(r"[\u0C00-\u0C7F]", text):
        return "te"

    # Kannada
    if re.search(r"[\u0C80-\u0CFF]", text):
        return "kn"

    # Malayalam
    if re.search(r"[\u0D00-\u0D7F]", text):
        return "ml"

    # Roman text default
    return "en"


def create_audio(text, language=None):

    if not text or not text.strip():
        return None

    lang = language or detect_language(text)

    audio = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    audio_path = audio.name
    audio.close()

    try:
        speech = gTTS(
            text=text,
            lang=lang,
            slow=False
        )

        speech.save(audio_path)

        return audio_path

    except Exception:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise


def speak(text, language=None):

    print("\nSakhi:", text, flush=True)

    audio_path = None

    try:
        audio_path = create_audio(text, language)

        if not audio_path:
            return

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

    except Exception as error:
        print("Voice playback error:", error)

    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                pass
