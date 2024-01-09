"""dota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from dotaapi.views import login_user, register_user, getMe, HeroView, RandomizerView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'hero', HeroView, 'hero')
router.register(r'heroes', HeroView, 'heroes')
router.register(r'random', RandomizerView, 'random')
# router.register(r'tabs', TabView, 'tab')
# router.register(r'items', ItemView, 'item')
# router.register(r'itemTypes', ItemTypeView, 'itemType')
# router.register(r'users', UserView, 'user')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_user),
    path('register', register_user),
    path('getMe', getMe),
    path('', include(router.urls))
]
