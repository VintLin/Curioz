#!/usr/bin/env python
"""
简单的论坛设置脚本
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from forum.models import Category, UserProfile
from django.utils.text import slugify


def setup_forum():
    print("🚀 开始设置创业成长论坛...")
    
    # 确保管理员用户存在
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ 创建管理员账户: admin/admin123")
    else:
        print("✅ 管理员账户已存在")
    
    # 创建管理员资料
    profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'bio': '论坛管理员，致力于为大家提供优质的创业成长交流平台。',
            'location': '北京',
            'signature': '一起成长，共同进步！'
        }
    )
    
    if created:
        print("✅ 创建管理员资料")
    
    # 创建基础分类（只有在没有分类时才创建）
    if Category.objects.count() == 0:
        categories = [
            ('创业讨论', '分享创业经验、讨论创业想法、寻求创业建议'),
            ('成长分享', '个人成长、技能提升、学习心得分享'),
            ('问题求助', '遇到问题时寻求帮助和建议'),
            ('资源分享', '分享有用的资源、工具、书籍等'),
            ('社区公告', '论坛公告、规则说明、活动通知'),
        ]
        
        for i, (name, desc) in enumerate(categories):
            Category.objects.create(
                name=name,
                slug=slugify(name),
                description=desc,
                order=i + 1
            )
            print(f"✅ 创建分类: {name}")
    else:
        print("✅ 论坛分类已存在")
    
    print("\n🎉 论坛设置完成！")
    print("\n📋 使用指南:")
    print("1. 访问 http://localhost:8000 查看论坛首页")
    print("2. 使用 admin/admin123 登录管理账户")
    print("3. 访问 http://localhost:8000/admin 进入Django管理后台")
    print("4. 在管理后台可以管理分类、主题和用户")
    print("\n🔧 开发相关:")
    print("- 源码位置: /Users/haolong/PycharmProjects/论坛")
    print("- 数据库: SQLite (db.sqlite3)")
    print("- 虚拟环境: venv/")


if __name__ == '__main__':
    setup_forum()
