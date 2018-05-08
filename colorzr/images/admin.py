from django.contrib import admin
from .models import *


class ImageConversionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'author',
        'created',
        'original_image',
        'bw_image',
        'color_image',
    ]
    readonly_fields = ['author', 'created']


admin.site.register(ImageConversion, ImageConversionAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
