from django import forms
from django.contrib import admin, messages
from django.db import models

from bot.forms import UserAdminForm
from bot.models import Board, User
from bot.tasks import (
    comment_task, confirm_email_task, create_boards_task, create_user_task,
    follow_task, interact_task, like_task, login_task, repin_task, sync_task,
    unfollow_task
)


class BoardInline(admin.StackedInline):

    model = Board
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    search_fields = ('name', 'username')
    list_display = (
        'name', 'username', 'board_count', 'pin_count', 'like_count',
        'follower_count', 'following_count'
    )
    actions = (
        'login_action', 'create_user_action', 'interact_action',
        'confirm_email_action', 'create_boards_action', 'sync_action',
        'repin_action', 'like_action', 'comment_action', 'follow_action',
        'unfollow_action',
    )
    form = UserAdminForm
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    inlines = (BoardInline, )

    def get_message(self, task_name, count):
        '''Return message for singular or plural selection.'''
        if count == 1:
            return 'Delayed {} for 1 user.'.format(task_name)
        return 'Delayed {} for {} users.'.format(task_name, count)

    def login_action(self, request, queryset):
        for user in queryset:
            login_task.delay(user)
        self.message_user(
            request,
            self.get_message('login_task', queryset.count()),
            level=messages.SUCCESS
        )

    def create_user_action(self, request, queryset):
        queryset = queryset.filter(cookies='[]')
        for user in queryset:
            create_user_task.delay(user)
        self.message_user(
            request,
            self.get_message('create_user_task', queryset.count()),
            level=messages.SUCCESS
        )

    def interact_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            interact_task.delay(user)
        self.message_user(
            request,
            self.get_message('interact_task', queryset.count()),
            level=messages.SUCCESS
        )

    def confirm_email_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            confirm_email_task.delay(user)
        self.message_user(
            request,
            self.get_message('confirm_email_task', queryset.count()),
            level=messages.SUCCESS
        )

    def create_boards_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            create_boards_task.delay(user)
        self.message_user(
            request,
            self.get_message('create_boards_task', queryset.count()),
            level=messages.SUCCESS
        )

    def sync_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            sync_task.delay(user)
        self.message_user(
            request,
            self.get_message('sync_task', queryset.count()),
            level=messages.SUCCESS
        )

    def like_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            like_task.delay(user)
        self.message_user(
            request,
            self.get_message('like_task', queryset.count()),
            level=messages.SUCCESS
        )

    def comment_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            comment_task.delay(user)
        self.message_user(
            request,
            self.get_message('comment_task', queryset.count()),
            level=messages.SUCCESS
        )

    def repin_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            repin_task.delay(user)
        self.message_user(
            request,
            self.get_message('repin_task', queryset.count()),
            level=messages.SUCCESS
        )

    def follow_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            follow_task.delay(user)
        self.message_user(
            request,
            self.get_message('follow_task', queryset.count()),
            level=messages.SUCCESS
        )

    def unfollow_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            unfollow_task.delay(user)
        self.message_user(
            request,
            self.get_message('unfollow_task', queryset.count()),
            level=messages.SUCCESS
        )

    login_action.short_description = 'login_task for selected users'
    create_user_action.short_description = (
        'create_user_task for selected users'
    )
    interact_action.short_description = 'interact_task for selected users'
    confirm_email_action.short_description = (
        'confirm_email_task for selected users'
    )
    create_boards_action.short_description = (
        'create_boards_task for selected users'
    )
    sync_action.short_description = 'sync_task for selected users'
    like_action.short_description = 'like_task for selected users'
    comment_action.short_description = 'comment_task for selected users'
    repin_action.short_description = 'repin_task for selected users'
    follow_action.short_description = 'follow_task for selected users'
    unfollow_action.short_description = 'unfollow_task for selected users'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    search_fields = ('name', )
    list_filter = ('category', 'description')
    list_display = (
        'name', 'description', 'category', 'user', 'pin_count',
        'follower_count'
    )
