from django.contrib import admin
from listings.models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('titre')
admin.site.register(Blog)
