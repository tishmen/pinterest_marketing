from django import forms
from django.contrib import admin
from django.db import models

from pinterest.forms import UserAdminForm
from pinterest.models import Board, User


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
        'comment_count', 'followers_count', 'following_count'
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
            followers_count=models.Count('followers'),
            following_count=models.Count('following')
        )

    def board_count(self, user):
        '''Return user board count.'''
        return user.board_count

    board_count.admin_order_field = 'board_count'

    def repin_count(self, user):
        '''Return user repin count.'''
        return user.repin_count

    repin_count.admin_order_field = 'repin_count'

    def like_count(self, user):
        '''Return user like count.'''
        return user.like_count

    like_count.admin_order_field = 'like_count'

    def comment_count(self, user):
        '''Return user comment count.'''
        return user.comment_count

    comment_count.admin_order_field = 'comment_count'

    def followers_count(self, user):
        '''Return user followers count.'''
        return user.followers_count

    followers_count.admin_order_field = 'followers_count'

    def following_count(self, user):
        '''Return user following count.'''
        return user.following_count

    following_count.admin_order_field = 'following_count'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    '''Admin integration for board.'''

    search_fields = ('name', )
    list_filter = ('category', 'description')
    list_display = ('name', 'description', 'category', 'user', 'pin_count')

    def get_queryset(self, request):
        '''Override model admin get_queryset. Return annotated queryset.'''
        return Board.objects.annotate(pin_count=models.Count('pins'))

    def pin_count(self, board):
        '''Return board pin count.'''
        return board.pin_count

    pin_count.admin_order_field = 'pin_count'
