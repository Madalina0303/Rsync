from zipfile import ZipFile
import os
from os import listdir
from os.path import isfile, join, isdir, exists
import datetime
import time


class Zip:
    def __init__(self, path):
        self.path = path
        self.zip_info = {}
        self.cont = {}

    def get_info(self):

        with ZipFile(self.path + ".zip", 'r') as zip:

            # print(zip.listdir)
            # print(zip.namelist())
            # print(zip.infolist())
            for info in zip.infolist():
                if info.is_dir():
                    self.zip_info[info.filename] = {'dir'}
                    # self.get_info_file(path=self.path + "\\" + info.filename[:-1])
                    # print(info.file_size)
                    # print(info.date_time)
                    # print(info.compress_size)
                else:
                    self.zip_info[info.filename] = {'file', info.file_size, info.date_time}

        return self.zip_info

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

    def get_content_file(self, file_name):
        # name = file_name.split("\\", 2)[2]
        # name = name.replace("\\", "/")
        name = file_name
        with ZipFile(self.path + ".zip", 'r') as zip:
            with zip.open(name) as f:
                print(f.read())

    def createFile(self, file_name, content=None, type_f=None):
        name = file_name
        # name = file_name.split("\\", 2)[2]
        # name = name.replace("\\", "/")
        # if type_f == 'file':
        with ZipFile(self.path + ".zip", 'a') as myzip:
            with myzip.open(name, 'w') as f:
                if content:
                    f.write(content.encode())

    def deleteFile(self, file_name, type_f):
        name = file_name
        # name = file_name.split("\\", 2)[2]
        # name = name.replace("\\", "/")
        # if "file" in type_f:
        self.cont = {}
        for file in self.zip_info:
            if file != file_name:
                self.cont[file] = self.get_content_file(file)

        with ZipFile(self.path + ".zip", 'w') as myzip:
            for name in self.cont:
                with myzip.open(name, 'w') as f:
                    if self.cont[name]:
                        f.write(self.cont[name].encode())

        # else:
        #     self.ftp.rmd(name)


if __name__ == '__main__':
    zp = Zip("D:\\an3\\python\\FolderZip")
    zp.get_info()
    # zp.get_info_file("D:\\multimi\\multimi\\obj")
    print(zp.zip_info)
    # zp.createFile("ajutor.txt", "Ceva", 'file')
    zp.deleteFile("FolderZip/mllll.txt", 'file')
    # zp.get_content_file("FolderZip/gol/")
