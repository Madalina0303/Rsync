import sys
import time
from time import sleep
from ftp import Ftp
from localFolder import LocalFolder
import datetime


class InitialSync:
    def __init__(self):
        self.location1 = None
        self.location2 = None
        self.fileContent = None

    def get_location(self, path1, path2):
        if "ftp" in path1:
            server = path1.split("@")[1][:-1]
            aux = path1.split(":")
            name = aux[1].strip()
            password = aux[2].split("@")[0]
            ftp_object = Ftp(server, name, password)
            ftp_object.conect()
            # print(ftp_object.get_info())
            self.location1 = ftp_object
            yield ftp_object.get_info()
        elif "folder" in path1:
            split_path = path1.split(":")
            local_path = split_path[1] + ":" + split_path[2]
            localFolder = LocalFolder(local_path)
            self.location1 = localFolder
            yield localFolder.get_info(localFolder.path)

        if "ftp" in path2:
            server = path1.split("@")[1][:-1]
            aux = path1.split(":")
            name = aux[1].strip()
            password = aux[2].split("@")[0]
            # print(server)
            # print(name)
            # print(password)
            ftp_object = Ftp(server, name, password)
            ftp_object.conect()
            # print(ftp_object.get_info())
            self.location2 = ftp_object
            yield ftp_object.get_info()
        elif "folder" in path2:
            split_path = path2.split(":")
            local_path = split_path[1] + ":" + split_path[2]
            localFolder = LocalFolder(local_path)
            self.location2 = localFolder
            yield localFolder.get_info(localFolder.path)
            # print(localFolder.get_info())

    def saveFile(self, content):
        print("HOOPA TOPA2222", content, type(content))
        if self.FileContent:
            self.FileContent += content
        else:
            self.FileContent = content

    def compare_locations(self, loc1, loc2):

        for file in loc1:
            print(loc1[file][0])
            if file not in loc2.keys():
                print("In local folder se creeaza fisier pentru ca exista doar la ftp", file)
                self.FileContent = None
                if "file" in loc1[file][0]:
                    self.location1.get_content_file(file, self.saveFile)
                self.location2.createFile(file, self.FileContent, loc1[file][0])
            else:

                if loc1[file][1] != loc2[file][1] and loc1[file][2] > loc2[file][2] and loc1[file][0] == 'file' and \
                        loc2[file][0] == 'file':
                    print("FTP", file, loc1[file][0], loc1[file][1]), loc1[file][2]
                    print("LOCAL", file, loc2[file][0], loc2[file][1], loc2[file][2])
                    print("In local folder se modifcia fisier pentru ca exista  modificari la ftp", file, loc1[file][1],
                          loc2[file][1])
                    self.FileContent = None
                    self.location1.get_content_file(file, self.saveFile)
                    self.location2.createFile(file, self.FileContent, loc1[file][0])

        for file in loc2:
            if file not in loc1.keys():
                print("In ftp se creaza folder pentru ca nu exista in local", file)
                self.FileContent = None
                if "file" in loc2[file][0]:
                    self.location2.get_content_file(file, self.saveFile)
                print("HOOPA TOPA ", self.FileContent, type(self.FileContent))
                self.location1.createFile(file, self.FileContent, loc2[file][0])

            else:

                if 'file' in loc2[file][0] and loc2[file][1] != loc1[file][1] and loc2[file][2] > loc1[file][2]:
                    print("In ftp folder se modifcia folder pentru ca exista  modificari la local", file, loc1[file][0],
                          loc2[file][0])
                    self.FileContent = None
                    print(self.location2.get_content_file(file, self.saveFile))
                    self.location1.createFile(file, self.FileContent, loc2[file][0])


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Specificati path ul locatiilor pentru sincronizare")
        exit(1)
    initialSync = InitialSync()
    loc1, loc2 = initialSync.get_location(sys.argv[1], sys.argv[2])
    initialSync.compare_locations(loc1, loc2)

