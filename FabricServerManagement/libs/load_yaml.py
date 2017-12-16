#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from libs import yaml


def load_yaml(yaml_file):
    '''加载yaml文件'''
    path_yaml = os.path.join(base_dir, "conf"+os.sep+yaml_file)
    with open(path_yaml) as f:
        return yaml.load(f)


if __name__ == '__main__':
    print(load_yaml("nodes.yml"))