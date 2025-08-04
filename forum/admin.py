from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Topic, Post, UserProfile


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'is_active', 'topic_count']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    
    def topic_count(self, obj):
        return obj.topic_count
    topic_count.short_description = '主题数量'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'topic_type', 'is_pinned', 'is_locked', 'views', 'created_at']
    list_filter = ['topic_type', 'is_pinned', 'is_locked', 'is_active', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_pinned', 'is_locked']
    raw_id_fields = ['author', 'last_post_by']
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['topic', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['content', 'author__username', 'topic__title']
    raw_id_fields = ['author', 'topic']
    date_hierarchy = 'created_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'post_count', 'reputation', 'last_seen']
    list_filter = ['last_seen']
    search_fields = ['user__username', 'user__email', 'location']
    raw_id_fields = ['user']
