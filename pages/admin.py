from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About


@admin.register(About)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('name', 'email')
    summernote_fields = ('content',)
