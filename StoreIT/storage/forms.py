# forms.py
import re
from .models import Stored_Item, Item
from . import models
from django import forms
from django.core.validators import FileExtensionValidator

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

class Destore_Item_Form(forms.Form):
    item_destore_quantity = forms.IntegerField(label='Item volume',
                                               min_value=1,
                                               required=True,
                                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                               'id': 'item-volume',
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
