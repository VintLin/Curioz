# Curioz - 创业成长论坛

一个基于Django开发的现代化创业成长社区论坛，专注于创业经验分享、成长讨论和问题求助。

## 🚀 项目特性

- **现代化界面** - 响应式设计，支持移动端访问
- **用户系统** - 完整的用户注册、登录、资料管理
- **论坛功能** - 分类管理、主题发布、回复讨论
- **Markdown支持** - 支持Markdown格式的富文本编辑
- **缓存优化** - Redis缓存提升性能
- **Docker支持** - 一键部署，环境隔离
- **国际化** - 中文界面，支持多语言扩展

## 📋 技术栈

- **后端框架**: Django 4.2+
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **缓存**: Redis
- **任务队列**: Celery
- **Web服务器**: Gunicorn
- **静态文件**: WhiteNoise
- **前端**: HTML/CSS/JavaScript + Bootstrap

## 🛠️ 安装和运行

### 方式一：本地开发环境（推荐）

#### 1. 克隆项目
```bash
git clone <repository-url>
cd Curioz
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 环境配置
创建 `.env` 文件（可选）：
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
REDIS_URL=redis://localhost:6379/0
```

#### 5. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. 创建超级用户
```bash
python manage.py createsuperuser
```

#### 7. 初始化论坛数据
```bash
python init_forum_data.py
```

#### 8. 启动Redis服务
```bash
# macOS (使用Homebrew)
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Windows
# 下载Redis for Windows并启动服务
```

#### 9. 启动开发服务器
```bash
python manage.py runserver
```

#### 10. 访问应用
- 论坛首页：http://localhost:8000
- 管理后台：http://localhost:8000/admin

### 方式二：Docker部署

#### 1. 启动所有服务
```bash
docker-compose up --build
```

#### 2. 初始化数据
```bash
docker-compose exec web python init_forum_data.py
```

#### 3. 访问应用
- 论坛首页：http://localhost:8000
- 管理后台：http://localhost:8000/admin

## 📁 项目结构

```
Curioz/
├── accounts/           # 用户账户应用
├── forum/             # 论坛核心应用
├── mysite/            # Django项目配置
├── templates/         # HTML模板
├── static/            # 静态文件
├── media/             # 用户上传文件
├── requirements.txt   # Python依赖
├── docker-compose.yml # Docker配置
├── Dockerfile        # Docker镜像配置
├── init_forum_data.py # 数据初始化脚本
└── README.md         # 项目说明
```

## 🎯 主要功能

### 用户系统
- 用户注册和登录
- 个人资料管理
- 用户头像和签名
- 权限管理

### 论坛功能
- 多级分类管理
- 主题发布和编辑
- 回复和讨论
- 帖子搜索
- 热门主题推荐

### 内容管理
- Markdown富文本编辑
- 图片上传
- 内容审核
- 垃圾信息过滤

### 管理功能
- Django管理后台
- 用户管理
- 内容审核
- 系统设置

## 🔧 配置说明

### 数据库配置
- **开发环境**: SQLite (默认)
- **生产环境**: PostgreSQL (需要修改settings.py)

### 缓存配置
- 使用Redis作为缓存后端
- 支持会话存储
- 提升页面加载速度

### 邮件配置
- 开发环境：控制台输出
- 生产环境：需要配置SMTP服务器

## 🚀 部署指南

### 生产环境部署

1. **环境变量配置**
```bash
export SECRET_KEY=your-production-secret-key
export DEBUG=False
export ALLOWED_HOSTS=your-domain.com
export DATABASE_URL=postgres://user:password@host:port/dbname
export REDIS_URL=redis://host:port/0
```

2. **收集静态文件**
```bash
python manage.py collectstatic --noinput
```

3. **使用Gunicorn启动**
```bash
gunicorn --bind 0.0.0.0:8000 mysite.wsgi:application
```

4. **配置Nginx反向代理**（推荐）

### Docker生产部署
```bash
# 构建生产镜像
docker build -t curioz-forum .

# 运行容器
docker run -d -p 8000:8000 curioz-forum
```

## 📊 默认数据

系统初始化时会创建以下内容：

### 论坛分类
- **创业讨论**: 创业想法、商业模式、融资经验
- **成长分享**: 学习心得、技能提升、职业发展
- **问题求助**: 技术问题、管理问题、法律咨询
- **资源分享**: 工具推荐、书籍推荐、网站资源
- **社区公告**: 论坛公告和规则

### 示例内容
- 欢迎帖子
- 创业想法讨论
- 学习心得分享

### 默认账户
- **管理员**: admin / admin123
- **邮箱**: admin@example.com

## 🔍 开发指南

### 添加新功能
1. 在相应的app中创建模型
2. 运行数据库迁移
3. 创建视图和模板
4. 配置URL路由
5. 添加测试

### 自定义主题
- 修改 `templates/` 目录下的模板
- 更新 `static/` 目录下的CSS文件
- 重启服务器查看效果

### API开发
项目支持RESTful API开发，可以基于现有模型创建API接口。

## 🐛 故障排除

### 常见问题

1. **Redis连接失败**
   - 确保Redis服务正在运行
   - 检查Redis配置和端口

2. **数据库迁移错误**
   - 删除数据库文件重新迁移
   - 检查模型定义

3. **静态文件404**
   - 运行 `python manage.py collectstatic`
   - 检查STATIC_ROOT配置

4. **权限问题**
   - 检查文件权限
   - 确保虚拟环境正确激活

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目主页：[GitHub Repository]
- 问题反馈：[Issues]
- 邮箱：admin@example.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**Curioz** - 让创业成长之路不再孤单 🚀
