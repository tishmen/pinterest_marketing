from django import forms
from django.contrib import admin, messages
from django.db import models

from pinterest.forms import UserAdminForm
from pinterest.models import Board, Pin, User
from pinterest.tasks import (
    comment_task, confirm_email_task, create_boards_task, create_user_task,
    follow_task, like_task, login_task, repin_task, scrape_task, sync_task,
    unfollow_task
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
        'name', 'username', 'board_count', 'pin_count', 'like_count',
        'follower_count', 'following_count'
    )
    actions = (
        'login_action', 'create_user_action', 'confirm_email_action',
        'create_boards_action', 'sync_task', 'repin_action', 'like_action',
        'comment_action', 'follow_action', 'unfollow_action', 'scrape_action'
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

    def login_action(self, request, queryset):
        '''Admin action for loging pinterest users.'''
        for user in queryset:
            login_task.delay(user)
        self.display_message(request, 'login_task', queryset.count())

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

    def sync_action(self, request, queryset):
        '''Admin action for syncing pinterest users.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            sync_task.delay(user)
        self.display_message(request, 'sync_task', queryset.count())

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
        self.display_message(request, 'comment_task', queryset.count())

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

    def scrape_action(self, request, queryset):
        '''Admin action for scraping random pinterest pins.'''
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            scrape_task.delay(user)
        self.display_message(request, 'scrape_task', queryset.count())

    login_action.short_description = 'Login task for selected users'
    create_user_action.short_description = (
        'Create user task for selected users'
    )
    confirm_email_action.short_description = (
        'Confirm email task for selected users'
    )
    create_boards_action.short_description = (
        'Create boards task for selected users'
    )
    sync_action.short_description = 'Sync task for selected users'
    like_action.short_description = 'Like task for selected users'
    comment_action.short_description = 'Comment task for selected users'
    repin_action.short_description = 'Repin task for selected users'
    follow_action.short_description = 'Follow task for selected users'
    unfollow_action.short_description = 'Unfollow task for selected users'
    scrape_action.short_description = 'Scrape task for selected users'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    '''Admin integration for board.'''

    search_fields = ('name', )
    list_filter = ('category', 'description')
    list_display = (
        'name', 'description', 'category', 'user', 'pin_count',
        'follower_count', 'collaborator_count'
    )


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):

    '''Admin integration for pin.'''

    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('title', 'description', 'link')
    list_display = (
        'title', 'description', 'link', 'repin_count', 'like_count',
        'comment_count'
    )
