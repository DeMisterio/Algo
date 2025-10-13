import re
from sympy import symbols, Eq, solve
import sys
import time

def tellhim(text, speed=0.03):
    '''if language_user != "en":
        text = GoogleTranslator(source='en', target=language_user).translate(text)'''
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def replacement(text):
    global newtext
    newtext = text
    wmatch = re.findall(r"plus|minus|devided|multiplied", text)
    byfind = re.search(r"by", text)
    if byfind:
        newtext = text.replace("by", "")
        print(newtext)
    if wmatch:
        print(wmatch)
        if 'plus' in wmatch:
            newtext = newtext.replace("plus", "+")
        if 'minus' in wmatch:
            newtext = newtext.replace("minus", "-")
        if 'devided' in wmatch:
            newtext = newtext.replace("devided", "/")
        if 'multiplied' in wmatch:
            newtext = newtext.replace("multiplied", "*")


def process_math_problem(text):
    #import aiCalendar3betagen
    # Шаг 1: Найти математическое выражение в тексте
    match = re.search(r"([\d\s\+\-\*/x=()]+)", text)
    wmatch = re.findall(r"plus|minus|devided|multiplied", text)
    if not match and not wmatch:
        tellhim("Алго не смог найти никакого примера или уравнения") 
        #aiCalendar3betagen.thestart()
    elif wmatch and not match:
        replacement(text)
        process_math_problem(newtext)
    elif wmatch and match:
        replacement(text)
        process_math_problem(newtext)
        

    math_expression = match.group(1).strip()
    tellhim(f"Надено выражение: {math_expression}")

    # Шаг 2: Проверить, является ли это уравнением (есть '=')
    if '=' in math_expression:
        # Обработка уравнений
        try:
            x = symbols('x')  # Определяем переменную
            left, right = math_expression.split('=')
            equation = Eq(eval(left), eval(right))  # Преобразуем в уравнение
            solution = solve(equation, x)
            tellhim(f"Решение уравнения: {solution}") 
            #aiCalendar3betagen.thestart()
        except Exception as e:
            tellhim(f"Алго пока не умеет решать такое: {e}") 
            #aiCalendar3betagen.thestart()
    else:
        # Обработка простых арифметических задач
        try:
            result = eval(math_expression)  # Вычисляем значение
            tellhim(f"Алго нашел решение: {result}") 
            #aiCalendar3betagen.thestart()
        except Exception as e:
            tellhim(f"Алго запутался при решении задачи, просим прощения: {e}") 
            #aiCalendar3betagen.thestart()

# Примеры использования




    
    