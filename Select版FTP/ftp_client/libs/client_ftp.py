#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import socket, os, json


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()


    def connect(self, address):
        '''连接服务器'''
        self.client.connect(address)

    def interactive(self):
        '''与服务器交互，包括上传'''
        while True:
            input_cmd = input(">>>").strip()
            if len(input_cmd) == 0: continue
            cmd_array = input_cmd.split()
            if len(cmd_array) != 2 and len(cmd_array) != 1:

                continue
            action_cmd = cmd_array[0]
            if hasattr(self, "cmd_%s"%action_cmd):
                func = getattr(self, "cmd_%s"%action_cmd)
                func(input_cmd)
            else:
                pass

    def cmd_put(self, *args):
        '''上传文件'''
        filename = args[0].split()[1]   # 文件名字
        if os.path.isfile(filename):
            filesize = os.stat(filename).st_size  # 文件大小

            mes = {
                'action': 'put',
                'filename': filename,
                'filesize': filesize,
            }  # 文件信息
            self.client.send(json.dumps(mes).encode("utf-8"))   # 将文件信息发送至服务器
            print("Send: %s"%json.dumps(mes))
            server_response = self.client.recv(1024) # 等待服务器回复，防止黏包
            print("Server Response: %s"%server_response.decode())

            file = open(filename, 'rb')

            for line in file:
                try:
                    self.client.sendall(line)
                except ConnectionResetError as e:
                    print(e)
                    print("server 中断")
                    return
            else:
                print("Upload file success....")
                file.close()
            received_value = self.client.recv(1024)
            print(received_value)


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
        # print("Send: %s" % json.dumps(mes))

        server_response = self.client.recv(1024).decode()

        if not server_response.startswith("200"):
            print(server_response)
            return

        print(server_response)

        filesize = int(server_response.split()[1].strip())  # 文件大小

        self.client.send("已收到，请发送文件".encode("utf-8"))  # 防止黏包

        if os.path.isfile(filename):
            new_filename = filename + ".new"
        else:
            new_filename = filename

        file = open(new_filename, "wb")

        received_size = 0


        while received_size < filesize:  # 接受文件
            try:
                data = self.client.recv(1024)
            except ConnectionResetError as e:
                print(e)
                print("中的异常")
                continue
            except Exception as e:
                print(e)
                print("其他异常")
                continue
            file.write(data)
            received_size += len(data)
        else:
            print("file [%s] has Downloaded..." % filename)

            file.close()





if __name__ == '__main__':
    ftpClient = FtpClient()
    ftpClient.connect(('127.0.0.1', 9999))



    ftpClient.interactive()