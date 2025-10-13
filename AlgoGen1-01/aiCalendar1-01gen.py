import re
import time
import sys
from textblob import TextBlob
import difflib

listofdates = [
    "today", "tomorrow", "yesterday",
    "next week", "last week", "this week",
    "next month", "last month", "this month",
    "next year", "last year", "this year",
    "day after tomorrow", "day before yesterday",
    "in two days", "in three days",
    "next Monday", "next Tuesday", "next Wednesday", "next Thursday", "next Friday", "next Saturday", "next Sunday",
    "last Monday", "last Tuesday", "last Wednesday", "last Thursday", "last Friday", "last Saturday", "last Sunday",
    "this Monday", "this Tuesday", "this Wednesday", "this Thursday", "this Friday", "this Saturday", "this Sunday",
    "in a week", "in a month", "in a year",
    "a week ago", "a month ago", "a year ago",
    "in the future", "in the past",
    "the day after", "the day before",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
]
listofpositiveresponses = [
    "Yes", "Of course", "Absolutely", "Definitely", "Sure", "Certainly", 
    "Exactly", "No doubt", "For sure", "Totally", "Without a doubt", 
    "Yep", "You bet", "Right on", "Affirmative", "Indubitably", 
    "Indeed", "Naturally", "Unquestionably", "Absolutely right", "For certain",
    "Yep, for sure", "That's correct", "Sounds good", "I agree", "That's right"
]
listofnegativeresponses = [
    "No", "No way", "Not at all", "Definitely not", "I don't think so", 
    "Absolutely not", "Nope", "Not really", "I don't agree", "Not likely", 
    "Can't say yes to that", "Unlikely", "Not a chance", "Negative", "Never", 
    "I’m afraid not", "That's not right", "That's incorrect", "I don't believe so", 
    "Unfortunately not", "I disagree"
]
listofgreetings = ["hello", "greetings", "hi", "hey", "howdy", "hola", "bonjour", "Good", ""]
def tellhim(text, speed=0.07):
    for char in text:
        sys.stdout.write(char)  # Печатает символ без перехода на новую строку
        sys.stdout.flush()  # Принудительный вывод символа на экран
        time.sleep(speed)  # Задержка между символами
    print()

def thestart():
    global UserPrompt, blob, corrected_text, Prompt
    UserPrompt = input("Please enter your prompt: ")
    blob = TextBlob(UserPrompt)  # Создаём объект TextBlob для обработки текста
    Prompt = blob.correct()  # Исправленный текст
    corrected_text = Prompt.string  # Получаем строку из исправленного текста
    replylogic()  # Запуск обработки (нужна реализация функции process)

# Функция для расчёта схожести между текстами
def get_similarity(UserPrompt, corrected_text):
    seq = difflib.SequenceMatcher(None, UserPrompt, corrected_text)  # Сравниваем исходный и исправленный текст
    return seq.ratio()

patternofdate = r"\b(?:today|yesterday|tomorrow|next\s(?:week|month|year)|last\s(?:week|month|year)|this\s(?:week|month|year)|\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"
meeting_words_pattern = r"\b(hello|hi|hey|greetings|howdy|what's up|good morning|good evening|good afternoon)\b"

def tryingtoreach(items, text):
        global item, best_match_item, best_match_word
        max_similarity = 0  # Инициализация максимальной схожести
        best_match_item = None  # Хранение наилучшего совпадения из items
        best_match_word = None  # Хранение слова из text, которое лучше всего совпадает

        for item in items:  # Перебираем каждый элемент
            for word in text.split():  # Перебираем каждое слово в тексте
                similarity = get_similarity(item, word)  # Вычисляем схожесть
                if similarity > max_similarity:  # Обновляем лучший результат при необходимости
                    max_similarity = similarity
                    best_match_item = item
                    best_match_word = word

def replylogic():
    global findingtheplanning
    findingtheplanning = re.search(patternofdate, corrected_text)
    findthegreeting = re.search(meeting_words_pattern, corrected_text)
    if findthegreeting:
        pleasure = True
    if findingtheplanning:
        processplanning()
    


def processplanning():
    global tryingtoreach, extracted_text, findingtheplanning
    similarity = get_similarity(UserPrompt, corrected_text)
    tellhim(f"Algo is trying to understand your text: {corrected_text}")  # Выводим исправленный текст для диагностики
    minlenprompt = 5
    tellhim("Algo working...")
    
        # Извлекаем текст между "to" и датой в исправленном тексте
    if "to" in corrected_text.split():
        tellhim("Algo found your mission...")
        start_idx = corrected_text.find("to") + len("to")
        end_idx = findingtheplanning.start()  # Индекс начала совпадения
        extracted_text = corrected_text[start_idx:end_idx].strip()  # Извлекаем текст
        
        # Удаление нескольких слов из строки
        words_to_remove = ["will", findingtheplanning.group()]
        for word in words_to_remove:
           extracted_text = extracted_text.replace(word, "").strip()
        
        if similarity > 60:
            tellhim(f"Just to Clarify, you want to {extracted_text}, yep?")
            AgreeDisagreeProcessing()
        else:
            print(f"Okay! I will remind you to {extracted_text} {findingtheplanning.group()}")
            thestart()
       
    elif not findingtheplanning:
        tryingtoreach(listofdates, corrected_text)
        if "to" in corrected_text:
            tellhim("Algo found your mission, but could not find your time...")
            start_idx = corrected_text.find("to") + len("to")
            end_idx = len(corrected_text)  # Исправление ошибки
            extracted_text = corrected_text[start_idx:end_idx].strip()  # Извлекаем текст
            wordtoremove = best_match_word
            fixed_extracted_text = extracted_text.replace(wordtoremove, "").strip()
            tellhim(f"I am sorry, but by '{best_match_word}' from your prompt, \n did you mean that you will {fixed_extracted_text}\n  '{best_match_item}'?") 
            AgreeDisagreeProcessing()
            

    else: 
        if len(corrected_text) < minlenprompt:
            time.sleep(0.3)
            tellhim("Well, if it's kind of work you need to do, please tell me when")
            findingtheplanning.group() == input("")
            print(f"Okay! I will remind you to {extracted_text} {findingtheplanning.group()}")
            thestart()


def AgreeDisagreeProcessing():
        responce = input("")
        best_match_word = None
        best_match_item = None
        tryingtoreach(listofpositiveresponses, responce)
        if best_match_word in listofpositiveresponses:
            tellhim(f"Okay! I will remind you to {extracted_text} {findingtheplanning.group()}")
            thestart()
        elif best_match_word not in listofpositiveresponses:
            tryingtoreach(listofnegativeresponses, responce)
            if best_match_word in listofnegativeresponses:
                tellhim(f"I'am so sorry! can you please tell me again?")
                thestart()
        elif best_match_word not in listofnegativeresponses and listofpositiveresponses:
            print("Sorry! My hearing is bad, could you repeat please?")
            responce = None
            responce = input("")

thestart()