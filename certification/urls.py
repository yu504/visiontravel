"""
# certification/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('mainmenu/', views.mainmenu_view, name='mainmenu'),  # mainmenuのURL設定
    path('upload/', views.upload, name='upload'),       # 画像アップロードへのURLパス
    path('result/', views.upload_image, name='upload_image'),
    path('settings/', views.settings_view, name='settings'),  # 設定ページのURL
    path('get_hotel_links/', views.get_hotel_links, name='get_hotel_links'),
]
"""

from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from . import views
 
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('mainmenu/', views.mainmenu_views, name='mainmenu'),  # メインメニュー用ビュー
    path('upload/', views.upload_image, name='upload'),
    path("upload_image/", views.upload_image, name="upload_image"),  # アップロード処理
    path('get_hotel_links/', views.get_hotel_links, name='get_hotel_links'),
 
]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)