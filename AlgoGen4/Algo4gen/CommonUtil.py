import difflib, re, AlgoParser, random, sys, time, json

decidion_completed = False  
def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()

def tellhim(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
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
        response = input("Your response: ").strip()
        agree = re.search(AlgoParser.Agrementpattern, response, re.IGNORECASE)
        disagree = re.search(AlgoParser.DisagreementPattern, response, re.IGNORECASE)
        if response == "/Users/denilarsanov/Denivenv/bin/python /Users/denilarsanov/Desktop/Dfolder/Zone/Algo4gen/aiCalendar3betagen.py":
            quit()
        return agree is not None, disagree is not None

def sayhello():
        tellhim(f"{random.choice(AlgoParser.listofgreetings)}" + "!")
        return

def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()
Debugstat = read_key_from_JSON("Debug")
if Debugstat:
    print("* CommonUtil has successfully loaded!")