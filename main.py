import sys
from ftp import Ftp
from localFolder import LocalFolder
import datetime as dt
from scheduler import schedule_sync
from zip import Zip
from scpp import SCP
from secureftp import SFTP

FTP_PATH = "D:\\an3\\python\\test" # shared folder FTP

class InitialSync:
    def __init__(self):
        """
         Constructorul clasei de sincronizare
         :returns: None

        """
        self.location1 = None
        self.location2 = None
        self.fileContent = None
        self.current_status = None
        self.type1 = None
        self.type2 = None
        self.FileContent = None

    def get_ftp_connection_info(self, path):
        """
        Prelucreaza stringul primit ca parametru pentru a extrage numele utilizatorului,parola si adresa hostului

        :param str path: path ul catre o locatie de tip ftp
        :returns: (tuple) serverul, numele si parola

        """
        server = path.split("@")[1][:-1]
        aux = path.split(":")
        name = aux[1].strip()
        password = aux[2].split("@")[0]

        return server, name, password

    def get_sftp_connection_info(self, path):

        """
        Prelucreaza stringul primit ca parametru pentru a extrage numele utilizatorului,parola si adresa hostului

        :param str path: path ul catre o locatie de tip sftp
        :returns: (tuple) serverul, numele si parola

        """
        server = path.split("@")[1]
        aux = path.split(":")
        name = aux[1].strip()
        password = aux[2].split("@")[0]

        return server, name, password

    def get_scp_connection_info(self, path):
        """
        Prelucreaza stringul primit ca parametru pentru a extrage numele utilizatorului,parola, adresa si portul hostului

        :param str path: path ul catre o locatie remote
        :returns: (tuple) serverul, numele, parola si portul

        """
        server = path.split("@")[1]
        aux = path.split(":")
        name = aux[1].strip()
        password = aux[2].strip()
        port = int(aux[3].split("@")[0])

        return server, name, password, port

    def is_zip(self, path, contor):
        """
        Se apeleaza constructorul clasei Zip si se initializeaza atributele location respectiv type

        :param str path: path ul catre o locatie de tip zip
        :param int contor: indica daca este prima sau a doua locatie/tip, 1 pentru locatia1/tip1 , 2 pentru locatia2/tip2
        :returns: None

        """
        split_path = path.split(":")
        zip_path = split_path[1] + ":" + split_path[2].split('.')[0]
        zip_f = Zip(zip_path)
        if contor == 1:
            self.location1 = zip_f
            self.type1 = "ZIP"
        else:
            self.location2 = zip_f
            self.type2 = "ZIP"

    def is_ftp(self, path, contor):
        """
        Se apeleaza constructorul clasei Ftp si se initializeaza atributele location respectiv type

        :param str path: path ul catre o locatie de tip ftp
        :param int contor: indica daca este prima sau a doua locatie/tip, 1 pentru locatia1/tip1 , 2 pentru locatia2/tip2
        :returns: None

        """
        server, name, password = self.get_ftp_connection_info(path)
        ftp_object = Ftp(server, name, password)
        ftp_object.conect()
        if contor == 1:
            self.location1 = ftp_object
            self.type1 = "FTP"
        else:
            self.location2 = ftp_object
            self.type2 = "FTP"

    def is_sftp(self, path, contor):
        """
        Se apeleaza constructorul clasei Sftp si se initializeaza atributele location respectiv type

        :param str path: path ul catre o locatie de tip sftp
        :param int contor: indica daca este prima sau a doua locatie/tip, 1 pentru locatia1/tip1 , 2 pentru locatia2/tip2
        :returns: None

        """
        server, name, password = self.get_sftp_connection_info(path)
        sftp_object = SFTP(server, name, password)
        if contor == 1:
            self.location1 = sftp_object
            self.type1 = "SFTP"
        else:
            self.location2 = sftp_object
            self.type2 = "SFTP"

    def is_folder(self, path, contor):
        """
        Se apeleaza constructorul clasei LocalFolder si se initializeaza atributele location respectiv type

        :param str path: path ul catre un folder local
        :param int contor: indica daca este prima sau a doua locatie/tip, 1 pentru locatia1/tip1 , 2 pentru locatia2/tip2
        :returns: None

        """
        split_path = path.split(":")
        local_path = split_path[1] + ":" + split_path[2]
        local_folder = LocalFolder(local_path)
        if contor == 1:
            self.location1 = local_folder
            self.type1 = "FOLDER"
        else:
            self.location2 = local_folder
            self.type2 = "FOLDER"

    def is_scp(self, path, contor):
        """
        Se apeleaza constructorul clasei Scp si se initializeaza atributele location respectiv type

        :param str path: path ul catre o locatie remote
        :param int contor: indica daca este prima sau a doua locatie/tip, 1 pentru locatia1/tip1 , 2 pentru locatia2/tip2
        :returns: None

        """
        server, name, password, port = self.get_scp_connection_info(path)
        scp = SCP(server, port, name, password)
        scp.connect()
        if contor == 1:
            self.location1 = scp
            self.type1 = "SCP"
        else:
            self.location2 = scp
            self.type2 = "SCP"

    def get_location(self, path1, path2):
        """
        Se obtin informatii despre tipul, size ul si data ultimii modificari a fisierelor/folderelor din fiecare locatie
        :param str path1: path ul catre o locatie ce trebuie sincronizata
        :param str path2: path ul catre a doua locatie
        :returns: (tuple) 2 dictionare cu informatii

        """

        if "sftp" in path1:
            self.is_sftp(path1, 1)
            yield self.location1.get_info(self.location1.path)

        elif "ftp" in path1:
            self.is_ftp(path1, 1)
            yield self.location1.get_info(self.location1.path)

        elif "folder" in path1:
            self.is_folder(path1, 1)
            yield self.location1.get_info(self.location1.path)

        elif "zip" in path1:
            self.is_zip(path1, 1)
            yield self.location1.get_info(self.location1.path)
        elif "scp" in path1:
            self.is_scp(path1, 1)
            yield self.location1.get_info(self.location1.path)

        if "sftp" in path2:
            self.is_sftp(path2, 2)
            yield self.location2.get_info(self.location2.path)
        elif "folder" in path2:
            self.is_folder(path2, 2)
            yield self.location2.get_info(self.location2.path)
        elif "zip" in path2:
            self.is_zip(path2, 2)
            yield self.location2.get_info(self.location2.path)
        elif "scp" in path2:
            self.is_scp(path2, 2)
            yield self.location1.get_info(self.location2.path)
        elif "ftp" in path2:
            self.is_ftp(path2, 1)
            yield self.location2.get_info(self.location1.path)

    def save_file(self, content):
        """
        Se salveaza continutul unui fisier

        :param str content: o parte din continutul unui fisier
        :returns: None

        """

        if self.FileContent:
            self.FileContent += content
        else:
            self.FileContent = content

    def create_file(self, model, where, key, type_f, supl=None):
        """
        Se obtine continutul fisierului daca este cazul si apeleaza functia createFile corespunzatoare fiecarei clase

        :param LocalFolder/Zip/Sftp/Ftp/Scp model: locatia care detine fisierul
        :param LocalFolder/Zip/Sftp/Ftp/Scp where: locatia in care trebuie creat fisierul
        :param str key: numele fisierului/directorului de creat
        :param str type_f: daca este fisier sau director
        :param string supl: parametru optional care indica denumirea cu care sa fie creat fisierul pentru Sftp si Scp
        :returns: None

        """
        self.FileContent = None
        if supl:
            where.createFile(key, supl, type_f)
        else:
            if "file" in type_f:
                model.get_content_file(key, self.save_file)
            where.createFile(key, self.FileContent, type_f)

    def delete_file(self, location, name, type_f):
        """
        Se sterge fisierul/folderul din locatia data

        :param LocalFolder/Zip/Sftp/Ftp/Scp location: locatia din care se sterge
        :param str name: numele fisierului/folderului
        :param str type_f: daca este fisier sau director
        :returns: None

        """
        location.deleteFile(name, type_f)

    def compare_locations(self, loc1, loc2):
        """
        Sincronizarea initiala dintre cele 2 locatii

        :param LocalFolder/Zip/Sftp/Ftp/Scp loc1: prima dintre locatiele ce trebuie sincronizata
        :param LocalFolder/Zip/Sftp/Ftp/Scp loc2: a doua dintre locatiele ce trebuie sincronizata
        :returns: None

        """

        for file in loc1:
            if file not in loc2.keys():
                print(f"In {self.type2} se creeaza fisier/folder pentru ca exista doar la {self.type1}", file)
                self.FileContent = None
                if "file" in loc1[file][0]:
                    self.location1.get_content_file(file, self.save_file)
                if "SCP" in self.type2 or "SFTP" in self.type2:
                    if self.type1 == "FTP":
                        file_ok = FTP_PATH + "\\" + file
                    else:
                        file_ok = self.location1.path + "/" + file
                    self.location2.createFile(file_ok, file, loc1[file][0])
                else:
                    file_ok = file

                    self.location2.createFile(file_ok, self.FileContent, loc1[file][0])
            else:

                if loc1[file][1] != loc2[file][1] and loc1[file][2] > loc2[file][2] and loc1[file][0] == 'file' and loc2[file][0] == 'file':
                    print(f"In {self.type2} se modifica fisier/folder pentru ca exista  modificari la {self.type1}",
                          file,
                          loc1[file][1],
                          loc2[file][1])
                    self.FileContent = None
                    self.location1.get_content_file(file, self.save_file)
                    if "SCP" in self.type2 or "SFTP" in self.type2:
                        if self.type1 == "FTP":
                            file_ok = FTP_PATH + "\\" + file
                        else:
                            file_ok = self.location1.path + "/" + file
                        self.location2.createFile(file_ok, file, loc1[file][0])
                    else:
                        file_ok = file
                        self.location2.createFile(file_ok, self.FileContent, loc1[file][0])

        for file in loc2:
            if file not in loc1.keys():
                print(f"In {self.type1} se creaza folder/fisier pentru ca nu exista in {self.type2}", file)
                self.FileContent = None
                if "file" in loc2[file][0]:
                    self.location2.get_content_file(file, self.save_file)
                if self.type1 == "SCP" or self.type1 == "SFTP":
                    if self.type2 == "FTP":
                        file_ok = FTP_PATH+ "\\" + file
                    elif self.type2 == "ZIP":
                        file_ok = self.location2.path + ".zip\\" + file
                    else:
                        file_ok = self.location2.path + "\\" + file

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
                    self.location2.get_content_file(file, self.save_file)
                    if self.type1 == "SCP" or self.type1 == "SFTP":
                        if self.type2 == "FTP":
                            file_ok = FTP_PATH + "\\" + file
                        else:
                            file_ok = self.location2.path + "\\" + file
                        self.location1.createFile(file_ok, file, loc2[file][0])
                    else:
                        file_ok = file

                        self.location1.createFile(file_ok, self.FileContent, loc2[file][0])

        self.current_status = self.location2.get_info(self.location2.path).copy()

    def get_status_after_sync(self):
        """
        Statusul cu cele doua locatii sincronizate
        :returns: (dict) un dictionar cu info despre fisierele comune

        """

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
        """
        Se compara si apoi se sincronizeaza cele 2 locatii daca exista diferente
        :returns: None

        """
        param1 = None
        param2 = None
        param3 = None
        print("Incepe  compararea locatiilor")
        dict1_info = self.location1.get_info(self.location1.path)
        dict2_info = self.location2.get_info(self.location2.path)
        print(f"Ce este in {self.type1} ", dict1_info)
        print(f"Ce este in {self.type2} ", dict2_info)
        for k in dict1_info:
            if k not in dict2_info and k not in self.current_status:  # trebuie creata intrarea si in loc2
                if "SCP" in self.type2 or "SFTP" in self.type2:
                    if self.type1 == "FTP":
                        file_ok = FTP_PATH + "\\" + k
                    else:
                        file_ok = self.location1.path + "/" + k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0], supl=k)
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
                    and dict1_info[k][1] != self.current_status[k][1]:  # loc1 a fost modificata, loc 2 trebuie actualizata

                if "SCP" in self.type2 or "SFTP" in self.type2:
                    if self.type1 == "FTP":
                        file_ok = FTP_PATH + "\\" + k
                    else:
                        file_ok = self.location1.path + "/" + k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0], supl=k)
                else:
                    file_ok = k
                    self.create_file(self.location1, self.location2, file_ok, dict1_info[k][0])
                print(f"Modificcat in {self.type2}", k)

        if param1 and param2 and param3:
            self.delete_file(param1, param2, param3)
            param1 = None
            param2 = None
            param3 = None
        for k in dict2_info:
            if k not in dict1_info and k not in self.current_status:  # trebuie creata intrarea si in loc1
                if "SCP" in self.type1 or "SFTP" in self.type1:
                    if self.type2 == "FTP":
                        file_ok = FTP_PATH + "\\" + k
                    else:
                        file_ok = self.location2.path + "/" + k
                    self.create_file(self.location2, self.location1, file_ok, dict2_info[k][0], k)
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
                    and dict2_info[k][1] != self.current_status[k][1]:
                # loc2 a fost modificata, loc 1 trebuie actualizata
                if "SCP" in self.type1 or "SFTP" in self.type1:
                    if self.type2 == "FTP":
                        file_ok = FTP_PATH + "\\" + k
                    else:
                        file_ok = self.location2.path + "/" + k
                    self.create_file(self.location2, self.location1, file_ok, dict2_info[k][0], supl=k)
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


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Specificati path ul locatiilor pentru sincronizare")
        exit(1)
    # log_file = open("info.log", 'w')
    # sys.stdout = sys.stderr = log_file
    initialSync = InitialSync()
    loc1, loc2 = initialSync.get_location(sys.argv[1], sys.argv[2])
    initialSync.compare_locations(loc1, loc2)
    sched = schedule_sync()
    sched.start(initialSync.compare_folders)
