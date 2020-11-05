from django.contrib.auth.models import AbstractUser
from django.db import models


class Family(models.Model):
    family_name = models.CharField(max_length=200)


class Person(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name="Pseudonim")
    first_name = models.CharField(max_length=50, verbose_name="Imię")
    second_name = models.CharField(max_length=20, verbose_name="Nazwisko")
    password = models.CharField(max_length=2000, verbose_name="Hasło")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, blank=True, null=True)
    chosen_person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=True, null=True)
    is_chosen = models.BooleanField(default=False)
    is_man = models.BooleanField(default=False)

    def full_name(self):
        return self.first_name + " " + self.second_name

    def __str__(self):
        return self.full_name()


class Changer(models.Model):
    possible = models.BooleanField(default=False)
