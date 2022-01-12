from zipfile import ZipFile
import os
from os import listdir
from os.path import isfile, join, isdir
import datetime
import time


class Zip:
    def __init__(self, path):
        """
         Constructorul clasei Zip
         :param str path: path ul catre fisierul zip
         :returns: None

        """
        self.path = path
        self.zip_info = {}
        self.cont = {}

    def get_info(self, path):
        """
         Se obtine un dictionar cu informatii despre fisierele si folderele existente la path ul dat
         :param str path: path ul directorului pentru care se doreste obtinerea de informatii
         :returns: (dict) dictionar cu informatii despre tip, size si timpul modificarii

        """
        self.zip_info = {}
        with ZipFile(self.path + ".zip", 'r') as zip:

            # print(zip.listdir)
            # print(zip.namelist())
            # print(zip.infolist())
            for info in zip.infolist():
                nou_n = info.filename.replace("/", "\\")
                if info.is_dir():
                    self.zip_info[nou_n[:-1]] = ('dir')
                    # self.get_info_file(path=self.path + "\\" + info.filename[:-1])
                    # print(info.file_size)
                    # print(info.date_time)
                    # print(info.compress_size)
                else:
                    # print(info.date_time, info.filename)
                    year = info.date_time[0]
                    month = info.date_time[1]
                    day = info.date_time[2]
                    h = info.date_time[3]
                    m = info.date_time[4]
                    s = info.date_time[5]
                    self.zip_info[nou_n] = ('file', info.file_size, datetime.datetime(year=year, month=month, day=day, hour=h, minute=m, second=s))

        return self.zip_info

    def callbck(self, path1):
        1 == 1

    def get_info_file(self, path):
        for f in listdir(path):
            full_path = join(path, f)

            if isfile(full_path):
                size = os.path.getsize(full_path)  # size in bytes/octeti
                modTimesinceEpoc = os.path.getmtime(full_path)
                modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
                modificationTime = datetime.datetime.strptime(modificationTime, '%Y-%m-%d %H:%M:%S')
                self.zip_info[full_path] = ('file', size, modificationTime)

            elif isdir(full_path):
                self.zip_info[full_path] = ('dir')
                self.get_info_file(path=full_path)

    def get_content_file(self, file_name, callback):
        """
         Obtinerea continutului unui fisier

         :param str file_name: numele fisierului
         :param function callback: functie callback care sa fie apelata la fiecare bloc citit din fisier
         :returns: (str) continutul unui fisier

        """
        # name = file_name.split("\\", 2)[2]
        name = file_name.replace("\\", "/")
        # name = file_name
        with ZipFile(self.path + ".zip", 'r') as zip:
            with zip.open(name) as f:
                aux = f.read()
                callback(aux)

        return aux



    def createFile(self, file_name, content=None, type_f=None):
        """
        Creerea unui fisier sau director

         :param str file_name: numele fisierului/directorului
         :param anystr content: continutul care sa fie salvat in cadrul fisierului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        name = file_name
        # name = file_name.split("\\", 2)[2]
        # name = name.replace("\\", "/")
        if type_f == 'file':
            with ZipFile(self.path + ".zip", 'a') as myzip:
                with myzip.open(name, 'w') as f:
                    if content:
                        f.write(content)
        # else:
        #     with ZipFile(self.path + ".zip", 'a') as myzip:
        #         myzip.open(name, 'w')

    def deleteFile(self, file_name, type_f):
        """
        Stergerea unui fisier sau director

         :param str file_name: numele fisierului/directorului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        print("DE STERS", file_name)
        name = file_name
        # name = file_name.split("\\", 2)[2]
        # name = name.replace("\\", "/")
        # if "file" in type_f:
        self.cont = {}
        for file in self.zip_info:
            print("GASIT", file)
            if file != file_name and "." in file:
                self.cont[file] = self.get_content_file(file, self.callbck)

        with ZipFile(self.path + ".zip", 'w') as myzip:
            for name in self.cont:
                with myzip.open(name, 'w') as f:
                    if self.cont[name]:
                        f.write(self.cont[name].encode())

        # else:
        #     self.ftp.rmd(name)


if __name__ == '__main__':
    zp = Zip("D:\\an3\\python\\FolderZip")
    zp.get_info('.')
    # zp.get_info_file("D:\\multimi\\multimi\\obj")
    print(zp.zip_info)
    # zp.createFile("ajutor.txt", "Ceva", 'file')
    # zp.get_info("FolderZip/mllll.txt", 'file')
    # zp.get_content_file("FolderZip/gol/")
