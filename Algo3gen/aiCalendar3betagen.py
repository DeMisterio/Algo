import re
import time
import sys
from textblob import TextBlob
import difflib
import random
from sklearn.linear_model import LinearRegression
import numpy as np

# Установить предсказуемость результатов
try:
    import AlgoParser
    print("Database successfully imported.")
except ImportError as e:
    print("Import error:", e)

#excluded_languages = ['bg', 'uk', 'be']  # Болгарский, Украинский, Белорусский

#def detect_with_restrictions(text):
 #   langs = detect_langs(text)
  #  for lang in langs:
   #     # Исключаем похожие на русский языки
    #    if lang.lang in excluded_languages:
     #       continue
      #  return lang.lang  # Возвращаем первый подходящий язык
   # return "unknown" 

def thestart():
    global UserPrompt, blob, corrected_text, Prompt, language_user
    UserPrompt = input("Please enter your prompt: ").lower()
    #if len(UserPrompt.strip()) < 5:
     #   print("Error: Input text too short to detect language.")
      #  thestart()

    #language_code = detect_with_restrictions(UserPrompt)
    #language_user = language_code[:2]
    #print(f"Detected language: {language_user}")
    try:
        #UserPrompt = GoogleTranslator(source=language_user, target='en').translate(UserPrompt)
        #print(f"Non-English detected! Language: {language_user}")
        blob = TextBlob(UserPrompt)
        Prompt = blob.correct()
        corrected_text = Prompt.string
        replylogic()
    except Exception as e:
        print("Translation error:", e)
        thestart()


def tellhim(text, speed=0.03):
    #if language_user != "en":
     #   text = GoogleTranslator(source='en', target=language_user).translate(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# Similarity calculation between two texts
def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)
    return seq.ratio()

def tryingtoreach(items, text):
    global best_match_item, best_match_word, guessed
    max_similarity = 0
    best_match_item = None
    best_match_word = None
    guessed = None  # Инициализируем переменную
    
    for item in items:
        for word in text.split():
            similarity = get_similarity(item, word)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_item = item
                best_match_word = word
                guessed = best_match_word

def replylogic():
    global findingtheplanning, pleasure, meating, Agrement, findtheplanningdate

    finding_adjusting_the_text = re.search(AlgoParser.correction_pattern, corrected_text)

    if finding_adjusting_the_text:
        meating = random.choice(AlgoParser.listofgreetings) + "!"
        processfixing()
        return

    findingtheplanning = re.search(AlgoParser.planning_pattern, corrected_text)
    findthegreeting = re.search(AlgoParser.meeting_words_pattern, corrected_text)
    find_the_prediction = re.search(AlgoParser.predictpattern, corrected_text)

    if findthegreeting and not finding_adjusting_the_text:
        pleasure = True
        meating = random.choice(AlgoParser.listofgreetings) + "!"
    else:
        pleasure = False
        meating = ""

    Agrement = random.choice(AlgoParser.agreement_words) + "!"

    if findingtheplanning:
        findtheplanningdate = re.search(AlgoParser.patternofdate, corrected_text)
        processplanning()
    elif find_the_prediction:
        tellhim("AI feature is in beta...")
        processPrediction()
    else:
        tellhim(f"{meating} Algo is sorry, but it can't process your request.")
        thestart()
    if findingtheplanning and find_the_prediction and finding_adjusting_the_text:
        tellhim("Sorry, Algo is unavailable to do so many tasks at the same time.")

def processplanning():
    global tryingtoreach, extracted_text, findingtheplanning, guessed
    similarity = get_similarity(UserPrompt, corrected_text)
    tellhim(f"{meating} Algo is trying to understand your text: \" {corrected_text} \"")
    minlenprompt = 5
    tellhim("Algo working...")

    if findingtheplanning and findtheplanningdate:
        tellhim("Algo found your mission...")
        start_idx = corrected_text.find(findingtheplanning.group()) + len(findingtheplanning.group())
        end_idx = findtheplanningdate.start() if findtheplanningdate else len(corrected_text)
        extracted_text = corrected_text[start_idx:end_idx].strip()

        words_to_remove = [findingtheplanning, findtheplanningdate, "me"]
        for word in words_to_remove:
            if isinstance(word, re.Match):
                extracted_text = re.sub(re.escape(word.group()), "", extracted_text).strip()
            elif isinstance(word, str):
                extracted_text = re.sub(re.escape(word), "", extracted_text).strip()

        extracted_text = re.sub(r'[\W_]+$', "", extracted_text)

        if similarity > 0.6:
            tellhim(f"Just to clarify, you want {extracted_text}, yes?")
            AgreeDisagreeProcessing()
        else:
            if findtheplanningdate:
                tellhim(f"{Agrement} I will remind you {extracted_text} on {findtheplanningdate.group()}")
            else:
                tellhim(f"{Agrement} I will remind you to {extracted_text} at the specified time.")
            thestart()
    elif findingtheplanning and not findtheplanningdate:
        tryingtoreach(AlgoParser.listofdates, corrected_text)
        tellhim("Algo found your mission, but couldn't find your time...")
        start_idx = corrected_text.find("to") + len("to")
        end_idx = len(corrected_text)
        extracted_text = corrected_text[start_idx:end_idx].strip()
        fixed_extracted_text = extracted_text.replace(best_match_word, "").strip()
        tellhim(f"By '{best_match_word}', did you mean {fixed_extracted_text} at '{best_match_item}'?")
        AgreeDisagreeProcessing()
    else:
        if len(corrected_text) < minlenprompt:
            tellhim("If you need help, please tell me when.")
            thestart()

def processfixing():
    tellhim(f"\n\n{meating} Algo is processing your text")
    tellhim(f"Corrected text: {corrected_text}")

def theguessing(the_parameters_value, parameter_training_value):
    # Convert the lists to NumPy arrays
    X = np.array(the_parameters_value).reshape(-1, 1)
    y = np.array(parameter_training_value)

    # Create a Linear Regression model instance
    model = LinearRegression()

    # Train the model using the prepared data
    model.fit(X, y)

    # Display the slope and intercept (optional debugging info)
    slope = model.coef_[0]
    intercept = model.intercept_

    print(f"Model trained with slope: {slope}, intercept: {intercept}")
    return model

def processPrediction():
    global the_parameters_value, parameter_training_value
    print("You are training Ai model. Enter parameters in the format 'number(the year for example, \nit is needed for training the model) -number (the result of this year for example)'.\n Type 'stop' to finish. More data - better results")
    the_parameters_value = []
    parameter_training_value = []
    while True:
        user_input = input("Enter parameters: ")
        if user_input.lower() == 'stop':
            break
        try:
            first_value, second_value = map(int, user_input.split('-'))
            the_parameters_value.append(first_value)
            parameter_training_value.append(second_value)
        except ValueError:
            print("Invalid format! Please enter values in the format 'number-number'.")
    # Lazy import inside the function
    tellhim("Algo is starting to train the model!")
    theguessing(the_parameters_value, parameter_training_value)

def AgreeDisagreeProcessing():
    global response
    if findingtheplanning: 
        response = input("Your response: ").strip()
        #if language_user != "en":
          #  response = GoogleTranslator(source=language_user, target='en').translate(response)
        agree = re.search(AlgoParser.Agrementpattern, response, re.IGNORECASE)
        disagree = re.search(AlgoParser.DisagreementPattern, response, re.IGNORECASE)

        if agree:
            if findtheplanningdate:
                tellhim(f"{Agrement} I will remind you to {extracted_text} {findtheplanningdate.group()}")
            else:
                tellhim(f"{Agrement} I will remind you to {extracted_text} at the specified time.")
            thestart()
        elif disagree:
            tellhim("I'm sorry! Could you clarify again?")
            thestart()
        else:
            tellhim("I didn't understand that. Could you repeat, please?")
            AgreeDisagreeProcessing()

thestart()