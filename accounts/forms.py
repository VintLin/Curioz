from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from forum.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单，包含微信号必填字段"""
    wechat = forms.CharField(
        label='微信号',
        max_length=50,
        required=True,
        help_text='请填写您的微信号，用于问题反馈和交流',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入您的微信号'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'wechat', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为所有字段添加Bootstrap样式
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # 自定义字段属性
        self.fields['username'].widget.attrs.update({
            'placeholder': '请输入用户名'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': '请输入密码'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '请再次输入密码'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # 创建用户资料并保存微信号
            UserProfile.objects.create(
                user=user,
                wechat=self.cleaned_data['wechat']
            )
        return user
