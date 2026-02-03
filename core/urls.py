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

    # Admin Gallery
    path('admin-gallery/', views.admin_gallery, name='admin_gallery'),
    path('admin-gallery/create/', views.admin_gallery_create, name='admin_gallery_create'),
    path('admin-gallery/<int:pk>/edit/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('admin-gallery/<int:pk>/delete/', views.admin_gallery_delete, name='admin_gallery_delete'),
    path('admin-gallery/reorder/', views.admin_gallery_reorder, name='admin_gallery_reorder'),

    # Admin Feedback
    path('admin-feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin-feedback/<int:pk>/toggle/', views.admin_feedback_toggle, name='admin_feedback_toggle'),
    path('admin-feedback/welcome/', views.admin_feedback_welcome, name='admin_feedback_welcome'),
]
