import random
import TheMaths, AlgoParser, TextCorrectEngine, CommonUtil, FileManagement, Ai_Engine, PlanCrafting
import re
import time
import sys
from textblob import TextBlob
import difflib
import traceback
import csv
import os
import pandas as pf
import json
from pathlib import Path
cashe_list = []
Enclave_completing = False
decidion_completed = False
usednickname = False 
config_path = Path("config.json")
if not config_path.exists():
    config = {"Debug": False}
    with open(config_path,"w") as file:
        json.dump(config, file, indent=4)
    Debugstat = config["Debug"]
    print("JSON config wile installated")
else:
    with open(config_path, "r") as file:
        config = CommonUtil.safe_load_json("config.json")
        Debugstat = config["Debug"]

class userbase:
    def __init__(self, message="", raw_message=""):
        self.message = message
        self.raw_message = raw_message

    def get_message(self):
        self.message = input("Please enter your prompt: ")
        if self.message == "/debug" or self.message == "/debug/status":
            if self.message == "/debug":
                with open("config.json", "r") as file:
                    config = CommonUtil.safe_load_json("config.json")
                    config["Debug"] = not(config["Debug"])
                    Debugstat = config["Debug"]
                with open("config.json", "w") as file:
                    json.dump(config, file, indent=4)
                tellhim(f"You have turned debug mode {'on' if Debugstat else 'off'}")
                print(Debugstat)
                thestart()
            elif self.message == "/debug/status":
                print(f"Debug is turned {'on' if Debugstat else 'off'}")
                thestart()
        elif self.message == "/stop" or self.message == {f"{("goodbye" or "bye") if self.message[-1] != "!" else ("goodbye!" or "bye!")}"} :
            tellhim("Finishing...")
            quit()
        elif self.message in AlgoParser.listofgreetings:
            return self.message
        else:
            self.raw_message = self.message
            blob = TextBlob(self.message)
            self.message = str(blob.correct())
            return self.message
        
def thestart():
    global User
    User = userbase()
    User.get_message()
    replylogic()

def tellhim(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def replylogic():
    global findingtheplanning, Agrement, findtheplanningdate, findthegreeting, find_the_prediction, finding_the_math, full_info_of_planning, Enclave_completing, cashe_list, match, Nick_finding, findingseparations
    full_info_of_planning = False
    Agrement = random.choice(AlgoParser.agreement_words) + "!"

    try:
        check_completing = re.search(AlgoParser.correction_pattern, User.message, re.IGNORECASE)
        if not check_completing:
            if Debugstat is True:
                print("\nТекст сообщения:", User.message)

            findingtheplanning = {"processplanning": re.search(AlgoParser.planning_pattern, User.message, re.IGNORECASE)}
            if findingtheplanning["processplanning"]:
                findtheplanningdate = {"date": re.search(AlgoParser.date_pattern, User.message, re.IGNORECASE)}
                if findtheplanningdate["date"]:
                    if Debugstat is True:
                        print("\nДата:", (findtheplanningdate["date"].group() if findtheplanningdate else "No date"))
                    full_info_of_planning = True
            findingseparations = {"separations:" : re.finditer(AlgoParser.separ_pattern, User.message, re.IGNORECASE)}
            findthegreeting = {"greeting": re.search(AlgoParser.meeting_words_pattern, User.message, re.IGNORECASE)}
            find_the_prediction = {"processPrediction": re.search(AlgoParser.predictpattern, User.message, re.IGNORECASE)}
            finding_the_math = [{"Maths": match} for match in re.finditer(AlgoParser.math_pattern, User.message, re.IGNORECASE)]
            Nick_finding = {"NameSet": re.search(AlgoParser.provider_pattern, User.message,  re.IGNORECASE)}
            matches = [findingtheplanning, find_the_prediction, findthegreeting, Nick_finding] + finding_the_math
            cashe_list = [match for match in matches if any(match.values())]
            cashe_list.sort(key=lambda match: next(iter(match.values())).span()[0] if match else 0)
            if Debugstat is True:
                print("\nОтсортированный список:", cashe_list)
            Enclave_completing = (True if len(cashe_list) > (2 if findthegreeting else 1) else False)
            def find_engine(User_message):
                if Enclave_completing and cashe_list.index(match) != len(cashe_list) - 1:
                    for searcher in findingseparations:
                        if (cashe_list[(cashe_list.index(match) + 1)].values.start() - 1) - (searcher.end() - 1) <= 3:
                            if searcher == "and" or searcher == "+":
                                end_index = searcher.start() - 1
                                return end_index
                            else:
                                if User_message[searcher.end() : (cashe_list[(cashe_list.index(match) + 1)].values.start())].isspace():
                                    end_index = searcher.end() - 1
                                    return end_index
                                else:
                                    for i in range(searcher.end(), (cashe_list[(cashe_list.index(match) + 1)].values.start())):
                                        if not User_message[i].isspace():
                                            infoamo += 1
                                    if infoamo * 100 / len( User_message[searcher.end() : (cashe_list[(cashe_list.index(match) + 1)].values.start())]) >= 40:
                                        end_index = searcher.end() - 1
                                        return end_index
                                    else:
                                        for i in range(searcher.end(), (cashe_list[(cashe_list.index(match) + 1)].values.start()), -1):
                                            if not User_message[i].isspace():
                                                end_index = i
                                                return end_index
                else:
                    end_index = len(User_message) - 1 
                print(find_engine(User.message))
            for match in cashe_list:
                if not match:
                    continue
                try:
                    key, value = next(iter(match.items()))
                    if value and hasattr(value, "group"):  # Ensure value is a match object
                        if Debugstat is True:
                            print(f"\nProcessing {cashe_list.index(match) + 1} task: {key}: {value.group()}")
                        if key == "Maths":
                            task_compiller("Maths", value.group())  # Pass the expression for Maths
                        elif key == "greeting":
                            task_compiller("greating")
                        else:
                            task_compiller(str(key), value.group())
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
        tellhim(f"\nError: {e}\nLength of cashe list: {len(cashe_list)}\n")
        error = traceback.format_exc()
        print(error)
        thestart()


def task_compiller(task_to_start, expression=None):
    if task_to_start == "Maths" and expression:
        Maths_complete_status = TheMaths.process_math(expression)
        if Maths_complete_status == "S":
            if not Enclave_completing:
                thestart()
        else:
            print("Task complecation is Either unsupported to process or faced error while processing.")
            if not Enclave_completing:
                thestart()
            
        
    if task_to_start == "greating":
        from CommonUtil import sayhello
        sayhello()
        if not Enclave_completing:
            thestart()
    elif task_to_start == "processplanning" or task_to_start == "AgreementPlanning":
        PlanningStatus = PlanCrafting.processplanning(User.message, User.raw_message)
        if Debugstat:
            print("\n=======PlanCrafterBios=======")
        if PlanningStatus == "S":
            if not Enclave_completing:
                thestart()
            else:
                print("The complication of 'PlanCrafting' has ended with error, sorry")
        else:
            print("\n\nsomething went wrong with processing the data")
    elif task_to_start == "processfixing":
        TextCorrectEngine.processfixing(User.message)
    elif task_to_start == "processPrediction":
        Ai_Engine.processPrediction()
    elif task_to_start == "NameSet":
        FileRenamingStatus, message = FileManagement.name_giver(User.message)
        if FileRenamingStatus == "Success":
            from FileManagement import end_index
            User.message = message[:Nick_finding["NameSet"].start()] + User.message[end_index:]
            if not Enclave_completing:
                thestart()
        else:
            tellhim("We coul not process the task due output error")
    else:
        if not Enclave_completing and not task_to_start == 'Maths':
            tellhim(f"An error occurred with {task_to_start} task.")

thestart()

