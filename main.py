import zipfile
import os
import datetime
import os.path
import urllib.parse
import pyminizip

from datetime import datetime as dt
from urllib.parse import quote
from os import getcwd

start_time=dt.now()

def read_folders(file):
    ahah='\\'+'\\'
    folders=list()
    with open(os.getcwd()+f'\\{file}') as f:
        folders=(f.read())
        folders.replace("\\", ahah)
        f.close
    fol=list(folders.split('\n'))
    print(fol)
    return(fol)

def cleaner():
    names = os.listdir(os.getcwd())
    for name in names:
        fullname = os.path.join(os.getcwd(), name)
        if os.path.isfile(fullname):  
            if fullname.endswith(".zip"):
                print(fullname)
                os.remove(os.path.join(os.getcwd(), fullname))

def log(log_text):
    if not(os.path.exists(os.getcwd()+"\\log.txt")):
        with open(os.getcwd()+"\\log.txt","w+") as log_file:
            log_file.write("hello \n")
            log_file.close()
        with open(os.getcwd()+"\\log.txt","a+") as log_file:
            log_file.write(f"{log_text}  \n")
            log_file.close()
    else:
        with open(os.getcwd()+"\\log.txt","a+") as log_file:
            log_file.write(f"{log_text} \n")
            log_file.close()
    return()

dt = datetime.datetime.now()  # получаем дату и время!
now_date = dt.date().strftime("%Y-%m-%d")  # Текущая дата
now_time = dt.time().strftime("%H-%M-%S")  # Текущее время
backup_folders = read_folders("folders.txt")  # Список папок для архивации
arch_name = "backup_" + str(now_date) + ".zip"  # имя архива!
ignore_file = read_folders("ignore_list.txt")  # если надо исключить файлы
mode="w"  # режим создания архива
compression_level = int(read_folders("param.txt")[1])  #задаем степень сжатия
password=read_folders("param.txt")[0]  #задаем пароль для архива

cleaner()  # удаляем все старые архивы в данной папке

def mybackup(arch, folder_list, mode):
    num = 0  # Счетчики
    num_ignore = 0
    z = zipfile.ZipFile(arch, mode, zipfile.ZIP_DEFLATED, True)  # Создание архива c файлами
    for add_folder in folder_list:   # Получаем папки из списка папок.
        for root, dirs, files in os.walk(add_folder):  # Список всех файлов и папок в директории add_folder
            for file in files:
                if file in ignore_file:  # Исключаем лишние файлы
                    print("Ignored", str(file))
                    num_ignore += 1
                    continue
                path = os.path.join(root, file)  # Создание относительных путей и запись файлов в архив
                try: 
                    z.write(path, compress_type=zipfile.ZIP_STORED)
                except:
                    log(f'Ошибка добавления файла {path}')
                num += 1
    z.close() #завершаем сбор всех файлов
    pyminizip.compress(f"{os.getcwd()}\\{arch}","", f"{os.getcwd()}\\compr_{arch}", password, compression_level)  #записываем всё в запароленный сжатый архив
    
    log('----------------------------') #запись информации в файл log.txt
    log(now_date)
    log(now_time)
    added=f'added files: {num}'
    ignored=f'ignored files: {num_ignore}'
    log(added)
    log(ignored)
    print("------------------------------")
    print("added files: ", num)
    print("ignored files: ", num_ignore)
    log("Size of files before comression, kb: ")
    log(os.stat(f"{os.getcwd()}\\{arch}").st_size)
    log("Size of files after comression, kb: ")
    log(os.stat(f"{os.getcwd()}\\compr_{arch}").st_size)
    os.remove(f"{os.getcwd()}\\{arch}")



print(now_time, now_date)
mybackup(arch_name, backup_folders, "w")


log("Running time:")  #записываем в логи время работы программы.
log(dt.now() - start_time)