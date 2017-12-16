#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys
client_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(client_dir)
from libs.FtpClient import FtpClient

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


