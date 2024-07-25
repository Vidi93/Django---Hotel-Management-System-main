from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Employee, CustomUser
from .models import *


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password1']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class CreateEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = PhoneNumberField()
    salary = forms.FloatField()

    class Meta:
        model = Employee
        fields = ['salary']

    def save(self, commit=True):
        user_data = self.cleaned_data
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        custom_user = CustomUser.objects.create(
            user=user,
            phone_number=user_data['phone_number']
        )
        employee = super().save(commit=False)
        employee.custom_user = custom_user
        if commit:
            employee.save()
        return employee


class editEmployee(ModelForm):
    class Meta:
        model = Employee
        fields = ["phoneNumber", "salary"]


class editUser(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class editGuest(ModelForm):
    class Meta:
        model = Guest
        fields = ["phoneNumber"]


class ROLES(forms.Form):
    ROLES_TYPES = [
        ('manager', 'manager'),
        ('receptionist', 'receptionist'),
        ('staff', 'staff'),
    ]
    ROLES_TYPES = forms.CharField(
        widget=forms.RadioSelect(choices=ROLES_TYPES))
