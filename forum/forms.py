from django import forms
from django.contrib.auth.models import User
from .models import Topic, Post, UserProfile


class TopicForm(forms.ModelForm):
    """Form for creating new topics"""
    
    class Meta:
        model = Topic
        fields = ['title', 'content', 'topic_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入主题标题...',
                'maxlength': 200
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入主题内容...',
                'rows': 10
            }),
            'topic_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': '标题',
            'content': '内容',
            'topic_type': '主题类型'
        }


class PostForm(forms.ModelForm):
    """Form for creating posts/replies"""
    
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入回复内容...',
                'rows': 6
            })
        }
        labels = {
            'content': '回复内容'
        }


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'avatar', 'signature']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '介绍一下自己...',
                'rows': 4,
                'maxlength': 500
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '所在城市'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'signature': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '个性签名...',
                'rows': 2,
                'maxlength': 200
            })
        }
        labels = {
            'bio': '个人简介',
            'location': '所在地',
            'website': '个人网站',
            'avatar': '头像',
            'signature': '个性签名'
        }


class SearchForm(forms.Form):
    """Search form"""
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '搜索主题和帖子...'
        }),
        label='搜索关键词'
    )
