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
from django.urls import path, include

import common.views as common_views
import manager.views as manager_views
import tenant.views as tenant_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', common_views.index_view, name='index'),

    path('accounts/login/', common_views.login_view, name='login'),
    path('accounts/logout/', common_views.logout_view, name='logout'),
    path('accounts/signup/', common_views.signup_view, name='signup'),
    
    path('common/feedback/', common_views.feedback, name='feedback'),

    path('manager/news/', manager_views.news_page, name='news'),
    path('manager/news/create/', manager_views.create_news_page, name='create_news'),

    path('profile/<str:username>', tenant_views.profile_view, name='profile'),
    #path('tenant/profile/', tenant_views.profile, name='profile'),
    path('redact_profile', tenant_views.redact_profile_view, name='redact_profile'),

    path('forum/<int:id>', tenant_views.forum_view, name="forum"),
    path('forum/discussion/<int:id>', tenant_views.discussion_view, name="discussion"),
    path('forum/discussion/<int:discussion_id>/thread/<int:thread_id>', tenant_views.thread, name="thread"),
    path('forum/<int:id>/cr_discussion', tenant_views.cr_discussion_view, name="cr_discussion"),
    path('forum/<int:id>/category/<str:name>', tenant_views.category_view, name="category"),

    path('my_appeals', tenant_views.my_appeals_view, name="my_appeals"),
    path('appeal/<int:id>', tenant_views.appeal_view, name="appeal"),
    path('cr_appeal', tenant_views.cr_appeal_view, name="cr_appeal"),

    #path('vol/test', tenant_views.test_view, name="test"),
    path('vol/volunteer', tenant_views.volunteer_view, name="volunteer"),
    path('vol/help', tenant_views.help_view, name="help"),
    path('vol/help/cr_task', tenant_views.cr_task_view, name="cr_task"),
    path('vol/task/<int:id>', tenant_views.task_view, name="task"),
]
