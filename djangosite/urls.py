"""djangosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # перенаправление на приложение admin(встроено по умолчанию)
    path('tictactoe/', include('tictactoe.urls')),  # перенаправление на приложение tictactoe
    path('api/', include('api.urls')),  # перенаправление на приложение api
    url(r'^register/$', views.MyRegisterFormView.as_view(), name="Страница регистрации"),
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="Страница с логином"),
    url(r'^logout/$', views.logout_user, name="Вторичная страница для logout"),
    url(r'^$', views.main_page, name="Основная страница"),
]
