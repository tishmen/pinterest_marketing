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


class Id(models.Model):

    '''Main storage for id.'''

    id = models.BigIntegerField(primary_key=True, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Username(models.Model):

    '''Main storage for username.'''

    username = models.CharField(max_length=15, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class User(models.Model):

    '''Main storage for user.'''

    proxy = models.OneToOneField('store.Proxy', null=True, blank=True)
    user_agent = models.ForeignKey('store.UserAgent')
    email = models.OneToOneField('store.Email')
    password = models.CharField(max_length=10)
    name = models.TextField()
    username = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField()
    photo = models.FilePathField(path=PHOTO_DIR, unique=True)
    about = models.CharField(max_length=160)
    location = models.TextField()
    repins = models.ManyToManyField('Id', related_name='+')
    likes = models.ManyToManyField('Id', related_name='+')
    comments = models.ManyToManyField('Id', related_name='+')
    following = models.ManyToManyField('Username', related_name='+')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


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
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
