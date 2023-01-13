# 本地部署

> **环境要求**
>
> 安装好最新的 [docker](https://www.docker.com/) 和 [docker-compose](https://docs.docker.com/compose/)。
>
> 安装好最新的 [Git](https://git-scm.com/)。
>
> 保证你的网络能够正常访问 [Github](https://github.com/)。

## 克隆仓库

参考 [克隆仓库](/deploy/server.html#克隆仓库)。

## 配置数据库密码

参考 [配置数据库密码](/deploy/server.html#配置数据库密码)。

随后运行 `docker compose` 的相关命令:

```bash
# 在后台启动猫猫头服务
$ docker compose up -d
```

## 启动服务

完成以上所有配置后，你可以启动服务了。

```bash
$ docker compose up --build -d
# or
$ ./manage.sh up
```

## 查看容器日志

```bash
# 查看服务器日志
$ ./manage.sh logs server

# 查看评测机日志
$ ./manage.sh logs judge
```
