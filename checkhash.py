import hashlib
import shutil
import time
import json
import os

update_secs = 2 #Периодичность проверок в секундах.
backup_dir = "backup" #Дирректория

with open('hashes.json') as f: #Открываем hashes.json
    templates = json.load(f)   #Загружаем имя контролируемого файла и его хэш
    
for section, commands in templates.items(): #Сохраняем имя файла и его хэш в переменные
    file_name = section
    file_hash = ('\n'.join(commands))

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

while True: #Цикл
    time.sleep(update_secs) #Периодичность проверок, отправляем программу спать на N-ое количество секунд
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
            print(f"Файл {file_name} не найден, восстанавливаю файл.")
            debug(f"Файл {file_name} не найден, восстанавливаю файл.")
            
            replace_file(f"{file_name}") #Если файл не найден, вызываем функцию для восттановления файла из резервной копии
            
    now_hash = get_hash_md5(f"{file_name}") #Сохраняем измененный хэш в переменную
    
    if now_hash == file_hash: #Проверяем файл на соответствие
        print("Файл прошёл проверку.")
    else:
        print("ВНИМАНИЕ! Файл изменился!")
        print(f"Текущий MD5 = {now_hash}, требуемый = {file_hash}")
        debug(f"{file_name} Не прошёл проверку, текущий хэш {now_hash}, требуемый хэш {file_hash}")
        print(f"Восстанавливаю файл...")
        replace_file(f"{file_name}")
        debug("Файл успешно восстановлен!")