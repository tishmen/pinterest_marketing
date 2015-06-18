import os
import random
import string

from django.db import models

from pinterest_marketing.settings import PHOTO_DIR

CATEGORIES = [
    'animals', 'architecture', 'art', 'cars_motorcycles', 'celebrities',
    'design', 'diy_crafts', 'education', 'film_music_books', 'food_drink',
    'gardening', 'geek', 'hair_beauty', 'health_fitness', 'history',
    'holidays_events', 'home_decor', 'humor', 'illustrations_posters', 'kids',
    'mens_fashion', 'outdoors', 'photography', 'products', 'quotes',
    'science_nature', 'sports', 'tattoos', 'technology', 'travel', 'weddings',
    'womens_fashion', 'other'
]


class AvailableUserManager(models.Manager):

    '''Custom manager for user. Return available users.'''

    def get_queryset(self):
        '''Override model manager get_queryset method.'''
        queryset = super(AvailableUserManager, self).get_queryset()
        return queryset.exclude(cookies='[]')


class RandomManager(models.Manager):

    '''Custom manager. Return rows in random order.'''

    def get_queryset(self):
        '''Override model manager get_queryset method.'''
        queryset = super(RandomManager, self).get_queryset()
        return queryset.order_by('?')


class User(models.Model):

    '''Main storage for user.'''

    proxy = models.OneToOneField('store.Proxy', null=True, blank=True)
    user_agent = models.ForeignKey('store.UserAgent')
    email = models.OneToOneField('store.Email')
    password = models.CharField(max_length=10)
    name = models.TextField()
    age = models.PositiveIntegerField()
    username = models.CharField(max_length=15, unique=True)
    photo = models.FilePathField(path=PHOTO_DIR, unique=True)
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
    available = AvailableUserManager()

    @staticmethod
    def get_name(first, last):
        '''Return full name.'''
        return '{} {}'.format(first, last)

    @staticmethod
    def get_age():
        '''Return random age.'''
        return random.randint(20, 60)

    @staticmethod
    def get_password():
        '''Return random alphanumeric password.'''
        alphanumerics = string.ascii_letters + string.digits
        return ''.join(random.choice(alphanumerics) for _ in range(10))

    @staticmethod
    def get_username(name, age):
        '''Return username from name and age.'''
        return '{}{}'.format(name.replace(' ', '').lower()[:11], age)

    @staticmethod
    def get_photo():
        '''Return available photo.'''
        photos = [os.path.join(PHOTO_DIR, f) for f in os.listdir(PHOTO_DIR)]
        bound = [user.photo for user in User.objects.all()]
        available = [photo for photo in photos if photo not in bound]
        if available:
            return random.choice(available)

    def __str__(self):
        '''Override model string method.'''
        return self.username

    def url(self):
        '''Return pinterest user url'''
        return 'https://www.pinterest.com/{}/'.format(self.username)

    def following_url(self):
        '''Return pinterest user following url'''
        return 'https://www.pinterest.com/{}/following/'.format(self.username)


class Board(models.Model):

    '''Main storage for pinterest board.'''

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
        '''Override model string method.'''
        return self.name

    def url(self):
        '''Return pinterest board url'''
        return 'https://www.pinterest.com/{}/{}'.format(
            self.user, self.name.replace(' ', '-').lower()[:50]
        )
