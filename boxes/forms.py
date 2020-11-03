from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from boxes.models import Person


class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Proszę podać poprawne Imię i Hasło. Wielkość liter ma znaczenie!"
        ),
        'inactive': ("Konto nie istnieje."),
    }

    class Meta:
        model = Person

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Imię'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Hasło', 'name': 'Hasło'})

# class StudentRegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=50)
#     second_name = forms.CharField(max_length=50,required=False, )
#     last_name = forms.CharField(max_length=50)
#
#     class Meta():
#         model = Person
#
#     def __init__(self, *args, **kwargs):
#         super(StudentRegisterForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Imię'})
#         self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Hasło', 'name': 'Hasło'})
#
#
#     @transaction.atomic
#     def save(self, **kwargs):
#         user = super().save(commit=False)
#         user.is_student = True
#         user.first_name = self.cleaned_data.get('first_name')
#         user.middle_name = self.cleaned_data.get('middle_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#         student = Person.objects.create(user=user)
#         student.my_class = self.cleaned_data.get('student_class')
#         student.save()
#         return user
