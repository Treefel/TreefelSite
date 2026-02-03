from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),

    # Admin Blog
    path('admin-blog/', views.admin_blog, name='admin_blog'),
    path('admin-blog/create/', views.admin_blog_create, name='admin_blog_create'),
    path('admin-blog/<int:pk>/edit/', views.admin_blog_edit, name='admin_blog_edit'),
    path('admin-blog/<int:pk>/delete/', views.admin_blog_delete, name='admin_blog_delete'),
    path('admin-blog/category/create/', views.admin_blog_category_create, name='admin_blog_category_create'),
    path('admin-blog/category/<int:pk>/delete/', views.admin_blog_category_delete, name='admin_blog_category_delete'),
]
