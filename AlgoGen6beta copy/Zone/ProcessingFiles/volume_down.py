import os
from CommonUtil import read_key_from_JSON, play_sound

def decrease_volume_mac(decrement):
    # Получаем текущее значение громкости
    current = int(os.popen("osascript -e 'output volume of (get volume settings)'").read().strip())
    new_volume = max(current - decrement, 0)  # ограничиваем от 0 до 100
    os.system(f"osascript -e 'set volume output volume {new_volume}'")
    play_sound("VolumeSound.mp3")
def decrease_volume_powershell(decrement):
    # Имитация нажатия клавиши "громкость вниз"
    presses = max(1, int(decrement / 2))
    os.system(
        f'powershell -command "$wshell = New-Object -ComObject WScript.Shell; '
        f'for($i=0;$i -lt {presses};$i++){{$wshell.SendKeys(\'{{VK_DOWN}}\'); Start-Sleep -Milliseconds 50}}"'
    )
    play_sound("VolumeSound.mp3")
def VolumeDown_Commander(decrement=10):
    system = read_key_from_JSON("System")
    if system == 'Windows':
        decrease_volume_powershell(decrement)
    elif system == 'Darwin':  # macOS
        decrease_volume_mac(decrement)
    else:
        print("Unsupported OS ATM")