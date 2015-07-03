from import_export import resources

from .models import (
    About, Board, Comment, Email, FirstName, Keyword, LastName, Location,
    Proxy, UserAgent
)


class EmailResource(resources.ModelResource):

    class Meta:
        model = Email
        exclude = ('added_at', )


class ProxyResource(resources.ModelResource):

    class Meta:
        model = Proxy
        exclude = ('added_at', )


class UserAgentResource(resources.ModelResource):

    class Meta:
        model = UserAgent
        exclude = ('added_at', )


class FirstNameResource(resources.ModelResource):

    class Meta:
        model = FirstName
        exclude = ('added_at', )


class LastNameResource(resources.ModelResource):

    class Meta:
        model = LastName
        exclude = ('added_at', )


class AboutResource(resources.ModelResource):

    class Meta:
        model = About
        exclude = ('added_at', )


class LocationResource(resources.ModelResource):

    class Meta:
        model = Location
        exclude = ('added_at', )


class BoardResource(resources.ModelResource):

    class Meta:
        model = Board
        exclude = ('added_at', )


class CommentResource(resources.ModelResource):

    class Meta:
        model = Comment
        exclude = ('added_at', )


class KeywordResource(resources.ModelResource):

    class Meta:
        model = Keyword
        exclude = ('added_at', )
