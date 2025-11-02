import numpy as np
import AlgoParser
import json
import time
try:
    with open("config.json", "r") as file:
        config = json.load(file)
    Debugstat = config.get("Udebug", None)
except (FileNotFoundError, json.JSONDecodeError):
    Debugstat = False

class userbase:
    def __init__(self, message="", raw_message="", origin_lang_message=""):
        self.message = message
        self.raw_message = raw_message
        self.origin_lang_message = origin_lang_message
    def get_message(self):
        global Debugstat
        import CommonUtil
        import json
        from Kernel_F.Kernel import thestart
        Voice_mode = CommonUtil.read_key_from_JSON('Umode')
        Ubotreference = CommonUtil.read_key_from_JSON('Ubotreference')
        Uage = CommonUtil.read_key_from_JSON("Uage")
        Uname = CommonUtil.read_key_from_JSON('Uname')
        Trained = CommonUtil.read_key_from_JSON("Uvoice_trained")
        if Voice_mode == "Voice":
            if Trained is True:
                audio_path = CommonUtil.record_until_silence_vad()
                if Debugstat:
                    print("🛑 Закончил слушать. Обрабатываю...")
                file_path = audio_path
                if file_path == "RE":
                    thestart()
                else:
                    pass
                try:
                    str_time = time.time()
                    language, self.message = CommonUtil.transcribe(file_path)
                    if Debugstat is True:
                        print("time spent:", time.time() - str_time, "s")
                except Exception as e:
                    if Debugstat:
                        print(f"⚠️ Ошибка при транскрипции: {e}")
                    language = "EN"
                    self.message = ""
                with open("config.json", "r") as file:
                    config = CommonUtil.safe_load_json("config.json")
                    config["Ulang"] = language
                with open("config.json", "w") as file:
                    json.dump(config, file, indent=4)
                self.origin_lang_message = self.message
                if Debugstat:
                    print(f"до перевода: {self.origin_lang_message}")
                language = CommonUtil.lang_detection(self.origin_lang_message)
                if language in ("Unsuccessful", "INTERNET_ERROR"):
                    if Debugstat:
                        print("Could not detect language, assuming English...")
                    language = "EN"

                # Нормализуем язык
                if language == "EN":
                    language = "EN-US"  # для единообразия

                if language not in ("EN", "EN-US", "EN-UK"):
                    if Debugstat:
                        print("The language is not English, translating to English...")
                    translated = CommonUtil.lang_validation(self.origin_lang_message)
                    if translated == "INTERNET_ERROR":
                        print("Sorry, Algo cannot understand non-English input while offline, i will assume it is english...")
                        self.message = self.origin_lang_message  
                    else:
                        self.message = translated

                else:
                    if Debugstat:
                        print("Language is English, no translation needed.")
                    self.message = self.origin_lang_message
                    if hasattr(self.message, "text"):
                        self.message = self.message.text
                if self.message == "INTERNET_ERROR":
                    print("Sorry, Algo cannot understand anything except english while being offline...")
                    thestart()
                if hasattr(self.message, "text"):
                    self.message = self.message.text
            else:
                self.message = "ERROR_NO_VOICE"

            
        elif Voice_mode == "Chat":
            self.origin_lang_message = input("Enter your prompt: ")
            language = CommonUtil.lang_detection(self.origin_lang_message)
            if language in ("Unsuccessful", "INTERNET_ERROR"):
                if Debugstat:
                    print("Could not detect language, assuming English...")
                language = "EN"

            # Нормализуем язык
            if language == "EN":
                language = "EN-US"  # для единообразия

            if language not in ("EN", "EN-US", "EN-UK"):
                if Debugstat:
                    print("The language is not English, translating to English...")
                translated = CommonUtil.lang_validation(self.origin_lang_message)
                if translated == "INTERNET_ERROR":
                    print("Sorry, Algo cannot understand non-English input while offline.")
                    thestart()
                    return
                self.message = translated
            else:
                if Debugstat:
                    print("Language is English, no translation needed.")
                self.message = self.origin_lang_message
            
            if self.message == "INTERNET_ERROR":
                print("Sorry, Algo cannot understand anything except english while being offline...")
                thestart()
            with open("config.json", "r") as file:
                config = CommonUtil.safe_load_json("config.json")
                config["Ulang"] = language
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)
            if hasattr(self.message, "text"):
                self.message = self.message.text
        if self.message and isinstance(self.message, str):
            if self.message == "/debug" or self.message == "/debug/status":
                if self.message == "/debug":
                    with open("config.json", "r") as file:
                        config = CommonUtil.safe_load_json("config.json")
                        config["UDebug"] = not(config["UDebug"])
                        Debugstat = config["UDebug"]
                    with open("config.json", "w") as file:
                        json.dump(config, file, indent=4)
                    CommonUtil.tellhim(f"You have turned debug mode {'on' if Debugstat else 'off'}")
                    print(Debugstat)
                    thestart()
                elif self.message == "/debug/status":
                    print(f"Debug is turned {'on' if Debugstat else 'off'}")
                    thestart()
            elif self.message.lower() == "/stop" or self.message in (("goodbye", "bye", "stop") if self.message[-1] != ("!" or ".") else ("goodbye!", "bye!", "goodbye.", "bye.")) or self.message == "0":
                CommonUtil.tellhim(f"Goodbye, {Uname}!")
                quit()
            elif self.message.lower() == Ubotreference:
                if Uage > 40:
                    np.random.choice(AlgoParser.name_responses["40, 150"])
                elif Uage >= 30 and Uage <=40:
                    np.random.choice(AlgoParser.name_responses["30, 40"])
                elif Uage >= 20 and Uage < 30:
                    np.random.choice(AlgoParser.name_responses["20, 30"])
                elif Uage > 0 and Uage < 20:
                    np.random.choice(AlgoParser.name_responses["0, 20"])
        return self.message
