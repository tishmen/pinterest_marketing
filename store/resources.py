from import_export import resources

from store.models import (
    About, Board, Comment, Email, FirstName, Keyword, LastName, Location,
    Proxy, UserAgent
)


class CustomResource(resources.ModelResource):

    '''Custom resource class containing dehydrate id functionality.'''

    def dehydrate_id(self, keyword):
        '''Remove id values on export.'''
        return ''


class EmailResource(CustomResource):

    '''Resource class for email.'''

    class Meta:
        model = Email
        exclude = ('added_at', )


class ProxyResource(CustomResource):

    '''Resource class for proxy.'''

    class Meta:
        model = Proxy
        exclude = ('added_at', )


class UserAgentResource(CustomResource):

    '''Resource class for user agent.'''

    class Meta:
        model = UserAgent
        exclude = ('added_at', )


class FirstNameResource(CustomResource):

    '''Resource class for first name.'''

    class Meta:
        model = FirstName
        exclude = ('added_at', )


class LastNameResource(CustomResource):

    '''Resource class for first name.'''

    class Meta:
        model = LastName
        exclude = ('added_at', )


class AboutResource(CustomResource):

    '''Resource class for about user.'''

    class Meta:
        model = About
        exclude = ('added_at', )


class LocationResource(CustomResource):

    '''Resource class for location.'''

    class Meta:
        model = Location
        exclude = ('added_at', )


class BoardResource(CustomResource):

    '''Resource class for board.'''

    class Meta:
        model = Board
        exclude = ('added_at', )


class CommentResource(CustomResource):

    '''Resource class for comment.'''

    class Meta:
        model = Comment
        exclude = ('added_at', )


class KeywordResource(CustomResource):

    '''Resource class for keyword.'''

    class Meta:
        model = Keyword
        exclude = ('added_at', )
