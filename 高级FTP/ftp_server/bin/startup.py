#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys
server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(server_dir)
import socketserver
from libs.FtpServer import MyTCPHandler

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 9998), MyTCPHandler)
    server.serve_forever()