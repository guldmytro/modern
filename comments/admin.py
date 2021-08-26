from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'comment', 'reply', 'post', 'status')
