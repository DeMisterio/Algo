import CommonUtil
from rapidfuzz import process
import re

from Kernel_F.user import userbase
User = userbase()
class Settings:
    def __init__(self):
        self.menu = {
            1: f"MODE: ({CommonUtil.read_key_from_JSON('Umode')}) or {'Chat' if CommonUtil.read_key_from_JSON('Umode') == 'Voice' else 'Voice'}",
            2: f"AGE: ({CommonUtil.read_key_from_JSON('Uage')})",
            3: f"GENDER: ({CommonUtil.read_key_from_JSON('Ugender')}) or " +
               (('Female' if CommonUtil.read_key_from_JSON('Ugender') == 'Male' else 'Male')
                if CommonUtil.read_key_from_JSON('Ugender') in ['Male', 'Famale'] else '(Male / Female)'),
            4: f"LANG: Auto",
            5: f"BOTREFERENCE: {CommonUtil.read_key_from_JSON('Ubotreference')}",
            6: f"DEBUG: ({CommonUtil.read_key_from_JSON('Udebug')}) or {'true' if CommonUtil.read_key_from_JSON('Udebug') == 'false' else 'false'} ",
            7: f"VOICEMODEL: ({CommonUtil.read_key_from_JSON('Uvoicemodel')} or {'light' if CommonUtil.read_key_from_JSON('Uvoicemodel') == 'big' else 'big'})",
            8: f"AI_api_key: {CommonUtil.read_key_from_JSON('AI_api_key')}"
        }

    def menu_show(self):
        CommonUtil.tellhim(f", ".join([f"{k}: {v}" for k, v in self.menu.items()]))

    def change(self, parameter):
        attempt = 0
        while attempt < 5:
            code_input = parameter.strip()
            attempt += 1

            # If digit and valid number
            if code_input.isdigit():
                code_num = int(code_input)
                if code_num in self.menu:
                    parameter = self.menu[code_num].split(":")[0].upper()
                    break
                else:
                    CommonUtil.tellhim("The number is not correct, try again.")
                    continue

            # Exact match by value
            if code_input.upper() in (v.split(":")[0].upper() for v in self.menu.values()):
                parameter = code_input.upper()
                break

            # Approximate match
            match = process.extractOne(code_input.upper(), [v.split(":")[0].upper() for v in self.menu.values()])
            if match:
                result, score, _ = match
                if score > 70:
                    parameter = result
                    break
            else:
                parameter = "UNS"
            CommonUtil.tellhim("The parameter is not valid, try again")
        parameterCONFIG = "U" + parameter.lower()
        parameterCONFIG = parameterCONFIG.strip()
        CommonUtil.tellhim('Enter the new value for this parameter (Copy paste available after slash or type your custom one)')
        newp = User.get_message()
        if parameterCONFIG == "Udebug":
            if (newp.lower() == 'false' or newp.lower() == "true"):
                if newp.lower() == 'false':
                    newp = False
                elif newp.lower() == 'true':
                    newp = True
            else:
                match = process.extractOne(newp.lower(), ['true', 'false', 'zero', 'one'])
                if match:
                    result, score, _ = match
                    if score > 80:
                        if match == 'zero':
                            newp == False
                        elif match == "one":
                            newp = True
                        elif match == "true":
                            newp = True
                        elif match == "false":
                            newp = False
                    
                else:
                    attempt = 0
                    while attempt < 6:
                        attempt += 1
                        if attempt == 1:
                            CommonUtil.tellhim("You can only set 'true' or 'false' value for this parameter")
                        elif attempt == 2:
                           CommonUtil.tellhim(f"Alraight, {CommonUtil.read_key_from_JSON('Uname')} you can only set 'true' or 'false' value for this parameter")
                        elif attempt == 3:
                            CommonUtil.tellhim(f"Please, use only 'true' or 'false' comands or {'say' if CommonUtil.read_key_from_JSON('Umode') == 'Voice' else 'type'} 0 (which means false) or 1 (which means yes)")
                        else: 
                            CommonUtil.tellhim(f"I will not be able to set the value which is not valid. If you say everything properly and i still can't understand you, please restart the bot or check the microphone. You can also swith to more accurate voice detection moedl.But now, please say 'true' or 'false' on english")
                        newp = User.get_message()
                        if not CommonUtil.is_stop_command(newp):
                            match = process.extractOne(newp.lower(), ['true', 'false', 'zero', 'one'])
                            if match:
                                result, score, _ = match
                                if score > 70:
                                    if match == 'zero':
                                        newp == False
                                    elif match == "one":
                                        newp = True
                                    elif match == "true":
                                        newp = True
                                    elif match == "false":
                                        newp = False
                                    break
                            else:
                                if newp.isdigit():
                                    if newp == 0:
                                        newp = False
                                    elif newp == 1:
                                        newp = True
                                    else:
                                        CommonUtil.tellhim("The number is out of range. Only 1 or 0 are acceptable.")
                                
                                if attempt == 5:
                                    CommonUtil.tellhim('Sorry, please restart the function')
                                    newp = 'UNS'
                                    break
        elif parameterCONFIG == "Umode":
            attempt = 0
            while attempt < 5:
                attempt += 1
                match = process.extractOne(newp.capitalize(), ['Chat', 'Voice'])
                if match and match[1] > 75:
                    newp = match[0]
                    break
                else:
                    if attempt == 1:
                        CommonUtil.tellhim("Mode can only be 'Chat' or 'Voice'.")
                    elif attempt == 2:
                        CommonUtil.tellhim("Please type either 'Chat' or 'Voice' clearly.")
                    else:
                        CommonUtil.tellhim("Try again. Valid options: Chat or Voice.")
                    newp = User.get_message()
            else:
                newp = "UNS"
        elif parameterCONFIG == "Uage":
            attempt = 0
            while attempt < 5:
                attempt += 1
                if newp.isdigit():
                    age = int(newp)
                    if 0 < age <= 140:
                        newp = age
                        break
                    else:
                        CommonUtil.tellhim("Age must be between 1 and 140.")
                else:
                    CommonUtil.tellhim("Invalid input. Please enter a number.")
                newp = User.get_message()
                import Algo_Intelligence
                newp = Algo_Intelligence.helper(newp, 'Please, extract the number from this prompt and return only the digit. If no digits in this parameter, return (No digits), if user asks to stop, return (stop)')
                if newp == "stop":
                    return "CANCELED"
                elif newp == "No digits":
                    pass
                else:
                    newp = int(newp)
                    break
            else:
                newp = "UNS"
        elif parameterCONFIG == "Ugender":
            attempt = 0
            while attempt < 5:
                attempt += 1
                match = process.extractOne(newp.capitalize(), ['Male', 'Female'])
                if match and match[1] > 75:
                    newp = match[0]
                    break
                else:
                    if attempt == 1:
                        CommonUtil.tellhim("Gender must be 'Male' or 'Female'.")
                    elif attempt == 2:
                        CommonUtil.tellhim("Try typing 'Male' or 'Female' again.")
                    else:
                        CommonUtil.tellhim("Please answer with: Male or Female.")
                    newp = User.get_message()
                    import Algo_Intelligence
                    newp = Algo_Intelligence.helper(newp, 'Please, extract the  users gender from the prompt. Male or Female. If no gender related text in prompt, return (No gender). if user asks to stop, return (stop)')
                    if newp == "stop":
                        return "CANCELED"
                    elif newp == "No gender":
                        pass
                    else:
                        break

            else:
                newp = "UNS"
        elif parameterCONFIG == "Ubotreference":
            attempt = 0
            while attempt < 5:
                attempt += 1
                if any(char.isdigit() for char in newp) or re.search(r'[{}[\];:<>/?\\|*^%$#@!~`]', newp):
                    CommonUtil.tellhim("Name can't contain digits or special characters.")
                elif len(newp.strip()) < 2:
                    CommonUtil.tellhim("The name is too short.")
                else:
                    newp = newp.strip().capitalize()
                    break
                newp = User.get_message()
            else:
                newp = "UNS"
        elif parameterCONFIG == "Uvoicemodel":
            attempt = 0
            while attempt < 6:
                if attempt == 1:
                    CommonUtil.tellhim("You can only set 'big', which is 450mb or 'light' which is 150mb for this parameter")
                elif attempt == 2:
                    CommonUtil.tellhim(f"Alraight, {CommonUtil.read_key_from_JSON('Uname')} you can only set 'big', which is 450mb or 'light' which is 150mb for this parameter")
                elif attempt == 3:
                    CommonUtil.tellhim(f"Please, use only 'big' or 'light' comands")
                elif attempt == 5:
                    CommonUtil.tellhim(f"I will not be able to set the value which is not valid. If you say everything properly and i still can't understand you, please restart the bot or check the microphone. You can also swith to more accurate voice detection moedl.")
                newp = User.get_message()
                print("The choice:", newp)
                if not CommonUtil.is_stop_command(newp):
                    match = process.extractOne(newp.lower(), ['big', 'light'])
                    if match:
                        result, score, _ = match
                        if score > 60:
                            newp = result 
                            break
                attempt += 1  
            else:
                newp = "UNS"  
        if newp != 'UNS':
            CommonUtil.JSON_config_changer(parameterCONFIG, newp)
            if parameterCONFIG == "Ubotreference":
                CommonUtil.JSON_config_changer("Uvoice_trained", False)
                import os
                base_dir = os.path.dirname(os.path.abspath(__file__))
                data_dir = os.path.join(base_dir, "WWD_DB")
                for f in os.listdir(data_dir):
                    if f.lower().endswith(".wav"):
                        os.remove(os.path.join(data_dir, f))
                CommonUtil.tellhim(f"Gent user, since your have changed my name, you will be asked to teach me to recognize your voice, when you will be returned.")
            elif parameterCONFIG == "Uvoicemodel":
                from pathlib import Path
                print("Changing your settings..")
                script_dir = Path(__file__).parent
                # Поднимаемся на 2 уровня вверх
                project_root = script_dir.parent.parent
                # Путь к папке models
                MD_folder = project_root / "AImodels"
                model_folder = MD_folder / "FWhisper"
                print(model_folder)
                CommonUtil.empty_folder(model_folder)
            return "SUCCESS"
        else:
            return "UNS"

UserS = Settings()
def seting_setter(parameter=None):
    if parameter == None:
        UserS.menu_show()
        CommonUtil.tellhim("What do you need to change?")
        WTC = User.get_message()
    else:
        WTC = parameter
    State = UserS.change(WTC)
    if State == "SUCCESS":
        return "S"
    elif State == "UNS":
        return "US"
    elif State == "CANCELED":
        return "CD"
    


                
                

                    
                                    
                                    
                            




            
        
        
        
