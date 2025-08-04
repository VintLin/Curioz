from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    # Forum index
    path('', views.forum_index, name='index'),
    
    # Category views
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:category_slug>/new/', views.create_topic, name='create_topic'),
    path('select-category/', views.select_category, name='select_category'),
    
    # Topic views
    path('topic/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('topic/<slug:slug>/reply/', views.reply_topic, name='reply_topic'),
    path('topic/<slug:slug>/delete/', views.delete_topic, name='delete_topic'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # User profile
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]
