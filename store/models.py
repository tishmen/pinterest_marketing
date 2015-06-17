from django.db import models

from pinterest.models import CATEGORIES, User
from store.spinner import TextSpinner


class RandomEmailManager(models.Manager):

    '''Custom manager for email. Return available emails in random order.'''

    def get_queryset(self):
        '''Override model manager get_queryset method.'''
        ids = [user.email.id for user in User.objects.all()]
        queryset = super(RandomEmailManager, self).get_queryset()
        return queryset.exclude(id__in=ids).order_by('?')


class RandomProxyManager(models.Manager):

    '''Custom manager for proxy. Return available proxies in random order.'''

    def get_queryset(self):
        '''Override model manager get_queryset method.'''
        ids = [user.proxy.id for user in User.objects.all() if user.proxy]
        queryset = super(RandomProxyManager, self).get_queryset()
        return queryset.exclude(id__in=ids).order_by('?')


class RandomManager(models.Manager):

    '''Custom manager. Return rows in random order.'''

    def get_queryset(self):
        '''Override model manager get_queryset method.'''
        queryset = super(RandomManager, self).get_queryset()
        return queryset.order_by('?')


class Email(models.Model):

    '''Main storage for email.'''

    address = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomEmailManager()

    def __str__(self):
        return self.address


class Proxy(models.Model):

    '''Main storage for proxy.'''

    class Meta:
        verbose_name_plural = 'Proxies'
        unique_together = ('host', 'port')

    host = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomProxyManager()

    def __str__(self):
        return '{}:{}'.format(self.host, self.port)


class UserAgent(models.Model):

    '''Main storage for user-agent.'''

    string = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.string


class FirstName(models.Model):

    '''Main storage for first name.'''

    name = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.name


class LastName(models.Model):

    '''Main storage for last name.'''

    name = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.name


class About(models.Model):

    '''Main storage for about user.'''

    about = models.CharField(max_length=160, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def spin(self):
        '''Return spun content from spintax format.'''
        text_spinner = TextSpinner()
        return text_spinner.spin(self.about)

    def __str__(self):
        return self.about


class Location(models.Model):

    '''Main storage for location.'''

    location = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def spin(self):
        '''Return spun content from spintax format.'''
        text_spinner = TextSpinner()
        return text_spinner.spin(self.location)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.location


class Board(models.Model):

    '''Main storage for board.'''

    class Meta:
        unique_together = ('name', 'description')

    name = models.TextField()
    description = models.TextField()
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def spin_name(self):
        '''Return spun name from spintax format.'''
        text_spinner = TextSpinner()
        return text_spinner.spin(self.name)

    def spin_description(self):
        '''Return spun description from spintax format.'''
        text_spinner = TextSpinner()
        return text_spinner.spin(self.description)

    def __str__(self):
        return self.name


class Comment(models.Model):

    '''Main storage for comment.'''

    class Meta:
        unique_together = ('comment', 'category')

    comment = models.TextField()
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def spin(self):
        '''Return spun content from spintax format.'''
        text_spinner = TextSpinner()
        return text_spinner.spin(self.comment)

    def __str__(self):
        return self.comment


class Keyword(models.Model):

    '''Main storage for keyword.'''

    class Meta:
        unique_together = ('keyword', 'category')

    keyword = models.TextField()
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    scraped = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def search_url(self):
        '''Return pinterest search url for keyword.'''
        return 'https://www.pinterest.com/search/?q={}'.format(
            self.keyword.replace(' ', '+')
        )

    def __str__(self):
        return self.keyword
