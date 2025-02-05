"""
URL configuration for visiontravel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.mainmenu, name='mainmenu')
Class-based views
    1. Add an import:  from other_app.views import mainmenu
    2. Add a URL to urlpatterns:  path('', mainmenu.as_view(), name='mainmenu')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user/', include('user.urls')),  # 追加
    path('admin/', admin.site.urls),
    path('certification/', include('certification.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)