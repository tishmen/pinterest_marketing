
from django.db import models

from bot.models import CATEGORIES, User


class RandomEmailManager(models.Manager):

    def get_queryset(self):
        ids = [user.email.id for user in User.objects.all()]
        queryset = super(RandomEmailManager, self).get_queryset()
        return queryset.exclude(id__in=ids).order_by('?')


class RandomProxyManager(models.Manager):

    def get_queryset(self):
        ids = [user.proxy.id for user in User.objects.all() if user.proxy]
        queryset = super(RandomProxyManager, self).get_queryset()
        return queryset.exclude(id__in=ids).order_by('?')


class RandomManager(models.Manager):

    def get_queryset(self):
        queryset = super(RandomManager, self).get_queryset()
        return queryset.order_by('?')


class Email(models.Model):

    host = models.TextField()
    port = models.PositiveIntegerField()
    address = models.EmailField(unique=True)
    password = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomEmailManager()

    def __str__(self):
        return self.address


class Proxy(models.Model):

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

    string = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.string


class FirstName(models.Model):

    name = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.name


class LastName(models.Model):

    name = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.name


class About(models.Model):

    about = models.CharField(max_length=160, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.about


class Location(models.Model):

    location = models.TextField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.location


class Board(models.Model):

    class Meta:
        unique_together = ('name', 'description')

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.name


class Comment(models.Model):

    class Meta:
        unique_together = ('comment', 'category')

    comment = models.CharField(max_length=500)
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.comment


class Keyword(models.Model):

    class Meta:
        unique_together = ('keyword', 'category')

    keyword = models.TextField()
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.keyword

    def url(self):
        return 'https://www.pinterest.com/search/?q={}'.format(
            self.keyword.replace(' ', '+')
        )
