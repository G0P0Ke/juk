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
from django.conf.urls import url, include

import common.views as common_views
import manager.views as manager_views
import tenant.views as tenant_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('martor/', include('martor.urls')),

    path('admin/', common_views.admin, name='admin'),
    path('admin/create/', common_views.admin_create, name='create_a_company'),

    path('', common_views.index_view, name='index'),

    path('accounts/login/', common_views.login_view, name='login'),
    path('accounts/logout/', common_views.logout_view, name='logout'),
    path('accounts/signup/', common_views.signup_view, name='signup'),

    path('common/feedback/', common_views.feedback, name='feedback'),

    path('manager', manager_views.manager_main_page, name='manager_main'),
    path('manager/my_cabinet', manager_views.my_cabinet_view, name='manager_my_cabinet'),
                  path('manager/edit_profile', manager_views.edit_profile_view, name='manager_edit_profile'),

                  path('manager/news/', manager_views.my_news_page_view, name='my_news'),
                  path('manager/news/create/', manager_views.create_news_page_view, name='create_news'),
                  path('manager/news/<int:news_id>', manager_views.news_page, name='news'),

    path('manager/company_forums/', manager_views.company_forums_view, name='company_forums'),
    path('manager/company_appeals/', manager_views.company_appeals_view, name='company_appeals'),
    path('manager/add_house/', manager_views.add_house_view, name='add_house'),
    path('manager/tenant_confirming/', manager_views.tenant_confirming_view, name='tenant_confirming'),

    path('tenant', tenant_views.tenant_main_page, name='tenant_main'),
    path('tenant/my_cabinet', tenant_views.my_cabinet_view, name='tenant_my_cabinet'),
                  path('tenant/edit_profile', tenant_views.edit_profile_view, name='tenant_edit_profile'),

    path('forum/<int:forum_id>', tenant_views.forum_view, name="forum"),
    path('forum/discussion/<int:discussion_id>', tenant_views.discussion_view, name="discussion"),
    path('forum/discussion/<int:discussion_id>/thread/<int:thread_id>', tenant_views.thread_view, name="thread"),
    path('forum/<int:forum_id>/cr_discussion', tenant_views.cr_discussion_view, name="cr_discussion"),
    path('forum/<int:forum_id>/category/<str:category_name>', tenant_views.category_view, name="category"),

    path('my_appeals', tenant_views.my_appeals_view, name="my_appeals"),
    path('appeal/<int:appeal_id>', tenant_views.appeal_view, name="appeal"),
    path('cr_appeal', tenant_views.cr_appeal_view, name="cr_appeal"),

    path('vol/test', tenant_views.test_view, name="test"),
    path('vol/volunteer', tenant_views.volunteer_view, name="volunteer"),
    path('vol/help', tenant_views.help_view, name="help"),
    path('vol/help/cr_task', tenant_views.cr_task_view, name="cr_task"),
    path('vol/task/<int:id>', tenant_views.task_view, name="task"),

    path('tenant/pass/my_passes', tenant_views.my_pass_view, name="my_passes"),
    path('pass/<int:pass_id>', tenant_views.pass_view, name="pass"),
    path('tenant/pass/cr_pass', tenant_views.cr_pass_view, name="cr_pass"),
    path('manager/pass/houses', manager_views.pass_view, name="houses_passes"),
    path('manager/pass/house_passes/<int:house_id>', manager_views.pass_list_view, name="pass_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
