import hashlib

def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192) #Читаем блоки
            if not data:
                break
            m.update(data)
        print(m.hexdigest()) #Возвращаем хэш
        x = input("\nНажмите любую клавишу...")

name_of_file = input("\nВведите имя файла или полный путь до файла: ")
get_hash_md5(name_of_file)