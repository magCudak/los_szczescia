from django.contrib.auth.forms import AuthenticationForm

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
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Pseudonim'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Hasło', 'name': 'Hasło'})
