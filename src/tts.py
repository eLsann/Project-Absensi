import threading
import tempfile
import os
from gtts import gTTS
import pygame

# ===============================
# INIT AUDIO SEKALI
# ===============================
pygame.mixer.init()


def speak(text: str):
    """
    Text-to-Speech Bahasa Indonesia
    Tanpa menyimpan file permanen
    """

    def _run():
        temp_file = None
        try:
            # Buat file audio sementara
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_file = fp.name

            # Generate suara
            tts = gTTS(text=text, lang="id", slow=False)
            tts.save(temp_file)

            # Play audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Tunggu sampai selesai
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.stop()

        except Exception as e:
            print("[TTS ERROR]", e)

        finally:
            # Pastikan file DIHAPUS
            try:
                if temp_file and os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass

    threading.Thread(target=_run, daemon=True).start()
