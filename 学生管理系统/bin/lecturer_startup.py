#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os,sys, time
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from core.main import MLecturer

if __name__ == '__main__':
    MLecturer().interactive()