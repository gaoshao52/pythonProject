#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socketserver, hashlib
import json, os
server_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # 用户验证
        self.current_dir = ""
        while True:
            result = self.validation()
            self.username = result[1].strip()
            self.current_dir = "/home/%s"%self.username
            self.home_path = os.path.join(server_root, "database" + os.sep + self.username)
            # self.file_path = os.path.join(self.home_path, "%s.json"% self.username)
            # print(self.file_path)

            if not result[0]:
                continue
            break

        # 处理用户指令
        while True:
            try:
                self.data = self.request.recv(1024).strip() # 接受服务器发来的文件信息
                print("Accept client address {}".format(self.client_address[0]))
                print("Rceive data: {}".format(self.data))
                cmd_dic = json.loads(self.data.decode()) # 转化为字典
                action = cmd_dic['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("err:", e)
                break
            except Exception as e:
                print(e)
                break

    def put(self, *args):
        '''用户上传'''
        # home_path = os.path.join(server_root, "database" + os.sep + self.username)

        cmd_dic = args[0]
        filename = cmd_dic['filename']
        print("%s will be put to server"%filename)
        filesize = cmd_dic['filesize']


        print("FileSize of %s: %s"%(filename, filesize))

        # 检查磁盘大小
        if not self.check_disk(filesize):
            self.request.send("400 磁盘空间不足".encode('utf-8'))
            return

        file_path = os.path.join(self.home_path, filename)

        if os.path.isfile(file_path):
            filename += ".new"
            f = open(file_path+ ".new", "wb")
        else:
            f = open(file_path, "wb")
        self.request.send(b"200 ok")

        received_size = 0
        m = hashlib.md5()

        while received_size < filesize:

            data = self.request.recv(1024)
            m.update(data)
            f.write(data)
            received_size += len(data)
        else:
            print("file [%s] has uploaded..."% filename)
            self.update_user_disk_size()  # 更新数据库用户磁盘配置大小
            self.update_file_to_db(filename)  # 更新文件名字到数据库
            md5_str = m.hexdigest()
            self.request.send(md5_str.encode())

    def get(self, *args):
        '''用户下载'''

        cmd_dic = args[0]
        filename = cmd_dic['filename']
        file_path = os.path.join(self.home_path, filename)
        if os.path.isfile(file_path):
            filesize = os.stat(file_path).st_size  # 文件大小
            print("filesize:",filesize)
            self.request.send(str(filesize).encode("utf-8"))
            self.request.recv(1024)
            m = hashlib.md5()
            file = open(file_path, 'rb')

            for line in file:
                m.update(line)
                self.request.send(line)
            else:
                print("Send file success....")
                md5_value = m.hexdigest()
                file.close()
            received_md5_value = self.request.recv(1024)

            if md5_value == received_md5_value.decode():
                print("Server md5 value equal to Client md5")
                print("Server md5 value: %s" % md5_value, "From Client md5 value: %s" % received_md5_value.decode())
        else:
            self.request.send(b"500")

    def validation(self):
        '''验证用户信息'''
        user_str = self.request.recv(1024).decode()
        user_data = json.loads(user_str)
        print("user data: %s"% user_str)
        client_name = user_data.get('username')
        client_pass = user_data.get('password')

        # self.username = client_name

        home_path = os.path.join(server_root, "database" + os.sep + client_name)
        if not os.path.isdir(home_path):
            print("用户名不存在。。。")
            self.request.send("400 用户名不存在".encode("utf-8")) # 400
            return False, client_name
        self.file_path = os.path.join(home_path, "%s.json"%client_name)
        # print(file_path)
        if not os.path.isfile(self.file_path):
            print("500 服务器数据不存在".encode("utf-8"))
            return False, client_name

        with open(self.file_path, "r") as f:
            data = json.load(f)
            print("client username:", client_name)
            print("client pass:", client_pass)

            print("server username:", data.get('username'))
            print("server pass:", data.get('password'))
            if client_name == data.get('username') and client_pass == data.get('password'):
                self.request.send("200 验证通过".encode("utf-8"))
                # self.current_dir = "/home/%s"% client_name
                return True, client_name
            else:
                self.request.send("400 错误的用户名或密码".encode("utf-8"))
                return False, client_name

    def pwd(self, *args):
        # user_home = "/home/%s"%self.username
        # print("user home : %s"% user_home)
        self.request.send(self.current_dir.encode("utf-8"))

    def ls(self, *args):
        '''查看用户目录文件'''

        with open(self.file_path) as f:
            data = json.load(f)
            print(data)
        file_list = data.get('home').get(self.current_dir)

        #
        # result = os.listdir(self.home_path)
        # result.remove("%s.json"%self.username)
        # result_str = " ".join(result)
        self.request.send(json.dumps(file_list).encode("utf-8"))

    def chkdisk(self, *args):
        '''查看用户磁盘配额'''
        with open(self.file_path, "r") as f:
            data = json.load(f)

        disk_data = {}
        disk_data['total_size'] = data.get('total_size')
        disk_data['used_size'] = data.get('used_size')

        # 返回用户磁盘数据
        self.request.sendall(json.dumps(disk_data).encode('utf-8'))

    def update_user_disk_size(self):
        '''更新用户'''
        total_used_size = 0
        with open(self.file_path) as f:
            data = json.load(f)

        result = os.listdir(self.home_path)
        result.remove("%s.json" % self.username)
        for file in result:
            resource_path = os.path.join(self.home_path, file)
            size = os.stat(resource_path).st_size
            total_used_size += size
        total_used_size_m = int(total_used_size/(1000*1024))
        data['used_size'] = total_used_size_m

        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def check_disk(self, filesize):
        '''检查用户磁盘空间'''
        with open(self.file_path) as f:
            data = json.load(f)

        remain_size = (int(data.get('total_size')) - int(data.get('used_size'))) *1024000

        if remain_size > int(filesize):
            # print("磁盘空间不足")
            return True
        else:
            print("磁盘空间不足")
            return False

    def update_file_to_db(self, filename):
        '''把用户上传的文件更新到数据库'''
        with open(self.file_path) as f:
            data = json.load(f)
        file_list = data.get('home').get(self.current_dir)
        if file_list == None:
            data['home'][self.current_dir] = [filename ,]
        else:
            data['home'][self.current_dir].append(filename)

        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def mkdir(self, *args):
        '''创建目录'''
        print("创建目录")
        cmd_dic = args[0]
        dirname = cmd_dic['dirname']
        # dir_path = os.path.join(self.current_dir, dirname)
        dir_path = self.current_dir + "/" + dirname
        with open(self.file_path) as f:
            data = json.load(f)
        file_list = data.get('home').get(dir_path)
        if file_list == None:
            data['home'][dir_path] = []
            data['home'][self.current_dir].append(dirname)
            self.request.send("200 目录创建成功".encode("utf-8"))
        else:
            self.request.send("400 目录创建失败".encode(("utf-8")))

        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def cd(self, *args):
        '''切换目录'''
        cmd_dic = args[0]
        path = cmd_dic['path']

        with open(self.file_path) as f:
            data = json.load(f)
        dir_list = data.get('home')

        if path == "..":
            if len(self.current_dir.split("/")) == 3:
                self.request.send("400 目录不能回退了".encode("utf-8"))
                return
            else:
                dir_list = self.current_dir.split("/")
                dir_list.pop()
                self.current_dir = "/".join(dir_list)
                self.request.send("200 目录切换成功".encode("utf-8"))
                return


        if not path.startswith("/home"):
            path = self.current_dir + "/" + path

        if path in dir_list:
            self.current_dir = path
            self.request.send("200 目录切换成功".encode("utf-8"))
            return
        else:
            self.request.send("400 目录不存在".encode("utf-8"))
            return














if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 9998), MyTCPHandler)
    server.serve_forever()



