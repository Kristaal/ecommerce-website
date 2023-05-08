from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostModelAdmin(SummernoteModelAdmin):
    """
    A class to register post model in admin panel
    """
    summernote_fields = ('content')
    list_filter = (
        'title',
        'date_created',
        )
    list_display = ('title', 'date_created')
    search_fields = ['title']
