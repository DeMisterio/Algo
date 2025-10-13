try:
    import openai
    import CommonUtil
    import random
except ImportError:
    print("Could not initialise the Algo Intelligence")

# 🔐 Рекомендуется: API ключ читается из переменной среды или .env
openai.api_key = "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"

Ubotreference = CommonUtil.read_key_from_JSON("Ubotreference")

def Commander(Indent, prompt):
    if Indent == "PC":
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a bash command generator for macOS 15. Given any user request, generate ONLY the corresponding bash command. Respond with a single, ready-to-execute bash command without explanation or comments. Use application names without '.app' when opening apps. You are allowed to use 'python3' in commands if it helps solve the task. Use native macOS tools when appropriate (e.g., 'open', 'say', 'sips', 'osascript'). Avoid unsafe commands unless explicitly asked (e.g., no 'rm -rf' unless clearly requested). Quote arguments properly. If the request is unclear or unsafe, respond with: 'echo Unable to process request safely. If the prompt requires saving file somewhere, the default place to save is the desktop.'"},
                {"role": "user", "content": prompt},
            ]
        )
        import subprocess
        from AlgoParser import agreement_words
        CommonUtil.tellhim(random.choice(agreement_words))
        subprocess.run([str(response["choices"][0]["message"]["content"])], shell=True)
        ActionExplanation = str(response["choices"][0]["message"]["content"])
        response = openai.ChatCompletion.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[
            {"role": "system", "content": "Describe this command as like you have performed it and you are saying to user what YOU did and if there is any file savings - WHERE YOU HAVE SAVED that, and give me full directory adress. Talk briefly, and friendly."},
            {"role": "user", "content": ActionExplanation},
        ]
        )
        CommonUtil.tellhim(response["choices"][0]["message"]["content"])
    if Indent == "Chat":
        response = openai.ChatCompletion.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[
            {"role": "system", "content": f"Answer to this question friendly, in minimum amount of words if needed. "},
            {"role": "user", "content": prompt},
        ]
    )
        CommonUtil.tellhim(response["choices"][0]["message"]["content"])


def taskINDENT(User_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[
            {"role": "system", "content": f"Identify, whether the text is about the PC task or not. If yes - reply 'PC', otherwhise - 'Chat'"},
            {"role": "user", "content": User_prompt},
        ]
    )
    Commander(response["choices"][0]["message"]["content"], User_prompt)
    
