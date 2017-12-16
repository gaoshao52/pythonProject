#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socketserver, hashlib
import json, os
server_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # 用户验证
        while True:
            result = self.validation()
            self.username = result[1].strip()
            self.home_path = os.path.join(server_root, "database" + os.sep + self.username)
            if not result[0]:
                continue
            break

        # 处理用户指令
        while True:
            try:
                self.data = self.request.recv(1024).strip() # 接受服务器发来的文件信息
                print("Accept client address {}".format(self.client_address[0]))
                print("Rceive data: {}".format(self.data))
                cmd_dic = json.loads(self.data.decode()) # 转化为字典
                action = cmd_dic['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("err:", e)
                break
            except Exception as e:
                print(e)
                break

    def put(self, *args):
        '''用户上传'''
        # home_path = os.path.join(server_root, "database" + os.sep + self.username)

        cmd_dic = args[0]
        filename = cmd_dic['filename']
        print("%s will be put to server"%filename)
        filesize = cmd_dic['filesize']
        print("FileSize of %s: %s"%(filename, filesize))

        file_path = os.path.join(self.home_path, filename)

        if os.path.isfile(file_path):
            f = open(file_path+ ".new", "wb")
        else:
            f = open(file_path, "wb")
        self.request.send(b"200 ok")

        received_size = 0
        m = hashlib.md5()

        while received_size < filesize:

            data = self.request.recv(1024)
            m.update(data)
            f.write(data)
            received_size += len(data)
        else:
            print("file [%s] has uploaded..."% filename)
            md5_str = m.hexdigest()
            self.request.send(md5_str.encode())

    def get(self, *args):
        '''用户下载'''

        cmd_dic = args[0]
        filename = cmd_dic['filename']
        file_path = os.path.join(self.home_path, filename)
        if os.path.isfile(file_path):
            filesize = os.stat(file_path).st_size  # 文件大小
            print("filesize:",filesize)
            self.request.send(str(filesize).encode("utf-8"))
            self.request.recv(1024)
            m = hashlib.md5()
            file = open(file_path, 'rb')

            for line in file:
                m.update(line)
                self.request.send(line)
            else:
                print("Send file success....")
                md5_value = m.hexdigest()
                file.close()
            received_md5_value = self.request.recv(1024)
            print("Server md5 value: %s" % md5_value, "From Client md5 value: %s" % received_md5_value.decode())
        else:
            self.request.send(b"500")

    def validation(self):
        '''验证用户信息'''
        user_str = self.request.recv(1024).decode()
        user_data = json.loads(user_str)
        print("user data: %s"% user_str)
        client_name = user_data.get('username')
        client_pass = user_data.get('password')

        # self.username = client_name

        home_path = os.path.join(server_root, "database" + os.sep + client_name)
        if not os.path.isdir(home_path):
            print("用户名不存在。。。")
            self.request.send("400 用户名不存在".encode("utf-8")) # 400
            return False, client_name
        file_path = os.path.join(home_path, "%s.json"%client_name)

        if not os.path.isfile(file_path):
            print("500 服务器数据不存在".encode("utf-8"))
            return False, client_name

        with open(file_path, "r") as f:
            data = json.load(f)
            if client_name == data.get('username') and client_pass == data.get('password'):
                self.request.send("200 验证通过".encode("utf-8"))
                return True, client_name
            else:
                self.request.send("400 错误的用户名或密码".encode("utf-8"))
                return False, client_name

    def pwd(self, *args):
        user_home = "/home/%s"%self.username
        print("user home : %s"% user_home)
        self.request.send(user_home.encode("utf-8"))

    def ls(self, *args):
        '''查看用户目录文件'''
        result = os.listdir(self.home_path)
        result.remove("%s.json"%self.username)
        result_str = " ".join(result)
        self.request.send(result_str.encode("utf-8"))


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 9998), MyTCPHandler)
    server.serve_forever()



