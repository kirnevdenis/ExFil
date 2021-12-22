import os
import shutil
import time
import random

class filesio: #объявляем класс file для того, чтобы работать с файлами

    minsize = 1024
    maxsize = 128*1024
    MEMORY = 1024*1024
    mainpath = "C:\\Users"
    
    def createpasswordfile(path):
        f = open(path+"\\exfil.exfil", "wb")
        size = random.randint(filesio.minsize, filesio.maxsize)
        arr = bytearray(size)
        filescounter = filesio.countfiles(filesio.mainpath)
        i = 0
        c = 0
        while i < size:
            tempfile = " "
            while tempfile==" ":
                c = random.randint(0, filescounter)
                if filesio.size(filesio.getFileByID(filesio.mainpath, c))>0:
                    tempfile = filesio.getFileByID(filesio.mainpath, c)
            tf = open(tempfile, "rb")
            tf.seek(random.randint(0, filesio.size(tempfile)-1))
            length = random.randint(1, size-i)
            c = 0
            while c < length:
                if tf.tell() == filesio.size(tempfile):
                    tf.seek(0)
                t = bytearray(tf.read(1))
                arr[i+c] = t[0]
                print(str(i+c+1) + " of " + str(size))
                c += 1
            i+=length
        f.write(arr)
        f.flush()
        f.close()
    
    def encrypt(path):
        print("Создание файла-пароля...")
        filesio.createpasswordfile(path)
        print("Файл-пароль exfil.exfil успешно создан!")
        counter = 0
        filecounter = filesio.countfiles(path)
        passwordfile = open(path+"\\exfil.exfil", "rb")
        passwordfilesize = filesio.size(path+"\\exfil.exfil")
        while counter < filecounter:
            if filecounter-counter-1 > 0:
                print("Осталось зашифровать еще: " + str(filecounter-counter-1) + " файлов!")
            filesize = filesio.size(filesio.getFileByID(path, counter))
            currentfilepath = filesio.getFileByID(path, counter)
            currentfile = open(currentfilepath, "r+b")
            seekpos = 0
            tellpos = 0
            if filesize>0 and currentfilepath!=path+"\\exfil.exfil":
                passwordfile.seek(filesize%passwordfilesize)
                tempsize = filesize
                while tempsize>0:
                    if tempsize>=filesio.MEMORY:
                        data1 = currentfile.read(filesio.MEMORY)
                        tempsize-=filesio.MEMORY
                    else:
                        data1 = currentfile.read(tempsize)
                        tempsize-=tempsize
                    arr = bytearray(data1)
                    i = 0
                    if passwordfilesize>0:
                        while i < len(arr):
                            if (passwordfile.tell() == passwordfilesize):
                                passwordfile.seek(0)
                            t = passwordfile.read(1)
                            arr[i] = (arr[i]+t[0])%256
                            i+=1
                    tellpos = currentfile.tell()
                    currentfile.seek(seekpos)
                    currentfile.write(arr)
                    currentfile.seek(tellpos)
                    seekpos = tellpos
                currentfile.flush()
                currentfile.close()
            counter+=1

    def decrypt(path):
        counter = 0
        filecounter = filesio.countfiles(path)
        passwordfile = open(path+"\\exfil.exfil", "rb")
        passwordfilesize = filesio.size(path+"\\exfil.exfil")
        while counter < filecounter:
            if filecounter-counter-1 > 0:
                print("Осталось расшифровать еще: " + str(filecounter-counter-1) + " файлов!")
            filesize = filesio.size(filesio.getFileByID(path, counter))
            currentfilepath = filesio.getFileByID(path, counter)
            currentfile = open(currentfilepath, "r+b")
            seekpos = 0
            tellpos = 0
            if filesize>0 and currentfilepath!=path+"\\exfil.exfil":
                passwordfile.seek(filesize%passwordfilesize)
                tempsize = filesize
                while tempsize>0:
                    if tempsize>=filesio.MEMORY:
                        data1 = currentfile.read(filesio.MEMORY)
                        tempsize-=filesio.MEMORY
                    else:
                        data1 = currentfile.read(tempsize)
                        tempsize-=tempsize
                    arr = bytearray(data1)
                    i = 0
                    if passwordfilesize>0:
                        while i < len(arr):
                            if (passwordfile.tell() == passwordfilesize):
                                passwordfile.seek(0)
                            t = passwordfile.read(1)
                            arr[i] = (arr[i]-t[0])%256
                            i+=1
                    tellpos = currentfile.tell()
                    currentfile.seek(seekpos)
                    currentfile.write(arr)
                    currentfile.seek(tellpos)
                    seekpos = tellpos
            counter+=1
        passwordfile.close()
        currentfile.flush()
        currentfile.close()
        filesio.delete(path+"\\exfil.exfil")
        

    #далее пойдут некоторые базовые функции для работы с папками и файлами

    def isDir(path):
        return os.path.isdir(path)
    
    def isFile(path):
        return os.path.isfile(path)
    
    def createFile(path):
        file = open(path, "w")
        file.close()

    def createDir(path):
        if not filesio.exists(path):
            os.mkdir(path)

    def exists(path):
        return os.path.exists(path)

    def delete(path):
        if filesio.isDir(path):
            shutil.rmtree(path) #удаляем всё дерево каталога, то есть папку со всем содержимым в ней
        else:
            os.remove(path) #удаляем файл

    def size(path):
        if filesio.isFile(path):
            return os.path.getsize(path)
        else:
            size = 0
            for subdir, dirs, files in os.walk(path): #здесь и далее, везде где есть строка с os.walk - там перебор всех папок и файлов в родительской папке path
                for f in files:
                    fp = os.path.join(subdir, f) #тоже самое, как и subdir + "\\" + f.name
                    size += os.path.getsize(fp) #суммирование размеров всех файлов
            return size
    
    def getAbsolutePath(path):
        return os.path.abspath(path)

    def read(path, seek, size):
        f = open(path, "r")
        f.seek(seek)
        data = f.read(size)
        f.close()
        return data

    def rewrite(path, data): #перезапись файла
        out_file = open(path, "w")
        out_file.write(data)
        out_file.close()

    def append(path, data): #дозапись в конец файла
        out_file = open(path, "a")
        out_file.write(data)
        out_file.close()

    def rename(path1, path2):
        os.rename(path1, path2)

    def copy(path1, path2):
        if filesio.isFile(path1):
            shutil.copy2(path1, path2)
        else:
            shutil.copytree(path1, path2)

    def move(path1, path2):
        shutil.move(path1, path2)

    def countfiles(path):
        counter = 0;
        for subdir, dirs, files in os.walk(path):
                for f in files:
                    counter+=1
        return counter

    def getFileByID(path, fileid):
        if fileid>filesio.countfiles(path)-1 or fileid<0:
            fileid = fileid%filesio.countfiles(path)
        counter = 0;
        for subdir, dirs, files in os.walk(path):
                for f in files:
                    if counter == fileid:
                        return subdir+"\\"+f
                    counter+=1
        return ""

def interface(): #здесь находится интерфейс
    print("Добро пожаловать в программу шифрования данных ExFil!")
    print("Посмотреть список команд можно командой \"commands\"")
    isRun = True
    command = ""
    while isRun:
        command = input("\nx---> ")
        print()
        if command=="commands":
            print("*-*-*-*--->>> Команды ExFil <<<---*-*-*-*")
            print("commands - пулучить список команд")
            print("information - получить информацию о программе")
            print("instruction - получить инструкцию к программе")
            print("encrypt - зашифровать все файлы в указанной папке")
            print("decrypt - расшифровать все файлы в указанной папке")
            print("evaluate - выполненить однострочную команду в интерпретаторе Python")
            print("system - выполненить однострочную команду в системной консоли")
            print("setram - установить размер буфера")
            print("getram - получить размер буфера")
            print("setmin - установить минимальный размер файла-пароля")
            print("getmin - получить минимальный размер файла-пароля")
            print("setmax - установить максимальный размер файла-пароля")
            print("getmax - получить максимальный размер файла-пароля")
            print("setmainpath - установить главный путь")
            print("getmainpath - получить главный путь")
            print("isdir - проверка принадлежности указанного пути к папке")
            print("isfile - проверка принадлежности указанного пути к файлу")
            print("createfile - создать новый файл")
            print("createdir - создать новую папку")
            print("exists - проверка папки или файла на существование")
            print("countfiles - посчитать, сколько файлов в указанной папке")
            print("getfile - получить путь к файлу по его порядковому номеру в указанной папке (индексация от нуля)")
            print("clear - очистить файл")
            print("delete - удалить папку или файл")
            print("size - определить размер папки или файла")
            print("getabsolutepath - получить абсолютный путь к папке или файлу")
            print("read - прочитать файл")
            print("rewrite - перезаписать файл")
            print("write - дозаписать в файл")
            print("append - дозаписать в файл")
            print("rename - переименовать папку или файл")
            print("copy - скопировать папку или файл")
            print("move - переместить папку или файл")
            print("! - игнорировать следующее сообщение")
            print("exit - выйти из программы")
            print("stop - выйти из программы")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        elif command=="information":
            print("*-*-*-*--->>> Информация <<<---*-*-*-*")
            print("Версия: 1.0.0")
            print("Почта: den.kirnev@yandex.ru")
            print("Задача:")
            print("        Шифрование и дешифрование файлов в папке по указанному пути")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        elif command=="instruction":
            print("*-*-*-*--->>> Инструкция <<<---*-*-*-*")
            print("Запустите программу. При надобности прочтите эту инструкцию, просмотрите информацию и список команд. Далее взаимодействуйте с программой как желаете. Можно шифровать папку, даже если там только один файл. Пустую папку шифровать или дешифровать нет смысла.")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        elif command=="encrypt":
            path = input("Введите путь к папке x--> ")
            if filesio.exists(path):
                if filesio.isDir(path):
                    filesio.encrypt(path)
                    print("Файлы успешно зашифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command=="decrypt":
            path = input("Введите путь к папке x--> ")
            if filesio.exists(path):
                if filesio.isDir(path):
                    filesio.decrypt(path)
                    print("Файлы успешно дешифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command=="encrypt":
            path = input("Введите путь к папке x--> ")
            if filesio.exists(path):
                if filesio.isDir(path):
                    filesio.encrypt(path)
                    print("Файлы успешно зашифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command=="decrypt":
            path = input("Введите путь к папке x--> ")
            if filesio.exists(path):
                if filesio.isDir(path):
                    filesio.decrypt(path)
                    print("Файлы успешно дешифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command=="evaluate":
            eval(input("eval x--> "))
        elif command=="system":
            print(os.system(input("system x--> ")))
        elif command=="setram":
            filesio.MEMORY = int(input("Введите размер буфера в байтах x--> "))
        elif command=="getram":
            print("Размер буфера в байтах "+str(filesio.MEMORY))
        elif command=="setmin":
            filesio.minsize = int(input("Введите минимальный размер файла-пароля в байтах x--> "))
        elif command=="getmin":
            print("Минимальный размер файла-пароля в байтах "+str(filesio.minsize))
        elif command=="setmax":
            filesio.maxsize = int(input("Введите максимальный размер файла-пароля в байтах x--> "))
        elif command=="getmax":
            print("Максимальный размер файла-пароля в байтах "+str(filesio.maxsize))
        elif command=="setmainpath":
            filesio.mainpath = input("Введите главный путь x--> ")
        elif command=="getmainpath":
            print("Главный путь "+filesio.mainpath)
        elif command=="isfile":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    print("По указанному пути находится файл!")
                else:
                    print("По указанному пути находится не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="isdir":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isDir(path):
                    print("По указанному пути находится папка!")
                else:
                    print("По указанному пути находится не папка!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="createfile":
            filesio.createFile(input("Введите путь к файлу x--> "))
            print("Файл создан!")
        elif command=="createdir":
            filesio.createDir(input("Введите путь к папке x--> "))
            print("Папка создана!")
        elif command=="exists":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    print("Файл найден!")
                else:
                    print("Папка найдена!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="countfiles":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isDir(path):
                    print("Всего в указанной папке " + str(filesio.countfiles(path)) + " файлов!")
                else:
                    print("Требуется указать папку, а не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="getfile":
            path = input("Введите путь x--> ")
            fileid = input("Введите порядковый номер файла (от нуля)")
            if filesio.exists(path):
                if filesio.isDir(path):
                    print("Путь к указанному по порядковому номеру файлу: " + filesio.getFileByID(path, fileid))
                else:
                    print("Требуется указать папку, а не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="clear":
            path = input("Введите путь к файлу x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.rewrite(path, "");
                    print("Файл очищен!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command=="delete":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.delete(path)
                    print("Файл по указанному пути успешно удалён!")
                else:
                    filesio.delete(path)
                    print("Папка по указанному пути успешно удалена со всем содержимым!")
            else:
                print("По указанному пути ничего не найдено")
        elif command=="size":
            path = input("Введите путь к файлу x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    print("Размер файла в байтах: " + str(filesio.size(path)))
                else:
                    print("Размер папки в байтах: " + str(filesio.size(path)))
            else:
                print("Путь указан не верно")
        elif command=="getabsolutepath":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    print("Абсолютный путь к указанному файлу: " + filesio.getAbsolutePath(path))
                else:
                    print("Абсолютный путь к указанной папке: " + filesio.getAbsolutePath(path))
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="read":
            path = input("Введите путь к файлу x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    size = int(input("Сколько символов нужно считать x--> "))
                    seek = int(input("Сколько символов пропустить перед считыванием x--> "))
                    if size>-1:
                        if seek>-1:
                            if size<=filesio.size(path):
                                if seek<=filesio.size(path):
                                    if seek+size<=filesio.size(path):
                                        print("Начало сообщения:")
                                        print(filesio.read(path, seek, size))
                                        print("Конец сообщения!")
                                    else:
                                        print("Область считывания выходит за границы файла!")
                                else:
                                    print("Недопустимо пропускать количество байтов, большее размера файла")
                            else:
                                print("Недопустимо считать количество байтов, большее размера файла")
                        else:
                            print("Недопустимо пропускать отрицательное количество байтов!")
                    else:
                        print("Недопустимо считать отрицательное количество байтов!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command=="rewrite":
            path = input("Введите путь к файлу x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.rewrite(path, input("Введите сообщение x--> "));
                    print("Файл успешно перезаписан!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command=="write" or command=="append":
            path = input("Введите путь к файлу x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.append(path, input("Введите сообщение x--> "));
                    print("Данные успешно дозаписаны в файл!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command=="rename":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.rename(path, input("Введите путь к файлу вместе с новым именем x--> "))
                    print("Файл успешно переименован!")
                else:
                    filesio.rename(path, input("Введите путь к папке с новым наименованием x--> "))
                    print("Папка успешно переименована!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="copy":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.copy(path, input("Куда скопировать файл x--> "))
                    print("Файл успешно скопирован!")
                else:
                    filesio.copy(path, input("Куда скопировать папку x--> "))
                    print("Папка успешно скопирована!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="move":
            path = input("Введите путь x--> ")
            if filesio.exists(path):
                if filesio.isFile(path):
                    filesio.move(path, input("Куда переместить файл x--> "))
                    print("Файл успешно перемещён!")
                else:
                    filesio.move(path, input("Куда переместить папку x--> "))
                    print("Папка успешно перемещена!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="":
            print()
        elif command=="!":
            input("\nx--> ");
            print()
        elif command=="exit" or command=="stop":
            isRun=False
            print("Выход из программы ExFil...\n")
            time.sleep(3)
        else:
            print ("Неизвестная команда!")

def main(): #главный метод main
    interface()

main() #запуск главного метода main