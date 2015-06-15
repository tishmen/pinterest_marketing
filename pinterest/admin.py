from django.contrib import admin

from django import forms
from django.db import models

from pinterest.models import User, Board
from pinterest.forms import UserAdminForm


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
        'name', 'username', 'board_count', 'repin_count', 'like_count',
        'comment_count', 'following_count'
    )
    form = UserAdminForm
    inlines = (BoardInline, )

    def get_queryset(self, request):
        '''Override model admin get_queryset. Return annotated queryset.'''
        return User.objects.annotate(
            board_count=models.Count('board'),
            repin_count=models.Count('repins'),
            like_count=models.Count('likes'),
            comment_count=models.Count('comments'),
            following_count=models.Count('following')
        )

    def board_count(self, user):
        '''Return user board count.'''
        return user.board_count

    def repin_count(self, user):
        '''Return user repin count.'''
        return user.repin_count

    def like_count(self, user):
        '''Return user like count.'''
        return user.like_count

    def comment_count(self, user):
        '''Return user comment count.'''
        return user.comment_count

    def following_count(self, user):
        '''Return user following count.'''
        return user.following_count

    board_count.admin_order_field = 'board_count'
    repin_count.admin_order_field = 'repin_count'
    like_count.admin_order_field = 'like_count'
    comment_count.admin_order_field = 'comment_count'
    following_count.admin_order_field = 'following_count'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    '''Admin integration for board.'''

    search_fields = ('name', 'description')
    list_filter = ('category', )
    list_display = ('name', 'description', 'category', 'user')
