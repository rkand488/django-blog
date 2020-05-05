# from django.apps import apps
from django.contrib import admin

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm

    search_fields = ['title', 'author__first_name']
    list_display = ('title', 'created_at', 'author')
    list_filter = ('author', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'slug')
    fieldsets = ((None, {
        'fields': ('title', 'text')
    }), ('Other Information', {
        'fields': ('created_at', 'updated_at', 'slug'),
        'classes': ('collapse', )
    }))

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            'plugins/summernote/summernote-lite.js',
            'js/summernote.js',
        )
        css = {'all': ('plugins/summernote/summernote-lite.css', )}

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.save()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentForm

    search_fields = ['name', 'email', 'website', 'post__title']
    list_display = ('name', 'email', 'website', 'created_at')
    list_filter = ('name', 'email', 'website', 'post__title')
    list_display_links = ('name', 'website')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = ((None, {
        'fields': ('name', 'email', 'website', 'text')
    }), ('Other Information', {
        'fields': ('created_at', 'updated_at'),
        'classes': ('collapse', )
    }))

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            'plugins/summernote/summernote-lite.js',
            'js/summernote.js',
        )
        css = {
            'all':
            ('plugins/summernote/summernote-lite.css', 'css/summernote.css')
        }
