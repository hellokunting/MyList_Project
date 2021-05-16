from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
  email = forms.EmailField(max_length=150, required=True)

  class Meta:
    model = User
    fields = ['username',
              'email', 'password1', 'password2']

  def save(self, commit=True):
    user = super(CustomRegisterForm, self).save(commit=False)
    user.email = ['email']

    if commit:
      user.save()

      return user

