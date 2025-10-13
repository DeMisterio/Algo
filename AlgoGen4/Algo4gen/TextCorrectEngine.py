import sys, time, CommonUtil
Debugstat = CommonUtil.read_key_from_JSON("Debug")
if Debugstat:
    print("* Text Correction hss successfully loaded")
def tellhim(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
def processfixing(User_message):
        parts = User_message.split(":", 1)
        if len(parts) > 1:
            tellhim(f"Corrected text: {parts[1].strip()}")
        else:
            tellhim("No correction found.")
        return "Succesed"

