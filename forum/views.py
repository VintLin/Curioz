from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F, Count
from django.utils.text import slugify
from django.utils import timezone
from .models import Category, Topic, Post, UserProfile
from .forms import TopicForm, PostForm


def forum_index(request):
    """Forum homepage showing categories and recent topics"""
    categories = Category.objects.filter(is_active=True, parent=None).order_by('order')
    
    # 最新主题
    recent_topics = Topic.objects.filter(is_active=True).select_related('author', 'category', 'last_post_by').order_by('-created_at')[:10]
    
    # 热门主题 - 基于浏览量和回复数的综合排序
    trending_topics = Topic.objects.filter(is_active=True).select_related('author', 'category', 'last_post_by').annotate(
        reply_count_db=Count('posts', filter=Q(posts__is_active=True)) - 1,  # 减去第一个帖子
        popularity_score=F('views') + F('reply_count_db') * 3  # 回复权重更高
    ).order_by('-popularity_score', '-created_at')[:10]
    
    # Forum statistics
    total_topics = Topic.objects.filter(is_active=True).count()
    total_posts = Post.objects.filter(is_active=True).count()
    total_users = UserProfile.objects.count()
    
    context = {
        'categories': categories,
        'recent_topics': recent_topics,
        'trending_topics': trending_topics,
        'total_topics': total_topics,
        'total_posts': total_posts,
        'total_users': total_users,
    }
    return render(request, 'forum/index.html', context)


def category_detail(request, slug):
    """Category detail page showing topics"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    topics_list = Topic.objects.filter(category=category, is_active=True).select_related('author', 'last_post_by')
    
    # Pagination
    paginator = Paginator(topics_list, 20)
    page_number = request.GET.get('page')
    topics = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'topics': topics,
        'all_categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'forum/category_detail.html', context)


def topic_detail(request, slug):
    """Topic detail page showing posts"""
    topic = get_object_or_404(Topic, slug=slug, is_active=True)
    
    # Increment view count
    Topic.objects.filter(id=topic.id).update(views=F('views') + 1)
    
    posts_list = topic.posts.filter(is_active=True).select_related('author', 'author__profile')
    
    # Pagination
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Reply form
    reply_form = PostForm() if request.user.is_authenticated else None
    
    context = {
        'topic': topic,
        'posts': posts,
        'reply_form': reply_form,
    }
    return render(request, 'forum/topic_detail.html', context)


@login_required
def create_topic(request, category_slug):
    """Create a new topic"""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.category = category
            topic.slug = slugify(topic.title)
            topic.last_post_by = request.user
            topic.save()
            
            # Create the first post
            Post.objects.create(
                topic=topic,
                author=request.user,
                content=topic.content
            )
            
            messages.success(request, '主题创建成功！')
            return redirect(topic.get_absolute_url())
    else:
        form = TopicForm()
    
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'forum/create_topic.html', context)


@login_required
def reply_topic(request, slug):
    """Reply to a topic"""
    topic = get_object_or_404(Topic, slug=slug, is_active=True)
    
    if topic.is_locked:
        messages.error(request, '该主题已被锁定，无法回复。')
        return redirect(topic.get_absolute_url())
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            
            # Update topic's last post info
            topic.last_post_at = timezone.now()
            topic.last_post_by = request.user
            topic.save()
            
            messages.success(request, '回复成功！')
            return redirect(post.get_absolute_url())
    
    return redirect(topic.get_absolute_url())


def search(request):
    """Search topics and posts"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search in topics
        topic_results = Topic.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_active=True
        ).select_related('author', 'category')
        
        # Search in posts
        post_results = Post.objects.filter(
            content__icontains=query,
            is_active=True
        ).select_related('topic', 'author')
        
        results = list(topic_results) + list(post_results)
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'forum/search.html', context)


def user_profile(request, username):
    """User profile page"""
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # User's recent topics and posts
    recent_topics = Topic.objects.filter(author=user, is_active=True)[:5]
    recent_posts = Post.objects.filter(author=user, is_active=True)[:10]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'recent_topics': recent_topics,
        'recent_posts': recent_posts,
    }
    return render(request, 'forum/user_profile.html', context)


@login_required
def delete_topic(request, slug):
    """删除主题"""
    topic = get_object_or_404(Topic, slug=slug, is_active=True)
    
    # 检查权限：只有作者或管理员可以删除
    if request.user != topic.author and not request.user.is_staff:
        messages.error(request, '您没有权限删除此主题')
        return redirect('forum:topic_detail', slug=slug)
    
    if request.method == 'POST':
        # 软删除：设置is_active为False
        topic.is_active = False
        topic.save()
        
        # 同时软删除所有相关的帖子
        topic.posts.update(is_active=False)
        
        messages.success(request, f'主题「{topic.title}」已删除')
        return redirect('forum:category_detail', slug=topic.category.slug)
    
    context = {
        'topic': topic,
    }
    return render(request, 'forum/delete_topic.html', context)


@login_required
def select_category(request):
    """选择板块页面"""
    categories = Category.objects.filter(is_active=True, parent=None).order_by('order')
    
    # 分组显示分类
    startup_categories = categories.filter(order__lte=8)
    growth_categories = categories.filter(order__gt=8)
    
    context = {
        'startup_categories': startup_categories,
        'growth_categories': growth_categories,
    }
    return render(request, 'forum/select_category.html', context)
