import CommonUtil
from pathlib import Path
import json
import time
from datetime import datetime 
import hashlib
import AlgoParser
def hash_and_caesar(text, shift=3): return (hashlib.sha256(text.encode()).hexdigest(), ''.join(chr((ord(c)-97+shift)%26+97) if c.islower() else c for c in text))
h, c = hash_and_caesar("privet")
Debugstat = CommonUtil.read_key_from_JSON("Debug")
try:
    import platform as plat
    from datetime import datetime
except:
    ImportError
def activatory_code():
    h, c = hash_and_caesar(
        str(datetime.today().strftime('%Y-%m-%d')[-2:]) +
        hash_and_caesar(str(time.localtime().tm_mon), time.localtime().tm_hour)[1] +
        hash_and_caesar(str(AlgoParser.personal_pronouns[time.localtime().tm_hour]), time.localtime().tm_hour)[1]
    )
    print(c)
    return c
def activation(age, name="Usero", gender="N/E", BotReference="Algo", doc=datetime.today().strftime('%Y-%m-%d')):
    config_path = Path("config.json")
    if not config_path.exists():
        config = {
            "Debug": False,
            "System": plat.system(),
            "Version": plat.version(),
            "Machine": plat.machine(),
            "Release": plat.release(),
            "Node Name": plat.node(),
            "RAC": True,
            "Uage": age,
            "Uname": name,
            "Ugender": gender,
            "Ubotreference": BotReference
        }

        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
        
        Debugstat = config["Debug"]
        return "success"
    else:
        with open(config_path, "r") as file:
            config = json.load(file)  # Лучше напрямую, если safe_load_json нет
            Debugstat = config["Debug"]
        
        print("Defining successful")

if __name__ == "__main__":
    # Этот код выполнится, только если запускаешь module.py напрямую,
    # а не при импорте.
    activation()