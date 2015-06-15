from django.db import models

from pinterest.models import User, CATEGORIES


class AvailableEmailManager(models.Manager):

    '''Custom manager for email. Return available emails.'''

    def get_queryset(self):
        '''Override get_queryset model manager method.'''
        ids = [user.email.id for user in User.objects.all()]
        return super(AvailableEmailManager, self).get_queryset().exclude(
            id__in=ids
        )


class AvailableProxyManager(models.Manager):

    '''Custom manager for proxy. Return available proxies.'''

    def get_queryset(self):
        '''Override get_queryset model manager method.'''
        ids = [user.proxy.id for user in User.objects.all() if user.proxy]
        return super(AvailableProxyManager, self).get_queryset().exclude(
            id__in=ids
        )


class RandomManager(models.Manager):

    '''Custom manager. Return rows in random order.'''

    def get_queryset(self):
        '''Override get_queryset model manager method.'''
        return super(RandomManager, self).get_queryset().order_by('?')


class Email(models.Model):

    '''Main storage for email.'''

    address = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    available = AvailableEmailManager()

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
    available = AvailableProxyManager()

    def __str__(self):
        return '{}:{}'.format(self.host, self.port)


class UserAgent(models.Model):

    '''Main storage for user agent.'''

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

    '''Main storage for about.'''

    about = models.CharField(max_length=160, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.about


class Location(models.Model):

    '''Main storage for location.'''

    location = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.name


class Keyword(models.Model):

    '''Main storage for keyword.'''

    class Meta:
        unique_together = ('keyword', 'category')

    keyword = models.TextField()
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword


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

    def __str__(self):
        return self.comment
