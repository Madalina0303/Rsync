import sys
import time
from time import sleep
from ftp import Ftp
from localFolder import LocalFolder
import datetime as dt
from scheduler import schedule_sync
from zip import Zip
from scpp import SCP


class InitialSync:
    def __init__(self):
        self.location1 = None
        self.location2 = None
        self.fileContent = None
        self.current_status = None
        self.type1 = None
        self.type2 = None

    def get_ftp_connection_info(self, path):
        server = path.split("@")[1][:-1]
        aux = path.split(":")
        name = aux[1].strip()
        password = aux[2].split("@")[0]

        return server, name, password

    def get_scp_connection_info(self, path):
        server = path.split("@")[1]
        aux = path.split(":")
        name = aux[1].strip()
        password = aux[2].strip()
        port = aux[3].split("@")[0]

        return server, name, password, port

    def is_zip(self, path, contor):
        split_path = path.split(":")
        print(split_path)
        zip_path = split_path[1] + ":" + split_path[2].split('.')[0]
        print("IA TE UITE", zip_path)
        zipF = Zip(zip_path)
        if contor == 1:
            self.location1 = zipF
            self.type1 = "ZIP"
        else:
            self.location2 = zipF
            self.type2 = "ZIP"

    def is_ftp(self, path, contor):
        server, name, password = self.get_ftp_connection_info(path)
        ftp_object = Ftp(server, name, password)
        ftp_object.conect()
        if contor == 1:
            self.location1 = ftp_object
            self.type1 = "FTP"
        else:
            self.location2 = ftp_object
            self.type2 = "FTP"

    def is_folder(self, path, contor):
        split_path = path.split(":")
        local_path = split_path[1] + ":" + split_path[2]
        print(local_path)
        localFolder = LocalFolder(local_path)
        if contor == 1:
            self.location1 = localFolder
            self.type1 = "FOLDER"
        else:
            self.location2 = localFolder
            self.type2 = "FOLDER"

    def is_scp(self, path, contor):
        server, name, password, port = self.get_scp_connection_info(path)
        print(server)
        print(name)
        print(password)
        print(port)
        scp = SCP(server, port, name, password)
        scp.connect()
        if contor == 1:
            self.location1 = scp
            self.type1 = "SCP"
        else:
            self.location2 = scp
            self.type2 = "SCP"

    def get_location(self, path1, path2):

        if "ftp" in path1:
            self.is_ftp(path1, 1)
            yield self.location1.get_info(self.location1.path)

        elif "folder" in path1:
            self.is_folder(path1, 1)
            yield self.location1.get_info(self.location1.path)

        elif "zip" in path1:
            print(path1)
            self.is_zip(path1, 1)
            yield self.location1.get_info(self.location1.path)
        elif "scp" in path1:
            print(path1)
            self.is_scp(path1, 1)
            yield self.location1.get_info(self.location1.path)

        if "ftp" in path2:
            self.is_ftp(path2, 2)
            yield self.location2.get_info(self.location2.path)
        elif "folder" in path2:
            self.is_folder(path2, 2)
            yield self.location2.get_info(self.location2.path)
        elif "zip" in path2:
            print(path2)
            self.is_zip(path2, 2)
            yield self.location2.get_info(self.location2.path)
            # split_path = path2.split(":")
            # zip_path = split_path[1].split('.')[0]
            # print(zip_path)
            # zipF = Zip(zip_path)
            # self.location1 = zipF
            # yield zipF.get_info(zipF.path)
            # self.type2 = "ZIP"
        elif "scp" in path2:
            print(path2)
            self.is_scp(path2, 2)
            yield self.location1.get_info(self.location2.path)

    def saveFile(self, content):
        if self.FileContent:
            self.FileContent += content
        else:
            self.FileContent = content

    def create_file(self, model, where, key, type_f, scp=None):
        self.FileContent = None
        if scp:
            where.createFile(key, scp, type_f)
        else:
            if "file" in type_f:
                model.get_content_file(key, self.saveFile)
            where.createFile(key, self.FileContent, type_f)

    def delete_file(self, location, name, type_f):
        location.deleteFile(name, type_f)

    def compare_locations(self, loc1, loc2):

        for file in loc1:
            # print(loc1[file][0])
            if file not in loc2.keys():
                print(f"In {self.type2} se creeaza fisier/folder pentru ca exista doar la {self.type1}", file)
                self.FileContent = None
                if "file" in loc1[file][0]:
                    self.location1.get_content_file(file, self.saveFile)
                if "SCP" in self.type2:
                    file_ok = self.location2.path + "/" + file
                    self.location2.createFile(file_ok, file, loc1[file][0])
                else:
                    file_ok = file

                    self.location2.createFile(file_ok, self.FileContent, loc1[file][0])
            else:

                # print("pentru file1- FTP", loc1[file])
                # print("pentru file2- local folder", loc2[file])
                # print("Au size ul diferit, esti sigur ? ", loc1[file][1] != loc2[file][1])
                if loc1[file][1] != loc2[file][1] and loc1[file][2] > loc2[file][2] and loc1[file][0] == 'file' and \
                        loc2[file][0] == 'file':
                    # print("FTP", file, loc1[file][0], loc1[file][1]), loc1[file][2]
                    # print("LOCAL", file, loc2[file][0], loc2[file][1], loc2[file][2])
                    print(f"In {self.type2} se modifica fisier/folder pentru ca exista  modificari la {self.type1}",
                          file,
                          loc1[file][1],
                          loc2[file][1])
                    self.FileContent = None
                    self.location1.get_content_file(file, self.saveFile)
                    self.location2.createFile(file, self.FileContent, loc1[file][0])

        for file in loc2:
            if file not in loc1.keys():
                print(f"In {self.type1} se creaza folder/fisier pentru ca nu exista in {self.type2}", file)
                self.FileContent = None
                if "file" in loc2[file][0]:
                    self.location2.get_content_file(file, self.saveFile)
                # print("HOOPA TOPA ", self.FileContent, type(self.FileContent))
                if self.type1 == "SCP":
                    print("HELOOUUUUUUUUUU")
                    file_ok = self.location2.path + "\\" + file
                    print("BUNA DIMINEATA", file_ok)
                    # in loc de content ca oricum nu avem nevoie sa dam asa cum trebuie la remote path
                    self.location1.createFile(file_ok, file, loc2[file][0])
                else:
                    file_ok = file
                    print("FILE-OK", file_ok)
                    self.location1.createFile(file_ok, self.FileContent, loc2[file][0])

            else:

                if 'file' in loc2[file][0] and loc2[file][1] != loc1[file][1] and loc2[file][2] > loc1[file][2]:
                    print(f"In {self.type1} se modifica fisier/folder pentru ca exista  modificari la {self.type2}",
                          file, loc1[file][0],
                          loc2[file][0])
                    self.FileContent = None
                    print(self.location2.get_content_file(file, self.saveFile))

                    self.location1.createFile(file, self.FileContent, loc2[file][0])
        self.current_status = self.location2.get_info(self.location2.path).copy()

    def get_status_after_sync(self):
        # print("Dupa  sync este in felul urmator, acuma sunt la fel")
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
        param1 = None
        param2 = None
        param3 = None
        print("Incepe  compararea locatiilor")
        dict1_info = self.location1.get_info(self.location1.path)
        dict2_info = self.location2.get_info(self.location2.path)
        # print("Vechiul syncron ", self.current_status)
        print(f"Ce este in {self.type1} ", dict1_info)
        print(f"Ce este in {self.type2} ", dict2_info)
        #  ar putea fi cazuri in care directorul sa nu fie gol si sa apara eroare la stergere
        # si abia mai apoi sa fie sterse si fisierele
        # ar trebui stabilit o ordine sa fie mai intai in dictionar cheile cu file si abia apoi cele cu dir
        # nu cred ca ordonarea ar fi neaparat cea mai buna solutie din cauza la createFile
        # trebuie imbunatatit !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        for k in dict1_info:
            if k not in dict2_info and k not in self.current_status:  # trebuie creata intrarea si in loc2
                if "SCP" in self.type2:
                    file_ok = self.location1.path + "/" + k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0], scp=k)
                else:
                    file_ok = k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0])
                print(f"Create in {self.type2}", k)
            elif k not in dict2_info and k in self.current_status:  # s-a sters din locatia 2 trebuie sters si in locatia 1
                try:
                    self.delete_file(self.location1, k, dict1_info[k][0])
                    print(f"Sters in {self.type1}", k)
                except:
                    print("Directorul nu este gol")
                    param1 = self.location1
                    param2 = k
                    param3 = dict1_info[k][0]

            elif k in dict2_info and k in self.current_status and dict2_info[k][0] == 'file' and dict2_info[k][1] == \
                    self.current_status[k][1] \
                    and dict1_info[k][1] != self.current_status[k][
                1]:  # loc1 a fost modificata, loc 2 trebuie actualizata

                if "SCP" in self.type2:
                    file_ok = self.location1.path + "/" + k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0], scp=k)
                else:
                    file_ok = k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0])
                print(f"Modificcat in {self.type2}", k)

        if param1 != None and param2 != None and param3 != None:
            self.delete_file(param1, param2, param3)
            param1 = None
            param2 = None
            param3 = None
        for k in dict2_info:
            if k not in dict1_info and k not in self.current_status:  # trebuie creata intrarea si in loc1
                if "SCP" in self.type1:
                    file_ok = self.location2.path + "/" + k
                    self.create_file(self.location2, self.location1, file_ok, dict2_info[k][0], scp=k)
                else:
                    file_ok = k
                    self.create_file(self.location2, self.location1, file_ok, dict2_info[k][0])
                print(f"Create in {self.type1}")
            elif k not in dict1_info and k in self.current_status:  # s-a sters din locatia 1 trebuie sters si in locatia 2
                try:
                    self.delete_file(self.location2, k, dict2_info[k][0])
                    print(f"Sters in {self.type2}", k)
                except:
                    print("Directorul nu este gol")
                    param1 = self.location2
                    param2 = k
                    param3 = dict2_info[k][0]
            elif k in dict1_info and k in self.current_status and dict1_info[k][0] == 'file' and dict1_info[k][1] == \
                    self.current_status[k][1] \
                    and dict2_info[k][1] != self.current_status[k][
                1]:  # loc2 a fost modificata, loc 1 trebuie actualizata
                if "SCP" in self.type1:
                    file_ok = self.location2.path + "/" + k
                    self.create_file(self.location2, self.location1, file_ok, dict2_info[k][0], scp=k)
                else:
                    file_ok = k
                    self.create_file(self.location2, self.location1, file_ok, dict2_info[k][0])
                print(f"Modificat in {self.type1}", k)

        if param1 and param2 and param3:
            self.delete_file(param1, param2, param3)
            param1 = None
            param2 = None
            param3 = None
        self.get_status_after_sync()

        # print("Acuma a  terminat, iata syncron ", self.current_status)
        # self.current_status["Prezent"] ="Prezent"


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Specificati path ul locatiilor pentru sincronizare")
        exit(1)
    # log_file = open("info.log", 'w')
    # sys.stdout = sys.stderr = log_file
    initialSync = InitialSync()
    print(sys.argv[1])
    print(sys.argv[2])
    loc1, loc2 = initialSync.get_location(sys.argv[1], sys.argv[2])
    print(loc1)
    print(loc2)
    initialSync.compare_locations(loc1, loc2)
    # initialSync.get_status_after_sync()
    # print(initialSync.current_status)
    sched = schedule_sync()
    sched.start(initialSync.compare_folders)
    sched.start()
