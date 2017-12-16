#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys
client_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(client_dir)
from libs.FtpClient import FtpClient
import hashlib

if __name__ == '__main__':
    ftpClient = FtpClient()
    ftpClient.connect(('127.0.0.1', 9998))

    while True:
        user = input("username>>>>").strip()
        passwd = input("password>>>>").strip()

        # 密码加密认证
        m5 = hashlib.md5()
        m5.update(passwd.encode('utf-8'))
        hash_passwd = m5.hexdigest()
        # print(hash_passwd)
        if ftpClient.login(user, hash_passwd):
            break
        else:
            continue

    ftpClient.interactive()


