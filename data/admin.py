from import_export.admin import ImportMixin

from django import forms
from django.contrib import admin
from django.db import models

from .models import (
    About, Board, Comment, Email, FirstName, Keyword, LastName, Location,
    Proxy, UserAgent
)
from .resources import (
    AboutResource, BoardResource, CommentResource, EmailResource,
    FirstNameResource, KeywordResource, LastNameResource, LocationResource,
    ProxyResource, UserAgentResource
)


@admin.register(Email)
class EmailAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = EmailResource
    search_fields = ('address', )
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}


@admin.register(Proxy)
class ProxyAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = ProxyResource


@admin.register(UserAgent)
class UserAgentAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = UserAgentResource
    search_fields = ('string', )
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}


@admin.register(FirstName)
class FirstNameAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = FirstNameResource
    search_fields = ('name', )
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}


@admin.register(LastName)
class LastNameAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = LastNameResource
    search_fields = ('name', )
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}


@admin.register(About)
class AboutAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = AboutResource
    search_fields = ('about', )


@admin.register(Location)
class LocationAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = LocationResource
    search_fields = ('location', )
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}


@admin.register(Board)
class BoardAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = BoardResource
    search_fields = ('name', 'description')
    list_filter = ('category', )
    list_display = ('name', 'description', 'category')


@admin.register(Comment)
class CommentAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = CommentResource
    search_fields = ('comment', )
    list_filter = ('category', )
    list_display = ('comment', 'category')


@admin.register(Keyword)
class KeywordAdmin(ImportMixin, admin.ModelAdmin):

    resource_class = KeywordResource
    search_fields = ('keyword', )
    list_filter = ('category', )
    list_display = ('keyword', 'category')
    formfield_overrides = {models.TextField: {'widget': forms.TextInput}}
