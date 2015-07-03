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

    def show_message(self, request, task, count):
        '''Display success message in the admin interface.'''
        self.message_user(
            request, self.get_message(task, count), level=messages.SUCCESS
        )

    def login_action(self, request, queryset):
        login_task = LoginTask()
        for user in queryset:
            login_task.delay(user)
        self.show_message('LoginTask', queryset.count())

    def create_user_action(self, request, queryset):
        queryset = queryset.filter(cookies='[]')
        create_user_task = CreateUserTask()
        for user in queryset:
            create_user_task.delay(user)
        self.message_success('CreateUserTask', queryset.count())

    def interact_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        interact_task = InteractTask()
        for user in queryset:
            interact_task.delay(user)
        self.show_message('InteractTask', queryset.count())

    def confirm_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        confirm_task = ConfirmTask()
        for user in queryset:
            confirm_task.delay(user)
        self.show_message('ConfirmTask', queryset.count())

    def create_boards_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        create_boards_task = CreateBoardsTask()
        for user in queryset:
            create_boards_task.delay(user)
        self.show_message('CreateBoardsTask', queryset.count())

    def sync_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        sync_task = SyncTask()
        for user in queryset:
            sync_task.delay(user)
        self.show_message('SyncTask', queryset.count())

    def like_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        like_task = LikeTask()
        for user in queryset:
            like_task.delay(user)
        self.show_message('LikeTask', queryset.count())

    def comment_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        comment_task = CommentTask()
        for user in queryset:
            comment_task.delay(user)
        self.show_message('CommentTask', queryset.count())

    def repin_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        repin_task = RepinTask()
        for user in queryset:
            repin_task.delay(user)
        self.show_message('RepinTask', queryset.count())

    def follow_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        follow_task = FollowTask()
        for user in queryset:
            follow_task.delay(user)
        self.show_message('FollowTask', queryset.count())

    def unfollow_action(self, request, queryset):
        queryset = queryset.exclude(cookies='[]')
        unfollow_task = UnfollowTask()
        for user in queryset:
            unfollow_task.delay(user)
        self.show_message('UnfollowTask', queryset.count())

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
    list_filter = ('category', 'description')
    list_display = (
        'name', 'description', 'category', 'user', 'pin_count',
        'follower_count'
    )
