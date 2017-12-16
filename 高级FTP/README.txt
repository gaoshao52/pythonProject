开发者：高绍阳
时间：2017年11月20日
邮箱：287586479@qq.com

需求：
    高级FTP服务器开发：
        1. 用户加密认证
        2. 多用户同时登陆
        3. 每个用户有自己的家目录且只能访问自己的家目录
        4. 对用户进行磁盘配额、不同用户配额可不同
        5. 用户可以登陆server后，可切换目录
        6. 查看当前目录下文件
        7. 上传下载文件，保证文件一致性
        8. 传输过程中现实进度条
        9. 支持断点续传

目录结构：
简单FTP
│  README.txt
│
├─ftp_client
│  │  __init__.py
│  │
│  ├─bin
│  │      startup.py
│  │
│  └─libs
│      │  FtpClient.py
│      │  progressBar.py
│      │
│      └─__pycache__
│              FtpClient.cpython-36.pyc
│              progressBar.cpython-36.pyc
│
└─ftp_server
    │  __init__.py
    │
    ├─bin
    │      startup.py
    │
    ├─database
    │  │  __init__.py
    │  │
    │  ├─gaosy
    │  │      gaosy.json
    │  │
    │  └─sam
    │          sam.json
    │
    └─libs
        │  FtpServer.py
        │
        └─__pycache__
                FtpServer.cpython-36.pyc


使用：
    客户端： ftp_client/bin  目录下 python startup.py
    服务器端： ftp_server/bin  目录下  python startup.py

客户登陆：需使用用户名和密码

客户命令：
    ls  # 查看当前目录文件
    pwd  # 查看当前路径
    get filename  #下载文件
    put filename   # 上传文件
    chkdisk   # 查看用户磁盘配额
    mkdir  # 创建目录
    cd path # 切换目录

