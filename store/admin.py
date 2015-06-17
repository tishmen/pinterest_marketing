from django import forms
from django.contrib import admin, messages
from django.db import models
from import_export.admin import ImportExportModelAdmin

from pinterest.tasks import scrape_keywords_task
from store.models import (
    About, Board, Comment, Email, FirstName, Keyword, LastName, Location,
    Proxy, UserAgent
)
from store.resources import (
    AboutResource, BoardResource, CommentResource, EmailResource,
    FirstNameResource, KeywordResource, LastNameResource, LocationResource,
    ProxyResource, UserAgentResource
)


@admin.register(Email)
class EmailAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for email.'''

    resource_class = EmailResource
    search_fields = ('address', )


@admin.register(Proxy)
class ProxyAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for proxy.'''

    resource_class = ProxyResource


@admin.register(UserAgent)
class UserAgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for user-agent.'''

    resource_class = UserAgentResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('string', )


@admin.register(FirstName)
class FirstNameAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for first name.'''

    resource_class = FirstNameResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('name', )


@admin.register(LastName)
class LastNameAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for last name.'''

    resource_class = LastNameResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('name', )


@admin.register(About)
class AboutAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for about user.'''

    resource_class = AboutResource
    search_fields = ('about', )


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for location.'''

    resource_class = LocationResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('location', )


@admin.register(Board)
class BoardAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for board.'''

    resource_class = BoardResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('name', 'description')
    list_filter = ('category', )
    list_display = ('name', 'description', 'category')


@admin.register(Keyword)
class KeywordAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for keyword.'''

    resource_class = KeywordResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('keyword', )
    list_filter = ('category', 'scraped')
    list_display = ('keyword', 'category', 'scraped')
    actions = ('scrape_keywords_action', )

    def display_message(self, request, task_name, count):
        '''Display message in list view for admin action.'''
        if count == 1:
            message = 'Delayed {} for 1 keyword.'.format(task_name)
        else:
            message = 'Delayed {} for {} keywords.'.format(task_name, count),
        self.message_user(request, message, level=messages.SUCCESS)

    def scrape_keywords_action(self, request, queryset):
        '''Admin action for scraping pinterest keywords suggestions.'''
        queryset = queryset.exclude(scraped=True)
        scrape_keywords_task.delay(queryset)
        self.display_message(request, 'scrape_keywords_task', queryset.count())

    scrape_keywords_action.short_description = (
        'Scrape keywords task for selected keywords'
    )


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    '''Admin integration for comment.'''

    resource_class = CommentResource
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
    search_fields = ('comment', )
    list_filter = ('category', )
    list_display = ('comment', 'category')
