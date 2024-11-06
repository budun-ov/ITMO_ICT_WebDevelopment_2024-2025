from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Owner
from .models import Ownership
from .models import DriverLicense
from .models import Car
from .models import User
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('passport_number', 'address', 'nationality')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Owner)
admin.site.register(DriverLicense)
admin.site.register(Ownership)
admin.site.register(Car)
