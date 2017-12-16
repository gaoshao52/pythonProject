开发者：高绍阳
时间：2017年11月22日
邮箱：287586479@qq.com

需求：
    SELECT版FTP:
        1. 使用SELECT或SELECTORS模块实现并发简单版FTP
        2. 允许多用户并发上传下载文件

目录结构：
│  README.txt
│
├─ftp_client
│  ├─bin
│  │      startup.py
│  │
│  └─libs
│      │  client_ftp.py
│      │
│      └─__pycache__
│              client_ftp.cpython-36.pyc
│
└─server_ftp
    ├─bin
    │      startup.py
    │
    └─libs
        │  server_ftp.py
        │
        └─__pycache__
                server_ftp.cpython-36.pyc


使用：
    客户端： ftp_client/bin  目录下 python startup.py
    服务器端： ftp_server/bin  目录下  python startup.py


客户命令：
   get filename 下载文件
   put filename 上传文件