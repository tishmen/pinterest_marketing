from django import forms
from django.contrib import admin, messages
from django.db import models

from pinterest.forms import UserAdminForm
from pinterest.models import Board, User
from pinterest.tasks import (
    create_user_task, confirm_email_task, login_task, create_boards_task,
    repin_task, like_task, comment_task, follow_task, unfollow_task
)


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
    actions = (
        'create_user_action', 'confirm_email_action', 'login_action',
        'create_boards_action', 'repin_action', 'like_action',
        'comment_action', 'follow_action', 'unfollow_action'
    )
    form = UserAdminForm
    inlines = (BoardInline, )

    def display_message(self, request, task_name, count):
        '''Display message in list view for admin action.'''
        if count == 1:
            message = 'Delayed {} for 1 user.'.format(task_name)
        else:
            message = 'Delayed {} for {} users.'.format(task_name, count),
        self.message_user(request, message, level=messages.SUCCESS)

    def create_user_action(self, request, queryset):
        '''Admin action for creating pinterest users.'''
        queryset = queryset.filter(cookies='[]')
        for user in queryset:
            create_user_task.delay(user)
        self.display_message(request, 'create_user_task', queryset.count())

    def confirm_email_action(self, request, queryset):
        '''Admin action for confirming pinterest email.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            confirm_email_task.delay(user)
        self.display_message(request, 'confirm_email_task', queryset.count())

    def create_boards_action(self, request, queryset):
        '''Admin action for creating pinterest boards.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            create_boards_task.delay(user)
        self.display_message(request, 'create_boards_task', queryset.count())

    def login_action(self, request, queryset):
        '''Admin action for loging pinterest users.'''
        for user in queryset:
            login_task.delay(user)
        self.display_message(request, 'login_task', queryset.count())

    def like_action(self, request, queryset):
        '''Admin action for liking random pinterest pins.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            like_task.delay(user)
        self.display_message(request, 'like_task', queryset.count())

    def comment_action(self, request, queryset):
        '''Admin action for commenting on random pinterest pins.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            comment_task.delay(user)
        self.display_message(request, 'like_task', queryset.count())

    def repin_action(self, request, queryset):
        '''Admin action for repinning random pinterest pins.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            repin_task.delay(user)
        self.display_message(request, 'repin_task', queryset.count())

    def follow_action(self, request, queryset):
        '''Admin action for following random pinterest users.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            follow_task.delay(user)
        self.display_message(request, 'follow_task', queryset.count())

    def unfollow_action(self, request, queryset):
        '''Admin action for unfollowing random pinterest users.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            unfollow_task.delay(user)
        self.display_message(request, 'unfollow_task', queryset.count())

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

    def repin_count(self, user):
        '''Return user repin count.'''
        return user.repin_count

    def like_count(self, user):
        '''Return user like count.'''
        return user.like_count

    def comment_count(self, user):
        '''Return user comment count.'''
        return user.comment_count

    def followers_count(self, user):
        '''Return user followers count.'''
        return user.followers_count

    def following_count(self, user):
        '''Return user following count.'''
        return user.following_count

    create_user_action.short_description = (
        'Create user task for selected users'
    )
    confirm_email_action.short_description = (
        'Confirm email task for selected users'
    )
    login_action.short_description = 'Login task for selected users'
    create_boards_action.short_description = (
        'Create boards task for selected users'
    )
    like_action.short_description = 'Like task for selected users'
    comment_action.short_description = 'Comment task for selected users'
    repin_action.short_description = 'Repin task for selected users'
    follow_action.short_description = 'Follow task for selected users'
    unfollow_action.short_description = 'Unfollow task for selected users'

    board_count.admin_order_field = 'board_count'
    repin_count.admin_order_field = 'repin_count'
    like_count.admin_order_field = 'like_count'
    comment_count.admin_order_field = 'comment_count'
    followers_count.admin_order_field = 'followers_count'
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
