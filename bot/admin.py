from django import forms
from django.contrib import admin, messages
from django.db import models

from .forms import UserAdminForm
from .models import Board, User
from .tasks import (
    CommentTask, ConfirmTask, CreateBoardsTask, CreateUserTask, FollowTask,
    InteractTask, LikeTask, LoginTask, RepinTask, SyncTask, UnfollowTask
)


class BoardInline(admin.StackedInline):

    model = Board
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    search_fields = ('username', )
    list_display = (
        'username', 'board_count', 'pin_count', 'like_count', 'follower_count',
        'following_count'
    )
    actions = (
        'login_action', 'create_user_action', 'interact_action',
        'confirm_action', 'create_boards_action', 'sync_action',
        'repin_action', 'like_action', 'comment_action', 'follow_action',
        'unfollow_action',
    )
    form = UserAdminForm
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    inlines = (BoardInline, )

    def get_message(self, task_name, count):
        if count == 1:
            return 'Delayed {} for 1 user.'.format(task_name)
        return 'Delayed {} for {} users.'.format(task_name, count)

    def show_message(self, request, task, count):
        self.message_user(
            request, self.get_message(task, count), level=messages.SUCCESS
        )

    def login_action(self, request, queryset):
        for user in queryset:
            LoginTask().delay(user)
        self.show_message(request, 'LoginTask', queryset.count())

    def create_user_action(self, request, queryset):
        queryset = queryset.filter(cookies='[]')
        for user in queryset:
            CreateUserTask().delay(user)
        self.show_message(request, 'CreateUserTask', queryset.count())

    def interact_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            InteractTask().delay(user)
        self.show_message(request, 'InteractTask', queryset.count())

    def confirm_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            ConfirmTask().delay(user)
        self.show_message(request, 'ConfirmTask', queryset.count())

    def create_boards_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            CreateBoardsTask().delay(user)
        self.show_message(request, 'CreateBoardsTask', queryset.count())

    def sync_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            SyncTask().delay(user)
        self.show_message(request, 'SyncTask', queryset.count())

    def like_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            LikeTask().delay(user)
        self.show_message(request, 'LikeTask', queryset.count())

    def comment_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            CommentTask().delay(user)
        self.show_message(request, 'CommentTask', queryset.count())

    def repin_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            RepinTask().delay(user)
        self.show_message(request, 'RepinTask', queryset.count())

    def follow_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            FollowTask().delay(user)
        self.show_message(request, 'FollowTask', queryset.count())

    def unfollow_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        for user in queryset:
            UnfollowTask().delay(user)
        self.show_message(request, 'UnfollowTask', queryset.count())

    login_action.short_description = 'LoginTask for selected users'
    create_user_action.short_description = 'CreateUserTask for selected users'
    interact_action.short_description = 'InteractTask for selected users'
    confirm_action.short_description = 'ConfirmTask for selected users'
    create_boards_action.short_description = (
        'CreateBoardsTask for selected users'
    )
    sync_action.short_description = 'SyncTask for selected users'
    like_action.short_description = 'LikeTask for selected users'
    comment_action.short_description = 'CommentTask for selected users'
    repin_action.short_description = 'RepinTask for selected users'
    follow_action.short_description = 'FollowTask for selected users'
    unfollow_action.short_description = 'UnfollowTask for selected users'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    search_fields = ('name', )
    list_filter = ('category', )
    list_display = ('name', 'category', 'user', 'pin_count', 'follower_count')
