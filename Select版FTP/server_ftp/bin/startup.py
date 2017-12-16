#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys
server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(server_dir)

from libs.server_ftp import ServerFTP


if __name__ == '__main__':
    ftp = ServerFTP(('127.0.0.1', 9999))
    ftp.initialize_sock()