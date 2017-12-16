开发者：高绍阳
时间：2017年11月16日
邮箱：287586479@qq.com

需求：
    开发简单的FTP：
    1. 用户登陆
    2. 上传/下载文件
    3. 不同用户家目录不同
    4. 查看当前目录下文件
    5. 充分使用面向对象知识

目录结构：
简单FTP
    │  README.txt
    │
    ├─ftp_client
    │  │  __init__.py
    │  │
    │  ├─bin
    │  │      startup.py   # 客户端启动接口
    │  │      atm.zip
    │  │
    │  └─libs
    │          FtpClient.py
    │
    └─ftp_server
        │  __init__.py
        │
        ├─bin
        │      startup.py   # 服务器端启动接口
        │
        ├─database
        │  │  __init__.py
        │  │
        │  ├─gaosy  # 用户家目录
        │  │      atm_gaosy.zip  #服务器端用户文件
        │  │      gaosy.json
        │  │
        │  └─sam    # 用户家目录
        │          atm_sam.zip   #服务器端用户文件
        │          sam.json
        │
        └─libs
                FtpServer.py


使用：
    客户端： ftp_client/bin  目录下 python startup.py
    服务器端： ftp_server/bin  目录下  python startup.py

客户登陆：需使用用户名和密码

客户命令：
   ls 查看用户目录下文件
   pwd  查看用户路径
   get filename 下载文件
   put filename 上传文件

