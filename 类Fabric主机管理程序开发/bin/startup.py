#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from core.main import MainFunction

if __name__ == '__main__':
    MainFunction("nodes.yml").run()