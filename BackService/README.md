# 运行说明
    1.运行nginx
        /usr/local/nginx/sbin/nginx
    2.进入后端目录 运行
    nohup python3 manage.py runserver 0.0.0.0:9090 > /home/lipenglo/workPro/ATP3/log/manage.log 2>&1 &
    nohup celery -A BackService worker -l info > /home/lipenglo/workPro/ATP3/log/celery_worker.log 2>&1 &
    nohup celery -A BackService beat -l info > /home/lipenglo/workPro/ATP3/log/celery_beat.log 2>&1 &

# Centos7部署说明
## 环境安装
### 环境注意
    一定要使用Django==2.0.7 和 dwebsocket==0.4.2 这个版本 --- 不然会报错

### 1.安装python37环境
    1.将部署文件中的 Python-3.7.0.tar.xz 上传到服务器中
    2.tar -xvJf  Python-3.7.0.tar.xz
    3.编译安装
        mkdir /usr/local/python3
        cd Python-3.7.0
        /configure --prefix=/usr/local/python3
        make && make install
    4.创建软连接
        ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
        ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
    5.测试
        python3 -V
        pip3 -V

### 2.安装Python依赖
    1.进入后端项目根目录
    2.pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-dependencies
    3.如遇报错请看下面环境安装错误提示

### 3.安装docker
    1.sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    2.sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    3.sudo yum install docker-ce docker-ce-cli containerd.io
    如果安装失败，需要进行升级包 yum -y update
    4.开启docker服务 systemctl start docker

### 4.创建docker内网
    1.docker network create --driver bridge --subnet=172.16.12.0/16 --gateway=172.16.12.1 mynetwork

### 5.安装 mysql 如有Mysql可跳过安装
    1.docker pull mysql:5.7.27
    2. 生成容器
    docker run -p 3306:3306 --restart=always --name mysql --network=mynetwork --ip 172.16.12.2 -v /home/docker/mysql/conf.d:/etc/mysql/conf.d -v /home/docker/mysql/my.cnf:/etc/my.cnf -v /home/docker/mysql/logs:/logs -v /home/docker/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=Hbwj@123 -d mysql:5.7.27
    3.开放端口
    firewall-cmd --zone=public --add-port=3306/tcp --permanent
    firewall-cmd --reload
    4.将环境目录下的sql导入到新增库中
    
    配置参数
    1.进入后端根目录
    2.将 _DataFiles/Setup/AutoTesting_v3.sql 文件导入到Mysql库中
    3.vim文件 BackService/settings.py
    4.修改 DATABASES参数:填写新增的数据库名称、IP、用户、密码。 用户密码默认为 root Hbwj@123

### 6.安装RabbitMQ 如有可跳过安装，但需要进入管理台中配置
    1.docker pull rabbitmq:3.6.6-management
    2.生成容器
    docker run -d --restart=always --name rabbitmq --network=mynetwork --ip 172.16.12.4 -p 5672:5672 -p 15672:15672 -v /home/rabbitmq/data:/var/lib/rabbitmq --hostname myRabbit -e RABBITMQ_DEFAULT_VHOST=/  -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq:3.6.6-management
    3.开发端口
    firewall-cmd --zone=public --add-port=15672/tcp --permanent
    firewall-cmd --reload
    4.访问 http://Server-IP:15672 用户密码都是admin

    配置参数：
    1.点击Queues
    2.点击Add a new queue
    3.Name中填写 celery 后点击添加
    4.回到后端根目录 vim文件 BackService/settings.py
    5.修改BROKER_URL amqp://用户名:密码@MQ的IP地址:5672

### 7.安装Redis 如已安装可跳过安装，但需要配置参数
    1.docker pull redis:3.2.12
    2.生成容器
    docker run -p 6379:6379 --restart=always --name redis --network=mynetwork --ip 172.16.12.3 -v /home/redis/redis.conf:/etc/redis/redis.conf -v /home/redis/data:/data -d redis:3.2.12 redis-server /etc/redis/redis.conf --appendonly yes --requirepass "Hbwj@123"
    
    配置参数：
    1.回到后端根目录 vim文件 BackService/settings.py
    2.修改 CACHES下的LOCATION为redis宿主机的IP地址也就是docker安装在哪台服务器上的地址
    3.PASSWORD 默认可不改

### 8.启动后台
    # 开放端口
    firewall-cmd --zone=public --add-port=9090/tcp --permanent
    firewall-cmd --reload

    分别运行以下命令运行成功后用，使用 ctrl+c 可返回 
    1.进入后台项目根目录
    python3 -u manage.py runserver 0.0.0.0:9090
    celery -A BackService worker -l info
    celery -A BackService beat -l info
    
    当提示未找到celery命令时，执行下面2行命令:
    export PATH=/usr/local/python3/bin:$PATH
    echo 'export PATH=/usr/local/python3/bin:$PATH' >> /etc/profile.d/python3.sh

    2.如果3个都没有问题时就可以使用以下命令后台启动：LOG地址可以根据自己修改保存
    nohup python3 manage.py runserver 0.0.0.0:9090 > /home/lipenglo/workPro/ATP3/log/manage.log 2>&1 &
    nohup celery -A BackService worker -l info > /home/lipenglo/workPro/ATP3/log/celery_worker.log 2>&1 &
    nohup celery -A BackService beat -l info > /home/lipenglo/workPro/ATP3/log/celery_beat.log 2>&1 &

# 环境安装错误处理：
## 安装mysqlcen错误处理
    yum install mysql-devel gcc gcc-devel python-devel
    pip3 install mysqlclient

    mac 环境 
    https://blog.csdn.net/m0_47970692/article/details/114106262

## Could not find a version that satisfies the requirement numpy==1.13.3
    pip3 install --upgrade pip

# 平台说明
## 接口维护
    1.接口中的前置操作,会在接口运行前运行
    2.接口中的后置操作,只会在接口运行完成后进行!

## 用例维护
    1.在执行用例时,如有引用{{变量}} 这种操作时,会存在优先级的引用顺序，在用例中优先查找当前用例提取的值,如果没有才会去全局变量中查找！
    2.历史恢复时,如当前用例中有上传类文件时，并不会恢复此文件!