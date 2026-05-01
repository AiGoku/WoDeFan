# 我的饭 (WoDeFan)

一款微信小程序，帮助朋友之间协作点菜，商量吃什么。

## 功能介绍

- **浏览菜谱**：按分类（凉菜、热菜、汤羹、主食、甜品小吃、饮品）浏览，支持当季推荐
- **选菜下单**：选择喜欢的菜加入菜单，查看总价（纯展示，无支付）
- **协作点菜**：将菜单分享给微信好友，好友可以追加自己想吃的菜
- **仪式感**：菜品带标价，模拟饭店点菜体验

## 核心流程

```
用户A → 浏览菜谱 → 选菜 → 生成点菜单 → 分享给用户B
用户B → 打开分享 → 查看已选菜品 → 追加自己想吃的 → 再分享给其他人
```

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | 微信小程序原生开发 |
| 后端 | Python FastAPI |
| 数据库 | SQLite |
| 数据采集 | Python 脚本 |

## 项目结构

```
WoDeFan/
├── miniprogram/              # 微信小程序前端
│   ├── pages/
│   │   ├── index/            # 首页（当季推荐 + 分类浏览）
│   │   ├── detail/           # 菜品详情
│   │   ├── cart/             # 选菜车 / 我的菜单
│   │   └── share/            # 打开分享页面
│   ├── components/           # 公共组件
│   ├── utils/api.js          # 后端 API 封装
│   ├── assets/               # 图标素材
│   └── app.js / app.json / app.wxss
│
├── backend/                  # Python 后端
│   ├── api/
│   │   ├── dishes.py         # 菜品 API
│   │   └── orders.py         # 点菜单 API
│   ├── models/
│   │   ├── database.py       # 数据库连接与初始化
│   │   └── schemas.py        # 数据模型
│   ├── main.py               # FastAPI 入口
│   └── requirements.txt
│
├── crawler/                  # 数据采集
│   ├── main.py               # 示例数据生成 + 数据库导入
│   └── requirements.txt
│
├── scripts/
│   └── generate_icons.py     # 图标素材生成脚本
│
└── docs/
    └── PROJECT.md            # 项目详细文档
```

## 快速开始

### 环境要求

- Python 3.10+
- 微信开发者工具

### 1. 启动后端服务

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务（默认运行在 http://localhost:8000）
python main.py
```

启动后可访问 http://localhost:8000 查看 API 文档（FastAPI 自动生成的 Swagger UI）。

### 2. 导入示例菜品数据

```bash
# 新开一个终端
cd crawler

# 安装依赖
pip install -r requirements.txt

# 生成示例数据并导入数据库
python main.py --import
```

这会生成 35 道示例菜品（涵盖 6 个分类）并写入 SQLite 数据库。

### 3. 运行小程序

1. 打开 **微信开发者工具**
2. 导入项目，选择 `miniprogram/` 目录
3. 修改 `miniprogram/utils/api.js` 中的 `BASE_URL` 为你的后端地址：

```javascript
// 本地开发时
const BASE_URL = 'http://localhost:8000';

// 部署后改为实际地址
const BASE_URL = 'https://your-server.com';
```

4. 编译运行

### 4. 生成图标素材（可选）

```bash
python scripts/generate_icons.py
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/dishes/` | 菜品列表，支持 `?category=&keyword=&season=` 筛选 |
| `GET` | `/api/dishes/categories` | 获取所有分类 |
| `GET` | `/api/dishes/{id}` | 菜品详情 |
| `POST` | `/api/orders/` | 创建点菜单 |
| `GET` | `/api/orders/{share_code}` | 根据分享码获取点菜单 |
| `POST` | `/api/orders/{share_code}/add` | 向点菜单追加菜品 |
| `DELETE` | `/api/orders/{share_code}/items/{item_id}` | 从点菜单移除菜品 |

## 菜品分类

| Key | 名称 |
|-----|------|
| `cold_dish` | 凉菜 |
| `hot_dish` | 热菜 |
| `soup` | 汤羹 |
| `staple` | 主食 |
| `dessert` | 甜品小吃 |
| `drink` | 饮品 |

## 部署说明

### 后端部署

推荐使用以下方式部署 Python 后端：

- **Gunicorn + Nginx**（传统服务器）
- **Docker** 容器化部署
- **云函数**（Serverless）

部署时需要：
1. 将 SQLite 替换为 PostgreSQL（生产环境推荐）
2. 配置 CORS 允许小程序域名
3. 使用 HTTPS（小程序要求）

### 小程序发布

1. 在微信公众平台注册小程序账号
2. 配置服务器域名（request 合法域名）
3. 在微信开发者工具中上传代码
4. 提交审核

## 后续计划 (V2)

- [ ] 用户往期点菜记录
- [ ] 更丰富的菜谱数据（爬虫采集）
- [ ] 菜品图片上传
- [ ] 菜品评价 / 点赞
- [ ] 菜单收藏功能

## License

MIT
