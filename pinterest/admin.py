from django.contrib import admin

from django import forms
from django.db import models

from pinterest.models import User, Board


class BoardInline(admin.StackedInline):

    '''Board inlined to user.'''

    model = Board
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    '''Admin integration for user.'''

    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('name', 'username')
    list_display = (
        'name', 'username', 'repin_count', 'like_count', 'comment_count',
        'following_count'
    )
    inlines = (BoardInline, )

    def queryset(self, request):
        return User.objects.annotate(
            repin_count=models.Count('repins'),
            like_count=models.Count('likes'),
            comment_count=models.Count('comments'),
            following_count=models.Count('following')
        )

    def repin_count(self, obj):
        return obj.repin_count

    def like_count(self, obj):
        return obj.like_count

    def comment_count(self, obj):
        return obj.comment_count

    def following_count(self, obj):
        return obj.following_count

    repin_count.admin_order_field = 'repin_count'
    repin_count.admin_order_field = 'like_count'
    repin_count.admin_order_field = 'comment_count'
    repin_count.admin_order_field = 'following_count'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    '''Admin integration for board.'''

    search_fields = ('name', 'description')
    list_filter = ('category', )
    list_display = ('name', 'category', 'user')
