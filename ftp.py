import datetime
from ftplib import FTP
import io
from dateutil import parser


class Ftp:

    def __init__(self, server="localhost", username="", password=""):
        self.server = server
        self.username = username
        self.password = password
        self.remote_file_info = {}
        self.ftp = None
        self.path = "./"

    def conect(self):
        # ftp = FTP('127.0.0.1', user='mspiridon', passwd="parola")
        # ftp.login(user="mspiridon",passwd="parola")
        ftp = FTP(host=self.server, user=self.username, passwd=self.password, timeout=1000)
        ftp.login(user=self.username, passwd=self.password)
        self.ftp = ftp

    def get_info(self, path="./", concaten=""):
        if concaten == "":
            self.remote_file_info = {}
        # print(concaten)

        files = self.ftp.mlsd(path)
        # print("BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA HAII ODATA", files)
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
        command = "RETR " + file_name
        self.ftp.retrbinary(command, callback=fct)

    def createFile(self, name, content, type_f):
        if "file" in type_f:
            command = "STOR " + name
            self.ftp.storbinary(command, io.BytesIO(content))
        else:
            self.ftp.mkd(name)

    def deleteFile(self, name, type_f):
        if "file" in type_f:
            self.ftp.delete(name)
            # self.remote_file_info.pop(name, None)
        else:
            # try:
            self.ftp.rmd(name)
            # self.remote_file_info.pop(name, None)
            # except:
            #     print("Directory not empty")
