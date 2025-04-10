from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

admin.site.site_header = 'Админ-панель'
admin.site.site_title = 'Админка'
admin.site.index_title = 'Добро пожаловать в админку'

User = get_user_model()
admin.site.unregister(Group)
