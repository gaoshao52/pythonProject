#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import selectors
import json
import random
import sys
import os

class ServerFTP(object):

    def __init__(self, address):

        self.address = address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel = selectors.DefaultSelector()

    def initialize_sock(self):
        '''initialize server connection'''
        self.server.setblocking(False)
        self.server.bind(self.address)
        self.server.listen(5)
        self.sel.register(self.server, selectors.EVENT_READ, self.accept)

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)



    def accept(self, sock, mask):
        conn, addr = sock.accept()
        print("Accept connection from {}".format(addr))
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        '''handle client request'''

        # file info from client
        file_meg = conn.recv(1024).strip()
        file_data = json.loads(file_meg.decode())

        cmd = file_data.get('action')
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            func(conn, file_data)
        else:
            conn.send(b"400 ")

    def put(self, conn, *args):
        '''Client upload file to server'''

        filename = args[0]['filename']
        conn.send(b"200 be ready to receive")
        filesize = args[0]['filesize']

        number = random.randrange(90)
        file = open(filename+str(number), "wb")

        # accept client file data and write to server file
        while filesize:
            try:
                data = conn.recv(1024)
            except BlockingIOError as e:
                continue
            file.write(data)
            filesize -= len(data)
        else:
            conn.send(b'Accept completed')
            print('Accept completed')
            file.close()





    def get(self, conn, *args):
        '''download file to client'''

        filename = args[0]['filename']
        if os.path.isfile(filename):

            filesize = os.stat(filename).st_size
            res_mess = "200 {}".format(filesize)
            conn.send(res_mess.encode("utf-8"))

            while True:
                try:
                    mess = conn.recv(1024)
                    break
                except BlockingIOError:
                    continue

            print(mess)

            # send file to client
            file = open(filename, "rb")
            for line in file:
                try:
                    conn.send(line)
                except BlockingIOError as e:
                    print("阻塞异常")
                    continue
                except Exception as e:
                    print(e)
                    print("其他异常")
                    continue
            else:
                print("Send completed")
                file.close()


        else:
            conn.send("500 文件不存在".encode("utf-8"))


if __name__ == '__main__':

    ftp = ServerFTP(('127.0.0.1', 9999))
    ftp.initialize_sock()








