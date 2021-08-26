from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Tag


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    summernote_fields = ('content', )
    date_hierarchy = 'publish'
    ordering = ('status', '-publish')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
