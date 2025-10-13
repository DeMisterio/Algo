try:
    import spacy
    import PlatKernel as plat
    import sys
    import time
    import random
    import os
    import FileManagement
    from shutil import get_terminal_size
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    # Можно сделать exit или инициализировать заглушки
    sys.exit(1)
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
            print("".join(line), end="")
        sys.stdout.flush()
    
    def move_cursor(self, row, col):
        sys.stdout.write(f"\033[{row};{col}H")
    
    def peel_sticker(self, is_top=True):
        sticker_start = 1 if is_top else 1 + self.sticker_height + self.empty_height
        max_peel_steps = self.box_width + self.sticker_height
        
        for step in range(max_peel_steps + 1):
            # Очищаем основную часть стикера
            for i in range(self.sticker_height):
                row = sticker_start + i
                col = step - i
                
                if 1 <= col <= self.box_width:
                    self.canvas[row][col] = ' '
            
            # Рисуем загнутый уголок
            if step > 0:
                corner_row = sticker_start + min(step, self.sticker_height) - 1
                corner_col = min(step, self.box_width)
                
                if 1 <= corner_col <= self.box_width and 1 <= corner_row < len(self.canvas)-1:
                    self.canvas[corner_row][corner_col] = '◢' if is_top else '◣'
            
            self.draw_sticker_section(sticker_start)
            
            # Плавное ускорение/замедление
            if step < 5 or step > max_peel_steps - 5:
                time.sleep(0.05)
            else:
                time.sleep(0.02)
        
        # Убираем уголок
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
            print("".join(self.canvas[start_row + i]), end="")
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
        
        # Возврат в исходное положение
        for i in range(self.empty_height):
            row = empty_start + i
            self.move_cursor(self.base_row + row, 1)
            print("".join(self.canvas[row]), end="")
        sys.stdout.flush()
    
    def reveal_iphone(self):
        center_row = 1 + self.sticker_height + self.empty_height // 2 - 1
        messages = [
            "Algo Gen 5",
            "Your new virtual assistant",
            "say 'Hello' to your new helper!"
        ]
        
        for i, msg in enumerate(messages):
            row = center_row + i
            centered = msg.center(self.box_width)
            
            for col in range(1, self.box_width + 1):
                self.canvas[row][col] = centered[col-1]
                self.move_cursor(self.base_row + row, col + 1)
                print(centered[col-1], end="")
                sys.stdout.flush()
                time.sleep(0.02)
            time.sleep(0.2)
    
    def run(self):
        try:
            # Initial draw
            self.draw_box()
            time.sleep(1)
            
            # Peel top sticker (слева направо)
            self.peel_sticker(is_top=True)
            time.sleep(0.2)
            
            # Wave effect (встряска волной)
            self.wave_effect()
            time.sleep(0.3)
            
            # Peel bottom sticker (слева направо)
            self.peel_sticker(is_top=False)
            time.sleep(0.2)
            
            # Wave effect (встряска волной)
            self.wave_effect()
            time.sleep(0.5)
            
            # Reveal iPhone
            self.reveal_iphone()
            time.sleep(1)
            
            # Final message
            self.move_cursor(self.base_row + len(self.canvas) + 2, 1)
            
        finally:
            sys.stdout.write("\033[?25h")  # Show cursor
            sys.stdout.flush()

def rnd_folder(base):
    folders = [os.path.join(root, d) for root, dirs, _ in os.walk(base) for d in dirs]
    return random.choice(folders) if folders else base

def unpack():
    code = plat.activatory_code()
    for attempt in range(4):
        try:
            Ucode = input("Enter Activation code")
            if Ucode == code:
                passed = True
                break
            else:
                print(f"⚠️ Wrong code, you have {4 - attempt} attempts left befor self deleting.")
        except ValueError:
            print("❌ That's not a number, bro. Digits only.")
    else:
        print("Access to program restricted.")
        quit()
    if passed == True:
        init()
def init():
    for attempt in range(10):
        try:
            time.sleep(1)
            Uage = int(input("\n\nWelcome to Algo!\n\nFirst of all, could you type your age? Please be honest, this does affect your usage experinece, this is only for customisation (No limitations): "))
            if 0 < Uage <= 140:
                break
            else:
                print("⚠️ Please enter a realistic age (1-140).")
        except ValueError:
            print("❌ That's not a number, bro. Digits only.")
    else:
        print("Access to program restricted.")
        quit()
    time.sleep(1)
    Uname = input(f"{"Okey! Now i need your name" if Uage <= 18 else "Please type your name: "}")
    time.sleep(1)
    Ugender = input(f"{f"{Uname}, what is your gender/sex?" if Uage <= 18 else f"{Uname},please enter your gender(sex):"}")
    time.sleep(1)
    Ubotreference = input(f"{"Okey! Please give me any name you want" if Uage <= 18 else "Please say, how do you want to call this bot?: "}")
    print("")
    creation = plat.activation(Uage, Uname, Ugender, Ubotreference)
    if creation == "success":
        print(f'\r10%, handling ENGLISH AI model..."', end='', flush=True)
    print("\n\n Step 1: \n\n")
    try: #1
        nlp = spacy.load("en_core_web_md")
        print(nlp.path)
    except OSError:
        print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)", file=sys.stderr)
        from spacy.cli import download
        download("en_core_web_md")
        nlp = spacy.load("en_core_web_md")
        print(f'\r30%, handling RUSSIAN AI model..."', end='', flush=True)
    print("\n\n Step 2: 35% \n\n")
    try: #1
        nlpr = spacy.load('ru_core_news_sm')
    except OSError:
        print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)", file=sys.stderr)
        from spacy.cli import download
        download('ru_core_news_sm')
        nlp = spacy.load('ru_core_news_sm')
        print(f'\r30%, Handling Russian Model finished..."', end='', flush=True)
    print("\n Step 4: 40% \n")
    base = os.path.dirname(os.path.abspath(__file__))  # папка с текущим файлом
    folder = rnd_folder(base)
    path = os.path.join(folder, "ActtextProove01beta01.txt")
    with open(path, "w") as f:
        f.write("success")
    print("\n Step 5: 45% \n")
    FileManagement.name_giver(path, "API")
    print(f'\r50%"', end='', flush=True)
    # folder_path = os.path.dirname(os.path.abspath(__file__))
    # items = os.listdir(folder_path)
    time.sleep(1)
    print(f'\r50%"', end='', flush=True)
    print(f'\r100%! Algo Initialisation is finished, please wait for launch.."', end='', flush=True)
    animation = UnboxingAnimation()
    animation.run() 
    print("\n\n\n\n")
    new_file = "Kernel.py"
    os.execv(sys.executable, [sys.executable, new_file])
if __name__ == "__main__":
    # Этот код выполнится, только если запускаешь module.py напрямую,
    # а не при импорте.
    unpack()
