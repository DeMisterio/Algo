try:
    from bs4 import BeautifulSoup
    import requests
    import wikipedia
    import numpy
    import CommonUtil
    import json
    import random
    Debugstat = CommonUtil.read_key_from_JSON("Debug")
    import spacy
    from readability import Document
    import webbrowser
    from multiprocessing import Process, Queue
    import re
    import os
    import time
    import asyncio
    import edge_tts
    from playwright.sync_api import sync_playwright
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from fake_useragent import UserAgent
    if Debugstat:
        print("* searching engine has successfully loaded!")
except:
    ImportError
# Язык (по умолчанию — английский)
wikipedia.set_lang("en") # or en
ua = UserAgent()
proxies = {
    "http": "250706J3w6v-resi_region-ES_Madrid_Madrid:o7HBZBSYF4XWmBA@eu.proxy-jet.io:1010",
    "https":  "250706J3w6v-resi_region-ES_Madrid_Madrid:o7HBZBSYF4XWmBA@eu.proxy-jet.io:1010"
}
nlp = spacy.load("en_core_web_md")
from pathlib import Path
config_path = Path("config.json")

def generate_viewport():
    # Часто встречающиеся разрешения экранов
    common_viewports = [
        {"width": 1366, "height": 768},
        {"width": 1440, "height": 900},
        {"width": 1536, "height": 864},
        {"width": 1600, "height": 900},
        {"width": 1920, "height": 1080},
        {"width": 1280, "height": 800},
        {"width": 1280, "height": 720},
        {"width": 375,  "height": 667},  # iPhone
        {"width": 414,  "height": 896},  # iPhone Plus
        {"width": 390,  "height": 844},  # iPhone 12/13/14
        {"width": 360,  "height": 740},  # Android
    ]
    return random.choice(common_viewports)


def generate_user_agent():
    import random
    platforms = [
        "Windows NT 10.0; Win64; x64",
        "Macintosh; Intel Mac OS X 13_4",
        "X11; Linux x86_64",
        "iPhone; CPU iPhone OS 15_2 like Mac OS X",
        "Android 11; Mobile"
    ]

    browsers = [
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36",
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Gecko/20100101 Firefox/{firefox_version}"
    ]

    chrome_versions = ["114.0.0.0", "115.0.0.0", "116.0.5845.188"]
    firefox_versions = ["117.0", "118.0", "119.0"]

    platform = random.choice(platforms)
    browser_template = random.choice(browsers)

    if "Chrome" in browser_template:
        browser = browser_template.format(chrome_version=random.choice(chrome_versions))
    elif "Firefox" in browser_template:
        browser = browser_template.format(firefox_version=random.choice(firefox_versions))
    else:
        browser = browser_template

    return f"Mozilla/5.0 ({platform}) {browser}"

if not config_path.exists():
    config = {"Debug": False,
    "System": "Darwin",
    "Version": "Darwin Kernel Version 24.5.0: Tue Apr 22 19:54:33 PDT 2025; root:xnu-11417.121.6~2/RELEASE_ARM64_T8122",
    "Machine": "arm64",
    "Release": "24.5.0",
    "Node Name": "Denis-iMac.local",
    "RAC": True,
    "Uage": 18,
    "Uname": "User",
    "Ugender": "Male",
    "Umode" : "Voice",
    "Ulang" : "eng",
    "Ubotreference": "Algo"}
    with open(config_path,"w") as file:
        json.dump(config, file, indent=4)
    Debugstat = config["Debug"]
    print("JSON config wile installated")
else:
    with open(config_path, "r") as file:
        config = CommonUtil.safe_load_json("config.json")
        Uname = config["Uname"]
        Uage = config["Uage"]
        Ugender = config['Ugender']
        Umode = config['Umode']
last_search_time = 0
search_delay = 15.0  # ОЧЕНЬ большая задержка - 15 секунд
is_duck_blocked = False
search_attempt_count = 0
consecutive_searches = 0  # счетчик подряд идущих поисков
from playwright.sync_api import sync_playwright


def start_page_search(query):
    results = []
    proxy = {
        "server": "http://eu.proxy-jet.io:1010",
        "username": "250706J3w6v-resi-any",
        "password": "o7HBZBSYF4XWmBA"
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy=proxy
        )
        import random

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        ]
        viewport = generate_viewport()
        context = browser.new_context(
            user_agent=generate_user_agent(),
            locale=random.choice(["en-US", "fr-FR", "ru-RU"]),
            timezone_id=random.choice(["Europe/Berlin", "Europe/Moscow", "America/New_York"]),
            viewport=viewport,
            device_scale_factor=1.25,
            java_script_enabled=True
        )
        page = context.new_page()
        page.goto(f"https://www.startpage.com/sp/search?query={query}")
        print(page.content())  
        try:
            page.wait_for_selector("a.result-link", timeout=15000)
            links = page.query_selector_all("a.result-link")
            for link in links:
                time.sleep(random.randint(0.05, 0.1))
                title = link.inner_text()
                href = link.get_attribute("href")
                if href:
                    results.append({"title": title, "href": href})
        except Exception as e:
            print(f"❌ Не удалось получить результаты: {e}")

        browser.close()
    return results

# def start_page_search(query):
#     results = []
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#             locale="en-US"
#         )
#         page = context.new_page()
#         page.goto(f"https://www.startpage.com/sp/search?query={query}")
        
#         try:
#             page.wait_for_selector("a.result-link", timeout=15000)
#             links = page.query_selector_all("a.result-link")
#             for link in links:
#                 title = link.inner_text()
#                 href = link.get_attribute("href")
#                 if href:
#                     results.append({"title": title, "href": href})
#         except Exception as e:
#             print(f"❌ Не удалось получить результаты: {e}")
        
#         browser.close()
#     return results


def get_page_content(url):
    # Еще больше задержки для загрузки страниц
    delay = random.uniform(2, 4)  # от 8 до 20 секунд
    if Debugstat:
        print(f"⏳ Ожидание {delay:.1f} секунд перед загрузкой страницы...")
    time.sleep(delay)
    
    # Меняем User-Agent для каждого запроса
    user_agents = [
        ua.chrome,
        ua.firefox,
        ua.safari,
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=30)

        if r.status_code != 200:
            if Debugstat:
                print(f"❌ Не удалось получить страницу: {r.status_code}")
            return "sp"

        doc = Document(r.text)
        html = doc.summary()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        
        if Debugstat:
            print(f"✅ Извлечено символов: {len(text)}")
        
        if not text:
            if Debugstat:
                print("⚠️ Текст пустой после очистки")
            return "sp"

        # Пауза после успешной загрузки
        time.sleep(random.uniform(2.0, 5.0))
        
        return text
        
    except Exception as e:
        if Debugstat:
            print(f"❌ Ошибка при получении страницы: {e}")
        return "sp"

# Функция для сброса бана (можно вызвать вручную)
def reset_duck_ban():
    global is_duck_blocked, search_attempt_count, consecutive_searches
    is_duck_blocked = False
    search_attempt_count = 0
    consecutive_searches = 0
    print("🔄 Сброс состояния бана DuckDuckGo")
def smart_summary(text, max_sentences):
    listsmart = text
    doc = nlp(listsmart)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:max_sentences])

def get_summary(title, sentences): # for wikipedia
    try:
        page = wikipedia.page(title, auto_suggest=False)
        text = smart_summary(page.summary, sentences)
        return text, page
    except wikipedia.exceptions.DisambiguationError as e:
        return f"⚠️ Ambiguous! Try: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "❌ No page found."
  # или "en", если хочешь по-английски
def cut_engine(User_input, searching):
    from Kernel import cashe_list
    global cuted_s_p, searchable_prompt
    if len(cashe_list) != 0:
        engine_act_dict = searching #The start of the next task 
        engine_act_list = next(iter(engine_act_dict.values()))
        engine_act_re_start_of_new_task = engine_act_list[0]
        str_index, end_index = engine_act_re_start_of_new_task.start(),  engine_act_re_start_of_new_task.end()
        searchable_prompt = User_input[str_index:]
        cuted_s_p = User_input[end_index:]
    else:
        # if Debugstat:
        #     print(User_input)
        # searching = next(iter(searching.values()))
        # if searching is not None:
        #     searching = searching[0]
        # if searching is not None:
        #     searching_end_index = searching.end()
        #     searchable_prompt = User_input
        #     cuted_s_p = searchable_prompt[searching_end_index:]
        # else:
        #     searchable_prompt = User_input
        #     cuted_s_p = searchable_prompt    
        #     if Debugstat:
        #         print("No key words in question were found.")
        searchable_prompt = searching
        cuted_s_p = searchable_prompt
    return searchable_prompt, cuted_s_p
# Поиск статьи
def semantic_similarity_spacy(w1, w2):
    doc1 = nlp(w1)
    doc2 = nlp(w2)
    return doc1.similarity(doc2)
def relevatizer(User_KMS, searching):
    global start_time_countdown, q, link
    start_time_countdown = time.time()
    searchable, cuted_s_p = cut_engine(User_KMS, searching)
    results = wikipedia.search(searchable)
    if Debugstat is True:
        print("\nНайдено:", results, "\n")
    analytic_lisst = numpy.array([])
    for result in results:
        analytic_lisst = numpy.append(analytic_lisst, semantic_similarity_spacy(searchable, result))
    if Debugstat is True:
        for i in range(0, len(analytic_lisst)):
            print(i,") ", results[i], " : " , analytic_lisst[i])
    if len(analytic_lisst) >= 1:
        if numpy.max(analytic_lisst) > 0.9:
            if len(analytic_lisst) >= 1:
                mr_result = numpy.where(analytic_lisst == numpy.max(analytic_lisst))[0][0]
            else:
                return 0
            if Debugstat is True:
                print("The most relevant: (According to similarity rate)",mr_result, results[mr_result])
            besttitle = results[mr_result]
            i = random.randint(1, 30)
            if i == 15:
                try:
                    s_amo = int(input("How much do you want to learn? (1-6)"))
                    if s_amo >= 1 and s_amo <=6:
                        pass
                    else:
                        while s_amo < 1 or s_amo > 6:
                            s_amo = int(input("Enter amount from 1 to  6"))
                            if s_amo >= 1 and s_amo <=6:
                                break
                except:
                    KeyboardInterrupt, IndexError
            else:
                s_amo = random.randint(2,5)
            infot, fullwikipage = get_summary(besttitle, s_amo)
            displayer(infot, fullwikipage)
        else:
            if Debugstat is True:
                print("\nWikipedia could not help! Starting Internet DDG search..")
            analytic_lisst = numpy.array([])
            link_list = []
            material = start_page_search(searchable)
            print("🔍 Использован поиск через StartPage.")
            if Debugstat:
                print("\nAll found material on internet:\n",material)
            for sites in range(0, len(material)):
                time.sleep(random.uniform(1, 2.5))
                site_info = material[sites]
                title = site_info["title"]
                link_list.append(site_info["href"])
                parts = title.split("—")
                article_title = parts[0].strip()
                analytic_lisst = numpy.append(analytic_lisst, semantic_similarity_spacy(searchable, article_title))
            if len(analytic_lisst) >= 1:
                if Debugstat:
                    for i in range(0, len(analytic_lisst)):
                        print(i,") ", material[i]["title"], " : " , analytic_lisst[i])
                mr_result = numpy.where(analytic_lisst == max(analytic_lisst))[0][0]
                relevant_list = material[mr_result]
                if Debugstat is True:
                    print("The most relevant:", relevant_list["title"])
                if "href" in relevant_list:
                    link = relevant_list["href"]
                    if Debugstat:
                        print(link)
                else:
                    print("⚠️ No valid link found in relevant_list")
                    return  # Прерываем выполнение, если нет ссылки
            i = random.randint(1, 30)
            if i == 15:
                try:
                    s_amo = int(input("How much do you want to learn? (1-6)"))
                    if s_amo >= 1 and s_amo <=6:
                        pass
                    else:
                        while s_amo < 1 or s_amo > 6:
                            s_amo = int(input("Enter amount from 1 to  6"))
                            if s_amo >= 1 and s_amo <=6:
                                break
                except:
                    KeyboardInterrupt, IndexError
            else:
                s_amo = random.randint(3, 8)
            text_from_duck = get_page_content(link)
            if text_from_duck == "sp":
                for checker in link_list:
                    text_from_duck = get_page_content(link)
                    if text_from_duck != "sp":
                        break
                if text_from_duck == "sp":
                    print("Algo: I am so sorry! I have tried so many sites, but the access is permited... I will open the site mamually on you pc in five seconds.")
                    end_timecountdown = time.time()
                    total_time = end_timecountdown - start_time_countdown
                    print(f"for time: {total_time}")
                    for i in range(5, 0, -1):
                        print(i)
                        time.sleep(1)
                    webbrowser.open(link)
            if Debugstat:
                print(text_from_duck)
            needed_text, webpage = organazer(text_from_duck, cuted_s_p)
            displayer(smart_summary(needed_text, s_amo), webpage)
    else:
        return 0
def organazer(webp, text):
    global found
    found = False
    i = 0
    z = len(text)
    amount_of_cheks = len(webp) - z
    current_check = 0
    analytic_list = numpy.array([])
    while z != len(webp):
        analytic_list = numpy.append(analytic_list, semantic_similarity_spacy(text, webp[i:z]))
        current_check += 1
        print(f'\rEvaluating your answer: {str((100 * current_check) / amount_of_cheks)[:4]}% is done', end='', flush=True)
        i += 1
        z += 1
    current_check = 0
    amount_of_cheks = 0
    if Debugstat:
        print("\nStatistics of possibility (Impossible to read!)")
        print(analytic_list[0], ", ...", analytic_list[-1])
    bestframe = numpy.where(analytic_list == max(analytic_list))[0][0] + 1
    if webp[bestframe].isalpha():
        for q in range(bestframe, 0, -1):
            if webp[q] == "." :
                bestframe = q
                found = True
                break
            else:
                pass
        if found == False:
            for q in range(bestframe, 0, -1):
                if webp[q] == " " :
                    bestframe = q
                    found = True
                    break
    elif webp[bestframe] == ".":
        pass
    relevanindex = bestframe
    if Debugstat is True:
        print("\nNeeded info:\n")
        print(webp[relevanindex:])
    return webp[relevanindex:], webp
async def main(infov, UnameV, entryV, intro_phraseV, purpose):
    if purpose == "retell":
        tts = edge_tts.Communicate(text=(intro_phraseV + entryV + UnameV + ":  " + infov), voice="en-CA-LiamNeural")
    elif purpose == "ask":
        tts = edge_tts.Communicate(text=(infov + "," + entryV + UnameV + "?"), voice="en-CA-LiamNeural")
    await tts.save("output.mp3")

def displayer(info, fullpage):
    end_timecountdown = time.time()
    total_time = end_timecountdown - start_time_countdown
   
    #Entry meeting 
    if Umode == "Voice":
        entry, intro_phrase = CommonUtil.user_info_giver()
        asyncio.run(main(info, Uname, entry, intro_phrase, "retell"))
        os.system("afplay output.mp3")
        asyncio.run(main("Do you need full information", Uname, entry, intro_phrase, "ask"))
        os.system("afplay output.mp3")
    elif Umode == "Chat":
        entry, intro_phrase = CommonUtil.user_info_giver()
        CommonUtil.tellhim(f"\nAlgo: ...{info} \n for time: {total_time}")
    # from Kernel import sound_recodnition
    # if sound_recodnition == "yes":
    #     asyncio.run(main("Algo: Just type in Google:", Uname, entry, intro_phrase, "retell"))
    #     os.system("afplay output.mp3")
    #     print(f"Algo: Just type in Google: {fullpage}")
    # else:
    #     print(f"Algo: Just type in Google: {fullpage}")
    # os.remove("output.mp3")

