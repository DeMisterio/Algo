import difflib, re, AlgoParser, random, sys, time, json, numpy
import asyncio
import os
import edge_tts
import deepl
import csv
import whisper
import webrtcvad
import pyaudio
import collections
import wave
import scipy.io.wavfile as wav
import tempfile
import numpy as np
auth_key = "40c1009b-ddf3-44bf-914d-0c6ca1adf429:fx"  # Replace with your key
deepl_client = deepl.DeepLClient(auth_key)
from faster_whisper import WhisperModel
import os

# Find the exact path to the model
# model = whisper.load_model("small")
def record_until_silence_vad():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    FRAME_DURATION = 30  # ms
    FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
    FRAME_BYTES = FRAME_SIZE * 2
    SILENCE_FRAMES = int(1.0 * 1000 / FRAME_DURATION)

    vad = webrtcvad.Vad(2)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=FRAME_SIZE)

    frames = []
    ring_buffer = collections.deque(maxlen=SILENCE_FRAMES)
    recording = False
    print("\n\n🎤 Говори...")
    try:
        while True:
            frame = stream.read(FRAME_SIZE)
            is_speech = vad.is_speech(frame, RATE)

            if is_speech:
                if not recording:
                    if Debugstat:
                        print("🔴 Запись началась")
                    recording = True
                ring_buffer.clear()
                frames.append(frame)
            else:
                if recording:
                    ring_buffer.append(frame)
                    if len(ring_buffer) == SILENCE_FRAMES:
                        if Debugstat:
                            print("🛑 Тишина обнаружена, остановка записи.")
                        frames.extend(ring_buffer)
                        break
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    filename = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    if Debugstat:
        print("🎙️ Аудио сохранено:", filename)
    return filename

def save_to_wav(audio_data, sample_rate):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    if Debugstat:
        print("🎙Сохраняю файл речи...")
    wav.write(temp_file.name, sample_rate, (audio_data * 32767).astype(np.int16))
    if Debugstat:
        print("🎙 Файл речи сохранен...")
    return temp_file.name

def transcribe(audio_path):
    if Debugstat:
        print("🎙 Анализирую речь...")

    segments, info = model.transcribe(audio_path)
    full_text = " ".join([segment.text for segment in segments])
    language = getattr(info, "language", "en")
    return language, full_text

def find_shortname(csv_file, target_locale, target_gender):
    target_locale = target_locale.lower()
    target_gender = target_gender.lower()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parts = (row["Language"].lower()).split("-", 1)
            rowp2 = parts[0].strip()
            if (row['Language'].lower() == target_locale or rowp2.lower() == target_locale) and row['Gender'].lower() == target_gender:
                return row['ShortName']
    return None


def lang_validation(origin_text, Retell_lang="EN-US"):
    if Retell_lang.upper() == "EN":
        Retell_lang = "EN-US"
    try:
        result = deepl_client.translate_text(origin_text, target_lang=Retell_lang)
        return result.text
    except Exception as e:
        print(f"[ERROR: Translation failed] {e}")
        return origin_text  # fallback to original
def lang_detection(origin_text):
    translated = deepl_client.translate_text(origin_text, target_lang="EN-US")
    return translated.detected_source_lang
decidion_completed = False  
def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()
async def main(infov, UnameV, entryV, intro_phraseV, purpose, language):
    if purpose == "retell":
        tts = edge_tts.Communicate(text=(infov), voice=language)
    elif purpose == "ask":
        tts = edge_tts.Communicate(text=(infov + "," + entryV + UnameV + "?"), voice=language)
    await tts.save("output.mp3")

def tellhim(text, speed=0.03):
    entry, intro_phrase = user_info_giver()
    Umode = read_key_from_JSON('Umode')
    Ulang = read_key_from_JSON('Ulang')
    if Umode == "Voice":
        csv_path = 'voices_parsed.csv'
        lang_code = Ulang
        if lang_code.upper() == "EN":
            lang_code = "EN-US"
        elif not lang_code.upper().startswith("EN-") and lang_code.upper().startswith("EN"):
            lang_code = "EN-US"  # safety against EN-GARBAGE

        text = lang_validation(text, lang_code) # твой CSV файл
        speak_lang = find_shortname(csv_path, Ulang, Ugender)
        asyncio.run(main(text, Uname, entry, intro_phrase, "retell", speak_lang))
        os.system("afplay output.mp3")
    if Umode == "Chat":
        text = lang_validation(text, (Ulang if Ulang != "EN" else Ulang + "-US"))
        for char in str(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)

def safe_load_json(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # Файл битый или пустой — пересоздаем дефолтный конфиг
        config = {"Debug": False}
        with open(filepath, "w") as file:
            json.dump(config, file, indent=4)
        return config
    
def read_key_from_JSON(key, filename="config.json"):
    try:
        with open(filename, "r") as file:
            config = json.load(file)
        return config.get(key, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
def tryingtoreach(items, text):
    global best_match_item, best_match_word, guessed
    max_similarity = 0
    best_match_item = None
    best_match_word = None
    guessed = None

    for item in items:
        for word in text.split():
            similarity = get_similarity(item, word)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_item = item
                best_match_word = word
                guessed = best_match_word
                return best_match_item, best_match_word, guessed
            
def AgreeDisagreeProcessing(wherefrom):
        global response, agree, disagree, decidion_completed
        Umode = read_key_from_JSON('Umode')
        if Umode == "Chat":
            response = input("Your response: ").strip()
        else:
            audio_path = record_until_silence_vad()
            if Debugstat:
                print("🛑 Закончил слушать. Обрабатываю...")
            file_path = audio_path
            try:
                language, message = transcribe(file_path)
            except Exception as e:
                if Debugstat:
                    print(f"⚠️ Ошибка при транскрипции: {e}")
                language = "EN"
                message = ""
            origin_lang_message = message
            if Debugstat:
                print(f"до перевода: {origin_lang_message}")
            response = lang_validation(message)
        if isinstance(response, str):
            response = response.strip().lower()
            if response.endswith('.'):
                response = response[:-1]
        agree = re.search(AlgoParser.Agrementpattern, response, re.IGNORECASE)
        disagree = re.search(AlgoParser.DisagreementPattern, response, re.IGNORECASE)
        return agree is not None, disagree is not None

def sayhello():
        tellhim(f"{random.choice(AlgoParser.listofgreetings)}" + "!")
        return

def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()

Debugstat = read_key_from_JSON("Debug")
Uname = read_key_from_JSON( "Uname")
Uage = read_key_from_JSON("Uage")
Ugender = read_key_from_JSON('Ugender')
Umode = read_key_from_JSON("Umode")
if Debugstat:
    print("* CommonUtil has successfully loaded!")
if Umode == "Voice":
    model_path = os.path.expanduser("~/.cache/huggingface/hub/models--Systran--faster-whisper-small")

    # Try loading with the full path
    try:
        model = WhisperModel(model_path, device="cpu", compute_type="int8")
    except Exception as e:
        print(f"Error: {e}")

def user_info_giver():
    if Uage > 30:
        if Ugender.lower() == "male":
            random_entry_selection = random.randint(0,1)
            if random_entry_selection == 0:
                entry = numpy.random.choice(AlgoParser.entry_titles["formal_older_men"])
            else:
                entry = numpy.random.choice(AlgoParser.entry_titles["neutral_men"])
        if Ugender.lower() == "woman":
            random_entry_selection = random.randint(0,1)
            if random_entry_selection == 0:
                entry = numpy.random.choice(AlgoParser.entry_titles["formal_older_women"])
            else:
                entry = numpy.random.choice(AlgoParser.entry_titles["neutral_women"])
        else:
            entry = numpy.random.choice(AlgoParser.entry_titles["neutral_men"])
    elif Uage < 30 or Uage == 30:
        if Ugender.lower() == "male":
            random_entry_selection = random.randint(0,1)
            if random_entry_selection == 0:
                entry = numpy.random.choice(AlgoParser.entry_titles["informal_young_men"])
            else:
                entry = numpy.random.choice(AlgoParser.entry_titles["neutral_men"])
        if Ugender.lower() == "woman":
            random_entry_selection = random.randint(0,1)
            if random_entry_selection == 0:
                entry = numpy.random.choice(AlgoParser.entry_titles["informal_young_women"])
            else:
                entry = numpy.random.choice(AlgoParser.entry_titles["neutral_women"])
        else:
            entry = numpy.random.choice(AlgoParser.entry_titles["neutral_men"])
    inro_phrase = numpy.random.choice(AlgoParser.entry_titles["intro_phrases"])
    return entry, inro_phrase