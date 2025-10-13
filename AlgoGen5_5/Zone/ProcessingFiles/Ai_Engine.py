from sklearn.linear_model import LinearRegression
import numpy as np
import sys
import time
import CommonUtil
Debugstat = CommonUtil.read_key_from_JSON("Udebug")
if Debugstat:
    print("* Ai_Engine has successfully loaded!")
def tellhim(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
import torch
import numpy as np

# Загружаем модель
# Текст

def processPrediction():
        print("You are training an AI model. Enter parameters as 'year - value'. Type 'stop' to finish.")
        the_parameters_key = []
        parameter_training_value = []

        while True:
            user_input = input("Enter parameters: ")
            if user_input.lower() == 'stop':
                break
            try:
                first_value, second_value = map(int, user_input.split('-'))
                the_parameters_key.append(first_value)
                parameter_training_value.append(second_value)
            except ValueError:
                print("Invalid format! Use 'number-number'.")

        if len(the_parameters_key) < 2:
            print("Not enough data for training. Enter at least two pairs.")
            return "Unsuccessed"

        tellhim("Training the model...")
        model = theguessing(the_parameters_key, parameter_training_value)

        while True:
            try:
                new_key = input("Enter a year to predict (or type 'exit'): ")
                if new_key.lower() == 'exit':
                    break
                new_key = int(new_key)
                prediction = model.predict(np.array([[new_key]]))[0]
                tellhim(f"Prediction for {new_key}: {prediction:.2f}")
            except ValueError:
                print("Invalid input! Enter a valid number.")

def theguessing(the_parameters_key, parameter_training_value):
    X = np.array(the_parameters_key).reshape(-1, 1)
    y = np.array(parameter_training_value)
    model = LinearRegression()
    model.fit(X, y)
    return model
    