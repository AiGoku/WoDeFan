# 我的饭 - 项目文档

## 项目简介
"我的饭"是一款微信小程序，帮助朋友之间协作点菜，商量吃什么。

## 技术栈
- **前端**：微信小程序原生开发
- **后端**：Python FastAPI
- **数据库**：SQLite（可迁移 PostgreSQL）
- **数据采集**：Python 爬虫

## 目录结构
```
WoDeFan/
├── miniprogram/          # 微信小程序前端
│   ├── pages/
│   │   ├── index/        # 首页（推荐+分类）
│   │   ├── detail/       # 菜品详情
│   │   ├── cart/         # 选菜车/我的菜单
│   │   └── share/        # 打开分享页面
│   ├── utils/api.js      # API 请求封装
│   └── app.js/json/wxss  # 小程序入口
├── backend/              # Python 后端
│   ├── main.py           # FastAPI 入口
│   ├── api/              # API 路由
│   ├── models/           # 数据模型和数据库
│   └── requirements.txt
├── crawler/              # 数据采集
│   ├── main.py           # 爬虫/示例数据生成
│   └── output/           # 采集结果
└── docs/                 # 项目文档
```

## 快速开始

### 1. 启动后端
```bash
cd backend
pip install -r requirements.txt
python main.py
# API 运行在 http://localhost:8000
```

### 2. 导入示例数据
```bash
cd crawler
python main.py --import
```

### 3. 小程序开发
1. 用微信开发者工具打开 `miniprogram/` 目录
2. 在 `utils/api.js` 中修改 `BASE_URL` 为后端地址
3. 编译运行

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/dishes/ | 菜品列表（支持分类、搜索筛选） |
| GET | /api/dishes/categories | 获取分类列表 |
| GET | /api/dishes/{id} | 菜品详情 |
| POST | /api/orders/ | 创建点菜单 |
| GET | /api/orders/{share_code} | 获取点菜单 |
| POST | /api/orders/{share_code}/add | 追加菜品 |

## 数据分类
| key | 名称 |
|-----|------|
| cold_dish | 凉菜 |
| hot_dish | 热菜 |
| soup | 汤羹 |
| staple | 主食 |
| dessert | 甜品小吃 |
| drink | 饮品 |

## 核心流程
1. 用户A打开小程序 → 浏览菜谱 → 选择菜品 → 生成点菜单
2. 用户A分享点菜单给用户B
3. 用户B打开分享 → 查看已选菜品 → 追加自己想吃的 → 再分享给其他人
4. 最终形成一份大家共同的菜单

## 待开发（V2）
- 用户往期点菜记录
- 菜品图片（爬虫采集或手动上传）
- 更丰富的菜谱数据
- 菜品评价/点赞
