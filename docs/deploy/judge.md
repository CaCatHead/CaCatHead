# 单独部署评测机

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

> **注意**
>
> 此时你部署的评测机，应该使用**与主服务器相同的密码配置**。
>
> 你应该自己知道密码是什么，或者向服务器管理员索要密码。

## 配置服务器设置

使用文本编辑器打开 [./deploy/judge/cacathead.yml](https://github.com/CaCatHead/CaCatHead/blob/main/deploy/judge/cacathead.yml)。

```bash
$ vim ./deploy/judge/cacathead.yml
# or vi, code, and so on
```

首先，修改你的评测机名称 `judge.name`，你需要**保证集群内所有评测机的名称互不相同**。

然后，修改使用使用的主服务器 RabbitMQ 的 Exchange 和队列名称配置，对应 `judge.broadcast.*` 和 `judge.queue.*`，这些配置应该**与主服务器的配置相同**（以下为生产环境默认配置）。例如：

```yaml
# ...
judge:
  name: <替换为你的评测节点名称>
  tasks: 1  # worker_max_tasks_per_child
  broadcast:
    ping: ping
    polygon: broadcast.polygon
  queue:
    repository: judge.repository
    contest: judge.contest
    polygon: judge.polygon
  checker:
    root: /root/checkers
# ...
```

然后，修改所有的数据库，MinIO，Redis，和 RabbitMQ 使用主机地址和端口号。你应该自己知道这些服务的具体主机地址和端口，或者向服务器管理员索要。

+ MinIO：主机地址 `testcase.minio.host`，端口 `testcase.minio.port`
+ Postgresql 数据库：主机地址 `database.host`，端口 `database.port`
+ Redis：主机地址 `redis.host`，端口 `redis.port`（暂未使用）
+ RabbitMQ：主机地址 `rabbitmq.host`，端口 `rabbitmq.port`

```yaml
testcase:
  root: /root/testcases
  minio:
    host: localhost
    port: '9000'
    username: root
    password: !ENV ${MINIO_PASS}
    bucket: testcase

database:
  engine: postgresql
  name: cacathead
  host: localhost
  port: '5432'
  username: root
  password: !ENV ${DB_PASS}

redis:
  host: localhost
  port: '6379'
  password: !ENV ${REDIS_PASS}

rabbitmq:
  host: localhost
  port: '5672'
  username: root
  password: !ENV ${RMQ_PASS}
```

## 启动评测机容器

完成以上所有配置后，你可以评测机容器了。

```bash
$ ./manage.sh judge up
```

## 查看评测机容器日志

```bash
$ ./manage.sh judge logs
```

## 常见问题

**先检查评测机容器内的日志**。

### Postgresql / MinIO / RabbitMQ 连接失败

检查是否正确按照 [配置数据库密码](/deploy/server.html#配置数据库密码) 内的说明，配置 4 个中间件密码。

检查密码文件的文件编码（UTF-8），是否只包含密码内容（不包含额外的换行符等）。

向主服务器管理员确认，服务是否允许外部访问，是否开启了相关端口。

### CaCatHead.config 解析失败

检查 [./deploy/judge/cacathead.yml](https://github.com/CaCatHead/CaCatHead/blob/main/deploy/judge/cacathead.yml) 是否为合法的 yml 格式文件。检查 field 名称是否正确，缩进是否正确，是否缺失某些配置。也可能因为 `git pull` (`git merge`) 遇到冲突，导致格式损坏。
