#!/bin/bash

echo "创业成长论坛启动脚本"
echo "====================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查数据库连接
echo "检查数据库连接..."
python manage.py check

# 运行迁移
echo "运行数据库迁移..."
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 创建超级用户 (如果需要)
echo "如果需要创建管理员账户，请运行: python manage.py createsuperuser"

# 启动开发服务器
echo "启动论坛服务器..."
echo "访问地址: http://localhost:8000"
python manage.py runserver
