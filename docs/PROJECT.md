# 我的饭 - 项目文档

## 项目简介
"我的饭"是一款微信小程序，帮助朋友之间协作点菜，商量吃什么。

## 技术栈
- **前端**：微信小程序原生开发
- **后端**：微信云开发（云函数 + 云数据库）
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
│   ├── utils/api.js      # 云函数调用封装
│   └── app.js/json/wxss  # 小程序入口
├── cloudfunctions/       # 微信云函数
│   ├── getCategories/    # 获取分类列表
│   ├── getDishes/        # 菜品列表（支持筛选）
│   ├── getDishById/      # 菜品详情
│   ├── createOrder/      # 创建点菜单
│   ├── getOrder/         # 获取点菜单
│   ├── addDishToOrder/   # 追加菜品到点菜单
│   └── initDatabase/     # 初始化示例数据（一次性）
├── backend/              # Python 后端（已废弃，保留参考）
├── crawler/              # 数据采集
│   ├── main.py           # 爬虫/示例数据生成
│   └── output/           # 采集结果
└── docs/                 # 项目文档
```

## 快速开始

### 1. 配置云开发环境
1. 在微信公众平台注册小程序，开通云开发
2. 创建云开发环境，获取环境 ID
3. 在 `miniprogram/app.js` 中将 `your-env-id` 替换为你的环境 ID

### 2. 部署云函数
1. 用微信开发者工具打开项目根目录
2. 右键 `cloudfunctions/initDatabase` → 上传并部署（云端安装依赖）
3. 右键其他云函数 → 上传并部署
4. 在云开发控制台调用 `initDatabase` 初始化示例数据

### 3. 创建云数据库集合
在云开发控制台创建以下集合：
- `dishes` — 菜品数据
- `orders` — 点菜单数据

### 4. 小程序开发
1. 微信开发者工具编译运行
2. 所有 API 调用自动走云函数，无需配置服务器地址

## 云函数接口

| 云函数 | 参数 | 说明 |
|--------|------|------|
| getCategories | 无 | 分类列表 |
| getDishes | category, season, keyword | 菜品列表 |
| getDishById | id | 菜品详情 |
| createOrder | dish_ids[] | 创建点菜单（自动获取 openid） |
| getOrder | share_code | 获取点菜单 |
| addDishToOrder | share_code, dish_id | 追加菜品（自动获取 openid） |
| initDatabase | 无 | 初始化示例数据（幂等） |

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
