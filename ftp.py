from ftplib import FTP
import parser

class Ftp:

    def __init__(self, server="localhost", username="", password=""):
        self.server = server
        self.username = username
        self.password = password
        self.remote_file_info = {}

    def conect(self):
        # ftp = FTP('127.0.0.1', user='mspiridon', passwd="parola")
        # ftp.login(user="mspiridon",passwd="parola")
        ftp = FTP(host=self.server, user=self.username, passwd=self.password)
        ftp.login(user=self.username, passwd=self.password)
        self.ftp = ftp

    def get_info(self, path="./"):
        files = self.ftp.mlsd(path)
        for file in files:
            timestamp = file[1]['modify']
            time = parser.parse(timestamp)
            size = file[0]
            print(self.path + ' - ' + str(time))
            print(size)

    def changemon(self, dir='./'):
        # ls_prev = set()
        #
        # while True:
        #     ls = set(self.ftp.nlst(dir))
        #
        #     add, rem = ls - ls_prev, ls_prev - ls
        #     if add or rem: yield add, rem
        #
        #     ls_prev = ls
        #     sleep(5)
        print(self.ftp.nlst(dir))
