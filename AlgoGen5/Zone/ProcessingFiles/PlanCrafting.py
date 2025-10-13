try:
    from Kernel import Debugstat, nlp, Uname
    import CommonUtil
    from datetime import datetime
    import dateparser
    import pandas as pf
    import csv
    import os
    import AlgoParser
    import re
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
    if Debugstat:
        print("* PlanCrafting successfully imported")
except:
    ImportError
attempt = 0
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
entryV, intro_phraseV = CommonUtil.user_info_giver()

def message_retreiver(User_message, SpotCommand):
    if Debugstat:
        print("\nMessage retreived successfully!")
    scalpel(User_message, SpotCommand)
    pass


def scalpel(User_message, SpotCommand, User_need="Prompt_analysis"):
    global text_cleaned, command_word, command
    text = User_message

    # Возможные команды
    if User_need == "Prompt_analysis":
        command_word = [str(SpotCommand)]

    # 1. Выделяем команду
    tokens = text.lower().split()
    if User_need == "Prompt_analysis":
        command = " ".join([w for w in tokens if w in command_word])

    # 2. Ищем дату (через отдельную проверку каждого слова/фразы)
    parsed_date = None
    for i in range(len(tokens)):
        phrase = " ".join(tokens[i:])
        parsed = dateparser.parse(phrase, languages=['en'])
        if parsed:
            parsed_date = parsed
            date_phrase = phrase
            break

    # 3. Чистим текст от команды и даты
    if User_need == "Prompt_analysis":
        text_cleaned = text
        if command:
            text_cleaned = text_cleaned.replace(command, "")
        if parsed_date:
            text_cleaned = text_cleaned.replace(date_phrase, "")

    # 4. Вывод 
    if Debugstat is True:
        if User_need == "Prompt_analysis":
            print("Команда:", command.strip())
            print("Текст:", text_cleaned.strip())
        print("Дата:", parsed_date)
    date_getter(command.strip(), parsed_date, text_cleaned.strip())
    pass

def date_getter(comand, date, task):
    
    if date == None:
        date_confirmer()
    event_saver(task, date)

def routine_setter(event):
    pass

def event_saver(event_task, event_date, event_place=None, event_participants=None, csv_file="Planning_base.csv"):
    #CSV file creation
    participant_pattern = r'\bwith\b\s+(\w+)'
    if not os.path.exists(csv_file):
        with open(csv_file, mode="w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["event_task", "event_place", "event_participants", "event_date"])
            if Debugstat:
                print("\nFile of dates successfully created.")
    places = []
    doc = nlp(event_task)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "FAC"]:  # FAC - facility, GPE - страны/города, LOC - локации
            places.append(ent.text)
    joined_places = ", ".join(places)
    if len(joined_places) > 1 and not joined_places.isspace():
        CommonUtil.tellhim(f"\nis the {joined_places} is where you will be?")
        agree, disagree = CommonUtil.AgreeDisagreeProcessing("PlanCrafting")
        if agree:
            event_place = joined_places
        if disagree:
            event_place = None
            CommonUtil.tellhim(f"\n {np.random.choice(AlgoParser.agreement_words)}")
        else:
            CommonUtil.tellhim(f"\n {np.random.choice(AlgoParser.agreement_words)}")

        event_participants = None
        participant_search = re.search(participant_pattern, event_task, re.IGNORECASE)
        if participant_search:
            CommonUtil.tellhim(f"\nAre you going {str(participant_search.group())} ?")
            agree, disagree = CommonUtil.AgreeDisagreeProcessing("PlanCrafting")
            if agree:
                event_participants = str(participant_search.group()) 
            if disagree:
                CommonUtil.tellhim(f"\n {np.random.choice(AlgoParser.agreement_words)}")
    try:
        df = pf.read_csv(csv_file)
    except FileNotFoundError:
        df = pf.DataFrame(columns=["event_task", "event_place", "event_participants", "event_date"])
    df = pf.concat([df, pf.DataFrame([{"event_task" : event_task, "event_place" : event_place, "event_participants" : event_participants, "event_date" : event_date}])], ignore_index=True)
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    CommonUtil.tellhim(f"\n{intro_phraseV}, {Uname}, You will be reminded {event_task} on time!")
def date_confirmer():
    global attempt
    attempt += 1
    if attempt < 4:
        date = input("\nPlease insert correct date" if attempt == 1 else "You need to insert only date in your text. Like (tomorrow) or (next week)\n To cancel say 'stop'.")
        if date != "stop":
            scalpel(date, None, None)
        