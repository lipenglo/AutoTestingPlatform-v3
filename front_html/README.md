# 部署说明：本系统需要自己修改store/index.js文件中的 3个IP地址的配置后在npm run build  生成的dist文件夹下的文件请复制到 部署文件的manage下，复制前请删除原manage下的文件
## Centos 部署VUE
### 1.安装 node、npm模块
    # 下载
    wget https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz

    # 解压
    xz -d node-v10.16.0-linux-x64.tar.xz
    tar -xvf node-v10.16.0-linux-x64.tar -C /usr/local

    # 进入目录
    cd /usr/local/node-v10.16.0-linux-x64/

    # 创建软连接
    ln -s /usr/local/node-v10.16.0-linux-x64/bin/node /usr/local/bin/node
    ln -s /usr/local/node-v10.16.0-linux-x64/bin/npm /usr/local/bin/npm

    # 测试
    node -v
    npm -v

    # 配置taobao镜像
    npm config set registry https://registry.npm.taobao.org

### 2.安装pm2
    1.npm install pm2 -g
    2.sudo ln -s /usr/local/node-v10.16.0-linux-x64/bin/pm2 /usr/local/bin/pm2

    其他命令
    pm2 show 0（id）//查看某个启动的应用详情
    pm2 show list//查看当前启动的所有应用
    pm2 stop 0(id)//关闭某个应用

### 3.修改前端文件
    1.进入front_html目录中
    2.app.js中可以最后一行可以修改启动端口
    3.运行 npm install 
    4.如果报错 chromedriver@2.46.0 install: `node install.js`
        运行 npm install --ignore-scripts
        然后在执行一次  npm install

    5.启动项目：pm2 start app.js
    6.开放自己设置的前端端口，默认是9091
        firewall-cmd --zone=public --add-port=9091/tcp --permanent
        firewall-cmd --reload

    7.访问站点 http://ip:9091 初始用户 admin hbwj@123

    

### 安装Nginx
    https://www.jianshu.com/p/7a37e03b2107

    重点：一般修改完nginx配制文件都需要对修改后的配制进行check
    [root@cat sbin]$ /usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf

    启动 /usr/local/nginx/sbin/nginx
    重启 /usr/local/nginx/sbin/nginx -s reload

    注意 上面这个安装时第6步，安装后文件会在/usr/local/nginx 

    开启端口
    firewall-cmd --zone=public --add-port=9092/tcp --permanent
    firewall-cmd --reload
