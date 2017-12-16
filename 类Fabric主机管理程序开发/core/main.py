#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from libs import load_yaml
from libs import node
import threading

class MainFunction(object):

    def __init__(self, yaml_file):

        self.yaml_data = load_yaml.load_yaml(yaml_file)

    def list_data(self):
        '''list nodes and groups'''
        for group in self.yaml_data:
            print("-" * 60)
            print("组：%s" %group)
            for node in self.yaml_data[group]:
                print("主机名：%s"% node['hostname'])
            print("-" * 60)

    def node_action(self, hostname, action_data):
        '''node execute cmd and uploadand loadload'''
        for group in self.yaml_data:
            for node_data in self.yaml_data[group]:
                if node_data['hostname'] == hostname:
                    ip = node_data['ip']
                    passwd = node_data['password']
                    port = node_data['ssh_port']
                    username = node_data['username']
                    node_obj = node.Node(ip, passwd, port, username)

                    # execute command
                    if action_data.get('action') == "exec":
                        cmd = action_data.get('cmd')
                        result = node_obj.ssh_cmd(cmd)
                        if not result[0]:
                            print("主机[%s]执行命令：[%s] 成功。返回结果为：[%s]"%(hostname, cmd, result[1]))
                        else:
                            print("主机[%s]执行命令：[%s] 失败" % (hostname, cmd))

                        return result

                    # download file
                    if action_data.get('action') == "get":
                        remote_file = action_data.get('remote_file')
                        local_file = action_data.get('local_file')
                        node_obj.ssh_get(remote_file, local_file)
                        print("主机[%s],下载[%s]完毕"%(hostname, remote_file))
                        return True

                    # upload file
                    if action_data.get('action') == "put":
                        remote_file = action_data.get('remote_file')
                        local_file = action_data.get('local_file')
                        node_obj.ssh_put(local_file, remote_file)
                        print("主机[%s], 上传[%s]完毕。"%(hostname, local_file))
                        return True
        print("主机名不存在")
        return False # honame不存在

    def group_action(self, name, action_data):
        '''group nodes execute cmd and uploadand loadload'''
        node_name = []
        for group in self.yaml_data:
            if group == name:
                for node in self.yaml_data[group]:
                    node_name.append(node['hostname'])

        if not node_name:
            return False    # group does not exit

        # multi threading
        thread_list = []
        for name in node_name:
            node_thread = threading.Thread(target=self.node_action, args=(name, action_data))
            node_thread.start()
            thread_list.append(node_thread)

        for th in thread_list:
            th.join()

    def run(self):
        while True:
            self.list_data()

            action = input("执行命令，请输入exec；上传，请输入put；下载，请输入get>>>>").strip()
            if action == 'exec':
                cmd = input("请输入执行的命令：").strip()

                ng_name = input("操作组请输入：group；操作节点请输入node >>>>").strip()
                if ng_name == "group":
                    g_name = input("请输入组的名称：").strip()
                    self.group_action(g_name, {'action': 'exec', 'cmd': cmd})

                elif ng_name == 'node':
                    n_name = input("请输入节点的名称：").strip()
                    self.node_action(n_name, {'action': 'exec', 'cmd': cmd})

                else:
                    continue

            elif action == 'put':
                local_file = input("请输入上传的文件：")
                print(local_file)
                remote_path = input("请输入上传到节点的路径：")

                ng_name = input("操作组请输入：group；操作节点请输入node >>>>").strip()
                if ng_name == "group":
                    g_name = input("请输入组的名称：").strip()
                    self.group_action(g_name, {'action': 'put', 'remote_file': remote_path+ "/" +local_file, 'local_file': local_file})

                elif ng_name == 'node':
                    n_name = input("请输入节点的名称：").strip()
                    self.node_action(n_name, {'action': 'put', 'remote_file': remote_path + "/" + local_file,
                                               'local_file': local_file})

                else:
                    continue


            elif action == 'get':
                remote_path = input("请输入下载的文件全路径：")
                file_name = input("请输入文件名：")

                ng_name = input("操作组请输入：group；操作节点请输入node >>>>").strip()
                if ng_name == "group":
                    g_name = input("请输入组的名称：").strip()
                    self.group_action(g_name, {'action': 'get', 'remote_file': remote_path + "/" + file_name,
                                               'local_file': file_name})

                elif ng_name == 'node':
                    n_name = input("请输入节点的名称：").strip()
                    self.node_action(n_name, {'action': 'get', 'remote_file': remote_path + "/" + file_name,
                                              'local_file': file_name})

                else:
                    continue

            else:
                continue












if __name__ == '__main__':
    # s = MainFunction("nodes.yml")
    # s.list_data()
    # print("done.....")
    #
    # action_data = {
    #     'action': "exec",
    #     'cmd': 'rm -fr /root/gao.mp4'
    # }
    # action_data = {
    #     'action': "put",
    #     'remote_file': "/root/gao.mp4",
    #     'local_file': "gao.mp4"
    # }

    # s.group_action("group1", action_data)

    # node_obj = node.Node("192.168.56.11", "123456")
    # print(node_obj.ssh_cmd("hostname"))

    MainFunction("nodes.yml").run()

