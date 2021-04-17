import hashlib
import shutil
import codecs
import time
import json
import os

update_secs = 1 #Периодичность проверок в секундах.
backup_dir = "backup" #Дирректория

file_name = []
file_hash = []

with codecs.open('hashes.json', 'r', encoding='utf-8') as f: #Открываем hashes.json
    templates = json.load(f)   #Загружаем имя контролируемого файла и его хэш
    
for section, commands in templates.items(): #Сохраняем имя файла и его хэш в переменные
    file_name.append(section)
    file_hash.append('\n'.join(commands))

def debug(name): #Данная функция формирует лог файл
    try:
        f = open(f'debug.log', 'a', encoding='utf8')
        f.write("\n[" + time.strftime("%d-%B-%Y %H-%M-%S] ") + name)
    except PermissionError:
        print(f"[ВНИМАНИЕ] Ошибка получения прав для записи в файл debug.log")
        return None
    
def replace_file(name): #Данная функция достаёт резервные копии из дирректории
    try: #Обрабатываем исключения если резервная копия не найдена!
        src = f"{backup_dir}\{name}"
    except FileNotFoundError:
        print(f"Не удалось найти резервную копию файла {name}")
        debug(f"Не уадлось найти резеврную копию файла {name}")
        return None
    dst = f"{name}"
    try: #Обрабатываем исключения если резервная копия не найдена!
        shutil.copy2(src, dst) #Копируем файл
    except FileNotFoundError:
        print(f"Не удалось найти резервную копию файла {name}")
        debug(f"Не уадлось найти резеврную копию файла {name}")
        return None

num_of_files = len(file_name)

while True: #Цикл
    os.system("cls")
    for i in range(0, num_of_files):
        def get_hash_md5(filename):
            try:
                with open(filename, 'rb') as f:
                    m = hashlib.md5()
                    while True:
                        data = f.read(8192) #Читаем блоки
                        if not data:
                            break
                        m.update(data)
                    return m.hexdigest() #Возвращаем хэш
            except FileNotFoundError:                
                replace_file(f"{file_name[i]}") #Если файл не найден, вызываем функцию для восттановления файла из резервной копии
                
        now_hash = get_hash_md5(f"{file_name[i]}") #Сохраняем измененный хэш в переменную
        
        if now_hash == file_hash[i]: #Проверяем файл на соответствие
            print(f"[+] {file_name[i]}")
        else:
            print(f"[X] {file_name[i]} - не прошёл проверку или не найден... Восстанавливаю файл...")
            debug(f"[X] {file_name[i]} - не прошёл проверку... Текущий хэш: {now_hash}. Требуемый хэш: {file_hash[i]}. Восстанавливаю файл.")
            replace_file(f"{file_name[i]}")
        
    time.sleep(update_secs) #Периодичность проверок, отправляем программу спать на N-ое количество секунд