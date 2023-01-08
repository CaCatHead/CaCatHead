# 本地部署

> **环境要求**
>
> 安装好最新的 [docker](https://www.docker.com/) 和 [docker-compose](https://docs.docker.com/compose/)。
>
> 安装好最新的 [Git](https://git-scm.com/)。
>
> 保证你的网络能够正常访问 [Github](https://github.com/)。

首先, 你需要克隆本仓库到本地, 并克隆子模块.

```bash
# 克隆本仓库到本地
$ git clone https://github.com/XLoJ/CaCatHead.git

# 进入仓库根目录
$ cd CaCatHead

# 克隆子模块
$ git submodule update --init --recursive
```

在项目根目录创建一个名为 `pass.txt` 的文本文件, 并往里面写入一个随机字符串，这将被设置为你的数据库密码。

随后运行 `docker compose` 的相关命令:

```bash
# 在后台启动猫猫头服务
$ docker compose up -d
```
