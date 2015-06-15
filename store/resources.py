from import_export import resources

from store.models import (
    Email, Proxy, UserAgent, FirstName, LastName, About, Location, Board,
    Keyword, Comment
)


class EmailResource(resources.ModelResource):

    '''Resource class for email.'''

    class Meta:
        model = Email
        exclude = ('added_at', )


class ProxyResource(resources.ModelResource):

    '''Resource class for proxy.'''

    class Meta:
        model = Proxy
        exclude = ('added_at', )


class UserAgentResource(resources.ModelResource):

    '''Resource class for user agent.'''

    class Meta:
        model = UserAgent
        exclude = ('added_at', )


class FirstNameResource(resources.ModelResource):

    '''Resource class for first name.'''

    class Meta:
        model = FirstName
        exclude = ('added_at', )


class LastNameResource(resources.ModelResource):

    '''Resource class for first name.'''

    class Meta:
        model = LastName
        exclude = ('added_at', )


class AboutResource(resources.ModelResource):

    '''Resource class for about.'''

    class Meta:
        model = About
        exclude = ('added_at', )


class LocationResource(resources.ModelResource):

    '''Resource class for location.'''

    class Meta:
        model = Location
        exclude = ('added_at', )


class BoardResource(resources.ModelResource):

    '''Resource class for board.'''

    class Meta:
        model = Board
        exclude = ('added_at', )


class KeywordResource(resources.ModelResource):

    '''Resource class for keyword.'''

    class Meta:
        model = Keyword
        exclude = ('scraped', 'added_at', )


class CommentResource(resources.ModelResource):

    '''Resource class for comment.'''

    class Meta:
        model = Comment
        exclude = ('added_at', )
