#!/usr/bin/env python
"""
初始化论坛数据脚本
创建基本的论坛分类和示例内容
"""

import os
import sys
import django
from django.utils.text import slugify

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from forum.models import Category, Topic, Post, UserProfile


def create_categories():
    """创建论坛分类"""
    categories_data = [
        {
            'name': '创业讨论',
            'description': '分享创业经验、讨论创业想法、寻求创业建议',
            'children': [
                {'name': '创业想法', 'description': '分享和讨论各种创业想法'},
                {'name': '商业模式', 'description': '探讨不同的商业模式和盈利方式'},
                {'name': '融资经验', 'description': '分享融资经验和投资相关话题'},
            ]
        },
        {
            'name': '成长分享',
            'description': '个人成长、技能提升、学习心得分享',
            'children': [
                {'name': '学习心得', 'description': '分享学习经验和心得体会'},
                {'name': '技能提升', 'description': '讨论各种技能的学习和提升方法'},
                {'name': '职业发展', 'description': '职业规划和发展经验分享'},
            ]
        },
        {
            'name': '问题求助',
            'description': '遇到问题时寻求帮助和建议',
            'children': [
                {'name': '技术问题', 'description': '技术相关问题求助'},
                {'name': '管理问题', 'description': '团队管理和运营问题'},
                {'name': '法律咨询', 'description': '法律相关问题咨询'},
            ]
        },
        {
            'name': '资源分享',
            'description': '分享有用的资源、工具、书籍等',
            'children': [
                {'name': '工具推荐', 'description': '推荐有用的工具和软件'},
                {'name': '书籍推荐', 'description': '推荐优秀的书籍和学习资料'},
                {'name': '网站资源', 'description': '分享有价值的网站和在线资源'},
            ]
        },
        {
            'name': '社区公告',
            'description': '论坛公告、规则说明、活动通知',
            'children': []
        }
    ]
    
    created_categories = []
    
    for cat_data in categories_data:
        # 创建主分类
        parent_category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': slugify(cat_data['name']),
                'description': cat_data['description'],
                'order': len(created_categories) + 1
            }
        )
        created_categories.append(parent_category)
        
        if created:
            print(f"创建分类: {parent_category.name}")
        
        # 创建子分类
        for i, child_data in enumerate(cat_data['children']):
            base_slug = slugify(child_data['name'])
            slug = base_slug
            counter = 1
            # 确保slug唯一性
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            child_category, created = Category.objects.get_or_create(
                name=child_data['name'],
                defaults={
                    'slug': slug,
                    'description': child_data['description'],
                    'parent': parent_category,
                    'order': i + 1
                }
            )
            
            if created:
                print(f"  创建子分类: {child_category.name}")
    
    return created_categories


def create_sample_content():
    """创建示例内容"""
    # 获取或创建管理员用户
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # 创建管理员的用户资料
    admin_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'bio': '论坛管理员，致力于为大家提供优质的创业成长交流平台。',
            'location': '北京',
            'signature': '一起成长，共同进步！'
        }
    )
    
    # 获取分类
    announcement_category = Category.objects.filter(name='社区公告').first()
    startup_category = Category.objects.filter(name='创业想法').first()
    growth_category = Category.objects.filter(name='学习心得').first()
    
    if not all([announcement_category, startup_category, growth_category]):
        print("请先创建分类")
        return
    
    # 创建示例主题
    sample_topics = [
        {
            'title': '欢迎来到创业成长论坛！',
            'content': '''欢迎大家来到创业成长论坛！

这里是一个专注于创业成长、经验分享和问题讨论的社区。我们希望通过这个平台，让更多有创业梦想和成长需求的朋友能够：

🚀 **分享创业经验** - 无论是成功的经验还是失败的教训，都是宝贵的财富
💡 **讨论创业想法** - 头脑风暴，碰撞出更多创新的火花
🤝 **互相帮助** - 遇到问题时，大家一起想办法解决
📚 **共同学习** - 分享学习资源，一起进步成长

## 论坛规则
1. 保持友善和尊重
2. 分享有价值的内容
3. 禁止广告和垃圾信息
4. 鼓励原创和深度思考

期待大家的积极参与，让我们一起打造一个优质的创业成长社区！''',
            'category': announcement_category,
            'topic_type': 'announcement'
        },
        {
            'title': '分享一个SaaS创业想法：在线协作工具',
            'content': '''最近在思考一个SaaS产品的想法，想和大家讨论一下可行性。

## 产品概念
一个专门为小团队设计的在线协作工具，主要功能包括：
- 项目管理和任务分配
- 实时文档协作
- 视频会议集成
- 简单的CRM功能

## 目标用户
- 5-20人的小团队
- 远程工作团队
- 创业公司
- 自由职业者组合

## 竞争优势
- 界面简洁，学习成本低
- 价格亲民，适合小团队预算
- 功能专注，不做大而全

大家觉得这个想法怎么样？市场上已经有很多类似产品了，还有机会吗？''',
            'category': startup_category,
            'topic_type': 'discussion'
        },
        {
            'title': '我的编程学习心得：从零基础到独立开发',
            'content': '''想和大家分享一下我的编程学习经历，希望能对正在学习的朋友有所帮助。

## 我的背景
- 非计算机专业出身
- 工作3年后决定转行
- 目标是成为全栈开发者

## 学习路径
### 第一阶段：基础语言（3个月）
- 选择Python作为入门语言
- 每天2小时，周末4小时
- 主要资源：廖雪峰教程 + LeetCode简单题

### 第二阶段：Web开发（6个月）
- 学习HTML/CSS/JavaScript
- 掌握Django框架
- 完成3个小项目

### 第三阶段：深入实践（持续进行）
- 参与开源项目
- 自己开发小工具
- 不断学习新技术

## 关键心得
1. **持续性比强度更重要** - 每天学一点比周末突击效果好
2. **项目驱动学习** - 带着目标学习更有动力
3. **加入社区** - 和其他学习者交流很重要
4. **不要完美主义** - 先做出来，再优化

现在我已经能够独立开发Web应用了，正在准备自己的SaaS产品。

大家在学习过程中有什么困惑吗？欢迎交流！''',
            'category': growth_category,
            'topic_type': 'sharing'
        }
    ]
    
    for topic_data in sample_topics:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            defaults={
                'slug': slugify(topic_data['title']),
                'content': topic_data['content'],
                'category': topic_data['category'],
                'author': admin_user,
                'topic_type': topic_data['topic_type'],
                'last_post_by': admin_user
            }
        )
        
        if created:
            print(f"创建主题: {topic.title}")
            
            # 创建第一个帖子
            Post.objects.get_or_create(
                topic=topic,
                author=admin_user,
                defaults={'content': topic_data['content']}
            )


def main():
    print("开始初始化论坛数据...")
    
    print("\n1. 创建论坛分类...")
    create_categories()
    
    print("\n2. 创建示例内容...")
    create_sample_content()
    
    print("\n✅ 论坛数据初始化完成！")
    print("\n现在你可以：")
    print("1. 访问 http://localhost:8000 查看论坛首页")
    print("2. 使用 admin/admin123 登录管理后台")
    print("3. 访问 http://localhost:8000/admin 进入Django管理后台")


if __name__ == '__main__':
    main()
