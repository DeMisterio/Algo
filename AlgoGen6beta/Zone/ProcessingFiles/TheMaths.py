import re
from sympy import symbols, Eq, solve
import sys
import time
import CommonUtil
import asyncio
import os
import edge_tts
Debugstat = CommonUtil.read_key_from_JSON("Udebug")
Uname = CommonUtil.read_key_from_JSON("Uname")
if Debugstat:
    print("* TheMaths has successfully loaded!")


async def main(infov, UnameV, entryV, intro_phraseV, purpose):
    if purpose == "retell":
        tts = edge_tts.Communicate(text=(infov), voice="en-CA-LiamNeural")
    elif purpose == "ask":
        tts = edge_tts.Communicate(text=(infov + "," + entryV + UnameV + "?"), voice="en-CA-LiamNeural")
    await tts.save("output.mp3")




def process_math(expression):
    if expression:
        success = process_math_problem(expression)
        if success == "S":
            return "S"



def replacement(text):
    """
    Функция заменяет слова-операторы на математические символы и убирает 'by',
    но не удаляет 'x' или другие переменные.
    """
    text = re.sub(r"\bby\b", "", text)  # Удаляем ВСЕ "by"
    
    # Полностью заменяем операторы с пробелами
    text = re.sub(r"\bplus\b", "+", text)
    text = re.sub(r"\bminus\b", "-", text)
    text = re.sub(r"\bmultiplied\b", "*", text)
    text = re.sub(r"\bdivided\b", "/", text)

    # Убираем лишние пробелы между числами, но сохраняем переменные (x, y, z)
    text = re.sub(r'(?<=\d)\s+(?=\d)', '', text)  # Убираем пробелы ТОЛЬКО между цифрами
    text = re.sub(r'\s+', ' ', text).strip()  # Удаляем лишние пробелы
    
    return text
def process_math_problem(text):
    """
    Функция находит и решает математическое выражение в тексте.
    """
    text = replacement(text)  # Предобработка текста

    # Теперь используем `re.findall()` для извлечения ВСЕЙ строки с числами и операциями
    matches = re.findall(r"[\d\s\+\-\*/=]+", text)

    if not matches:
        CommonUtil.tellhim("Algo could'nt find any math problems.") 
        return "Uncussessed"

    # Объединяем все найденные части выражения
    math_expression = " ".join(matches).strip()
    print(f"Algo is solving {math_expression}", end="")

    # Проверяем, является ли это уравнением (если есть '=')
    if '=' in math_expression:
        try:
            x = symbols('x')  # Определяем переменную
            left, right = math_expression.split('=')
            equation = Eq(eval(left), eval(right))  # Преобразуем в уравнение
            solution = solve(equation, x)
            CommonUtil.tellhim(f"Solution: \n{'=' * len(str(solution))} {solution} \n{'=' * len(str(solution))}") 
            return "S"
        except Exception as e:
            CommonUtil.tellhim(f"Algo dont know how to solve it") 
            return "U"
    else:
        # Решаем обычный арифметический пример
        try:
            result = eval(math_expression)  # Вычисляем значение
            CommonUtil.tellhim(f"\n it's {result}") 
            return "S"
        except Exception as e:
            CommonUtil.tellhim(f"Algo has head aik, sorry... {e}") 

# 🧪 **Тестовый пример**
