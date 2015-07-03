from django import forms

from data.models import (
    About, Email, FirstName, LastName, Location, Proxy, UserAgent
)

from .models import User


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('cookies', )

    def __init__(self, *args, **kwargs):
        if not kwargs.get('instance'):
            kwargs.update(initial=self.get_initial())
        super(UserAdminForm, self).__init__(*args, **kwargs)

    def get_initial(self):
        '''Return user initial values dict.'''
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
