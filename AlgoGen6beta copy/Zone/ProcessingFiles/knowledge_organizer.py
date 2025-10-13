def write_to_knowledge(text):
    # 'a' — режим добавления. Если файла нет, он создаётся.
    with open("knowledge.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")  # добавляем новую строку
        
