from django.contrib import admin
from django.db import models

from django.utils.safestring import mark_safe

from .models import CmsSlider

class CmsAdmin(admin.ModelAdmin):
    list_display = ("pk","cms_img")

    def get_img(self, obj):
        if obj.cms_img:
            return mark_safe(f'<img src="{obj.cms_img.url}" width="80px"')
        else:
            return 'нет картинки'

    get_img.short_description = 'Миниатюра'

admin.site.register(CmsSlider, CmsAdmin)
