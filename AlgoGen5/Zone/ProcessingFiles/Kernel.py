import random
import TheMaths, AlgoParser, TextCorrectEngine, CommonUtil, FileManagement, Ai_Engine, PlanCrafting, searching_engine, Algo_Intelligence
import re
from textblob import TextBlob
import traceback
import numpy as np
import json
from pathlib import Path
import spacy
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
from pathlib import Path
try:
    nlp = spacy.load("en_core_web_md")
except:
    OSError

cashe_list = []
Enclave_completing = False
decidion_completed = False
usednickname = False 
config_path = Path("config.json")
if not config_path.exists():
    config = {"Debug": False,
    "System": "Darwin",
    "Version": "Darwin Kernel Version 24.5.0: Tue Apr 22 19:54:33 PDT 2025; root:xnu-11417.121.6~2/RELEASE_ARM64_T8122",
    "Machine": "arm64",
    "Release": "24.5.0",
    "Node Name": "Denis-iMac.local",
    "RAC": True,
    "Uage": 18,
    "Uname": "User",
    "Ugender": "Male",
    "Umode" : "Voice",
    "Ulang" : "eng",
    "Ubotreference": "Algo"}
    with open(config_path,"w") as file:
        json.dump(config, file, indent=4)
    Debugstat = config["Debug"]
    Voice_mode = config["Umode"]
    Uname = config["Uname"]
    Ubotreference = config["Ubotreference"]
    Uage = config['Uage']
    print("JSON config wile installated")
else:
    with open(config_path, "r") as file:
        config = CommonUtil.safe_load_json("config.json")
        Debugstat = config["Debug"]
        Voice_mode = config["Umode"]
        Uname = config["Uname"]
        Ubotreference = config["Ubotreference"]
        Uage = config['Uage']
# if Debugstat is True:
#     print("Initialization of the voice model...")
# Подменяем функцию проверки

class userbase:
    def __init__(self, message="", raw_message="", origin_lang_message=""):
        self.message = message
        self.raw_message = raw_message
        self.origin_lang_message = origin_lang_message
    def get_message(self):
        global Debugstat
        if Voice_mode == "Voice":
            audio_path = CommonUtil.record_until_silence_vad()
            if Debugstat:
                print("🛑 Закончил слушать. Обрабатываю...")
            file_path = audio_path
            try:
                language, self.message = CommonUtil.transcribe(file_path)
            except Exception as e:
                if Debugstat:
                    print(f"⚠️ Ошибка при транскрипции: {e}")
                language = "EN"
                self.message = ""
            with open("config.json", "r") as file:
                config = CommonUtil.safe_load_json("config.json")
                config["Ulang"] = language
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)
            self.origin_lang_message = self.message
            if Debugstat:
                print(f"до перевода: {self.origin_lang_message}")
            self.message = CommonUtil.lang_validation(self.message)
            if hasattr(self.message, "text"):
                self.message = self.message.text
        elif Voice_mode == "Chat":
            self.message = input("\nEnter your prompt:")
            self.origin_lang_message = self.message
            self.message = CommonUtil.lang_validation(self.message)
            language = CommonUtil.lang_detection(self.origin_lang_message)
            with open("config.json", "r") as file:
                config = CommonUtil.safe_load_json("config.json")
                config["Ulang"] = language
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)
            if hasattr(self.message, "text"):
                self.message = self.message.text
        if self.message and isinstance(self.message, str):
            if self.message == "/debug" or self.message == "/debug/status":
                if self.message == "/debug":
                    with open("config.json", "r") as file:
                        config = CommonUtil.safe_load_json("config.json")
                        config["Debug"] = not(config["Debug"])
                        Debugstat = config["Debug"]
                    with open("config.json", "w") as file:
                        json.dump(config, file, indent=4)
                    CommonUtil.tellhim(f"You have turned debug mode {'on' if Debugstat else 'off'}")
                    print(Debugstat)
                    thestart()
                elif self.message == "/debug/status":
                    print(f"Debug is turned {'on' if Debugstat else 'off'}")
                    thestart()
            elif self.message.lower() == "/stop" or self.message in (("goodbye", "bye", "stop") if self.message[-1] != ("!" or ".") else ("goodbye!", "bye!", "goodbye.", "bye.")) or self.message == "0":
                CommonUtil.tellhim(f"Goodbye, {Uname}!")
                quit()
            elif self.message.lower() == Ubotreference:
                if Uage > 40:
                    np.random.choice(AlgoParser.name_responses["40, 150"])
                elif Uage >= 30 and Uage <=40:
                    np.random.choice(AlgoParser.name_responses["30, 40"])
                elif Uage >= 20 and Uage < 30:
                    np.random.choice(AlgoParser.name_responses["20, 30"])
                elif Uage > 0 and Uage < 20:
                    np.random.choice(AlgoParser.name_responses["0, 20"])
            elif self.message in AlgoParser.listofgreetings:
                return self.message
            else:
                # self.raw_message = self.message
                # blob = TextBlob(self.message)
                # self.message = str(blob.correct())
                return self.message
        else:
            CommonUtil.tellhim("Goodbye!")
            quit()
def thestart():
    global User
    User = userbase()
    User.get_message()
    if not User.message:
        CommonUtil.tellhim("No input received. Try again.")
        thestart()
        return
    replylogic()

def find_engine(User_message, match_TARGET):
    global infoamo
    infoamo = 0
    engine_act_dict = cashe_list[(cashe_list.index(match_TARGET))] #The start of the next task 
    engine_act_list = next(iter(engine_act_dict.values()))
    engine_act_re_start_of_new_task = engine_act_list[0]
    str_index = engine_act_re_start_of_new_task.start()
    if cashe_list[cashe_list.index(match_TARGET)] != cashe_list[-1]:
        next_match_dict = cashe_list[cashe_list.index(match_TARGET) + 1]
        next_match_obj = next(iter(next_match_dict.values()))[0]
        next_match_start = next_match_obj.start()
    if Debugstat is True:
        print("**************\nStart of Find Engine Working! ")
    if cashe_list[cashe_list.index(match_TARGET)] != cashe_list[-1]:
        if Debugstat is True:
            print("Condition that the processing task is not last satisfied")
        engine_dict = cashe_list[(cashe_list.index(match_TARGET) + 1)] #The start of the next task 
        engine_list = next(iter(engine_dict.values()))
        engine_re_start_of_new_task = engine_list[0]
        next_match_dict = cashe_list[cashe_list.index(match_TARGET) + 1]
        next_match_obj = next(iter(next_match_dict.values()))[0]
        next_match_start = next_match_obj.start()
        for seps in findingseparations:
            for sep in seps.values():
                
                if (User_message[sep.end():next_match_start]).isspace():
                    end_index = (sep.start() - 2)
                    if Debugstat:
                        print(f"separator: {sep}")
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
                    else:
                        if Debugstat:
                            print(f"separator: {sep}")
                        z = next_match_start
                        for i in range(next_match_start, 0, -1):
                            z -= 1
                            if User_message[i].isspace():
                                end_index = z
                                if User_message[end_index] == ",":
                                    end_index -= 1
                                return str_index, end_index
            
    else:
        end_index = len(User_message) - 1
        if User_message[end_index] == ",":
            end_index -= 1
        return str_index, end_index
def replylogic():
    global findingtheplanning, Agrement, findtheplanningdate, findthegreeting, find_the_prediction, finding_the_math, full_info_of_planning, Enclave_completing, cashe_list, match, Nick_finding, findingseparations, UMC, searching, key
    full_info_of_planning = False
    Agrement = random.choice(AlgoParser.agreement_words) + "!"
    if Debugstat:
        print(User.message)
    try:
        check_completing = re.search(AlgoParser.correction_pattern, User.message, re.IGNORECASE)
        if not check_completing:
            if Debugstat is True:
                print("\nТекст сообщения:", User.message)
            
            findingtheplanning = [{"processplanning": match} for match in re.finditer(AlgoParser.planning_pattern, User.message, re.IGNORECASE)]
            findingseparations = [{"separation:" : match} for match in re.finditer(AlgoParser.separ_pattern, User.message, re.IGNORECASE)]
            findthegreeting = [{"greeting": match} for match in re.finditer(AlgoParser.meeting_words_pattern, User.message, re.IGNORECASE)]
            find_the_prediction = [{"processPrediction": match} for match in  re.finditer(AlgoParser.predictpattern, User.message, re.IGNORECASE)]
            finding_the_math = [{"Maths": match} for match in re.finditer(AlgoParser.math_pattern, User.message, re.IGNORECASE)]
            Nick_finding = [{"NameSet": match} for match in re.finditer(AlgoParser.provider_pattern, User.message,  re.IGNORECASE)]
            searching = {"searching": re.search(AlgoParser.search_pattern, User.message, re.IGNORECASE)}
            matches = [findingtheplanning, find_the_prediction, findthegreeting, Nick_finding, searching, finding_the_math]
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
            if Debugstat:
                print(cashe_list)
            # cashe_list.sort(key=lambda match: next(iter(match.values())).span()[0] if match else 0)
            # cashe_list.sort(key=lambda match: next(iter(match.values())).span()[0] if match else 0)

            for i in cashe_list:
                for key, value in i.items():
                    if not isinstance(value, list):
                        i[key] = [value]
            if Debugstat is True:
                print("\nОтсортированный список:", cashe_list)
            if Debugstat:
                print(f"\nHere is the sep list: {findingseparations}")
            Enclave_completing = (True if len(cashe_list) > (2 if findthegreeting else 1) else False)
            if len(cashe_list) == 0:
                # task_compiller("searching", User.message)
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
                        if key == "Maths":
                            task_compiller("Maths", UMC)  # Pass the expression for Maths
                        elif key == "greeting":
                            task_compiller("greating", UMC)
                        else:
                            task_compiller(str(key), UMC, value[0].group())
                except (StopIteration, AttributeError) as e:
                    if Debugstat is True:    
                        print(f"\nError while processing match {match}: {e}")
                    continue
            if not Enclave_completing:
                thestart()
        else:
            task_compiller("processfixing")
    except Exception as e:
        print(f"An error occurrefd: {e}")
        CommonUtil.tellhim(f"\nError: {e}\nLength of cashe list: {len(cashe_list)}\n")
        error = traceback.format_exc()
        print(error)
        thestart()


def task_compiller(task_to_start, UMC, SpotCommand=None):
    if task_to_start == "Maths":
        Maths_complete_status = TheMaths.process_math(UMC)
        if Maths_complete_status == "S":
            if not Enclave_completing:
                thestart()
        else:
            print("Task complecation is Either unsupported to process or faced error while processing.")
            if not Enclave_completing:
                thestart()           
    if task_to_start == "searching":
        # searching_engine.relevatizer(User.message, UMC)
        # if not Enclave_completing:
        #     thestart()
        Algo_Intelligence.taskINDENT(User.message)
        if not Enclave_completing:
            thestart()
    if task_to_start == "greating":
        from CommonUtil import sayhello
        sayhello()
        if not Enclave_completing:
            thestart()
    elif task_to_start == "processplanning" or task_to_start == "AgreementPlanning":
        # CommonUtil.tellhim(f"{Uname}, i can plan anything at the moment")
        PlanCrafting.message_retreiver(UMC, SpotCommand)
    elif task_to_start == "processfixing":
        TextCorrectEngine.processfixing(UMC)
    elif task_to_start == "processPrediction":
        Ai_Engine.processPrediction()
    elif task_to_start == "NameSet":
        FileRenamingStatus, message = FileManagement.name_giver(UMC)
        if FileRenamingStatus == "Success":
            from FileManagement import end_index
            UMC = message[:Nick_finding[0]["NameSet"].start()] + UMC[end_index:]
            if not Enclave_completing:
                thestart()
        else:
            if Debugstat:
                print("We coul not process the task due output error")
    else:
        if not Enclave_completing and not task_to_start == 'Maths' and not task_to_start == "searching":
            CommonUtil.tellhim(f"An error occurred with {task_to_start} task.")

if __name__ == "__main__":
    thestart()
