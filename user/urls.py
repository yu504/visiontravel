# user/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from .views import CustomPasswordResetView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # ログアウトページ
    path('register/', views.register, name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='user_login'),
]
