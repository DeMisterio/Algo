import re, json
from datetime import datetime, timedelta
print("Loading...")
def read_key_from_JSON(key, filename="config.json"):
    try:
        with open(filename, "r") as file:
            config = json.load(file)
        return config.get(key, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
name = read_key_from_JSON("Uname")
Debugstat = read_key_from_JSON("Debug")

if Debugstat is True:
    print("\n\n========STARTING IMPORT========", "\n* AlgoParser.py is loaded... Your are here bro")
listofgreetings = ["hello", "greetings", "hi", "hey", "howdy", "hola", "bonjour", "Hola!", ""]
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
list_of_separations = [",", "and", "+"]
listofpositiveresponses = [
    "Y","Yes", "Of course", "Absolutely", "Definitely", "Sure", "Certainly", 
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

# List of agreement words and phrases for a chatbot
agreement_words = [
    "Yes", "Certainly", "Understood", "Absolutely", "Noted", "Of course", 
    "Very well", "I acknowledge", "Affirmative", "As you wish", "I understand",
    "Sure thing", "Alright", "No problem", "Got it", "Sounds good", 
    "Okay then", "All set", "Happy to assist", "Not an issue",
    "Okay", "Yep", "No worries", "Sure", "Fine by me", 
    "Cool", "You got it", "Alrighty", "Alright, no probs", "Gotcha",
    "Consider it done", "Let’s proceed", "I’ll take care of that", "On it", "Works for me"
]
personal_pronouns = [
    "I",        # First person singular
    "You",      # Second person singular/plural
    "He",       # Third person singular (masculine)
    "She",      # Third person singular (feminine)
    "It",       # Third person singular (neutral)
    "We",       # First person plural
    "They",     # Third person plural
    "Me",       # Object form of 'I'
    "Him",      # Object form of 'He'
    "Her",      # Object form of 'She'
    "Us",       # Object form of 'We'
    "Them",     # Object form of 'They'
    "Myself",   # Reflexive form of 'I'
    "Yourself", # Reflexive form of 'You' (singular)
    "Himself",  # Reflexive form of 'He'
    "Herself",  # Reflexive form of 'She'
    "Itself",   # Reflexive form of 'It'
    "Ourselves",# Reflexive form of 'We'
    "Yourselves", # Reflexive form of 'You' (plural)
    "Themselves",
    "me",
    "mine",
    "Thee",
    "Ye" # Reflexive form of 'They'
]
synonyms = ["predict", "forecast", "anticipate", "foresee", "prophesy", "project"]

planning_pattern = r'\b(\w+ing\s+to)\b|plan|remind|notice|remember|want'
patternofdate = r"\b(?:today|yesterday|tomorrow|next\s(?:week|month|year)|last\s(?:week|month|year)|this\s(?:week|month|year)|\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"
meeting_words_pattern = r"\b(hello|hi|hey|greetings|howdy|what's up|good morning|good evening|good afternoon)\b"
Agrementpattern = r'\b(?:yes|yeah|yep|ok(?:ay)?|sure|absolutely|fine|noted|understood|got it|cool|no problem|works for me|sounds good|affirmative|roger|consider it done|absolutely|you are right|probably|particulary|definetely|leterally)\b'
DisagreementPattern = r'\b(?:no|nah|nope|never|not really|don\'t agree|disagree|absolutely not|certainly not|that\'s wrong|false|incorrect|I doubt it|unlikely|not sure|don\'t think so|impossible|not at all|reject|nonsense|not quite)\b'
correction_pattern = r'^(?:correct|fix|adjust|improve|edit|revise|proofread|mistake|error|typo|gramm(?:ar|atical)|spell(?:ing)?|wrong|rewrite|rephrase|tweak|modify|filters|settings)\b'
predictpattern = r"^(?:{})\b|(?:{})\b$".format("|".join(synonyms), "|".join(synonyms))
math_pattern = r"(?i)\b(calculate|compute|do the math|solve|evaluate|count|find|determine)\b.*?(\d+(\s*(plus|minus|multiplied by|divided by|\+|\-|\*|/)\s*\d+)*)"
date_pattern = r'\b(?:' + '|'.join(map(re.escape, listofdates)) + r')\b'
provider_pattern = r"\b(give|set|define)\s+nickname\b(?=\s|$)"
separ_pattern =  r"\s*(?:,|\band\b|\bthen\b|\bafter that\b|\bnext\b|\balso\b|\bplus\b|\band then\b|\+|&|/)\s*"
search_pattern = r"^(how|why|when|what|where|who|which|whom|whose|как|почему|зачем|что|где|когда|кто|чей|чья)\b"
entry_titles = {
    "formal_older_men": [
        "Sir", "Mister", "Gentleman", "Respected sir", "Senior", "Kind sir"
    ],
    "formal_older_women": [
        "Madam", "Ma'am", "Missus", "Lady", "Respected madam", "Dear lady"
    ],
    "informal_young_men": [
        "Bro", "Dude", "Bruv", "My guy", "Buddy", "King", "Fella", "Big man", "Champ"
    ],
    "informal_young_women": [
        "Sis", "Girl", "My girl", "Queen", "Bestie", "Hun", "Shorty", "Angel", "Babe"
    ],
    "neutral_men": [
        "Gent", "Fellow", "Dear"
    ],
    "neutral_women": [
        "Gent", "Fellow", "Dear"
    ],
    "intro_phrases": [
        "So...", "Alright,", "Look,", "Okay, listen:", "Here's the thing,", 
        "Now then,", "Well,", "Let me tell you something:", "Listen up,", "So basically,"
    ]
}
name_responses = {
    "40, 150": [
        f"What you need, my friend {name}?",
        f"Hey, {name}, what’s up?",
        f"Tell me, {name}, what’s on your mind?",
        f"Yo, {name}, I’m listening.",
       f"What’s good, {name}?"
    ],
    "30, 40": [
        f"Yo, {name}, what’s the deal?",
        f"Hey, {name}, what you need?",
        f"What’s crackin’, {name}?",
        f"Sup, {name}? Speak up!",
        f"What’s poppin’, {name}?"
    ],
    "20, 30": [
        f"Yo, {name}! What’s good, bro?",
        f"Hey, {name}, spill it!",
        f"What’s up, {name}? Shoot.",
        f"Sup, {name}, what’s happenin’?",
        f"What you got, {name}?"
    ],
    "0, 20": [
        f"Yo, {name}, what’s the vibe?",
       f"Hey, {name}, what’s poppin’?",
        f"What’s good, {name}, my dude?",
        f"Yo, {name}, spill the tea!",
        f"What’s crackin’, {name}?"
    ],
}
test_prompts_list = [
    # Spell Check Tests
    "Helo, hw are yu?",
    "Plase corect my sentnce.",
    "I wnt to meet tomorow.",
    "Calclate 5 + 9*3.",
    "Remind me abot my apointment tommorow.",

    # Reminder Tests (single task reminders)
    "Remind me to call John at 3 PM.",
    "Set a reminder for my doctor's appointment on Monday.",
    "Remind me to buy groceries at 5 PM.",
    "Set a reminder to submit my report next Friday.",
    "Remind me to wish Lisa a happy birthday on June 10th.",
    "Remind me to take my medicine at 8 AM every day.",
    "Set a reminder for my gym session at 7 PM.",
    "Remind me to book flight tickets for my vacation.",
    "Set a reminder to check my email in the morning.",
    "Remind me to water the plants every Sunday.",

    # Math Problem Solving Tests (single task calculations)
    "Solve 25 + 47.",
    "Calculate 8 * 6.",
    "What is 100 / 5?",
    "Find the square root of 144.",
    "Calculate 10^3.",
    "Solve for x: 5x = 20.",
    "Calculate (12 + 18) * 2.",
    "What is the remainder when 50 is divided by 7?",
    "Find the sum of the first 10 natural numbers.",
    "What is the factorial of 5?",

    # Edge Case Testing
    "Remind me to .",
    "Set a reminder for tomorrow.",
    "Remind me at 3 PM.",
    "Solve this equation: ",
    "Fix my sentence: ",
    "What is 0 / 0?",
    "Remind me about my meeting at 25:00.",
    "Calculate sqrt(-1).",
    "Set a reminder to finish work yesterday.",
    "Fix thiiss speellling misttakee.",

    # Avoiding Multi-Tasking (Testing for failure cases)
    "Correct this: Ths is a tset.",
    "Remind me to solve 12*4 at 6 PM.",  # Should fail as it includes two tasks
    "Calculate 20 + 15 and remind me to check the answer at 8 PM.",  # Should fail
    "Set a reminder to check the stock market and solve 45/5.",  # Should fail
    "Fix this: I wnt to remeber my appintment on Saterday.",  # Should pass
    "Remind me to complete my homework at 9 PM and solve 5^3.",  # Should fail
    "Correct this: Tomorow I wil go to scholl.",  # Should pass
    "Solve 7*8 and remind me to check the result at 10 AM.",  # Should fail
    "Fix this: Plase remeber to set the alram at 6 AM.",  # Should pass
    "Set a reminder to call the bank and correct 'I ned help with my accunt'.",  # Should fail
]
