from django.urls import path
from . import views

app_name = 'sskUser'

# http://127.0.0.1:8000/account/img_captcha   xxxxx

urlpatterns = [
    path('', views.user_info, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('delete/', views.user_delete, name='delete'),
    path('resetpwd/', views.user_resetpwd, name='resetpwd'),
    # 图形验证码
    path('img_captcha/', views.img_captcha, name='img_captcha'),
]
