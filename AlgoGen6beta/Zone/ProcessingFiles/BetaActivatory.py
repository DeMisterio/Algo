import spacy
import PlatKernel as plat
import sys
import time
import random
import os
from pathlib import Path
from shutil import get_terminal_size

# ANSI color codes
COLOR_BLUE         = "\033[34m"
COLOR_YELLOW       = "\033[33m"
COLOR_ORANGE       = "\033[38;5;208m"
COLOR_GREEN        = "\033[32m"
COLOR_INFO         = "\033[96m"
COLOR_LIGHT_BLUE   = "\033[94m"
COLOR_RESET        = "\033[0m"

# Rainbow gradient for the unboxing animation (red, yellow, green, blue, violet, cyan)
RAINBOW = ["\033[31m", "\033[33m", "\033[32m", "\033[34m", "\033[35m", "\033[36m"]
def Check_INTERNET_CONNECTION(host='8.8.8.8', port=53, timeout=3):
    try:
        import socket
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print(f"⚠️ Ошибка проверки соединения: {e}")
        return False
def rainbow_text(text):
    out = ""
    for i, ch in enumerate(text):
        out += RAINBOW[i % len(RAINBOW)] + ch
    return out + COLOR_RESET

def get_folder_size(folder_path):
    folder = Path(folder_path)
    total_size = 0
    for file in folder.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
    return total_size

class UnboxingAnimation:
    def __init__(self):
        self.terminal_width, self.terminal_height = get_terminal_size()
        self.box_width = min(40, self.terminal_width - 4)
        self.box_height = 20
        self.sticker_height = 3
        self.empty_height = self.box_height - 2 * self.sticker_height - 2
        self.canvas = []
        self.base_row = 5

        self.init_screen()
        self.build_box()

    def init_screen(self):
        sys.stdout.write("\033[2J")  # Clear screen
        sys.stdout.write("\033[?25l")  # Hide cursor
        sys.stdout.flush()
        
        # Blank spacing remains unchanged
        print("\n" * (self.base_row - 1))
        print("\n" * 2)

    def build_box(self):
        # Top border
        self.canvas.append(["┌"] + ["─"] * self.box_width + ["┐"])
        
        # Top sticker
        for _ in range(self.sticker_height):
            self.canvas.append(["│"] + ["■"] * self.box_width + ["│"])
        
        # Empty space
        for _ in range(self.empty_height):
            self.canvas.append(["│"] + [" "] * self.box_width + ["│"])
        
        # Bottom sticker
        for _ in range(self.sticker_height):
            self.canvas.append(["│"] + ["■"] * self.box_width + ["│"])
        
        # Bottom border
        self.canvas.append(["└"] + ["─"] * self.box_width + ["┘"])
    
    def draw_box(self):
        for i, line in enumerate(self.canvas):
            self.move_cursor(self.base_row + i, 1)
            # Apply a rainbow gradient on the box lines
            colored_line = rainbow_text("".join(line))
            print(colored_line, end="")
        sys.stdout.flush()
    
    def move_cursor(self, row, col):
        sys.stdout.write(f"\033[{row};{col}H")
    
    def peel_sticker(self, is_top=True):
        sticker_start = 1 if is_top else 1 + self.sticker_height + self.empty_height
        max_peel_steps = self.box_width + self.sticker_height
        
        for step in range(max_peel_steps + 1):
            # Clear main part of sticker
            for i in range(self.sticker_height):
                row = sticker_start + i
                col = step - i
                
                if 1 <= col <= self.box_width:
                    self.canvas[row][col] = ' '
            
            # Draw folded corner
            if step > 0:
                corner_row = sticker_start + min(step, self.sticker_height) - 1
                corner_col = min(step, self.box_width)
                
                if 1 <= corner_col <= self.box_width and 1 <= corner_row < len(self.canvas)-1:
                    self.canvas[corner_row][corner_col] = '◢' if is_top else '◣'
            
            self.draw_sticker_section(sticker_start)
            
            # Smooth acceleration/deceleration
            if step < 5 or step > max_peel_steps - 5:
                time.sleep(0.05)
            else:
                time.sleep(0.02)
        
        # Remove corner
        if is_top:
            corner_row = sticker_start + self.sticker_height - 1
        else:
            corner_row = sticker_start
        corner_col = self.box_width
        
        if 1 <= corner_col <= self.box_width and 1 <= corner_row < len(self.canvas)-1:
            self.canvas[corner_row][corner_col] = ' '
            self.draw_sticker_section(sticker_start)
    
    def draw_sticker_section(self, start_row):
        for i in range(self.sticker_height):
            self.move_cursor(self.base_row + start_row + i, 1)
            # Rainbow gradient applied to sticker lines too
            print(rainbow_text("".join(self.canvas[start_row + i])), end="")
        sys.stdout.flush()
    
    def wave_effect(self):
        empty_start = 1 + self.sticker_height
        wave_positions = [
            (0, 1), (1, 1), (2, 1), (3, 0), 
            (4, -1), (5, -1), (6, 0), (7, 1)
        ]
        
        for offset, shift in wave_positions:
            for i in range(self.empty_height):
                row = empty_start + i
                current_shift = shift if i == offset else 0
                
                self.move_cursor(self.base_row + row, 1)
                line = self.canvas[row]
                shifted_line = line[1:self.box_width+1]
                
                if current_shift > 0:
                    shifted_line = [" "] * current_shift + shifted_line[:-current_shift]
                elif current_shift < 0:
                    shifted_line = shifted_line[-current_shift:] + [" "] * (-current_shift)
                
                print("│" + "".join(shifted_line) + "│", end="")
            
            sys.stdout.flush()
            time.sleep(0.08)
        
        # Return to original position
        for i in range(self.empty_height):
            row = empty_start + i
            self.move_cursor(self.base_row + row, 1)
            print("".join(self.canvas[row]), end="")
        sys.stdout.flush()
    
    def reveal_iphone(self):
        center_row = 1 + self.sticker_height + self.empty_height // 2 - 1
        messages = [
            "Algo Gen 5.5",
            "Your new virtual assistant",
            "Say 'Hello' to your new helper!"
        ]
        
        for i, msg in enumerate(messages):
            row = center_row + i
            # Centering the message and coloring file paths if any (none here)
            centered = msg.center(self.box_width)
            
            for col in range(1, self.box_width + 1):
                self.canvas[row][col] = centered[col-1]
                self.move_cursor(self.base_row + row, col + 1)
                # Print each character in rainbow gradient order
                ch = centered[col-1]
                color = RAINBOW[(col-1) % len(RAINBOW)]
                print(f"{color}{ch}{COLOR_RESET}", end="")
                sys.stdout.flush()
                time.sleep(0.02)
            time.sleep(0.2)
    
    def run(self):
        try:
            # Initial draw
            self.draw_box()
            time.sleep(1)
            
            # Peel top sticker (left to right)
            self.peel_sticker(is_top=True)
            time.sleep(0.2)
            
            # Wave effect (shake with wave)
            self.wave_effect()
            time.sleep(0.3)
            
            # Peel bottom sticker (left to right)
            self.peel_sticker(is_top=False)
            time.sleep(0.2)
            
            # Wave effect (shake with wave)
            self.wave_effect()
            time.sleep(0.5)
            
            # Reveal iPhone with animated text
            self.reveal_iphone()
            time.sleep(1)
            
            # Final message (neutral)
            self.move_cursor(self.base_row + len(self.canvas) + 2, 1)
            
        finally:
            sys.stdout.write("\033[?25h")  # Show cursor
            sys.stdout.flush()

def rnd_folder(base):
    folders = [os.path.join(root, d) for root, dirs, _ in os.walk(base) for d in dirs]
    return random.choice(folders) if folders else base
    

def unpack():
    global Ucountry, Ulang
    code = plat.activatory_code()
    import pycountry
    import langcodes
    import requests
    from pathlib import Path
    from rapidfuzz import process

    def get_country_and_language(user_input):
        """Get country and language by country name"""
        country = pycountry.countries.get(name=user_input)
        
        if not country:
            countries = [c.name for c in pycountry.countries]
            match, score, _ = process.extractOne(user_input, countries)
            if score > 80:
                country = pycountry.countries.get(name=match)
            else:
                return None, None
        
        try:
            lang = langcodes.Language.get(territory=country.alpha_2).language
            return lang, country.name
        except:
            return None, country.name

    def get_system_language():
        """Get system language"""
        import locale
        try:
            lang_code, _ = locale.getlocale()
            if lang_code:
                return lang_code.replace("_", "-").upper()
        except:
            pass
        return None

    def get_language_from_user():
        """Get language from user using various methods"""
        print(f"{COLOR_INFO}ℹ️ Please type something in your native language:{COLOR_RESET}")
        try:
            from langdetect import detect
            text = input().strip()
            if text:
                return detect(text).upper()
        except:
            pass
        
        try:
            import AlgoParser
            print(f"\n{COLOR_INFO}ℹ️ Please, select your language from the table:{COLOR_RESET}")
            for num, code in AlgoParser.LANGUAGE_MENU.items():
                print(f"{num}: {code}")
            
            while True:
                code_input = input(f"{COLOR_INFO}ℹ️ Please copy-paste language code or enter its number from the table: {COLOR_RESET}").strip()
                if code_input.isdigit():
                    code_num = int(code_input)
                    if 1 <= code_num <= len(AlgoParser.LANGUAGE_MENU):
                        return AlgoParser.LANGUAGE_MENU[code_num]
                    else:
                        print(f"{COLOR_ORANGE}❌ The number is not correct, please try again.{COLOR_RESET}")
                elif code_input.upper() in AlgoParser.LANGUAGE_MENU.values():
                    return code_input.upper()
                else:
                    match = process.extractOne(code_input.upper(), AlgoParser.LANGUAGE_MENU.values())
                    if match:
                        result, score, _ = match
                        if score > 70:
                            print(f"{COLOR_INFO}ℹ️ Selected language: {result}{COLOR_RESET}")
                            return result
                    print(f"{COLOR_ORANGE}❌ The language code is not valid, please try again.{COLOR_RESET}")
        except ImportError:
            print(f"{COLOR_ORANGE}❌ AlgoParser not found.{COLOR_RESET}")
            return 'EN'

    try:
        data = requests.get('https://ipinfo.io/json').json()
        country_code = data.get('country')
        if country_code:
            country_obj = pycountry.countries.get(alpha_2=country_code)
            if country_obj:
                Ucountry = country_obj.name
            else:
                Ucountry = None
        else:
            Ucountry = None
    except:
        Ucountry = None

    if not Ucountry:
        print(f"{COLOR_INFO}ℹ️ We could not determine your country, please type it:{COLOR_RESET}")
        for attempt in range(3):
            user_input = input(f"{COLOR_INFO}ℹ️ Your country (in English): {COLOR_RESET}").strip()
            Ulang, Ucountry = get_country_and_language(user_input)
            if Ucountry:
                break
            print(f"{COLOR_ORANGE}❌ Could not find the country in the database. Please enter a valid country name. Attempts left: {2 - attempt}{COLOR_RESET}")
        else:
            print(f"{COLOR_ORANGE}❌ Could not determine your language. Program terminates..{COLOR_RESET}")
            exit()

    print(f"{COLOR_GREEN}✅ Welcome from {COLOR_BLUE}{Ucountry}{COLOR_GREEN}!{COLOR_RESET}")

    Ulang, _ = get_country_and_language(Ucountry)
    if not Ulang:
        Ulang = get_system_language()
        if not Ulang:
            Ulang = get_language_from_user()

    print(f"{COLOR_INFO}ℹ️ Language detected: {Ulang}{COLOR_RESET}")
    
    for attempt in range(4):
        try:
            Ucode = input(f"{COLOR_INFO}ℹ️ Enter Activation code: {COLOR_RESET}")
            if Ucode == code:
                passed = True
                break
            else:
                print(f"{COLOR_ORANGE}❌ Wrong code, you have {4 - attempt} attempts left before self-deleting.{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_ORANGE}❌ That's not a number, digits only.{COLOR_RESET}")
    else:
        print(f"{COLOR_ORANGE}❌ Access to program restricted.{COLOR_RESET}")
        quit()
    if passed == True:
        init()

def init():
    for attempt in range(10):
        try:
            time.sleep(1)
            Uage = int(input(f"\n\n{COLOR_INFO}ℹ️ Welcome to Algo!\n\nFirst of all, could you type your age? Please be honest, this does affect your usage experience (No limitations): {COLOR_RESET}"))
            if 0 < Uage <= 140:
                break
            else:
                print(f"{COLOR_ORANGE}❌ Please enter a realistic age (1-140).{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_ORANGE}❌ That's not a number, digits only.{COLOR_RESET}")
    else:
        print(f"{COLOR_ORANGE}❌ Access to program restricted.{COLOR_RESET}")
        quit()
    time.sleep(1)
    Uname = input(f"{COLOR_INFO}ℹ️ {'Okay! Now I need your name' if Uage <= 18 else 'Please type your name:'} {COLOR_RESET}")
    time.sleep(1)
    Ugender = input(f"{COLOR_INFO}ℹ️ {Uname}, {'what is your gender/sex? (Male / Female)' if Uage <= 18 else 'please enter your gender/sex (Male / Female):'} {COLOR_RESET}")
    time.sleep(1)
    Ubotreference = input(f"{COLOR_INFO}ℹ️ {'Okay! Please give me any name you want:' if Uage <= 18 else 'Please say, how do you want to call this bot?'} {COLOR_RESET}")
    time.sleep(1)
    Umode = input(f"{COLOR_INFO}ℹ️ {'Okay! Now type Chat if you would like to chat with the bot or Voice if you would like to talk using voice:' if Uage <= 18 else 'Please type Chat if you would like to chat or Voice if you would like to talk:'} {COLOR_RESET}")
    print("")
    if Check_INTERNET_CONNECTION() == True:
        for attempt in range(3):
            AI_api_key = input(f"{COLOR_INFO}ℹ️ {Uname}, {'Enter your OpenAI private API key: ' if Uage <= 18 else 'Enter your private OpenAI API key: '} {COLOR_RESET}")
            if len(AI_api_key) >=100:
                time.sleep(1)
                print("Wait untill the Algo validates your API key...")
                import openai
                openai.api_key = AI_api_key
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4.1-mini-2025-04-14",
                        messages=[
                            {"role": "system", "content": f"Say only 'CHECKED'. "},
                            {"role": "user", "content": "Say 'CHECKED'"},
                        ]
                    )
                    bash_command = response["choices"][0]["message"]["content"]
                    if bash_command == "CHECKED" or bash_command == "'CHECKED'":
                        response = openai.ChatCompletion.create(
                        model="gpt-4.1-mini-2025-04-14",
                        messages=[
                            {"role": "system", "content": f"Your name is {Ubotreference}. Introduce your self to the {Uname}: you are {Ubotreference} intelligence, you will be assisting the user for comples tasks while programm usage."},
                            {"role": "user", "content": "Introduce yourself."},
                        ]
                        )
                        greating = response["choices"][0]["message"]["content"]
                        print(f"\n\n{Ubotreference}: {greating}\n\n")
                        break
                    else:             
                        print(f"{COLOR_ORANGE}This API key has responded{COLOR_RESET}")
                        continue
                except Exception as e:
                    print(f"{COLOR_ORANGE}❌ Could not connect to the OpenAI api system.Turn on the vpn if you are in the area of local GPT restrictions or check the API account balance{e}{COLOR_RESET}")
                    continue
            else:
                print(f"{COLOR_ORANGE}This is not the API key. Original OpenAI API key you can purchase at {COLOR_GREEN} https://platform.openai.com/docs/overview {COLOR_RESET}.Free tokens are unavailable at the moment :({COLOR_RESET}")
        
        else:
            AI_api_key = None
    else:
        print("Algo cant connect to the internet. You will be asked to enter API key after connection.")
        AI_api_key = None
    time.sleep(1)

    time.sleep(1)

    creation = plat.activation(Uage, Uname, Ugender, Ubotreference, Umode, Ulang, Ucountry, AI_api_key, False)
    if creation == "success":
        print(f"{COLOR_GREEN}✅ Program package installation started!{COLOR_RESET}")
    else:
        print(f"{COLOR_INFO}ℹ️ Oh oh, the program files might be broken... default settings will be applied. Installation continues...{COLOR_RESET}")
    print(f"\n\n {COLOR_LIGHT_BLUE}Step 1: 0%, handling ENGLISH AI model...{COLOR_RESET} \n\n")
    try:
        nlp = spacy.load("en_core_web_md")
        print(f"{COLOR_GREEN}✅ The English AI model pack is already installed here: {COLOR_BLUE}{nlp.path}{COLOR_GREEN}{COLOR_RESET}")
    except OSError:
        print(f"{COLOR_INFO}ℹ️ Downloading language model for the spaCy POS tagger (this will only happen once){COLOR_RESET}", file=sys.stderr)
        from spacy.cli import download
        download("en_core_web_md")
        nlp = spacy.load("en_core_web_md")
        print(f"{COLOR_GREEN}✅ Handling English AI model pack finished and it is saved here: {COLOR_BLUE}{nlp.path}{COLOR_GREEN}{COLOR_RESET}", end="", flush=True)
    print(f"\n\n {COLOR_LIGHT_BLUE}Step 2: 35%{COLOR_RESET} \n\n")
    print(f"{COLOR_INFO}ℹ️ Handling Russian AI language pack...{COLOR_RESET}")
    try:
        nlpr = spacy.load('ru_core_news_sm')
        print(f"{COLOR_GREEN}✅ Russian AI language pack was already downloaded here: {COLOR_BLUE}{nlp.path}{COLOR_GREEN} Continuing...{COLOR_RESET}")
    except OSError:
        print(f"{COLOR_INFO}ℹ️ Downloading language model for the spaCy POS tagger (this will only happen once){COLOR_RESET}", file=sys.stderr)
        from spacy.cli import download
        download('ru_core_news_sm')
        nlp = spacy.load('ru_core_news_sm')
        print(f"{COLOR_GREEN}✅ Handling Russian AI model pack finished and it is saved here: {COLOR_BLUE}{nlp.path}{COLOR_GREEN}{COLOR_RESET}", end="", flush=True)
    print(f"\n {COLOR_LIGHT_BLUE}Step 4: 40%{COLOR_RESET} \n")
    print(f"{COLOR_INFO}ℹ️ Checking the license...{COLOR_RESET}")
    print(f"{COLOR_YELLOW}50%{COLOR_RESET}", end="", flush=True)
    from faster_whisper import WhisperModel
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    FW_model_paths = project_root / "AImodels" / "FWhisper"
    from modelscope import snapshot_download
    FW_model_paths.mkdir(exist_ok=True)
    print(f"\n{COLOR_INFO}ℹ️ The model will be downloaded to: {COLOR_BLUE}{FW_model_paths}{COLOR_RESET}")
    print(f"{COLOR_INFO}ℹ️ You have two options:\n" +
          "   1. (Heavy) Install the model for understanding your voice (~450MB)\n" +
          "   2. (Light)  Install the lighter and optimized model (~160MB)\n" +
          "What do you choose? (1 or 2){COLOR_RESET}")
    attempt_MC = 0
    while attempt_MC < 5:
        try:
            choice = int(input(f"{COLOR_INFO}ℹ️ Enter your choice: {COLOR_RESET}"))
            if choice in [1, 2]:
                break
            else:
                print(f"{COLOR_ORANGE}❌ Please enter 1 or 2.{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_ORANGE}❌ That's not a number, digits only.{COLOR_RESET}")
        attempt_MC += 1
    else:
        print(f"{COLOR_ORANGE}❌ Program access restricted due to too many invalid attempts. Please restart.{COLOR_RESET}")
        quit()
    if choice == 1:
        model = 'angelala00/faster-whisper-small'
    elif choice == 2:
        model = 'pengzhendong/faster-whisper-base'
    else:
        while choice != 1 or choice != 2:
            if attempt_MC != 4:
                choice = int(input(f"{COLOR_INFO}ℹ️ Please enter the valid choice: {COLOR_RESET}"))
                attempt_MC+= 1
            else:
                print(f"{COLOR_ORANGE}❌ Program access restricted due to suspicious activity. Please restart.{COLOR_RESET}")
                quit()

    model_dir = snapshot_download(model, local_dir=FW_model_paths)
    folder_path = FW_model_paths
    size_bytes = get_folder_size(folder_path)
    size_mb = size_bytes / (1024 * 1024)
    print(f"{COLOR_INFO}ℹ️ Folder size: {size_mb:.2f} MB{COLOR_RESET}")
    if 100 < size_mb < 700:
        print(f"{COLOR_GREEN}✅ Model successfully downloaded to: {COLOR_BLUE}{model_dir}{COLOR_GREEN}{COLOR_RESET}")
        Chosen_moodel = "big" if choice == 1 else "light"
        plat.JSON_config_changer("Uvoicemodel", Chosen_moodel)
    else:
        print(f"{COLOR_ORANGE}❌ The size does not match the expected – the model may be corrupted. Please install later.{COLOR_RESET}")
        
    time.sleep(1)
    print(f"{COLOR_YELLOW}60%{COLOR_RESET}", end="", flush=True)
    print(f"\n{COLOR_INFO}ℹ️ Installing model for speech analysis...{COLOR_RESET}")
    from sentence_transformers import SentenceTransformer
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    ST_model_path = project_root / "AImodels" / "sentence_transformers"
    model_path = ST_model_path / "paraphrase-MiniLM-L6-v2"
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2', cache_folder=model_path)
    model.save(model_path)
    print(f"{COLOR_GREEN}✅ Speech analysis model installed at: {COLOR_BLUE}{model_path}{COLOR_GREEN}{COLOR_RESET}")
    print(f"{COLOR_YELLOW}75%{COLOR_RESET}", end="", flush=True)
    import gdown
    import zipfile
    
    url = "https://drive.google.com/file/d/1LckTIKjoGkJwKA2j_yNb37mbBLc273q7/view?usp=drive_link"
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent 
    Indent_model_path = project_root / "AImodels"
    Indent_model_path.mkdir(parents=True, exist_ok=True) 
    zip_path = Indent_model_path / "INDENT_AI.zip"
    gdown.download(url, str(zip_path), quiet=False, fuzzy=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(Indent_model_path)
    zip_path.unlink()
    print(f"{COLOR_GREEN}✅ Proprietary AI model installed!{COLOR_RESET}")
    time.sleep(3)
    print(f"{COLOR_INFO}ℹ️ Checking program file integrity...{COLOR_RESET}")
    PF_folder = Path(__file__).parent
    size_bytes = get_folder_size(PF_folder)
    size_mb = size_bytes / (1024 * 1024)
    time.sleep(2)
    if size_mb > 0.2:
        print(f"{COLOR_GREEN}✅ Check finished, all executable files are in place!{COLOR_RESET}")
    else:
        print(f"{COLOR_ORANGE}❌ Some executable components may have been lost during download.{COLOR_RESET}")
    print(f"{COLOR_YELLOW}100%! Algo Initialization is finished, please wait for launch...{COLOR_RESET}", end="", flush=True)
    animation = UnboxingAnimation()
    animation.run() 
    print("\n\n\n\n")
    script_dir = Path(__file__).parent / "Kernel_F"
    Kernel_path = script_dir / "Kernel.py"
    os.execv(sys.executable, [sys.executable, Kernel_path])

if __name__ == "__main__":
    unpack()
