import datetime as dt
import os

import pysftp
import paramiko


class SFTP:
    def __init__(self, hostname, user, password):
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
        name_n = name.split("/", 1)[1]
        # print(name)
        type = 'file'
        info = self.sftp.lstat(name)
        # print(info.st_size)
        # print(dt.datetime.fromtimestamp(info.st_mtime))
        name_nou = name_n.replace("/", "\\")
        self.sftp_info[name_nou] = (type, info.st_size, dt.datetime.fromtimestamp(info.st_mtime))

    def fill_info_dir(self, name):
        name_n = name.split("/", 1)[1]
        name_nou = name_n.replace("/", "\\")
        self.sftp_info[name_nou] = ('dir')

    def unknow_file(self):
        print("Unknow file type")

    def get_info(self, path):
        self.sftp_info = {}
        self.sftp.walktree('.', self.fill_info_file, self.fill_info_dir, self.unknow_file)
        return self.sftp_info

    def get_content_file(self, filename, callback):
        local_path = "sftp\\"+filename
        self.sftp.get(remotepath=filename, localpath=local_path)
        with open(local_path, mode='rb') as f:
            callback(f.read())
        os.remove(local_path)

    def createFile(self, filename, short_path, type):
        name_s = short_path.replace("\\", "/")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        print(name_s)
        print(type)

        if type == 'file':
            self.sftp.put(localpath=filename, remotepath=name_s)
        else:
            self.sftp.mkdir(name_s)

    def deleteFile(self, filename, type):
        name_s = filename.replace("\\", "/")
        if type == 'dir':
            self.sftp.rmdir(name_s)
        else:
            self.sftp.remove(name_s)


if __name__ == "__main__":
    sftp = SFTP("127.0.0.1", "mspiridon", "parola")
    sftp.get_info()
    print(sftp.sftp_info)
