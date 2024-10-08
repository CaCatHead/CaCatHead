# 开始

推荐使用 [Docker Compose](https://docs.docker.com/compose/) 一键部署。

## 部署指北

+ 如果你想为 [CaCatHead](https://github.com/CaCatHead/CaCatHead) 贡献代码，或者本地调试代码，请参考 [本地开发](./development.md)，配置本地开发环境；
+ 如果你想在本地部署 [CaCatHead](https://github.com/CaCatHead/CaCatHead)，查看运行效果，请参考 [本地部署](./local.md)，配置数据库密码，使用 [Docker Compose](https://docs.docker.com/compose/) 一键部署；
+ 如果你想在服务器上部署 [CaCatHead](https://github.com/CaCatHead/CaCatHead)，用于生产环境，请参考 [服务器部署](./server.md)，在本地部署的基础上，配置 nginx 和后端服务，使用 [Docker Compose](https://docs.docker.com/compose/) 一键部署；
+ 如果你想为已有的生产环境 [CaCatHead](https://github.com/CaCatHead/CaCatHead) 添加评测机，请参考 [单独部署评测机](./judge.md)，向主服务器管理员询问主机地址和密码等信息并进行相应的配置后，使用 [Docker Compose](https://docs.docker.com/compose/) 一键部署。

## 注意事项

+ 系统的**所有状态** (数据库, 数据库备份, 题目测试数据等) 存储在 `.cacathead` 目录内，请勿随意清除
+ **推荐客户端浏览器版本**：>= Chrome 100
