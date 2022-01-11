import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os
import datetime as dt
import spur


class SCP:
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.client = None
        self.scp = None
        self.scp_info = {}

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(self.server, self.port, self.user, self.password)
        self.scp = SCPClient(self.client.get_transport())

    def get_info(self, path):
        self.scp.get(".", local_path="scp", recursive=True, preserve_times=True)
        for root, dirs, files in os.walk("scp"):
            for name in files:
                if name[0] != '.':
                    name = os.path.join(root, name)
                    info = self.scp._read_stats(name)
                    size = info[1]
                    timestamp = info[2]  # timesptamp
                    time = dt.datetime.fromtimestamp(timestamp)
                    name_dict = name.split("\\", 1)[1]
                    self.scp_info[name_dict] = ('file', size, time)
            for name in dirs:
                name = os.path.join(root, name)
                name_dict = name.split("\\", 1)[1]
                self.scp_info[name_dict] = ('dir')

    def get_content_file(self, file_name, callback):
        for root, dirs, files in os.walk("scp"):
            for name in files:
                name = os.path.join(root, name)
                if file_name == name:
                    with open(file_name, mode='rb') as f:
                        callback(f.read())

    def createFile(self, name, content, type_f):
        # content poate fi None
        self.scp.put(name, remote_path=name)

    def close(self):
        self.scp.close()

    def deleteFile(self, name, type_f=None):
        self.client.exec_command('rm -rf  ' + name)


if __name__ == '__main__':
    scpObj = SCP("students.info.uaic.ro", 22, "madalina.spiridon", "AAAbbbMMM303SSS")
    scpObj.connect()
    # scpObj.get_info()
    scpObj.deleteFile("python", "dir")
    # print(scpObj.scp_info)
