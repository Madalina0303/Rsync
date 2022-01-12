import datetime
from ftplib import FTP
import io
from dateutil import parser


class Ftp:

    def __init__(self, server="localhost", username="", password=""):
        """
         Constructorul clasei FTP
         :param str server: serverul ftp
         :param str username: numele utilizatorului
         :param str password: parola
         :returns: None

        """
        self.server = server
        self.username = username
        self.password = password
        self.remote_file_info = {}
        self.ftp = None
        self.path = "./"

    def conect(self):
        """
        Conectarea la serverul Ftp
        :returns: None

        """
        ftp = FTP(host=self.server, user=self.username, passwd=self.password, timeout=1000)
        ftp.login(user=self.username, passwd=self.password)
        self.ftp = ftp

    def get_info(self, path="./", concaten=""):
        """
         Se obtine un dictionar cu fisierele si folderele existente la path ul dat
         :param str path: path ul directorului pentru care se doreste obtinerea de informatii
         :param str concaten: parametru optional pentru a fi concatenat cu primul parametru si a se obtine un path complet in cazul apelarii recursive
         :returns: (dict) dictionar cu informatii despre tip, size si timpul modificarii

        """

        if concaten == "":
            self.remote_file_info = {}

        files = self.ftp.mlsd(path)
        for file in files:
            try:
                # print(file)
                type_f = file[1]["type"]
                # print(type)
                timestamp = file[1]['modify']
                time = parser.parse(timestamp) + datetime.timedelta(hours=2)
                if "./" == path:
                    concaten1 = file[0]
                else:
                    concaten1 = path + "\\" + file[0]
                if "file" in type_f:
                    size = int(file[1]["size"])
                    self.remote_file_info[concaten + file[0]] = (type_f, size, time)
                if type_f == "dir":
                    self.remote_file_info[concaten + file[0]] = (type_f)
                    self.get_info(path=concaten1, concaten=concaten1 + "\\")
            except:
                print("Nu are toate campurile")

        return self.remote_file_info

    def get_content_file(self, file_name, fct):
        """
         Obtinerea continutului unui fisier

         :param str file_name: numele fisierului
         :param function fct: functie callback care sa fie apelata la fiecare bloc citit din fisier
         :returns: None

        """
        command = "RETR " + file_name
        self.ftp.retrbinary(command, callback=fct)

    def createFile(self, name, content, type_f):
        """
        Creerea unui fisier sau director

         :param str name: numele fisierului/directorului
         :param str content: continutul care sa fie salvat in cadrul fisierului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        if "file" in type_f:
            command = "STOR " + name
            self.ftp.storbinary(command, io.BytesIO(content))
        else:
            self.ftp.mkd(name)

    def deleteFile(self, name, type_f):
        """
        Stergerea unui fisier sau director

         :param str name: numele fisierului/directorului
         :param str type_f: daca este fisier sau folder
         :returns: None

        """
        if "file" in type_f:
            self.ftp.delete(name)
        else:
            self.ftp.rmd(name)
