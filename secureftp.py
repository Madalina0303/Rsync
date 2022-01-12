import datetime as dt
import os

import pysftp
import paramiko


class SFTP:
    def __init__(self, hostname, user, password):
        """
         Constructorul clasei SFTP
         :param str hostname: serverul sftp
         :param str user: numele utilizatorului
         :param str password: parola
         :returns: None

        """
        self.hostname = hostname
        self.user = user
        self.password = password
        self.path = "."
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.sftp_info = {}
        self.sftp = pysftp.Connection(host=self.hostname, username=self.user, password=self.password,
                                      private_key=".ppk", cnopts=cnopts)

    def fill_info_file(self, name):
        """
        Se adauga in dictionar informatii despre un fisier
        :param str name: numele fisierului
        :returns: None

        """
        name_n = name.split("/", 1)[1]
        type_f = 'file'
        info = self.sftp.lstat(name)
        name_nou = name_n.replace("/", "\\")
        self.sftp_info[name_nou] = (type_f, info.st_size, dt.datetime.fromtimestamp(info.st_mtime))

    def fill_info_dir(self, name):
        """
        Se adauga in dictionar informatii despre un folder
        :param str name: numele directorului pentru care se doreste obtinerea de informatii
        :returns: None

        """
        name_n = name.split("/", 1)[1]
        name_nou = name_n.replace("/", "\\")
        self.sftp_info[name_nou] = ('dir')

    def unknow_file(self):
        """
        Functie callback apelata in cazul fisierelor necunoscute
        :returns: None

        """
        print("Unknow file type")

    def get_info(self, path):
        """
         Se obtine un dictionar cu informatii despre fisierele si folderele existente la path ul dat
         :param str path: path ul directorului pentru care se doreste obtinerea de informatii
         :returns: (dict) dictionar cu informatii despre tip, size si timpul modificarii

        """
        self.sftp_info = {}
        self.sftp.walktree('.', self.fill_info_file, self.fill_info_dir, self.unknow_file)
        return self.sftp_info

    def get_content_file(self, filename, callback):
        """
         Obtinerea continutului unui fisier

         :param str filename: numele fisierului
         :param function callback: functie callback care sa fie apelata la fiecare bloc citit din fisier
         :returns: None

        """
        local_path = "sftp\\"+filename
        path_complet = ""
        local_path_dir = local_path.split("\\")
        for i in range(0, len(local_path_dir)-1):
            if i < len(local_path_dir)-2:
                path_complet += local_path_dir[i]+"\\"
            else:
                path_complet += local_path_dir[i]
        if not os.path.exists(path_complet):
            os.makedirs(path_complet)
        self.sftp.get(remotepath=filename, localpath=local_path)
        with open(local_path, mode='rb') as f:
            callback(f.read())
        os.remove(local_path)

    def createFile(self, filename, short_path, type_f):
        """
        Creerea unui fisier sau director

         :param str filename: numele fisierului/directorului original
         :param str short_path: numele fisierului remote
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        filename = filename.replace("/", "\\")
        name_s = short_path.replace("\\", "/")
        if type_f == 'file':
            self.sftp.put(localpath=filename, remotepath=name_s)
        else:
            self.sftp.mkdir(name_s)

    def deleteFile(self, filename, type_f):
        """
        Stergerea unui fisier sau director

         :param str filename: numele fisierului/directorului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        name_s = filename.replace("\\", "/")
        if type_f == 'dir':
            self.sftp.rmdir(name_s)
        else:
            self.sftp.remove(name_s)


if __name__ == "__main__":
    sftp = SFTP("127.0.0.1", "mspiridon", "parola")
    sftp.get_info()
    print(sftp.sftp_info)
