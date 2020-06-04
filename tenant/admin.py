"""
Используемые модули
"""
from django.contrib import admin
from .models import Tenant
from .models import Appeal
from .models import Comment
from .models import AppealMessage
from .models import Task
from .models import Discussion
from .models import Company
from .models import Manager
from .models import Pass
from .models import Forum
from .models import House


admin.site.register(Company)
admin.site.register(Task)
admin.site.register(Discussion)
admin.site.register(Comment)
admin.site.register(Tenant)
admin.site.register(Appeal)
admin.site.register(AppealMessage)
admin.site.register(Manager)
admin.site.register(Pass)
admin.site.register(Forum)
admin.site.register(House)

# Register your models here.
