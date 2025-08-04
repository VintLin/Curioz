from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Forum categories with hierarchical structure"""
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('URL标识', unique=True)
    description = models.TextField('描述', blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父分类')
    order = models.PositiveIntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class MPTTMeta:
        order_insertion_by = ['order', 'name']
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('forum:category_detail', kwargs={'slug': self.slug})
    
    @property
    def topic_count(self):
        return self.topics.filter(is_active=True).count()
    
    @property
    def post_count(self):
        return Post.objects.filter(topic__category=self, is_active=True).count()


class Topic(models.Model):
    """Forum topics/threads"""
    TOPIC_TYPES = (
        ('discussion', '讨论'),
        ('question', '提问'),
        ('sharing', '分享'),
        ('announcement', '公告'),
    )
    
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL标识', unique=True)
    content = models.TextField('内容')
    topic_type = models.CharField('主题类型', max_length=20, choices=TOPIC_TYPES, default='discussion')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics', verbose_name='分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics', verbose_name='作者')
    is_pinned = models.BooleanField('置顶', default=False)
    is_locked = models.BooleanField('锁定', default=False)
    is_active = models.BooleanField('是否启用', default=True)
    views = models.PositiveIntegerField('浏览次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    last_post_at = models.DateTimeField('最后回复时间', default=timezone.now)
    last_post_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_posts', verbose_name='最后回复者')
    
    class Meta:
        verbose_name = '主题'
        verbose_name_plural = '主题'
        ordering = ['-is_pinned', '-last_post_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum:topic_detail', kwargs={'slug': self.slug})
    
    @property
    def reply_count(self):
        return self.posts.filter(is_active=True).count() - 1  # Exclude the first post
    
    @property
    def first_post(self):
        return self.posts.filter(is_active=True).first()
    
    @property
    def last_post(self):
        return self.posts.filter(is_active=True).last()


class Post(models.Model):
    """Forum posts/replies"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts', verbose_name='主题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    content = models.TextField('内容')
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.topic.title} - {self.author.username}'
    
    def get_absolute_url(self):
        return f"{self.topic.get_absolute_url()}#post-{self.id}"


class UserProfile(models.Model):
    """Extended user profile for forum"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    bio = models.TextField('个人简介', blank=True, max_length=500)
    location = models.CharField('所在地', max_length=100, blank=True)
    website = models.URLField('个人网站', blank=True)
    wechat = models.CharField('微信号', max_length=50, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)
    signature = models.TextField('个性签名', blank=True, max_length=200)
    post_count = models.PositiveIntegerField('发帖数', default=0)
    reputation = models.IntegerField('声望', default=0)
    last_seen = models.DateTimeField('最后在线', default=timezone.now)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f'{self.user.username} 的资料'
