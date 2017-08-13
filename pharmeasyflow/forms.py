from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    CATEG = (
             ("doctor", ("doctor")),
             ("patient", ("patient")),
             ("pharmacist", ("pharmacist"))
            )
    category = forms.ChoiceField(choices=CATEG, label="category")

    class Meta:
        model = User
        fields = ('username', 'name', 'category', 'password1', 'password2', )

