import pandas as pf
import os
import csv
import re
import CommonUtil
from Kernel_F.user import userbase
User = userbase()
Debugstat = CommonUtil.read_key_from_JSON("Udebug")
usednickname = False
csvrowrewriting = False
attempt = 0
if Debugstat:
    print("* FileManagement module has successfully loaded!")


def NickGiver(file_directory, nickname, point, csv_file="Base.csv"):
        global csvrowrewriting, usednickname

        # Проверяем наличие файла, создаем его, если отсутствует
        if point == "WriteNEW":
            if not os.path.exists(csv_file):
                with open(csv_file, mode="w", encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["FileDirectory", "Nickname"])
                    if Debugstat:
                        print("\nFile successfully created.")
        elif point == "Rewrite":
            Renamer(df_index)
        # Загружаем данные из CSV
        try:
            df = pf.read_csv(csv_file)
        except FileNotFoundError:
            df = pf.DataFrame(columns=["FileDirectory", "Nickname"])  # Создаем пустой DataFrame

        def Renamer(df_index):
            df.at[df_index, "Nickname"] = name
            df.to_csv(csv_file, index=False)

            # Перезагружаем DataFrame после сохранения
            df_updated = pf.read_csv(csv_file)
            if df_updated.iloc[df_index]["Nickname"] == name:
                return True
            else:
                CommonUtil.tellhim("❌ Ошибка при изменении ника.")
                return False

        # Проверяем существующую запись
        for df_index, row in df.iterrows():
            if row["FileDirectory"] == file_directory:
                if Debugstat:
                    print("\nСовпадение найдено.")
                CommonUtil.tellhim(f"Путь '{file_directory}' уже существует в базе, перезапишем ник?")
                agree, disagree = CommonUtil.AgreeDisagreeProcessing("NickSet")
                
                if agree:
                    csvrowrewriting = True
                    name = User.get_message()
                    file_directory = file_directory
                    if Renamer(df_index):
                        return True
                    else:
                        CommonUtil.tellhim("An error occurred in renamer function.")
                        return False
                if disagree:
                    
                    CommonUtil.tellhim(f"Путь '{file_directory}' с ником '{row['Nickname']}' оставлен без изменений.")
                    usednickname = True
                    return True

        # Добавляем новую запись
        df = pf.concat([df, pf.DataFrame([{"FileDirectory": file_directory, "Nickname": nickname}])], ignore_index=True)
        df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        if Debugstat:
            print(f"\nПуть '{file_directory}' с ником '{nickname}' успешно добавлен.")
        return True


def name_giver(User_message, name=0):
    global end_index, attempt
    substring = "/"
    indexes = [match.start() for match in re.finditer(substring, str(os.getcwd()))]
    if len(indexes) < 2:
        CommonUtil.tellhim("Ошибка: путь не найден.")
        return

    the_path_head = os.getcwd()[indexes[0]:indexes[1]]
    the_path_head = the_path_head[1:]

    if User_message and the_path_head in User_message:
        start_index = User_message.index(the_path_head)
        end_index = len(User_message)
        for i, char in enumerate(User_message[start_index:]):
            if char == " ":
                end_index = start_index + i
                break

        file_directory = User_message[start_index:end_index]

        if Debugstat:
            print("Данные:", start_index, end_index, file_directory)
        if name == 0:
            name = User.get_message()
        success = NickGiver(file_directory, name, "WriteNEW")
            
        if success == True:
            if not usednickname:
                pass
            else:
                CommonUtil.tellhim(f"Success! The path is already in the base. You can find it by the 'find {name}' command.")
        else:
            print("An error occurred, no success.")
            return "Success", User_message
    else:
        attempt += 1
        if attempt != 2:
            CommonUtil.tellhim(f"The path is not found. The path head is {the_path_head}. Please check if the path is valid. and enter in again:")
            luck_of_path_solver()
        else:
            CommonUtil.tellhim(f"To use this fuction, you must call it by typing: give nickname 'Your path'\n Please try again") 
            return "Unsuccess", User_message

def luck_of_path_solver():
    file_path = User.get_message()
    name_giver(file_path)
