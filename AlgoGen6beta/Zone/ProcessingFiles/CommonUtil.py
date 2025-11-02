import difflib, re, AlgoParser, random, sys, time, json, numpy
import asyncio
import os
import shutil
import edge_tts
import deepl
import csv
import webrtcvad
import pyaudio
import requests
import pycountry
import subprocess
import collections
import wave
from pathlib import Path
import time
import scipy.io.wavfile as wav
import tempfile
import numpy as np
auth_key = "40c1009b-ddf3-44bf-914d-0c6ca1adf429:fx"  # Replace with your key
deepl_client = deepl.DeepLClient(auth_key)
from faster_whisper import WhisperModel
import os
ModelS_Path = Path("paraphrase-MiniLM-L6-v2")
from sentence_transformers import SentenceTransformer, util
modelS = SentenceTransformer(str(ModelS_Path))
from Kernel_F.user import userbase
User = userbase()
# Find the exact path to the model
modelW = None

COLOR_BLUE         = "\033[34m"
COLOR_YELLOW       = "\033[33m"
COLOR_ORANGE       = "\033[38;5;208m"
COLOR_GREEN        = "\033[32m"
COLOR_INFO         = "\033[96m"
COLOR_LIGHT_BLUE   = "\033[94m"
COLOR_RESET        = "\033[0m"

def set_modelW(model):
    global modelW
    modelW = model


def read_key_from_JSON(key, filename="config.json"):
    try:
        with open(filename, "r") as file:
            config = json.load(file)
        return config.get(key, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
def play_sound(Path):
    try:
        if read_key_from_JSON("System") == 'Windows':
            import pygame
            import time
            
            pygame.mixer.init()
            pygame.mixer.music.load(Path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        else:
            os.system(f"afplay {Path}")
    except Exception as e:
        print(f"⚠️ Ошибка воспроизведения: {e}")
def clean_response(text):
    text = text.lower().strip()
    return text[:-1] if text.endswith('.') else text


def record_until_silence_vad(train=False):
    NO_SPEACH = False
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    FRAME_DURATION = 30  # ms
    FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
    FRAME_BYTES = FRAME_SIZE * 2
    SILENCE_FRAMES = int(1.0 * 1000 / FRAME_DURATION)
    try:
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
        # play_sound("Bot_activation.mp3")
        print("\n\n🎤 Говори...")

        try:
            silence_start = None  # момент начала тишины
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
                    silence_start = None  # сброс, так как речь есть
                else:
                    if recording:
                        if silence_start is None:
                            silence_start = time.time()  # фиксируем начало тишины

                        ring_buffer.append(frame)

                        # условие: накопилась "техническая" тишина
                        if len(ring_buffer) == SILENCE_FRAMES:
                            if Debugstat:
                                print("🛑 Тишина обнаружена, остановка записи.")
                            frames.extend(ring_buffer)
                            break

                        # условие: прошло больше 3 секунд без речи
                        if time.time() - silence_start >= 3:
                            if Debugstat:
                                print("🛑 3 секунды без речи, остановка записи.")
                            frames.extend(ring_buffer)
                            NO_SPEACH = True
                            break
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
        if NO_SPEACH == True:
            return "RE"
        if train == False:
            filename = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        else:
            import os
            # Получаем путь к папке, где находится текущий скрипт
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Добавляем к нему папку WWD_DB
            wwd_db_path = os.path.join(base_dir, "WWD_DB")
            from datetime import datetime

            now = datetime.now()
            filename = now.strftime("audio_%Y%m%d_%H%M%S_%f.wav")
            filename = os.path.join(wwd_db_path, filename)
            if not os.path.exists(wwd_db_path):
                os.makedirs(wwd_db_path)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        if Debugstat:
            print("🎙️ Аудио сохранено:", filename)
        return filename
    except Exception as e:
        print(f"⚠️ Ошибка записи: {e}")
        return "RE"



def save_to_wav(audio_data, sample_rate):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    if Debugstat:
        print("🎙Сохраняю файл речи...")
    try:
        wav.write(temp_file.name, sample_rate, (audio_data * 32767).astype(np.int16))
    except Exception as e:
        print(f"⚠️ Ошибка сохранения WAV: {e}")
    if Debugstat:
        print("🎙 Файл речи сохранен...")
    return temp_file.name

def transcribe(audio_path):
    try:
        if Debugstat:
            print("🎙 Анализирую речь...")
        segments, info = modelW.transcribe(audio_path)
        full_text = " ".join([segment.text for segment in segments])
        language = getattr(info, "language", "en")
        return language, full_text
    except Exception as e:
        print(f"⚠️ Ошибка транскрипции: {e}")
        return "ERROR", ""

def find_shortname(csv_file, target_locale, target_gender):
    target_locale = target_locale.lower()
    target_gender = target_gender.lower()
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parts = (row["Language"].lower()).split("-", 1)
                rowp2 = parts[0].strip()
                if (row['Language'].lower() == target_locale or rowp2.lower() == target_locale) and row['Gender'].lower() == target_gender:
                    return row['ShortName']
    except Exception as e:
        print(f"⚠️ Ошибка при поиске shortname: {e}")
    return None


def is_stop_command(user_input: str, threshold: float = 0.75) -> bool:
    try:
        user_embedding = modelW.encode(user_input, convert_to_tensor=True)
        similarity_scores = util.cos_sim(user_embedding, stop_embeddings)[0]
        max_score = similarity_scores.max().item()
        print(f"🧠 Similarity score: {max_score:.3f}")
        return max_score >= threshold
    except Exception as e:
        print(f"⚠️ Ошибка проверки стоп-команды: {e}")
        return False

def Check_INTERNET_CONNECTION(host='8.8.8.8', port=53, timeout=3):
    try:
        import socket
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print(f"⚠️ Ошибка проверки соединения: {e}")
        return False
       
def safe_libre_translate(text, target='en', source='auto', url='https://libretranslate.de/translate'):
    import requests
    try:
        payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
        }
        response = requests.post(url, json=payload, timeout=2)
        response.raise_for_status() # Проверка HTTP-кода (200 OK)
        result = response.json()
        return result.get("translatedText", "")
    except requests.RequestException as e:
        print(f"⚠️ Ошибка перевода LibreTranslate: {e}")
        return None # Или вернуть исходный текст, или None, как удобнее
def empty_folder(folder_path):
    """
    Empties the specified folder by deleting all its contents (files and subdirectories).
    The folder itself remains.
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)  # Remove file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory and its contents
        except OSError as e:
            print(f"Error deleting '{item_path}': {e}")

def lang_validation(origin_text, Retell_lang="EN-US"):
    if Check_INTERNET_CONNECTION():
        if Retell_lang.upper() == "EN":
            Retell_lang = "EN-US"
        try:
            if read_key_from_JSON('Ucountry') != "RU":
                result = deepl_client.translate_text(origin_text, target_lang=Retell_lang)
                return result.text
            else:
                pass # Тут остановился 
        except Exception as e:
            print("Looks like the deepl is not supported in your country or so....")
            print(f"⚠️ Ошибка DeepL перевода: {e}")
            if Check_INTERNET_CONNECTION():
                if read_key_from_JSON('Ucountry') != "Russia":
                    print("I will try to translate using the LibreTranslate...")
                    result = safe_libre_translate(origin_text)
                    if result is not None:
                        return result
                    else:
                        return "INTERNET_ERROR"
    else:
        return "INTERNET_ERROR"

def lang_detection(origin_text):
    try:
        if Debugstat is True:
            print("Detecting your language using Deepl...")
        langdetected = deepl_client.translate_text(origin_text, target_lang="EN-US")
        if Debugstat is True:
            print(f"Detected language using Deepl: {langdetected.detected_source_lang}")
        if langdetected != "INTERNET_ERROR":
            return langdetected.detected_source_lang
        else:
            from langdetect import detect
            text = origin_text.strip()
            if text:
                langdetected = detect(text).upper()
                if Debugstat is True:
                    print(f"Detected language: {langdetected}")
                return langdetected
    except Exception as e:
        print(f"⚠️ Ошибка Deepl detection: {e}")
        try:
            if Debugstat is True:
                print("Detecting your language lang detect...")
            from langdetect import detect
            text = origin_text.strip()
            langdetected = detect(text).upper()
            if Debugstat is True:
                print(f"Detected language: {langdetected}")
            return langdetected
        except Exception:
            print("⚠️ Ошибка langdetect")
            pass
    return 'Unsuccessful'
decidion_completed = False  
def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()
async def main(infov, UnameV, entryV, intro_phraseV, purpose, language):
    if purpose == "retell":
        tts = edge_tts.Communicate(text=(infov), voice=language)
    elif purpose == "ask":
        tts = edge_tts.Communicate(text=(infov + "," + entryV + UnameV + "?"), voice=language, output_format="riff-24khz-16bit-mono-pcm" )
    try:
        await tts.save("output.mp3")
    except Exception as e:
        print(f"⚠️ Ошибка TTS сохранения: {e}")
def config_restore():
    for attempt in range(10):
        try:
            time.sleep(1)
            Uage = int(input(f"\n\n{COLOR_INFO}ℹ️ \n\nFirst of all, could you type your age? Please be honest, this does affect your usage experience (No limitations): {COLOR_RESET}"))
            if 0 < Uage <= 140:
                break
            else:
                print(f"{COLOR_ORANGE}❌ Please enter a realistic age (1-140).{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_ORANGE}❌ That's not a number, digits only.{COLOR_RESET}")
    else:
        print(f"{COLOR_ORANGE}❌ Access to program restricted.{COLOR_RESET}")
        quit()
    time.sleep(1)
    Uname = input(f"{COLOR_INFO}ℹ️ {'Okay! Now I need your name' if Uage <= 18 else 'Please type your name:'} {COLOR_RESET}")
    time.sleep(1)
    Ugender = input(f"{COLOR_INFO}ℹ️ {Uname}, {'what is your gender/sex? (Male / Female)' if Uage <= 18 else 'please enter your gender/sex (Male / Female):'} {COLOR_RESET}")
    time.sleep(1)
    Ubotreference = input(f"{COLOR_INFO}ℹ️ {'Okay! Please give me any name you want:' if Uage <= 18 else 'Please say, how do you want to call this bot?'} {COLOR_RESET}")
    time.sleep(1)
    Umode = input(f"{COLOR_INFO}ℹ️ {'Okay! Now type Chat if you would like to chat with the bot or Voice if you would like to talk using voice:' if Uage <= 18 else 'Please type Chat if you would like to chat or Voice if you would like to talk:'} {COLOR_RESET}")
    print("")
    for attempt in range(3):
        AI_api_key = input(f"{COLOR_INFO}ℹ️ {Uname}, {'Enter your OpenAI private API key: ' if Uage <= 18 else 'Enter your private OpenAI API key: '} {COLOR_RESET}")
        if len(AI_api_key) >=100:
            time.sleep(1)
            print("Wait untill the Algo validates your API key...")
            import openai
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4.1-mini-2025-04-14",
                    messages=[
                        {"role": "system", "content": f"Say only 'CHECKED'"},
                        {"role": "user", "content": "Say 'CHECKED"},
                    ]
                )
                bash_command = response["choices"][0]["message"]["content"]
                if bash_command == "CHECKED":
                    break
                else:             
                    print(f"{COLOR_ORANGE}This API key has responded{COLOR_RESET}")
                    continue
            except Exception as e:
                print(f"{COLOR_ORANGE}❌ Could not connect to the OpenAI api system.Turn on the vpn if you are in the area of local GPT restrictions or check the API account balance{e}{COLOR_RESET}")
                continue
        else:
            print(f"{COLOR_ORANGE}This is not the API key. Original OpenAI API key you can purchase at {COLOR_GREEN} https://platform.openai.com/docs/overview {COLOR_RESET}.Free tokens are unavailable at the moment :({COLOR_RESET}")
    else:
        AI_api_key = None
    import locale
    time.sleep(1)
    try:
        lang_code, _ = locale.getlocale()
        if lang_code:
            Ulang = lang_code.replace("_", "-").upper()
        else:
            Ulang = "EN-US"
    except:
        pass
    tellhim("I have tried to identify your language automatically using your system language. If it is wrong - dont worry, say anything to algo on your native language and Algo will adapt.")
    time.sleep(1)
    try:
        data = requests.get('https://ipinfo.io/json').json()
        country_code = data.get('country')
        if country_code:
            country_obj = pycountry.countries.get(alpha_2=country_code)
            if country_obj:
                Ucountry = country_obj.name
            else:
                Ucountry = None
        else:
            Ucountry = None
    except:
        Ucountry = None
    import PlatKernel
    creation = PlatKernel.activation(Uage, Uname, Ugender, Ubotreference, Umode, Ulang, Ucountry, AI_api_key, False)
    if creation == "success":
        print(f"{COLOR_GREEN}✅ Program package installation started!{COLOR_RESET}")
    else:
        print(f"{COLOR_INFO}ℹ️ Oh oh, the program files might be broken... default settings will be applied. Installation continues...{COLOR_RESET}")
    return "S"

def JSON_config_changer(parameter, value):
    try:
        with open("config.json", "r") as file:
            config = safe_load_json("config.json")
            config[parameter] = value
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"⚠️ Ошибка изменения JSON: {e}")

def tellhim(text, speed=0.03):
    entry, intro_phrase = user_info_giver()
    Umode = read_key_from_JSON('Umode')
    Ulang = read_key_from_JSON('Ulang').upper()
    try:
        if Umode == "Voice":
            csv_path = 'voices_parsed.csv'
            lang_code = Ulang
            
            # Нормализуем язык
            if lang_code == "EN" or lang_code.startswith("EN-"):
                lang_code = "EN-US"
            else:
                # Только если НЕ английский — пробуем перевести
                if Check_INTERNET_CONNECTION():
                    text = lang_validation(text, lang_code)
                else:
                    print("⚠️ No internet: skipping translation for non-English voice.")
                    # Оставляем текст на английском — лучше, чем молчать

            speak_lang = find_shortname(csv_path, Ulang, Ugender)
            asyncio.run(main(text, Uname, entry, intro_phrase, "retell", speak_lang))
            
            if read_key_from_JSON("System") == 'Windows':
                import pygame
                import time
                
                pygame.mixer.init()
                pygame.mixer.music.load("output.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                pygame.mixer.quit()
            else:
                os.system("afplay output.mp3")

        elif Umode == "Chat":
            # Только если язык пользователя — не английский
            if not Ulang.startswith("EN") and Check_INTERNET_CONNECTION():
                text = lang_validation(text, Ulang)
            import time
            # Выводим по символам
            for char in str(text):
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(speed)
    except Exception as e:
        print(f"⚠️ Ошибка вывода текста/голоса: {e}")

def safe_load_json(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"⚠️ Ошибка загрузки JSON: {e}")
        # Файл битый или пустой — пересоздаем дефолтный конфиг
        config = {"Debug": False}
        with open(filepath, "w") as file:
            json.dump(config, file, indent=4)
        return config
    

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
            

def get_user_response():
    return User.get_message()

def semantic_match(response, embeddings, threshold=0.75):
    try:
        if not response:
            return False
        user_embedding = modelW.encode(response, convert_to_tensor=True)
        similarity_scores = util.cos_sim(user_embedding, embeddings)[0]
        max_score = similarity_scores.max().item()
        if Debugstat:
            print(f"🔎 Semantic match score: {max_score:.3f}")
        return max_score >= threshold
    except Exception as e:
        print(f"⚠️ Ошибка семантического сравнения: {e}")
        return False

def AgreeDisagreeProcessing(wherefrom):
    try:
        response = get_user_response()
        response = clean_response(response)

        if not response:
            return False, False

        # Regex-based detection
        agree_regex = re.search(AlgoParser.Agrementpattern, response, re.IGNORECASE)
        disagree_regex = re.search(AlgoParser.DisagreementPattern, response, re.IGNORECASE)

        # Semantic-based fallback
        agree_semantic = semantic_match(response, agree_embeddings)
        disagree_semantic = semantic_match(response, disagree_embeddings)

        agree = agree_regex is not None or agree_semantic
        disagree = disagree_regex is not None or disagree_semantic

        return agree, disagree
    except Exception as e:
        print(f"⚠️ Ошибка обработки ответа: {e}")
        return False, False


def sayhello():
    if Uage > 40:
        tellhim(np.random.choice(AlgoParser.name_responses["40, 150"]))
    elif Uage >= 30 and Uage <=40:
        tellhim(np.random.choice(AlgoParser.name_responses["30, 40"]))
    elif Uage >= 20 and Uage < 30:
        tellhim(np.random.choice(AlgoParser.name_responses["20, 30"]))
    elif Uage > 0 and Uage < 20:
        tellhim(np.random.choice(AlgoParser.name_responses["0, 20"]))
    else:
        print("Cannot initialize as the information about the age is in lack")
        return None
# def find_folder_subprocess(folder_name):
#     try:
#         # Поиск с корня '/' — долго, но без жёстких путей
#         result = subprocess.run(
#             ["find", "/", "-type", "d", "-name", folder_name],
#             capture_output=True, text=True, check=True
#         )
#         paths = result.stdout.strip().split('\n')
#         if paths and paths[0]:
#             return paths[0]
#     except subprocess.CalledProcessError as e:
#         print(f"⚠️ Ошибка subprocess поиска: {e}")
#         return None

# folder = find_folder_subprocess("FWhisper")

def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()

def get_users_country():
    import requests
    try:
        data = requests.get('https://ipinfo.io/json').json()
        ip = data['ip']
        country = data['country']
        if Debugstat is True:
            print(f'Ваш IP: {ip}')
            print(f'Страна: {country}')
        return country
    except requests.RequestException as e:
        print("Неудалось определить вашу страну,введите пожалуйста ее вручную..")
        print(f"⚠️ {e}")
        return None
Debugstat = read_key_from_JSON("Udebug")
Uname = read_key_from_JSON("Uname")
Uage = read_key_from_JSON("Uage")
Ugender = read_key_from_JSON('Ugender')
Umode = read_key_from_JSON("Umode")
stop_embeddings = modelS.encode(AlgoParser.stop_phrases, convert_to_tensor=True)
agree_embeddings = modelS.encode(AlgoParser.listofpositiveresponses, convert_to_tensor=True)
disagree_embeddings = modelS.encode(AlgoParser.listofnegativeresponses, convert_to_tensor=True)

def get_folder_size(folder_path):
    folder = Path(folder_path)
    
    # print(f"🔍 Проверяем путь: {folder.absolute()}")

    if not folder.exists():
        print("❌ Путь не существует")
        return 0

    if not folder.is_dir():
        print("❌ Это не папка")
        return 0

    total_size = 0
    file_count = 0

    for file in folder.rglob("*"):
        if file.is_file():
            try:
                size = file.stat().st_size
                total_size += size
                file_count += 1
                # Раскомментируй, чтобы видеть всё:
                # print(f"  + {file.name}: {size} байт")
            except OSError as e:
                print(f"⚠️ Ошибка чтения {file}: {e}")
    return total_size

if Debugstat:
    print("* CommonUtil has successfully loaded!")
            
def user_info_giver():
    try:
        if Uage is not None and Uage > 30:
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
        else:
            print("Cannot initialize as the information about the age is in lack")
        inro_phrase = numpy.random.choice(AlgoParser.entry_titles["intro_phrases"])
        return entry, inro_phrase
    except Exception as e:
        print(f"⚠️ Ошибка user_info_giver: {e}")