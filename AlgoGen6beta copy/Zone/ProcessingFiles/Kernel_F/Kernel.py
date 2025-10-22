import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))  # Kernel_F/
parent_dir = os.path.dirname(current_dir)                # ProcessingFiles/
sys.path.append(parent_dir)
# Теперь можно импортировать "обычным способом"
import random 
import TheMaths
import AlgoParser
import volume_up
import os, sys, time, wave, tempfile, collections
import pyaudio, webrtcvad, librosa
import tensorflow as tf
from tensorflow import keras
from keras import layers, models
import CommonUtil
import FileManagement
import PlanCrafting
import searching_engine
import Algo_Intelligence
import knowledge_organizer
import volume_down
from rasa.core.agent import Agent
from rasa.model import get_latest_model
from rasa.core.agent import Agent
import settings
import WOD
import re
import traceback
import numpy as np
import spacy
import warnings
import locale
from user import userbase
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
import logging
logging.getLogger('rasa').setLevel(logging.INFO)
logging.getLogger("rasa").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("rasa.nlu").setLevel(logging.WARNING)
logging.getLogger("rasa.core").setLevel(logging.WARNING)
logging.getLogger("rasa.shared").setLevel(logging.WARNING)
log_level = logging.DEBUG if os.getenv("DEBUG_RASA") else logging.WARNING

COLOR_BLUE         = "\033[34m"
COLOR_YELLOW       = "\033[33m"
COLOR_ORANGE       = "\033[38;5;208m"
COLOR_GREEN        = "\033[32m"
COLOR_INFO         = "\033[96m"
COLOR_LIGHT_BLUE   = "\033[94m"
COLOR_RESET        = "\033[0m"
from pathlib import Path
try:
    nlp = spacy.load("en_core_web_md")
except:
    OSError

def get_user_response():
    return User.get_message()
# Load rasa agent and parse
def rasa_loader():
    global agent
    try:
        script_dir = Path(__file__).parent
        script_dir = script_dir.parent
        project_root = script_dir.parent.parent
        MD_folder = project_root / "AImodels"
        RASAmodel_folder = MD_folder / "INDENT_AI"
        RASA_agent_path = RASAmodel_folder / "models"
        if Debugstat is True:
            print(RASA_agent_path)
    except:
        OSError
    agent = Agent.load(RASA_agent_path)
    print("Agent loaded successfully.")


def config_initializer():
    global cashe_list, Enclave_completing, decidion_completed, usednickname,Debugstat, Umode, Uname, Ubotreference, Uage, Trained, Ucountry
    cashe_list = []
    Enclave_completing = False
    decidion_completed = False
    usednickname = False 
    config_path = Path("config.json")
    if not config_path.exists():
        CommonUtil.tellhim("Algo has detected that the config file has been removed. Please reenter the information needed to restore the config file now.")
        config = CommonUtil.config_restore()
        if config == "S":
            pass
        else:
            CommonUtil.tellhim("Seems like Algo could not restore the config file, algo cannot continue running. Reboot the Algo for entering the DEBUG algo mode.")
            quit()
        config = CommonUtil.safe_load_json("config.json")
        Debugstat = config["Udebug"]
        Umode = config["Umode"]
        Uname = config["Uname"]
        Ubotreference = config["Ubotreference"]
        Uage = config['Uage']
        Trained = CommonUtil.read_key_from_JSON("Uvoice_trained")
        Ucountry = config['Ucountry']
        print("JSON config wile installated")
    else:
        try:
            with open(config_path, "r") as file:
                config = CommonUtil.safe_load_json("config.json")
                Debugstat = config["Udebug"]
                Umode = config["Umode"]
                Uname = config["Uname"]
                Ubotreference = config["Ubotreference"]
                Uage = config['Uage']
                Ucountry = config['Ucountry']
                Trained = CommonUtil.read_key_from_JSON("Uvoice_trained")
        except FileNotFoundError:
            from PlatKernel import activation
            activation()


def listen_vad_once():
    SAMPLE_RATE = 16000
    CLIP_DURATION = 1.0
    N_MFCC = 40
    N_FFT = 512
    HOP_LENGTH = 160
    KWS_THRESHOLD = 0.99
    KEYWORD = CommonUtil.read_key_from_JSON("Ubotreference")
 
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = SAMPLE_RATE
    FRAME_DURATION = 30  # ms
    FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
    SILENCE_FRAMES = int(1.0 * 1000 / FRAME_DURATION)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent  # поднялись на 3 уровня вверх
    MD_folder = project_root / "AImodels"
    MODEL_PATH = MD_folder / "kws_model.h5"
      # поднялись на 3 уровня вверх
    MD_folder = project_root / "AImodels"
    MODEL_PATH = MD_folder / "kws_model.h5" 
    try:
        model = keras.models.load_model(MODEL_PATH)
    except FileExistsError:
        if Debugstat is True:   
            print("AHH, the WWD model is not found! raising the auto debug...")
            modelbin = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(modelbin, "WWD_DB")
            size = CommonUtil.get_folder_size(data_dir)
            if size > 0:
                WOD.train()
            else:
                if Debugstat is True:
                    print("We need to retrain the bot...")
                    CommonUtil.JSON_config_changer("Uvoice_trained", False)
                    return "CRITICAL_ERROR"
    vad = webrtcvad.Vad(2)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=FRAME_SIZE)
    try:
        print(f"{Ubotreference} is waiting to be called..")
    except ValueError:
        print("Bot is waiting to be called..")
    try:
        while True:
            frames = []
            ring_buffer = collections.deque(maxlen=SILENCE_FRAMES)
            recording = False

            while True:
                frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
                is_speech = vad.is_speech(frame, RATE)

                if is_speech:
                    recording = True
                    ring_buffer.clear()
                    frames.append(frame)
                else:
                    if recording:
                        ring_buffer.append(frame)
                        if len(ring_buffer) == SILENCE_FRAMES:
                            frames.extend(ring_buffer)
                            break

            # сохраняем временный WAV
            tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            with wave.open(tmpfile, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))

            # предсказываем
            y_sig, _ = librosa.load(tmpfile, sr=SAMPLE_RATE, mono=True)
            y_sig = librosa.util.fix_length(y_sig, size=int(CLIP_DURATION * SAMPLE_RATE))
            X = WOD.mfcc_features(y_sig, SAMPLE_RATE)
            pred = float(model.predict(np.array([X]), verbose=0)[0][0])
            if pred >= KWS_THRESHOLD:
                ts = int(time.time())
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # <- на уровень выше
                data_dir = os.path.join(base_dir, "WWD_DB")
                os.makedirs(data_dir, exist_ok=True)
                saved_path = os.path.join(data_dir, f"capture_{ts}.wav")
                os.replace(tmpfile, saved_path)
                if Debugstat is True:
                    print(f"⚡ Слово засечено! ({saved_path})")
                return saved_path  # <- возвращаем путь к аудио
            else:
                os.remove(tmpfile)

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
def Voice_Initial_Check():
    if Umode == "Voice":
        from faster_whisper import WhisperModel
        script_dir = Path(__file__).parent
        # Поднимаемся на 2 уровня вверх
        project_root = script_dir.parent.parent.parent

        # Путь к папке models
        MD_folder = project_root / "AImodels"
        model_folder = MD_folder / "FWhisper"

        model_size_bytes = CommonUtil.get_folder_size(model_folder)
        print(model_size_bytes)
        size_mb = model_size_bytes / (1024 * 1024)
        if Debugstat is True:
            print("Model size initial check:", size_mb, model_folder)
        if 120 < size_mb < 500:
            # Если у тебя есть GPU, используй device="cuda", иначе "cpu"`
            modelW = WhisperModel(str(model_folder), device="cpu")
            CommonUtil.set_modelW(modelW)
        else:
            CommonUtil.tellhim("It seams you've just changed the voice model, i will try to download it...")
            import time
            time.sleep(10)
            CommonUtil.empty_folder(model_folder)
            from modelscope import snapshot_download
            try:
                try:
                    Voice_model = CommonUtil.read_key_from_JSON("Uvoicemodel")
                except ValueError and IndexError:
                    print(f"Now, {Uname} you have two options: \n You can either install the model for understanding your voice \nwhich is heavier, and has higher pc requirements, or \n\n You can also install the model which is lighter,\n and more optimised for usage on slow pc \n\nThe weight of big model - ~450mb\n\nThe weight of small model - ~160mb \n\n What do you choose? (1 or 2), please, choose carefully!")
                    Voice_model = int(input("Enter your choice:"))
                choice = 1 if Voice_model == "big" else 2
                if choice == 1:
                    model = 'angelala00/faster-whisper-small'
                elif choice == 2:
                    model = 'pengzhendong/faster-whisper-base'
                else:
                    attempt_MC = 0
                    while choice != 1 or choice != 2:
                        if attempt_MC != 4:
                            choice = int(input("Please enter the valid choice:"))
                            attempt_MC+= 1
                        else:
                            print("programm access restricted due the suspicious activity. PLease restart the programm...")
                            quit()
            except ValueError:
                while choice != 1 or choice != 2:
                    if attempt_MC != 4:
                        choice = int(input("Please enter the valid choice:"))
                        attempt_MC+= 1
                    else:
                        print("programm access restricted due the suspicious activity. PLease restart the programm...")
                        quit()
            try:
                model_dir = snapshot_download(
                    model,
                    local_dir=model_folder  # ← сохраняем прямо сюда
                )

            except ConnectionError:
                CommonUtil.tellhim("The bot has no internet for downloading the model! please restart the bot!")
            script_dir = Path(__file__).parent
            # Поднимаемся на 2 уровня вверх
            project_root = script_dir.parent.parent

            # Путь к папке models
            MD_folder = project_root / "AImodels"
            model_folder = MD_folder / "FWhisper"
            size_bytes = CommonUtil.get_folder_size(model_folder)
            size_mb = size_bytes / (1024 * 1024)
            if Debugstat is True:
                print(f"Folder size: {size_mb:.2f} МБ")
            # Ожидаемый размер для faster-whisper-small: ~500–600 МБ (float16)
            if 150 < size_mb < 700:
                Chosen_moodel = "big" if choice == 1 else "light"
                print(f"✅ {Chosen_moodel} model has been successfully saved in: {model_dir}")
                modelW = WhisperModel(str(model_folder), device="cpu")
                CommonUtil.JSON_config_changer("Uvoicemodel", Chosen_moodel)
                CommonUtil.set_modelW(modelW)
            else:
                print("⚠️ Oh oh, it looks like i cannot download the file properly... please ensure your internet connection is stable abd restart the programm...")
                quit()

def thestart():
    global User
    # Initialize waiting_time if it doesn't exist
    User = userbase()
    if CommonUtil.read_key_from_JSON("Umode") == "Voice":
        if "waiting_time" not in globals():
            global waiting_time
            waiting_time = 0
        Trained = CommonUtil.read_key_from_JSON("Uvoice_trained") 
        if Trained is True:
            if "waiting_time" not in globals() or time.time() - waiting_time > 10:
                audio_path = listen_vad_once()
                if audio_path != "CRITICAL_ERROR":
                    pass
                else:
                    CommonUtil.tellhim("Извините, бот должен перезагрузится для исправления ошибки...")
                    time.sleep(10)
                    thestart()
                waiting_time = time.time()
        else:
            AI_Voice_educator()
    else:
        pass
    message = User.get_message()  # Сохраняем результат один раз
    if message == "ERROR_NO_VOICE":
        AI_Voice_educator()
    else:
        replylogic()

def find_engine(User_message, match_TARGET):
    global infoamo
    infoamo = 0
    try:
        engine_act_dict = cashe_list[(cashe_list.index(match_TARGET))] #The start of the next task 
        engine_act_list = next(iter(engine_act_dict.values()))
        engine_act_re_start_of_new_task = engine_act_list[0]
        str_index = engine_act_re_start_of_new_task.start()
    except IndexError:
        if Debugstat is True:
            print("There is no cashelist for finding the actions!")
        return 0, 0
    if cashe_list[cashe_list.index(match_TARGET)] != cashe_list[-1]:
        next_match_dict = cashe_list[cashe_list.index(match_TARGET) + 1]
        next_match_obj = next(iter(next_match_dict.values()))[0]
        next_match_start = next_match_obj.start()
    if Debugstat is True:
        print("**************\nStart of Find Engine Working! ")
    if cashe_list[cashe_list.index(match_TARGET)] != cashe_list[-1]:
        engine_dict = cashe_list[(cashe_list.index(match_TARGET) + 1)] #The start of the next task 
        engine_list = next(iter(engine_dict.values()))
        engine_re_start_of_new_task = engine_list[0]
        next_match_dict = cashe_list[cashe_list.index(match_TARGET) + 1]
        next_match_obj = next(iter(next_match_dict.values()))[0]
        next_match_start = next_match_obj.start()
        key, value = next(iter(match_TARGET.items()))
        if key == 'maths':
            return str_index, engine_act_re_start_of_new_task.end() + 1
        try:
            for seps in findingseparations:
                for sep in seps.values():
                    
                    if (User_message[sep.end():next_match_start]).isspace():
                        end_index = (sep.start() - 2)
                        if Debugstat:
                            print(f"separator: {sep}")
                        if end_index < 0:
                            end_index = sep.start() - 1
                        else:
                            pass
                        if User_message[end_index] in ("," , "-", "!", "!", "?", ";", "."):
                            end_index -= 1
                        return str_index, end_index
                    else:
                        if len(User_message[sep.end():next_match_start]) < 3:
                            z = next_match_start
                            if Debugstat:
                                print(f"separator: {sep}")
                            for i in range(next_match_start, sep.start(), -1):
                                z -= 1
                                if User_message[i].isspace():
                                    end_index = z-1
                                    if User_message[end_index] == ",":
                                        end_index -= 1
                                    return str_index, end_index
                            return str_index, z - 1
                        else:
                            if Debugstat:
                                print(f"separator: {sep}")
                            z = next_match_start
                            for i in range(next_match_start, 0, -1):
                                z -= 1
                                if User_message[i].isspace():
                                    end_index = z
                                    try:
                                        if User_message[end_index] == ",":
                                            end_index -= 1
                                    except IndexError:
                                        pass
                                
                                    return str_index, end_index
        except IndexError as e:
            print("The find engine retrieved error while processing")
            if Debugstat is True:
                print(e, "\n\n\n")
            return 0,0
        return str_index, next_match_start - 1
    else:
        end_index = len(User_message) - 1
        if User_message[end_index] == ",":
            end_index -= 1
        return str_index, end_index
def cashe_list_creator(User_message):
    global User
    global findingtheplanning, Agrement, findthegreeting, find_the_prediction, finding_the_math, full_info_of_planning, Enclave_completing, cashe_list, match, Nick_finding, findingseparations, UMC, searching, key
    try:
        if Debugstat is True:
            print("\nТекст сообщения:", User_message)
        findingthesettings = [{"settings": match} for match in re.finditer(AlgoParser.settings_pattern, User_message, re.IGNORECASE)]
        findingtheplanning = [{"processplanning": match} for match in re.finditer(AlgoParser.planning_pattern, User_message, re.IGNORECASE)]
        findingseparations = [{"separation:" : match} for match in re.finditer(AlgoParser.separ_pattern, User_message, re.IGNORECASE)]
        findthegreeting = [{"greeting": match} for match in re.finditer(AlgoParser.meeting_words_pattern, User_message, re.IGNORECASE)]
        find_the_prediction = [{"processPrediction": match} for match in  re.finditer(AlgoParser.predictpattern, User_message, re.IGNORECASE)]
        finding_the_math = [{"maths": match} for match in re.finditer(AlgoParser.math_pattern, User_message, re.IGNORECASE)]
        Nick_finding = [{"NameSet": match} for match in re.finditer(AlgoParser.provider_pattern, User_message,  re.IGNORECASE)]
        Nick_finding = [{"AgentCreation": match} for match in re.finditer(AlgoParser.agent_pattern, User_message,  re.IGNORECASE)]
        searching = {"searching": re.search(AlgoParser.search_pattern, User_message, re.IGNORECASE)}
        matches = [findingtheplanning, find_the_prediction, findthegreeting, Nick_finding, searching, finding_the_math, findingthesettings]
        # cashe_list = [(match for match in matches if any(match.values())) ] old version
        for group in matches:
            if isinstance(group, list):
                for item in group:
                    for key, value in item.items():
                        if value:
                            cashe_list.append({key: value})
            elif isinstance(group, dict):
                for key, value in group.items():
                    if value:
                        cashe_list.append({key: value})

        for i in cashe_list:
            for key, value in i.items():
                if not isinstance(value, list):
                    i[key] = [value]
        Enclave_completing = (True if len(cashe_list) > (2 if findthegreeting else 1) else False)
        return cashe_list
    except Exception as e:
        print(f"An error occurrefd: {e}")
        CommonUtil.tellhim(f"\nError: {e}\nLength of cashe list: {len(cashe_list)}\n")
        error = traceback.format_exc()
        print(error)
        thestart()
def processor(cashe_list):
    global User
    if len(cashe_list) == 0:
        task_compiller("searching", User.raw_message)
    for match in cashe_list:
        if not match:
            continue
        try:
            key, value = next(iter(match.items()))
            if value and hasattr(value[0], "group"):  # Ensure value is a match object
                if Debugstat is True:
                    print(f"\nProcessing {cashe_list.index(match) + 1} task: {key}: {value[0].group()}")
                text_str_index, text_end_index = find_engine(User.message, match)
                UMC = User.message[text_str_index:(text_end_index + 1)] #UMC = USER MESSAGE COMMAND
                if Debugstat is True:
                    print("text:", User.message[text_str_index:(text_end_index + 1)], "/ lengh of prompt:",len(User.message))
                if key == "maths":
                    task_compiller("maths", UMC)  # Pass the expression for Maths
                elif key == "greeting":
                    task_compiller("greating", UMC)
                else:
                    task_compiller(str(key), UMC, value[0].group())
        except (StopIteration, AttributeError, IndexError) as e:
            if Debugstat is True:    
                print(f"\nError while processing match {match}: {e}")
            continue
    if not Enclave_completing:
        thestart()

# def intent_reader(result1, result2):



def AI_Voice_educator():
    CommonUtil.tellhim(f"Hello, dear {Uname}! Lets teach me to understand your voice commands perfectly!\n Your mission will be to call me by my name which was given by you 3-5 times. Please call me as if i am one of your best-friends. My name is {Ubotreference} and if you are not shure you will be able to spell that, please change my name in a settings Just type 'change bot reference settings'. Lets start!.")
    CommonUtil.play_sound("starter_song1.mp3")
    CommonUtil.record_until_silence_vad(True)
    CommonUtil.tellhim("Great! Now again...")
    CommonUtil.play_sound("starter_song2.mp3")
    CommonUtil.record_until_silence_vad(True)
    CommonUtil.tellhim("What a magical voice! Continue please...")
    CommonUtil.play_sound("starter_song2.mp3")
    CommonUtil.record_until_silence_vad(True)
    CommonUtil.tellhim("Great! One more...")
    CommonUtil.play_sound("starter_song2.mp3")
    CommonUtil.record_until_silence_vad(True)
    CommonUtil.tellhim(f"{Uname}, keep it up! I cant't not learn to recognize such a beautiful voice, continue!")
    CommonUtil.play_sound("starter_song2.mp3")
    CommonUtil.record_until_silence_vad(True)
    CommonUtil.tellhim("Great! Now we are finished...")
    CommonUtil.JSON_config_changer("Uvoice_trained", True)
    CommonUtil.tellhim("I will start learning your voice in a second, please wait! It may take a minutes to do that, \nfinal model may weight up to 300mb, please ensure you have a free space!")
    WOD.train()
    CommonUtil.tellhim("Great! Now i know how exactly your voice sounds like. You can activate me by calling by my name!")
    thestart()
def replylogic():
    global findingtheplanning,agent, tot, Agrement, findthegreeting, find_the_prediction, finding_the_math, full_info_of_planning, Enclave_completing, cashe_list, Nick_finding, findingseparations, searching, key
    full_info_of_planning = False
    Agrement = random.choice(AlgoParser.agreement_words) + "!"
    if Debugstat is True:
        print("Reply logic working now")
    tot = False
    intent_box = []
    tasks = []
    result_AI_intent = Algo_Intelligence.task_certifier(User.message, agent)
    result_cache_list = cashe_list_creator(User.message)
    if Debugstat is True:
        print(result_AI_intent)
        print(result_cache_list)
    if len(cashe_list) >1:
        list_of_indexes = []
        for i in cashe_list:
            st_index, end_index = find_engine(User.message, i)
            if st_index and end_index != 0:
                pass
            else:
                if Debugstat is True:
                    print(f"An error occured while processing task {i}")
                engine_act_dict = cashe_list[(cashe_list.index(i))] #The start of the next task 
                engine_act_list = next(iter(engine_act_dict.values()))
                engine_act_re_start_of_new_task = engine_act_list[0]
                str_index = engine_act_re_start_of_new_task.start()
            tasks.append(User.message[st_index:])
            list_of_indexes.append((st_index, end_index))
        if Debugstat:
            print(tasks)
    elif len(cashe_list) == 1:
        key, value = next(iter(cashe_list[0].items()))
        if len(result_AI_intent) > 0:
            main_intent = result_AI_intent['Intent'] # Берем первый интент
            if main_intent != str(key):
                str_index, end_index = find_engine(User.message, cashe_list[0])
                task = User.message[:str_index] + User.message[end_index:]
                tasks.append(task)
                tasks.append(User.message[str_index:end_index])
            else:
                tasks.append(User.message)
        else:
            # Обработка случая, если result_AI_intent не список или пустой
            pass
    else:
        tot = True
        tasks.append(User.message)
        Enclave_completing = False
    #how do we even defy the tasks? Okey ,first of all, we send both texts to intent defiers. We check, what 
    #did we get from each of them, and lets discuss different cases of what we gonna do with results:
    #1)The tasks in Ai_Intent and Regex are same, and Regex contains only one founding => we send all the prompt to the module for processing
    #2)The amount of tasks in Ai_Intent and Regext is same, but different: imagine Ai_Intent to find Process_Planning FOR ALL PROMPT for some reason,'
        #and Regex finding maths for some reason. What we do? Lets imaging the prompt:
        #make me to remember to call my mom tomorrow and calculate 3 + 3. 
        #we SPLIT the promt by finding engine, and both parts we do send tothe Ai_intent again. If the results from the both parts are different,
        #which means no of the finding modules was incorrect, we send the parts separetely from AI_intenter to the needed modules, but if they are the same, which
        #means that one of the modules has made the mistake, we send the one from regex.
    if len(tasks) != 0:
        intent_box = []
        for task in tasks:
            if tot is not True:
                intent_box.append(Algo_Intelligence.task_certifier(task, agent))
            else:
                intent_box.append(result_AI_intent)
    if Debugstat is True:
        print("starting to process the intents")
    for i in intent_box:
        dict_intent = i
        try:
            main_intent = dict_intent['Intent']
            probability = dict_intent['Probability']
            text = dict_intent['Text']
        except ValueError as er:
            if Debugstat is True:
                print(f"Youve got and error while analysing the {i} in intent box: {intent_box}, here is the error: \n\n", er)
            next
        if Debugstat is True:
            print("Processing main intent:", main_intent, "Text:", text)
        if main_intent == "settings":
            entities = dict_intent.get("Entities", {})
            if "object_of_settings" in entities and entities["object_of_settings"]:
                value = entities["object_of_settings"][0].get("value")
                if Debugstat:
                    print("Settings intent detected with value:", value)
                task_compiller(main_intent, text, value)
            else:
                task_compiller(main_intent, text)
        else:
            if probability > 0.96:
                task_compiller(main_intent, text)
            else:
                task_compiller('searching', text)
    cashe_list = []
    Enclave_completing = False
    intent_box = []
    tasks = []

def task_compiller(task_to_start, UMC, SpotCommand=None):
    if task_to_start == "maths":
        Maths_complete_status = TheMaths.process_math(UMC)
        if Maths_complete_status == "S":
            if not Enclave_completing:
                thestart()
        else:
            print("Task complecation is Either unsupported to process or faced error while processing.")
            if not Enclave_completing:
                thestart()           
    if task_to_start == "AI_prompt":
        # i = random.randint(0,2)
        # Agree = None
        # disagree = None
        # if i == 1:
        #     Agree, disagree = CommonUtil.AgreeDisagreeProcessing('taskcompiler')
        # if Agree:
        # searching_engine.relevatizer(User.message, UMC
        # else:
        Algo_Intelligence.taskINDENT(User.message)
        if not Enclave_completing:
            thestart()
    elif task_to_start == 'AgentCreation':
        import Agent_creator
        Agent_creator.initializer(UMC)
        if not Enclave_completing:
            thestart()
    elif task_to_start == "greeting":
        from CommonUtil import sayhello
        sayhello()
        if not Enclave_completing:
            thestart()
    elif task_to_start == "processplanning" or task_to_start == "AgreementPlanning":
        # CommonUtil.tellhim(f"{Uname}, i can plan anything at the moment")
        PlanCrafting.message_retreiver(UMC, SpotCommand)
        if not Enclave_completing:
                thestart()
    elif task_to_start == "settings":
        if SpotCommand == None:
            status = settings.seting_setter()
        else:
            if Debugstat is True:
                print(f"Settings command received: {SpotCommand}")
            status = settings.seting_setter(SpotCommand)
        if status == "S":
            CommonUtil.tellhim("You have changed the settings successfully!!")
        elif status == "CD":
            CommonUtil.tellhim("Ok")
        else:
            CommonUtil.tellhim("Sorry, but the process of changing the settings was unsuccessful. But you can always try again!")
        
        if not Enclave_completing:
            thestart()
    elif task_to_start == "NameSet":
        if CommonUtil.read_key_from_JSON("Umode") != 'Voice':
            FileRenamingStatus, message = FileManagement.name_giver(UMC)
            if FileRenamingStatus == "Success":
                from FileManagement import end_index
                UMC = message[:Nick_finding[0]["NameSet"].start()] + UMC[end_index:]
            else:
                if Debugstat:
                    print("We coul not process the task due output error")     
        else:
            CommonUtil.tellhim("Sorry, but you cant use the function of setting the nicknames for the file paths in the Voice mode, please, switch to chat mode to use this function.")
        if not Enclave_completing:
            thestart()
    elif task_to_start == "volume_up":
        volume_up.VolumeUP_Commander()
        if not Enclave_completing:
            thestart()
    elif task_to_start == "volume_down":
        volume_down.VolumeDown_Commander()
        if not Enclave_completing:
            thestart()
    elif task_to_start == "knowledge":
        knowledge_organizer.write_to_knowledge(UMC)
        CommonUtil.tellhim(f"Got you, {Uname}, i have remembered that.")
        if not Enclave_completing:
            thestart()
    elif task_to_start == "AgentCreation":
        import Agent_creator
        Agent_creator.initializer(User.message)
        if not Enclave_completing:
            thestart()
    else:
        if not Enclave_completing and not task_to_start == 'maths' and not task_to_start == "searching":
            CommonUtil.tellhim(f"The {task_to_start} task is not available at the moment.")
            if not Enclave_completing:
                thestart()

if __name__ == "__main__":
    CommonUtil.play_sound("PROGRAMM_LAUNCH.mp3")
    config_initializer()
    Voice_Initial_Check()
    rasa_loader()
    CommonUtil.play_sound("Ready_sound.mp3")
    thestart()




