import sys
import time
from time import sleep
from ftp import Ftp
from localFolder import LocalFolder
import datetime as dt
from scheduler import schedule_sync


class InitialSync:
    def __init__(self):
        self.location1 = None
        self.location2 = None
        self.fileContent = None
        self.current_status = None

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
            yield ftp_object.get_info(ftp_object.path)
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
            yield ftp_object.get_info(ftp_object.path)
        elif "folder" in path2:
            split_path = path2.split(":")
            local_path = split_path[1] + ":" + split_path[2]
            localFolder = LocalFolder(local_path)
            self.location2 = localFolder
            yield localFolder.get_info(localFolder.path)
            # print(localFolder.get_info())

    def saveFile(self, content):
        # print("HOOPA TOPA2222", content, type(content))
        if self.FileContent:
            self.FileContent += content
        else:
            self.FileContent = content

    def create_file(self, model, where, key, type_f):
        self.FileContent = None
        if "file" in type_f:
            model.get_content_file(key, self.saveFile)
        where.createFile(key, self.FileContent, type_f)

    def delete_file(self, location, name, type_f):
        location.deleteFile(name, type_f)

    def compare_locations(self, loc1, loc2):

        for file in loc1:
            # print(loc1[file][0])
            if file not in loc2.keys():
                # print("In local folder se creeaza fisier pentru ca exista doar la ftp", file)
                self.FileContent = None
                if "file" in loc1[file][0]:
                    self.location1.get_content_file(file, self.saveFile)
                self.location2.createFile(file, self.FileContent, loc1[file][0])
            else:

                # print("pentru file1- FTP", loc1[file])
                # print("pentru file2- local folder", loc2[file])
                # print("Au size ul diferit, esti sigur ? ", loc1[file][1] != loc2[file][1])
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
        self.current_status = self.location2.get_info(self.location2.path).copy()

    def get_status_after_sync(self):
        print("Dupa  sync este in felul urmator, acuma sunt la fel")
        self.current_status = None
        time = dt.datetime.now()
        self.current_status = self.location2.get_info(self.location2.path).copy()
        for k in self.current_status:
            if 'file' in self.current_status[k][0]:
                lst = list(self.current_status[k])
                # print(self.current_status[k][2])
                lst[0] = self.current_status[k][0]
                lst[1] = self.current_status[k][1]
                lst[2] = time
                self.current_status[k] = tuple(lst)
        print(self.current_status)
        return self.current_status

    def compare_folders(self):
        print("Acuma intra pe comparat folderele")
        dict1_info = self.location1.get_info(self.location1.path)
        dict2_info = self.location2.get_info(self.location2.path)
        print("Vechiul syncron ", self.current_status)
        print("Ce este in FTP1 ", dict1_info)
        print("Ce este in folderul local ", dict2_info)
        #  ar putea fi cazuri in care directorul sa nu fie gol si sa apara eroare la stergere
        # si abia mai apoi sa fie sterse si fisierele
        # ar trebui stabilit o ordine sa fie mai intai in dictionar cheile cu file si abia apoi cele cu dir
        # nu cred ca ordonarea ar fi neaparat cea mai buna solutie din cauza la createFile
        # trebuie imbunatatit !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        for k in dict1_info:
            if k not in dict2_info and k not in self.current_status:  # trebuie creata intrarea si in loc2
                self.create_file(self.location1, self.location2, k, dict1_info[k][0])
                print("Create in 2", k)
            elif k not in dict2_info and k in self.current_status:  # s-a sters din locatia 2 trebuie sters si in locatia 1
                self.delete_file(self.location1, k, dict1_info[k][0])
                print("Sters in 1", k)
            elif k in dict2_info and k in self.current_status and dict2_info[k][0] == 'file' and dict2_info[k][1] == \
                    self.current_status[k][1] \
                    and dict1_info[k][1] != self.current_status[k][
                1]:  # loc1 a fost modificata, loc 2 trebuie actualizata
                self.create_file(self.location1, self.location2, k, dict1_info[k][0])
                print("Modificcat in 2", k)
        for k in dict2_info:
            if k not in dict1_info and k not in self.current_status:  # trebuie creata intrarea si in loc1
                self.create_file(self.location2, self.location1, k, dict2_info[k][0])
                print("Create in 1")
            elif k not in dict1_info and k in self.current_status:  # s-a sters din locatia 1 trebuie sters si in locatia 2
                self.delete_file(self.location2, k, dict2_info[k][0])
                print("Sters in 2", k)
            elif k in dict1_info and k in self.current_status and dict1_info[k][0] == 'file' and dict1_info[k][1] == \
                    self.current_status[k][1] \
                    and dict2_info[k][1] != self.current_status[k][1]:  # loc2 a fost modificata, loc 1 trebuie actualizata
                self.create_file(self.location2, self.location1, k, dict2_info[k][0])
                print("Modificat in 1", k)

        self.get_status_after_sync()

        print("Acuma a  terminat, iata syncron ", self.current_status)
        # self.current_status["Prezent"] ="Prezent"


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Specificati path ul locatiilor pentru sincronizare")
        exit(1)
    initialSync = InitialSync()
    loc1, loc2 = initialSync.get_location(sys.argv[1], sys.argv[2])
    initialSync.compare_locations(loc1, loc2)
    # initialSync.get_status_after_sync()
    # print(initialSync.current_status)
    sched = schedule_sync()
    sched.start(initialSync.compare_folders)
    sched.start()
