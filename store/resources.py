from import_export import resources

from store.models import (
    About, Board, Comment, Email, FirstName, Keyword, LastName, Location,
    Proxy, UserAgent
)


class CustomResource(resources.ModelResource):

    def dehydrate_id(self, keyword):
        '''Dehydrate id value on export.'''
        return ''


class EmailResource(CustomResource):

    class Meta:
        model = Email
        exclude = ('added_at', )


class ProxyResource(CustomResource):

    class Meta:
        model = Proxy
        exclude = ('added_at', )


class UserAgentResource(CustomResource):

    class Meta:
        model = UserAgent
        exclude = ('added_at', )


class FirstNameResource(CustomResource):

    class Meta:
        model = FirstName
        exclude = ('added_at', )


class LastNameResource(CustomResource):

    class Meta:
        model = LastName
        exclude = ('added_at', )


class AboutResource(CustomResource):

    class Meta:
        model = About
        exclude = ('added_at', )


class LocationResource(CustomResource):

    class Meta:
        model = Location
        exclude = ('added_at', )


class BoardResource(CustomResource):

    class Meta:
        model = Board
        exclude = ('added_at', )


class CommentResource(CustomResource):

    class Meta:
        model = Comment
        exclude = ('added_at', )


class KeywordResource(CustomResource):

    class Meta:
        model = Keyword
        exclude = ('added_at', )
