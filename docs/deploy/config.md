# 其它配置

## 前端应用

见 `deploy/app/cacathead.json`。

```json
{
  "title": "CaCatHead",
  "description": "CaCatHead 是一个开源的在线评测系统，目前仍在开发过程中。",
  "images": {
    "logo": "/favicon.png",
    "announcement": "/ccpc.png"
  },
  "home": {
    "rating": true,
    "recentPost": true,
    "recentContest": true
  }
}
```

静态资源存放在 `deploy/app/public/` 目录内，你可以将自定义的图片文件放入此目录，并修改上面配置文件的图片名称，以切换图标等图片。
