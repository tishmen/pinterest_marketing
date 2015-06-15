from django.db import models

from pinterest.models import CATEGORIES


class Email(models.Model):

    '''Main storage for email.'''

    address = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    added_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return '{}:{}'.format(self.host, self.port)


class UserAgent(models.Model):

    '''Main storage for user agent.'''

    string = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.string


class FirstName(models.Model):

    '''Main storage for first name.'''

    name = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LastName(models.Model):

    '''Main storage for last name.'''

    name = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class About(models.Model):

    '''Main storage for about.'''

    about = models.CharField(max_length=160, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Location(models.Model):

    '''Main storage for location.'''

    location = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


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
        return self.username


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
        return self.text
