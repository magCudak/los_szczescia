import random

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View

from boxes.forms import UserLoginForm
from boxes.models import Person, Changer


def index(request):
    return render(request, 'index.html')


@login_required
def profile_page(request):
    current_user = Person.objects.get(username=request.user.username)
    context = {
        'person': current_user
    }
    return render(request, 'profile.html', context)


@login_required
def random_page(request):
    chosen_person = None
    if request.method == "POST":
        if request.POST.get('losuj_button'):
            current_user = Person.objects.get(username=request.user.username)
            if current_user.chosen_person is None:
                possible_users = Person.objects.all() \
                    .exclude(family=current_user.family) \
                    .filter(is_chosen=False) \
                    .exclude(is_superuser=True)
                if possible_users:
                    random_person = random.choice(possible_users)
                    random_person.is_chosen = True
                    random_person.save()
                    current_user.chosen_person = random_person
                    current_user.save()
                else:
                    messages.error(request,
                                   'Poważny konflikt interesów! Brak wolnych losów! '
                                   'Skontaktuj się z pomocą techniczną!')
            else:
                messages.error(request, 'Już wylosowano! Jeden prezent do kupienia wystarczy!')
        if request.POST.get('check'):
            current_user = Person.objects.get(username=request.user.username)
            if current_user.chosen_person is None:
                messages.error(request,
                               'Jeszcze nie ma wylosowanej osoby! Sprawdź później.')
            else:
                chosen_person = current_user.chosen_person

        if request.POST.get('ha'):
            current_user = Person.objects.get(username=request.user.username)

            while True:
                people = Person.objects.all().exclude(is_superuser=True)
                current_per = random.choice(people)
                if current_per.chosen_person is None:
                    possible_users = Person.objects.all() \
                        .exclude(family=current_per.family) \
                        .filter(is_chosen=False) \
                        .exclude(is_superuser=True)
                    if possible_users:
                        random_person = random.choice(possible_users)
                        random_person.is_chosen = True
                        random_person.save()
                        current_per.chosen_person = random_person
                        current_per.save()
                        print(current_per)
                    else:
                        messages.error(request,
                                       'Poważny konflikt interesów! Brak wolnych losów! '
                                       'Skontaktuj się z pomocą techniczną! %s' % current_per.username)

        if request.POST.get('clean'):
            current_user = Person.objects.get(username=request.user.username)
            people = Person.objects.all().exclude(is_superuser=True)
            people.update(is_chosen=False)
            people.update(chosen_person=None)

        if request.POST.get('supercheck'):
            print("supercheck")
            current_user = Person.objects.get(username=request.user.username)
            people = Person.objects.all().exclude(is_superuser=True)
            for person in people:
                print(person)
                if person.chosen_person is not None:
                    chosen_person_family = person.chosen_person.family.family_name
                    person_family = person.family.family_name

                    if chosen_person_family == person_family:
                        messages.error(request,
                                       'Błąd w losowaniu :( '
                                       '%s == %s' % (chosen_person_family, person_family))
                    else:
                        messages.success(request, "Poprawne dopasowanie!")
                else:
                    messages.info(request, "Nie wylosowano!")

        if request.POST.get("superchange"):
            current_changer = Changer.objects.all()[0]
            current_changer.update(possible=(not current_changer))
            print(current_changer.possible)

    return render(request, 'losuj.html', {'goal': chosen_person})


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
