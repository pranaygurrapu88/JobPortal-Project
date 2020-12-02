from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from .models import Accounts,Invite,Blogging


class AccountRegisterForm(UserCreationForm):
    CHOICES = [("is_employee","Employee"),("is_employer","Employer")]
    user_types = forms.CharField(label="User Type",widget=forms.RadioSelect(choices=CHOICES))

    class Meta:
        model = Accounts
        fields = ["email","first_name","last_name"]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user",)

        widget = {
            "birth_day" : forms.DateInput(attrs={"type" : "date"})
        }

class InviteEmployeeForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ("date","message")

        widgets = {
            "date":forms.DateInput(attrs={"type":"date"})
        }

class BloggingForm(forms.ModelForm):
    class Meta:
        model = Blogging
        fields = ["title" , "img" , "content"]
