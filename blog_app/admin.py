from django.contrib import admin
from .models import Post, Comment, About


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'image')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('block_1', 'block_2', 'block_3', 'c_title_1', 'c_title_2', 'c_img_1', 'c_img_2', 'c_text_1',
                    'c_text_2', 'publish', 'created', 'updated')
    list_filter = ('created', 'updated', 'publish')
