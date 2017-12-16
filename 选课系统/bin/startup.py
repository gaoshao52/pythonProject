#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from core.manage_main import Manage_main

if __name__ == '__main__':
    Manage_main().run()

