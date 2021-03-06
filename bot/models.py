import os
import random
import string

from django.db import models
from django.conf import settings

CATEGORIES = [
    'animals', 'architecture', 'art', 'cars_motorcycles', 'celebrities',
    'design', 'diy_crafts', 'education', 'film_music_books', 'food_drink',
    'gardening', 'geek', 'hair_beauty', 'health_fitness', 'history',
    'holidays_events', 'home_decor', 'humor', 'illustrations_posters', 'kids',
    'mens_fashion', 'outdoors', 'photography', 'products', 'quotes',
    'science_nature', 'sports', 'tattoos', 'technology', 'travel', 'weddings',
    'womens_fashion', 'other'
]


class RandomUserManager(models.Manager):

    def get_queryset(self):
        queryset = super(RandomUserManager, self).get_queryset()
        return queryset.exclude(cookies='[]').order_by('?')


class RandomManager(models.Manager):

    def get_queryset(self):
        queryset = super(RandomManager, self).get_queryset()
        return queryset.order_by('?')


class User(models.Model):

    proxy = models.OneToOneField('data.Proxy', null=True, blank=True)
    user_agent = models.ForeignKey('data.UserAgent')
    email = models.OneToOneField('data.Email')
    password = models.CharField(max_length=10)
    name = models.TextField()
    age = models.PositiveIntegerField()
    username = models.CharField(max_length=15, unique=True)
    photo = models.FilePathField(path=settings.PHOTO_DIR, unique=True)
    about = models.CharField(max_length=160)
    location = models.TextField()
    cookies = models.TextField(default='[]')
    board_count = models.PositiveIntegerField(default=0)
    pin_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomUserManager()

    @staticmethod
    def get_name(first, last):
        if first and last:
            return '{} {}'.format(first, last)

    @staticmethod
    def get_age():
        return random.randint(20, 60)

    @staticmethod
    def get_password():
        alphanumerics = string.ascii_letters + string.digits
        return ''.join(random.choice(alphanumerics) for _ in range(10))

    @staticmethod
    def get_username(name, age):
        if name:
            return '{}{}'.format(name.replace(' ', '').lower()[:11], age)

    @staticmethod
    def get_photo():
        photos = [
            os.path.join(settings.PHOTO_DIR, f)
            for f in os.listdir(settings.PHOTO_DIR)
        ]
        bound = [user.photo for user in User.objects.all()]
        available = [photo for photo in photos if photo not in bound]
        if available:
            return random.choice(available)

    def __str__(self):
        return self.username

    def url(self):
        return 'https://www.pinterest.com/{}/'.format(self.username)

    def following_url(self):
        return 'https://www.pinterest.com/{}/following/'.format(self.username)


class Board(models.Model):

    class Meta:
        unique_together = ('user', 'name', 'description')

    user = models.ForeignKey('User')
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=21,
        choices=((category, category) for category in CATEGORIES)
    )
    description = models.CharField(max_length=500)
    pin_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.name

    def url(self):
        return 'https://www.pinterest.com/{}/{}'.format(
            self.user, self.name.replace(' ', '-').lower()[:50]
        )
