import random

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View

from boxes.forms import UserLoginForm
from boxes.models import Person


def index(request):
    return render(request, 'index.html')


@login_required
def profile_page(request):
    current_user = Person.objects.get(username=request.user.username)
    context = {
        'header_1': 'O mnie',
        'person': current_user
    }
    return render(request, 'profile.html', context)


@login_required
def random_page(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get('losuj_button'):
            current_user = Person.objects.get(username=request.user.username)

            if current_user.chosen_person is None:
                possible_users = Person.objects.all() \
                    .exclude(family=current_user.family) \
                    .filter(is_chosen=False)

                if possible_users:
                    random_person = random.choice(possible_users)
                    random_person.is_chosen = True
                    random_person.save()
                    current_user.chosen_person = random_person
                    current_user.save()
                else:
                    messages.error(request,
                                   'Poważny konflikt interesów! Brak wolnych losów! Skontaktuj się z pomocą techniczną!')
            else:
                messages.error(request, 'Już wylosowano! Jeden prezent do kupienia wystarczy!')

    return render(request, 'losuj.html', {})


@login_required
def logout_view(request):
    logout(request)
    return redirect('boxes:login')


class CustomLoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {'form': UserLoginForm})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(request, 'registration/login.html', {'form': form, 'invalid_creds': True})
            login(request, form.get_user())
            return redirect('boxes:user_profile')

        return render(request, 'registration/login.html', {'form': form})
