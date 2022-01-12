import paramiko
from scp import SCPClient
import os
import datetime as dt
import shutil


class SCP:
    def __init__(self, server, port, user, password):
        """
         Constructorul clasei SCP
         :param str server: serverul SCP
         :param str user: numele utilizatorului
         :param int port: portul utilizat
         :param str password: parola
         :returns: None

        """
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.client = None
        self.scp = None
        self.scp_info = {}
        self.path = "."

    def connect(self):
        """
        Conectarea la server
        :returns: None

        """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(self.server, self.port, self.user, self.password)
        self.scp = SCPClient(self.client.get_transport())

    def get_info(self, path):
        """
         Se obtine un dictionar cu informatii despre fisierele si folderele existente la path ul dat
         :param str path: path ul directorului pentru care se doreste obtinerea de informatii
         :returns: (dict) dictionar cu informatii despre tip, size si timpul modificarii

        """
        shutil.rmtree("scp")
        self.scp_info = {}
        self.scp.get(".", local_path="scp", recursive=True, preserve_times=True)
        for root, dirs, files in os.walk("scp"):
            for name in files:
                if name[0] != '.':
                    name = os.path.join(root, name)
                    info = self.scp._read_stats(name)
                    size = info[1]
                    timestamp = info[2]
                    time = dt.datetime.fromtimestamp(timestamp)
                    name_dict = name.split("\\", 1)[1]
                    self.scp_info[name_dict] = ('file', size, time)
            for name in dirs:
                name = os.path.join(root, name)
                name_dict = name.split("\\", 1)[1]
                self.scp_info[name_dict] = ('dir')

        return self.scp_info

    def get_content_file(self, file_name, callback):
        """
         Obtinerea continutului unui fisier

         :param str file_name: numele fisierului
         :param function callback: functie callback care sa fie apelata la fiecare bloc citit din fisier
         :returns: None

        """

        for root, dirs, files in os.walk("scp"):
            for name in files:
                name = os.path.join(root, name)
                if file_name == name.split("\\", 1)[1]:
                    with open(name, mode='rb') as f:
                        callback(f.read())

    def createFile(self, name, short_name, type_f):
        """
        Creerea unui fisier sau director

         :param str name: numele fisierului/directorului original
         :param str short_name: numele fisierului remote
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        name_s = short_name.replace("\\", "/")
        if type_f == 'file':
            self.scp.put(name, remote_path=name_s)
        else:
            self.client.exec_command('mkdir -p  ' + short_name)

    def close(self):
        """
         Inchiderea conexiunii initiate
         :returns: None

        """

        self.scp.close()

    def deleteFile(self, name, type_f=None):
        """
        Stergerea unui fisier sau director

         :param str name: numele fisierului/directorului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        nou = name.replace("\\", "/")
        self.client.exec_command('rm -rf  ' + nou)


if __name__ == '__main__':
    scpObj = SCP("students.info.uaic.ro", 22, "madalina.spiridon", "AAAbbbMMM303SSS")
    scpObj.connect()
    scpObj.get_info('.')
    # scpObj.deleteFile("python", "dir")
    print(scpObj.scp_info)
