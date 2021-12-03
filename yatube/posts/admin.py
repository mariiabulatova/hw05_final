from django.contrib import admin

from .models import Group, Post, Comment, Follow

EMPTY_VALUE_DISPLAY = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)
    list_filter = ('description',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'created',)
    search_fields = ('author', 'text')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    search_fields = ('user', 'author')
    list_filter = ('user',)
    empty_value_display = '-пусто-'
