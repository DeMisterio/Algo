import sys, time, CommonUtil
import asyncio
import os
import edge_tts
from textblob import TextBlob
Debugstat = CommonUtil.read_key_from_JSON("Debug")
Uname = CommonUtil.read_key_from_JSON("Uname")
Umode = CommonUtil.read_key_from_JSON("Umode")
if Debugstat:
    print("* Text Correction hss successfully loaded")

async def main(infov, UnameV, entryV, intro_phraseV, purpose):
    if purpose == "retell":
        tts = edge_tts.Communicate(text=(infov), voice="en-CA-LiamNeural")
    elif purpose == "ask":
        tts = edge_tts.Communicate(text=(infov + "," + entryV + UnameV + "?"), voice="en-CA-LiamNeural")
    await tts.save("output.mp3")

def processfixing(User_message):
        if Umode == "Chat":
            parts = User_message.split(":", 1)
            if len(parts) > 1:
                blob = TextBlob(parts[1].strip())
                User_message = str(blob.correct())
                CommonUtil.tellhim(f"Corrected text: {User_message}")
            else:
                CommonUtil.tellhim("No correction found.")
            return "Succesed"
        elif Umode == "Voice":
            blob = TextBlob(User_message)
            User_message = str(blob.correct())
            CommonUtil.tellhim(f"Corrected text: {User_message}")
            return "Succesed"
