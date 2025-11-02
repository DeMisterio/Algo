import pyaudio
import wave
import dateparser
from datetime import datetime
from CommonUtil import tellhim, read_key_from_JSON
from Kernel_F.user import userbase
User = userbase()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.mp3"

def recorder(lengh=None):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    if lengh == None:
        tellhim("For how long?")
        RECORD_SECONDS = User.get_message()
        tokens = RECORD_SECONDS.lower().split()
        parsed_date = None
        for i in range(len(tokens)):
            phrase = " ".join(tokens[i:])
            parsed = dateparser.parse(phrase, languages=['en'])
            if parsed:
                parsed_date = parsed
                date_phrase = phrase
                break
        if date_phrase:
            now = datetime.now()
            delta = date_phrase - now
            RECORD_SECONDS = delta.total_seconds()
        else:
            RECORD_SECONDS=10
            tellhim("I will be recording your voice for 10 seconds, starting now!")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    tellhim("How shall i name the file?")
    WAVE_OUTPUT_FILENAME = User.get_message()
    system = read_key_from_JSON("System")
    import os
    if system in ["Windows", "Darwin", "Linux"]:
        if system == "Windows":
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        elif system == "Darwin":  # macOS
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        elif system == "Linux":
            # На некоторых системах может быть "Рабочий стол" или "Desktop"
            # Попробуем стандартный путь
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            # Если папки нет, можно использовать локализованное имя (опционально)
            if not os.path.exists(desktop_path):
                # Например, в русской локали: "Рабочий стол"
                localized_desktop = os.path.join(os.path.expanduser("~"), "Рабочий стол")
                if os.path.exists(localized_desktop):
                    desktop_path = localized_desktop
                else:
                    # Если ничего нет — создаём на всякий случай в домашней директории
                    desktop_path = os.path.expanduser("~")
        tellhim("Your file has been saved in on your desktop!")
    else:
        # Если система не распознана — сохраняем в текущую директорию
        desktop_path = "."
        tellhim("Your file has been saved in the programms folder! (inside of the Processing Files)")
    # Полный путь к файлу
    output_path = os.path.join(desktop_path, WAVE_OUTPUT_FILENAME)

    # Запись WAV-файла
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return "S"

recorder()