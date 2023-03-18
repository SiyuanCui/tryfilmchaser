"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from common import views

urlpatterns = [
                  path('admins/', include('admins.urls')),
                  path('users/', include('users.urls')),
                  path('picture/', include('picture.urls')),
                  path('issues/', include('issues.urls')),
                  path('history/', include('history.urls')),
                  path('collection/', include('collection.urls')),
                  path('columns/', include('columns.urls')),
                  path('movies/', include('movies.urls')),
                  path('common/', include('common.urls')),

                  path('', views.index, name='index'),
                  path('login/', views.login, name='login'),
                  path('logout/', views.logout, name='logout'),
                  path('main/', views.main, name='main'),
                  path('sy/', views.adminsy, name='adminsy'),

                  #   内置管理界面
                  #   path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
