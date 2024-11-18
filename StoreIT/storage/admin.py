from django.contrib import admin
from .models import Item, Storage, Bin, Stored_Item, User
from django.contrib.auth.admin import UserAdmin
from .forms import User_Registration_Form, User_Change_Form

class User_Admin(UserAdmin):
    # Defines which form is used for adding users
    add_form = User_Registration_Form
    # Defines which form is used to change existing user data
    form = User_Change_Form

    # This adds the possibility to filter for costum fields
    list_filter = UserAdmin.list_filter + ('email',)

    # This defines which fiels are shown for the add new user form
    # Here all standart fields plus the email field is shown
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ("email", "first_name", "last_name",)}),
    )
    
admin.site.register(Item)
admin.site.register(Storage)
admin.site.register(Bin)
admin.site.register(Stored_Item)
admin.site.register(User, User_Admin)