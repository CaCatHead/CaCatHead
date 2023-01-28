# 服务器部署

> **环境要求**
>
> 安装好最新的 [docker](https://www.docker.com/) 和 [docker-compose](https://docs.docker.com/compose/)。
>
> 安装好最新的 [Git](https://git-scm.com/)。
>
> 保证你的网络能够正常访问 [Github](https://github.com/)。

## 克隆仓库

假设你现在什么都没有做，比如你现在可能位于服务器的 Home 目录下。

首先, 你需要克隆本仓库到本地, 并克隆子模块.

```bash
# 克隆本仓库到本地
$ git clone https://github.com/CaCatHead/CaCatHead.git --depth 1

# 进入仓库根目录
$ cd CaCatHead

# 克隆子模块
$ git submodule update --init --recursive
```

## 配置数据库密码

部署环境使用的数据库的密码存储在 [./deploy/password/](https://github.com/CaCatHead/CaCatHead/tree/main/deploy/password) 目录下。

包含 4 个密码文件：

+ `db_pass.txt`：Postgresql 数据库密码；
+ `redis_pass.txt`：Redis 密码（暂时未使用）；
+ `minio_pass.txt`：MinIO 密码；
+ `rmq_pass.txt`：RabbitMQ 密码。

创建密码文件示例（生产环境中请使用足够强度的密码）：

```bash
echo "12345678" > ./deploy/password/db_pass.txt
echo "12345678" > ./deploy/password/redis_pass.txt
echo "12345678" > ./deploy/password/minio_pass.txt
echo "12345678" > ./deploy/password/rmq_pass.txt
```

然后，对于 RabbitMQ 还需要单独配置其密码，创建一个 `./deploy/rabbitmq.conf` 文件。这个配置文件用于启动 RabbitMQ 服务的容器，如果你是单独部署评测节点，不需要配置 `./deploy/rabbitmq.conf`。

**注意**：密码需要与 `./deploy/password/rmq_pass.txt` 里的内容**相同**。

```bash
echo "default_user = root" >> ./deploy/rabbitmq.conf
echo "default_pass = $(cat ./deploy/password/rmq_pass.txt)" >> ./deploy/rabbitmq.conf
```

> **注意**
>
> 不要在 Windows 上的 PowerShell 中运行以上的 `echo` 指令，因为 PowerShell 默认使用 UTF-16 编码，可能会导致问题出现。
>
> 建议使用一些文本编辑器创建这些密码文件。

## 配置 nginx

使用文本编辑器打开 [./deploy/nginx/sites-enabled/cacathead.conf](https://github.com/CaCatHead/CaCatHead/blob/main/deploy/nginx/sites-enabled/cacathead.conf)。

```bash
$ vim ./deploy/nginx/sites-enabled/cacathead.conf
# or vi, code, and so on
```

你可以看到以下配置：

```nginx
server {
    listen              80;
    listen              [::]:80;
    server_name         <server domain>;
    # listen              443 ssl http2;
    # listen              [::]:443 ssl http2;
    # server_name         <server domain>;
    # ...
}
```

如果你使用的是 HTTP，你只需要将 `<server domain>` 替换为你的网站域名。例如：

```nginx
server {
    listen              80;
    listen              [::]:80;
    server_name         cacathead.cn;
    # ...
}
```

如果你使用的是 HTTPS，你需要使用下面注释的配置，并将 `<server domain>` 替换为你的网站域名，并取消下面的 SSL 证书位置配置的注释。例如：

```nginx
server {
    listen              443 ssl http2;
    listen              [::]:443 ssl http2;
    server_name         cacathead.cn;
    # ...
    # SSL
    ssl_certificate     /root/cert/ssl.pem;
    ssl_certificate_key /root/cert/ssl.key;
    # ...
}
```

除此以外，你还需要在 [./deploy/nginx/cert](https://github.com/CaCatHead/CaCatHead/blob/main/deploy/nginx/cert) 目录下，创建 SSL 证书文件 `ssl.key` 和 `ssl.pem`。

## 配置服务器设置

使用文本编辑器打开 [./deploy/server/cacathead.yml](https://github.com/CaCatHead/CaCatHead/blob/main/deploy/server/cacathead.yml)。

```bash
$ vim ./deploy/server/cacathead.yml
# or vi, code, and so on
```

将你的服务器域名填写到 `server.allowed_host` 和 `server.trusted_origin` 下，例如：

```yaml
server:
  allowed_host:
    - '127.0.0.1'
    - server  # This is docker-compose service name, and is used for nginx
    - cacathead.cn  # Config your domain here
  trusted_origin:
    - http://127.0.0.1
    - https://cacathead.cn  # Config your domain here
  # ...
```

## 启动服务

完成以上所有配置后，你可以启动服务了。

```bash
$ ./manage.sh up
```

## 查看容器日志

```bash
# 查看服务器日志
$ ./manage.sh logs server

# 查看评测机日志
$ ./manage.sh logs judge
```
