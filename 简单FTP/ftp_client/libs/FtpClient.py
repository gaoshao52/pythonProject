#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, os, json, hashlib

class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def help(self):
        '''查看帮助'''
        msg = '''
        ls
        pwd
        get filename
        put filename
        '''
        print(msg)

    def connect(self, address):
        '''连接服务器'''
        self.client.connect(address)

    def login(self, username, password):
        '''用户登录'''
        user_data = {
            'username': username,
            'password': password
        }

        self.client.send(json.dumps(user_data).encode("utf-8")) # 将用户名和密码发给服务器验证

        server_response = self.client.recv(1024).decode().strip()
        status = server_response.split()

        if status[0] == '200':
            print("成功登陆。。。。")
            return True
        else:
            print("登陆失败。。。。")
            return False



    def register(self, username, password):
        '''用户注册'''
        pass

    def interactive(self):
        '''与服务器交互，包括上传，下载，查看当前目录文件，以及查看路径'''
        while True:
            input_cmd = input(">>>").strip()
            if len(input_cmd) == 0: continue
            cmd_array = input_cmd.split()
            if len(cmd_array) != 2 and len(cmd_array) != 1:
                self.help()
                continue
            action_cmd = cmd_array[0]
            if hasattr(self, "cmd_%s"%action_cmd):
                func = getattr(self, "cmd_%s"%action_cmd)
                func(input_cmd)
            else:
                self.help()



    def cmd_put(self, *args):
        '''上传文件'''
        filename = args[0].split()[1]   # 文件名字
        if os.path.isfile(filename):
            filesize = os.stat(filename).st_size  # 文件大小

            mes = {
                'action': 'put',
                'filename': filename,
                'filesize': filesize,
                'overriden': True
            }  # 文件信息
            self.client.send(json.dumps(mes).encode())   # 将文件信息发送至服务器
            print("Send: %s"%json.dumps(mes))
            server_response = self.client.recv(1024) # 等待服务器回复，防止黏包
            print("Server Response: %s"%server_response.decode())

            m = hashlib.md5()

            file = open(filename, 'rb')

            for line in file:
                m.update(line)
                self.client.send(line)
            else:
                print("Upload file success....")
                md5_value = m.hexdigest()
                file.close()
            received_md5_value = self.client.recv(1024)
            print("Client md5 value: %s"%md5_value, "From Server md5 value: %s"%received_md5_value.decode())

        else:
            print(filename, "is not exits")




    def cmd_get(self, *args):
        '''下载文件包'''
        filename = args[0].split()[1]  # 文件名字
        mes = {
            'action': 'get',
            'filename': filename,
        }  # 文件信息

        self.client.send(json.dumps(mes).encode())  # 将文件信息发送至服务器
        print("Send: %s" % json.dumps(mes))

        server_response_filesize = self.client.recv(1024).decode()

        if server_response_filesize == "500":
            print("文件不存在")
            self.client.close()
            return
        print(server_response_filesize)
        filesize = int(server_response_filesize)  # 文件大小

        self.client.send("已收到，请发送文件".encode("utf-8"))  # 防止黏包

        if os.path.isfile(filename):
            new_filename = filename + ".new"
        else:
            new_filename = filename

        file = open(new_filename, "wb")

        received_size = 0
        m = hashlib.md5()

        while received_size < filesize:  # 接受文件

            data = self.client.recv(1024)
            m.update(data)
            file.write(data)
            received_size += len(data)
        else:
            print("file [%s] has Downloaded..." % filename)
            md5_str = m.hexdigest()
            self.client.send(md5_str.encode())
            file.close()

    def cmd_pwd(self, *args):
        print("查看路径")
        mes = {
            'action': 'pwd',
        }  # 文件信息
        self.client.send(json.dumps(mes).encode())  # 将文件信息发送至服务器
        print("Send: %s" % json.dumps(mes))

        server_response_path = self.client.recv(1024).decode()

        print("\033[31;1m用户路径：%s\033[0m"%server_response_path)

    def cmd_ls(self, *args):
        print("查看目录下文件")
        mes = {
            'action': 'ls',
        }  # 文件信息
        self.client.send(json.dumps(mes).encode())  # 将文件信息发送至服务器
        print("Send: %s" % json.dumps(mes))

        server_response_path = self.client.recv(1024).decode()

        print("\033[31;1m文件：%s\033[0m" % server_response_path)




if __name__ == '__main__':
    ftpClient = FtpClient()
    ftpClient.connect(('127.0.0.1', 9998))

    while True:
        user = input("username>>>>").strip()
        passwd = input("password>>>>").strip()
        if ftpClient.login(user, passwd):
            break
        else:
            continue

    ftpClient.interactive()





