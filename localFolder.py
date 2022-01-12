import datetime
import time
import os
from os import listdir
from os.path import isfile, join, isdir, exists


class LocalFolder:
    def __init__(self, path):
        """
         Constructorul clasei LocalFolder
         :param str path: path ul catre fisierul local
         :returns: None

        """
        self.path = path
        self.local_file_info = {}

    def get_info(self, path, compl_name=""):
        """
         Se obtine un dictionar cu informartii despre fisierele si folderele existente la path ul dat
         :param str path: path ul directorului pentru care se doreste obtinerea de informatii
         :param str compl_name: parametru optional pentru a fi concatenat cu primul parametru si a se obtine un path complet in cazul apelarii recursive
         :returns: (dict) dictionar cu informatii despre tip, size si timpul modificarii

        """
        if compl_name == "":
            self.local_file_info = {}
        for f in listdir(path):
            full_path = join(path, f)
            if compl_name != "":
                k = compl_name + "\\" + f
            else:
                k = f
            if isfile(full_path):
                size = os.path.getsize(full_path)  # size in bytes/octeti
                modTimesinceEpoc = os.path.getmtime(full_path)
                modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
                modificationTime = datetime.datetime.strptime(modificationTime, '%Y-%m-%d %H:%M:%S')
                # print("Last Modified Time : ", type(modificationTime))
                self.local_file_info[k] = ('file', size, modificationTime)

            elif isdir(full_path):
                self.local_file_info[k] = ('dir')
                self.get_info(path=full_path, compl_name=k)

        return self.local_file_info

    def get_content_file(self, name, callback):
        """
         Obtinerea continutului unui fisier

         :param str name: numele fisierului
         :param function callback: functie callback care sa fie apelata la fiecare bloc citit din fisier
         :returns: None

        """

        full_path = self.path + "\\" + name
        print(full_path)
        with open(full_path, mode='rb') as f:
            lines = f.readlines()
            for line in lines:
                callback(line)

    def createFile(self, name, content, type_f):
        """
        Creerea unui fisier sau director

         :param str name: numele fisierului/directorului
         :param str content: continutul fisierului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        full_path = self.path + "\\" + name
        if "file" in type_f:
            with open(full_path, "wb") as f:
                if content:
                    f.write(content)
                f.close()
        elif 'dir' in type_f or type_f == 'd':
            os.mkdir(full_path)

    def deleteFile(self, name, type_f):
        """
        Stergerea unui fisier sau director

         :param str name: numele fisierului/directorului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        full_path = self.path + "\\" + name
        if "file" in type_f:
            if exists(full_path):
                os.remove(full_path)

        else:
            # se pot sterge doar directoare goale
            os.rmdir(full_path)
