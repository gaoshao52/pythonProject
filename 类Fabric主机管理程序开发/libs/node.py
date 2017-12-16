#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import paramiko

class Node(object):
    '''节点类'''
    def __init__(self, ip, password, port=22, username="root"):
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password

        # 远程执行命令属性
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh.connect(ip, port, username, password)

        # 远程上传/下载属性
        self.ftp = self.ssh.open_sftp()


    def ssh_cmd(self, cmd):
        '''远程执行命令'''
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = stdout.read()
        if stderr.read():
            status = 1
        else:
            status =0
        return status, result

    def ssh_put(self, local_file, remote_file):
        '''远程上传'''
        self.ftp.put(local_file, remote_file)

    def ssh_get(self, remote_file, local_file):
        '''远程下载'''
        try:
            self.ftp.get(remote_file, local_file)
        except FileNotFoundError:
            print("下载文件[%s]不存在"%remote_file)

    def __del__(self):
        self.ftp.close()
        self.ssh.close()

if __name__ == '__main__':
    node = Node("192.168.56.11", "123456")
    print(node.ssh_cmd("hostname"))

    # node.ftp.put("test.txt", "/root/test.gao")
    node.ssh_get("/root/puppetfff.txt", "./puppet.log")





