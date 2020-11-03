from django.contrib import admin

from boxes.models import Person, Family
from django.contrib.auth.admin import Group, GroupAdmin, UserAdmin

admin.site.unregister(Group)


class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0


@admin.register(Group)
class GenericGroup(GroupAdmin):
    inlines = [UserInLine]


class MyUserAdmin(admin.ModelAdmin):
    class Metal:
        model = UserAdmin


admin.site.register(Person, MyUserAdmin)

admin.site.register(Family)
