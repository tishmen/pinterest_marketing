from django import forms

from pinterest.models import User
from store.models import (
    About, Email, FirstName, LastName, Location, Proxy, UserAgent
)


class UserAdminForm(forms.ModelForm):

    '''Custom user admin form with pre-set initial values.'''

    class Meta:
        model = User
        fields = (
            'proxy', 'user_agent', 'email', 'password', 'name', 'age',
            'username', 'photo', 'about', 'location', 'repins', 'likes',
            'comments', 'followers', 'following'
        )

    def __init__(self, *args, **kwargs):
        if not kwargs.get('instance'):
            kwargs.update(initial=self.get_initial())
        super(UserAdminForm, self).__init__(*args, **kwargs)

    def get_initial(self):
        '''Return initial values dictionary from random store data.'''
        name = User.get_name(FirstName.random.first(), LastName.random.first())
        age = User.get_age()
        return {
            'proxy': Proxy.random.first(),
            'user_agent': UserAgent.random.first(),
            'email': Email.random.first(),
            'password': User.get_password(),
            'name': name,
            'age': age,
            'username': User.get_username(name, age),
            'about': About.random.first(),
            'location': Location.random.first(),
            'photo': User.get_photo(),
        }
