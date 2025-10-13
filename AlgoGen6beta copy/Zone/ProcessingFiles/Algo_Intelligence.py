try:
    import openai
    import CommonUtil
    import random
    import asyncio
    import asyncio
    import warnings
    warnings.filterwarnings("ignore")
    import os
except ImportError:
    print("Could not initialise the Algo Intelligence")






def format_rasa_result(result):
    formatted = {}

    # Основной интент
    main_intent = result.get("intent", {})
    formatted["Intent"] = main_intent.get("name", "")
    formatted["Probability"] = main_intent.get("confidence", 0.0)
    formatted["Text"] = result.get("text", "")

    # Все сущности
    entities = result.get("entities", [])
    entities_dict = {}
    for ent in entities:
        ent_name = ent.get("entity")
        if ent_name not in entities_dict:
            entities_dict[ent_name] = []
        entities_dict[ent_name].append({
            "start": ent.get("start"),
            "end": ent.get("end"),
            "value": ent.get("value"),
            "confidence": ent.get("confidence_entity", 0.0)
        })
    formatted["Entities"] = entities_dict

    # Остальные интенты
    ranking = result.get("intent_ranking", [])
    nested_intents = []
    for intent in ranking:
        if intent.get("name") != main_intent.get("name"):
            nested_intents.append({
                "Intent": intent.get("name", ""),
                "Probability": intent.get("confidence", 0.0)
            })

    if nested_intents:
        formatted["Other Intents"] = nested_intents

    return formatted



def process_message(message, agent):
    # ВНИМАНИЕ: запускаем асинхронную функцию вручную
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(agent.parse_message(message))
    
    formatted_result = format_rasa_result(result)
    return formatted_result


def task_certifier(User_message, agent):
    message = User_message
    if message.lower() == 'exit': 
        print("Exiting...")
        return
    intent_list = process_message(message, agent)
    return intent_list


# 🔐 Рекомендуется: API ключ читается из переменной среды или .env
openai.api_key = "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"
Ubotreference = CommonUtil.read_key_from_JSON("Ubotreference")
UserOS = CommonUtil.read_key_from_JSON("System")
OS_version = CommonUtil.read_key_from_JSON("Release")
username = os.getlogin()
def Commander(Indent, prompt):
    
    if Indent == "PC":
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-mini-2025-04-14",
                messages=[
                    {"role": "system", "content": f"You are a bash command generator for {UserOS + ' ' + OS_version}. The username is {username}. Given any user request, generate ONLY the corresponding bash command. Respond with a single, ready-to-execute bash command without explanation or comments. Use application names without '.app' when opening apps. You are allowed to use 'python3' in commands if it helps solve the task.Remember that windows uses backslash '\' in the file paths. Use native {UserOS} tools when appropriate. Avoid unsafe commands unless explicitly asked (e.g., no 'rm -rf' unless clearly requested). Quote arguments properly. If the request is unclear or unsafe, respond with: 'echo Unable to process request safely. If the prompt requires saving file somewhere, the default place to save is the desktop.'"},
                    {"role": "user", "content": prompt},
                ]
            )
            bash_command = response["choices"][0]["message"]["content"]
            
        except Exception as e:
            # Если OpenAI не работает, используем DeepSeek
            import requests
            import json
            
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": "Bearer sk-9a23db8b643f44ddb4335c85aac9f9d7",  # Замени на свой ключ
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"You are a bash command generator for {UserOS + ' ' + OS_version}.The username is {username}. Given any user request, generate ONLY the corresponding bash command. Respond with a single, ready-to-execute bash command without explanation or comments. Use application names without '.app' when opening apps. You are allowed to use 'python3' in commands if it helps solve the task.Remember that windows uses backslash '\' in the file paths. Use native {UserOS} tools when appropriate. Avoid unsafe commands unless explicitly asked (e.g., no 'rm -rf' unless clearly requested). Quote arguments properly. If the request is unclear or unsafe, respond with: 'echo Unable to process request safely. If the prompt requires saving file somewhere, the default place to save is the desktop.'"},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                if response.status_code == 200:
                    bash_command = result["choices"][0]["message"]["content"]
                else:
                    CommonUtil.tellhim("Ошибка при получении команды")
                    return
            except Exception as deepseek_error:
                CommonUtil.tellhim("Не удалось подключиться к DeepSeek")
                return
        
        # Выполняем команду
        import subprocess
        import random
        from AlgoParser import agreement_words
        CommonUtil.tellhim(random.choice(agreement_words))
        
        try:
            subprocess.run([bash_command], shell=True)
            ActionExplanation = bash_command
        except Exception as exec_error:
            CommonUtil.tellhim(f"Ошибка выполнения команды: {str(exec_error)}")
            return
        
        # Получаем объяснение выполненной команды
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-mini-2025-04-14",
                messages=[
                    {"role": "system", "content": "Describe this command as like you have performed it and you are saying to user what YOU did and if there is any file savings - WHERE YOU HAVE SAVED that, and give me full directory adress. Talk briefly, and friendly."},
                    {"role": "user", "content": ActionExplanation},
                ]
            )
            explanation = response["choices"][0]["message"]["content"]
            
        except Exception as e:
            # Если OpenAI не работает для объяснения, используем DeepSeek
            explanation_data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Describe this command as like you have performed it and you are saying to user what YOU did and if there is any file savings - WHERE YOU HAVE SAVED that, and give me full directory adress. Talk briefly, and friendly."},
                    {"role": "user", "content": ActionExplanation}
                ],
                "stream": False
            }
            
            try:
                explanation_response = requests.post(url, headers=headers, json=explanation_data)
                explanation_result = explanation_response.json()
                if explanation_response.status_code == 200:
                    explanation = explanation_result["choices"][0]["message"]["content"]
                else:
                    explanation = "Команда выполнена успешно"
            except Exception as deepseek_explain_error:
                explanation = "Команда выполнена успешно"
        
        CommonUtil.tellhim(explanation)
    elif Indent == "Chat":
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-mini-2025-04-14",
                messages=[
                    {"role": "system", "content": f"Answer to this question friendly, in minimum amount of words if needed. "},
                    {"role": "user", "content": prompt},
                ]
            )   
            # Для OpenAI используем правильный путь к контенту
            CommonUtil.tellhim(response["choices"][0]["message"]["content"])
            
        except openai.error.APIConnectionError:
            # Если OpenAI недоступен, используем DeepSeek
            import requests
            
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": "Bearer sk-9a23db8b643f44ddb4335c85aac9f9d7",  # Не забудь вставить свой ключ
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Answer to this question friendly, in minimum amount of words if needed."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                # Проверка на успешный ответ
                if response.status_code == 200:
                    CommonUtil.tellhim(result["choices"][0]["message"]["content"])
                else:
                    CommonUtil.tellhim(f"Ошибка API: {response.status_code}")
                    
            except Exception as e:
                CommonUtil.tellhim(f"Ошибка при запросе к DeepSeek: {str(e)}")
    else:
        parts = Indent.split('/', 1)
        if parts[0] == "Paths analyse":
            if parts[2] == "PATH":
                pass
            elif parts[2] == "NAME":
                from pathlib import Path
                filepath = os.path.abspath(str(parts[1].strip()))
                if filepath:
                    pass
            else:
                filepath = str(parts[1].strip())
                if filepath:
                    pass
            with open(filepath, "r", encoding="utf-8") as f:
                filedata = f.read()
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4.1-mini-2025-04-14",
                    messages=[
                        {"role": "system", "content": f"You are a file analyser for {UserOS + ' ' + OS_version}. The username is {username}. Your mission is to read attached information which includes prompt, and file data, and give a complex soution or answer to the prompt."},
                        {"role": "user", "content": (prompt + ' ' + filedata)},
                    ]
                )
                file_analysis = response["choices"][0]["message"]["content"]
            except Exception as e:
                # Если OpenAI не работает, используем DeepSeek
                import requests
                import json
                
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": "Bearer sk-9a23db8b643f44ddb4335c85aac9f9d7",  # Замени на свой ключ
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": f"You are a file analyser for {UserOS + ' ' + OS_version}. The username is {username}. Your mission is to read attached information which includes prompt, and file data, and give a complex soution or answer to the prompt."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                }
                
                try:
                    response = requests.post(url, headers=headers, json=data)
                    result = response.json()
                    if response.status_code == 200:
                        file_analysis = result["choices"][0]["message"]["content"]
                    else:
                        CommonUtil.tellhim("Ошибка при получении команды")
                        return
                except Exception as deepseek_error:
                    CommonUtil.tellhim("Не удалось подключиться к DeepSeek")
                    return
            CommonUtil.tellhim(file_analysis)

def taskINDENT(User_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": f"Identify, whether the text is about the PC task or not. If yes - reply 'PC', otherwhise - 'Chat'. If this is a PC task that requires file reading - reply like ''Paths analyse' / (filepath or filename from the prompt if user has provided it) / (say PATH if what you have found was path and say NAME if what you have found was file name)'"},
                {"role": "user", "content": User_prompt},
            ]
        )
    except Exception:
        from openai import OpenAI
        client = OpenAI(api_key="sk-9a23db8b643f44ddb4335c85aac9f9d7", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Identify, whether the text is about the PC task or not. If yes - reply 'PC', otherwhise - 'Chat'. If this is a PC task that requires file reading - reply 'Paths analyse' / (filepath or filename if attached) / (say PATH if what you have found was path and say NAME if what you have found was file name)"},
            {"role": "user", "content": User_prompt
            },
        ],
        stream=False
        )

    Commander(response["choices"][0]["message"]["content"], User_prompt)
    
def helper(User_prompt, instruction):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": User_prompt},
            ]
        )
    except Exception:
        from openai import OpenAI
        client = OpenAI(api_key="sk-9a23db8b643f44ddb4335c85aac9f9d7", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": User_prompt
            },
        ],
        stream=False
        )

    return response["choices"][0]["message"]["content"]