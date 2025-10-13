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

# List of agreement words and phrases for a chatbot
agreement_words = [
    "Yes", "Certainly", "Understood", "Absolutely", "Noted", "Of course", 
    "Very well", "I acknowledge", "Affirmative", "As you wish", "I understand",
    "Sure thing", "Alright", "No problem", "Got it", "Sounds good", 
    "Okay then", "Will do", "All set", "Happy to assist", "Not an issue",
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
    "Themselves"
    "me" # Reflexive form of 'They'
]
synonyms = ["predict", "forecast", "anticipate", "foresee", "prophesy", "project"]

planning_pattern = r'\b(\w+ing\s+to)\b|will|plan|remind|notice|remember|want'
patternofdate = r"\b(?:today|yesterday|tomorrow|next\s(?:week|month|year)|last\s(?:week|month|year)|this\s(?:week|month|year)|\d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"
meeting_words_pattern = r"\b(hello|hi|hey|greetings|howdy|what's up|good morning|good evening|good afternoon)\b"
Agrementpattern = r'\b(?:yes|yeah|yep|ok(?:ay)?|sure|absolutely|fine|noted|understood|got it|cool|no problem|works for me|sounds good|affirmative|roger|consider it done|absolutely|you are right|probably|particulary|definetely|leterally)\b'
DisagreementPattern = r'\b(?:no|nah|nope|never|not really|don\'t agree|disagree|absolutely not|certainly not|that\'s wrong|false|incorrect|I doubt it|unlikely|not sure|don\'t think so|impossible|not at all|reject|nonsense|not quite)\b'
correction_pattern = r'\b(?:correct|fix|adjust|improve|edit|revise|proofread|mistake|error|typo|gramm(?:ar|atical)|spell(?:ing)?|wrong|rewrite|rephrase|tweak|modify|filters|settings)\b'
predictpattern = r"^(?:{})\b|(?:{})\b$".format("|".join(synonyms), "|".join(synonyms))


