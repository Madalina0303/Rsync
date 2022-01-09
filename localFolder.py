import datetime
import time
import os
from os import listdir
from os.path import isfile, join, isdir, exists


class LocalFolder:
    def __init__(self, path):
        self.path = path
        self.local_file_info = {}

    def get_info(self, path, compl_name=""):
        for f in listdir(path):
            full_path = join(path, f)
            if compl_name:

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
                self.get_info(path=full_path, compl_name=f)

        return self.local_file_info

    def get_content_file(self, name, callback):

        full_path = self.path + "\\" + name
        print(full_path)
        with open(full_path, mode='rb') as f:
            lines = f.readlines()
            for line in lines:
                callback(line)

    def createFile(self, name, content, type_f):

        full_path = self.path + "\\" + name
        # print("SE CREAAZA local un ", type_f, full_path, )
        if "file" in type_f:
            with open(full_path, "wb") as f:
                if content:
                    f.write(content)
                f.close()
        elif 'dir' in type_f or type_f == 'd':
            os.mkdir(full_path)

    def deleteFile(self, name, type_f):
        full_path = self.path + "\\" + name
        if "file" in type_f:
            if exists(full_path):
                os.remove(full_path)
        else:
            # se pot sterge doar directoare goale
            try:
                os.rmdir(full_path)
            except:
                print("Dir not empty")
