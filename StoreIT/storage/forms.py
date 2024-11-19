# forms.py
import re
from django import forms
from .models import Stored_Item, Item, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class User_Registration_Form_Django_Admin(UserCreationForm):
    """ Costum user registaration form

    This form is only used for the django admin side.
    A costum user registration form. This is needed because the application is overwriting the standart auth.User modal.
    This is done to have better costumisation options of users in the future.

    Inherits:
        UserCreationForm
    """
    # Django standart form doesnt include a email field
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use!")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name.isalpha():
            raise forms.ValidationError("Your first name can only contain letters!")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name.isalpha():
            raise forms.ValidationError("Your last name can only contain letters!")
        return last_name
    
    class Meta:
        model = User
        fields = ["username",
                  "email",
                  "first_name",
                  "last_name",
                  "password1",
                  "password2",]
        
class User_Registration_Form(UserCreationForm):
    """ Costum user registaration form

    This form is used for User registration on the webside.
    A costum user registration form. This is needed because the application is overwriting the standart auth.User modal.
    This is done to have better costumisation options of users in the future.

    Inherits:
        UserCreationForm
    """
    # Django standart form doesnt include a email field
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-lg",
            "id": "registration-email",
            "type": "email",
            "placeholder": "Email"
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "id": "registration-first-name",
            "type": "text",
            "placeholder": "First Name"
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "id": "registration-last-name",
            "type": "text",
            "placeholder": "Last Name"
        })
    )
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "id": "registration-username",
            "type": "text",
            "placeholder": "Username"
        })
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "id": "registration-password1",
            "type": "password",
            "placeholder": "Password"
        })
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "id": "registration-password2",
            "type": "password",
            "placeholder": "Confirm Password"
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use!")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name.isalpha():
            raise forms.ValidationError("Your first name can only contain letters!")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not last_name.isalpha():
            raise forms.ValidationError("Your last name can only contain letters!")
        return last_name
    
    class Meta:
        model = User
        fields = ["username",
                  "email",
                  "first_name",
                  "last_name",
                  "password1",
                  "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In invalid case the bootstrap clase is-invalid needs to be added
        # to the form elements
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                # Fetches to current classes
                css_classes = field.widget.attrs.get('class', '')
                # Add to the current classes is-invalid
                field.widget.attrs['class'] = f'{css_classes} is-invalid'
        
class User_Login_Form(AuthenticationForm):
    """ Login form

    This form is used for the user login. The standart AuthenticationForm
    is used except some bootstrap styling that is added to the fields.

    Inherits:
        AuthenticationForm
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                      "id": "login-username",
                                      "type": "text",
                                      "placeholder": "Username"})
    )

    password = forms.CharField(
        widget = forms.PasswordInput(attrs={"class": "form-control form-control-lg",
                                          "id": "login-password",
                                          "type": "password",
                                          "placeholder": "Password"})
    )

class User_Change_Form(UserChangeForm):
    """ Form for changing current user data
    """
    class Meta:
        model = User
        fields = ["username",
                  "email",
                  "first_name",
                  "last_name"]

class Store_Item_Form(forms.ModelForm):
    item_quantity = forms.IntegerField(min_value=1,
                                       label='Item quantity', 
                                       widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                       'id': 'item-quantity',
                                                                       'placeholder': 'Quantity to be stored',
                                                                       'required': 'true'
    }))

    class Meta:
        model = Item
        fields = [
            'item_name', 'item_image', 'item_volume', 'item_node', 'item_datasheet', 'item_purchase_place'
        ]

        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'item-name',
                'placeholder': 'Item name',
                'required': 'true'
            }),
            'item_image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'item-image'
            }),
            'item_volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'item-volume',
                'placeholder': 'Volume of the item/s'
            }),
            'item_node': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'item-node',
                'placeholder': 'Optional nodes',
                'rows': 1
            }),
            'item_datasheet': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'item-datasheet',
                'placeholder': 'Optional datasheet'
            }),
            'item_purchase_place': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'item-purchase-place',
                'placeholder': 'Optional link to purchase place'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In invalid case the bootstrap clase is-invalid needs to be added
        # to the form elements
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                # Fetches to current classes
                css_classes = field.widget.attrs.get('class', '')
                # Add to the current classes is-invalid
                field.widget.attrs['class'] = f'{css_classes} is-invalid'

class Destore_Item_Form(forms.Form):
    # TODO: id if this field is not unique
    item_destore_quantity = forms.IntegerField(label='Item destore quantity',
                                               min_value=1,
                                               required=True,
                                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                               'id': 'item-destore-quantity',
                                                                               'placeholder': '0'
    }))

    def __init__(self, *args,  stored_item_fk=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.stored_item_fk = stored_item_fk
        # In invalid case the bootstrap clase is-invalid needs to be added
        # to the form elements
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                # Fetches to current classes
                css_classes = field.widget.attrs.get('class', '')
                # Add to the current classes is-invalid
                field.widget.attrs['class'] = f'{css_classes} is-invalid'

    def clean_item_destore_quantity(self):
        input_quantity = self.cleaned_data.get("item_destore_quantity")

        if self.stored_item_fk:
            # Check if the user wants to destore more as exists
            if input_quantity > Stored_Item.get_total_stored_quantity_of_one_item(self.stored_item_fk):
                raise forms.ValidationError(
                    "You can only destore what's there!"
                )
        return input_quantity
    
class Storage_Layout_Form(forms.Form):
    storage_rows = forms.IntegerField(label="Number of storage rows",
                                      min_value=1,
                                      max_value=99,
                                      required=True,
                                      widget=forms.NumberInput(attrs={"type": "number",
                                                                      "class": "form-control",
                                                                      "id": "storage-rows",
                                                                      "name": "storage-row-input",
                                                                      "placeholder": "n rows",
                                                                      "min": "1",
                                                                      "max:": "99",
                                                                      "oninput": "generateCollumnInputFields(this)",
                                                                      'required': 'true'}))
    
    def __init__(self, *args, **kwargs):
        super(Storage_Layout_Form, self).__init__(*args, **kwargs)
        # In invalid case the bootstrap clase is-invalid needs to be added
        # to the form elements
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                # Fetches to current classes
                css_classes = field.widget.attrs.get('class', '')
                # Add to the current classes is-invalid
                field.widget.attrs['class'] = f'{css_classes} is-invalid'

        #print(f"Args: {args}")
        #print(f"Kwargs: {kwargs}")

        if len(args) != 0:
            form_data = args[0]
            
            for field, value in form_data.items():
                if "number-of-bins-row-" in field:
                    match = re.search(r'-(\d+)$', field)
                    row_number = int(match.group(1))
                    self.fields[field] = forms.IntegerField(label="Number of bins in row " + str(row_number),
                                                            min_value=1,
                                                            max_value=20,
                                                            required=True,
                                                            initial=value,
                                                            widget=forms.NumberInput(attrs={"type": "number",
                                                                                            "class": "form-control",
                                                                                            "id": "storage-rows",
                                                                                            "name": field,
                                                                                            "placeholder": "n bins",
                                                                                            "min": "1",
                                                                                            "max:": "20",
                                                                                            "oninput": "generateStorageLayout(this, i+1)",
                                                                                            'required': 'true'}))
        #print(f"All fields: {self.fields}")