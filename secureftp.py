import datetime as dt

import pysftp
import paramiko


class SFTP:
    def __init__(self, hostname, user, password):
        self.hostname = hostname
        self.user = user
        self.password = password
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.sftp_info = {}
        self.sftp = pysftp.Connection(host=self.hostname, username=self.user, password=self.password,
                                      private_key=".ppk", cnopts=cnopts)

    def fill_info_file(self, name):
        print(name)
        type = 'file'
        info = self.sftp.lstat(name)
        # print(info.st_size)
        # print(dt.datetime.fromtimestamp(info.st_mtime))
        self.sftp_info[name] = (type, info.st_size, dt.datetime.fromtimestamp(info.st_mtime))

    def fill_info_dir(self, name):
        self.sftp_info[name] = ('dir')

    def unknow_file(self):
        print("Unknow file type")

    def get_info(self):
        self.sftp.walktree('.', self.fill_info_file, self.fill_info_dir, self.unknow_file)

    def get_content_file(self, filename):
        local_path = "sftp" + filename.split("/", 1)[1]
        self.sftp.get(filename, local_path)
        with open(local_path, mode='rb') as f:
            return f.read()

    def createFile(self, filename, type):
        if type == 'dir':
            self.sftp.mkdir(filename)
        else:
            self.sftp.put(localpath=filename, remotepath=filename)

    def deleteFile(self, filename, type):
        if type == 'dir':
            self.sftp.rmdir(filename)
        else:
            self.sftp.remove(filename)


if __name__ == "__main__":
    sftp = SFTP("127.0.0.1", "mspiridon", "parola")
    sftp.get_info()
    print(sftp.sftp_info)
