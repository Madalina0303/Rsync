import sys
import time
from time import sleep
from ftp import Ftp
from localFolder import  LocalFolder

def get_location(path1, path2):
    if "ftp" in path1:
        server = path1.split("@")[1][:-1]
        aux = path1.split(":")
        name = aux[1].strip()
        password = aux[2].split("@")[0]
        print(server)
        print(name)
        print(password)
        ftp_object = Ftp(server, name, password)
        ftp_object.conect()
        print(ftp_object.get_info())
        #ftp_object.changemon()
        # for add, rem in self.changemon:
        #     print('\n'.join('+ %s' % i for i in add))
        #     print('\n'.join('- %s' % i for i in rem))
    if "folder" in path2: #daca este local folder, putem lua
        split_path = path2.split(":")
        local_path = split_path[1]+":"+split_path[2]
        localFolder = LocalFolder(local_path)
        print(localFolder.get_info())


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Specificati path ul locatiilor pentru sincronizare")
        exit(1)
    get_location(sys.argv[1], sys.argv[2])


