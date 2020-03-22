"""juk URL Configuration

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
from django.contrib import admin
from django.urls import path

import common.views as common_views
import manager.views as manager_views
import tenant.views as tenant_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', common_views.index_view, name='index'),
    path('accounts/login/', common_views.login_view, name='login'),
    path('accounts/logout/', common_views.logout_view, name='logout'),
    path('accounts/signup/', common_views.signup_view, name='signup'),
    path('feedback/', common_views.feedback, name='feedback'),
    path('news/', manager_views.news_page, name='news'),
    path('profile/', tenant_views.profile, name='profile'),
]
