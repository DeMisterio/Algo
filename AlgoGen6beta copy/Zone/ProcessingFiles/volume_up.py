import os
from CommonUtil import read_key_from_JSON, play_sound

def increase_volume_mac(increasement):
    # Получаем текущую громкость
    current = int(os.popen("osascript -e 'output volume of (get volume settings)'").read().strip())
    new_volume = min(current + increasement, 100)  # громкость ограничена 0–100
    os.system(f"osascript -e 'set volume output volume {new_volume}'")
    play_sound("VolumeSound.mp3")
def increase_volume_powershell(increasement):
    # тут лучше циклом нажимать "VolumeUp"
    for _ in range(increasement // 2):  # условно, шаги
        os.system('powershell -command "(New-Object -ComObject WScript.Shell).SendKeys(\'{VK_UP}\')"')
    play_sound("VolumeSound.mp3")
def VolumeUP_Commander(increasement=10):
    if read_key_from_JSON("System") == 'Windows':
        increase_volume_powershell(increasement)
    elif read_key_from_JSON("System") == 'Darwin':  # macOS
        increase_volume_mac(increasement)
    else:
        print("Unsupported ATM")
