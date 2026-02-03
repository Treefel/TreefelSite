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
]
