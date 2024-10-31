# forms.py
from .models import Stored_Item
from . import models
from django import forms
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404

class Store_Item_Form(forms.Form):

    item_image_file = forms.ImageField(label='Item image',
                                       required=True,
                                       allow_empty_file=False,
                                       widget=forms.FileInput(attrs={'class': 'form-control',
                                                                     'id': 'item-image-file'}))
    
    item_name = forms.CharField(max_length=models.MAX_ITEM_NAME_LENGTH,
                                min_length=1,
                                label='Item name',
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'id': 'item-name',
                                                              'placeholder': 'Item name',
                                                              'required': 'true'
    }))
    
    item_quantity = forms.IntegerField(min_value=1,
                                       label='Item quantity', 
                                       widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                       'id': 'item-quantity',
                                                                       'placeholder': 'Quantity to be stored',
                                                                       'required': 'true'
    }))
    
    item_volume = forms.IntegerField(label='Item volume',
                                     required=True,
                                     widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                     'id': 'item-volume',
                                                                     'placeholder': 'Volume of the item/s'
    }))
    
    item_node = forms.CharField(max_length=models.MAX_ITEM_NODE_LENGTH,
                                label='Item node',
                                required=False,
                                widget=forms.Textarea(attrs={'class': 'form-control',
                                                             'id': 'item-node',
                                                             'placeholder': 'Optional nodes',
                                                             'rows': 1   # Minimal height for the text field
    }))
    
    item_datasheet = forms.URLField(max_length=models.MAX_ITEM_DATASHEET_URL_LENGTH,
                                    label='Item datasheet', 
                                    required=False, 
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'id': 'item-datasheet',
                                                                  'placeholder': 'Optional datasheet'
    }))
    
    item_purchase_place = forms.URLField(label='Item purchase place',
                                         required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'id': 'item-purchase-place',
                                                                       'placeholder': 'Optional link to purchase place'
    }))

    # In invalid case the bootstrap clase is-invalid needs to be added
    # to the form elements
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add's the class is-invalid
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
        #TODO this only works if a item is just i one stored_item
        input_quantity = self.cleaned_data.get("item_destore_quantity")

        if self.stored_item_fk:
            # Check if the user wants to destore more as exists
            if input_quantity > Stored_Item.get_total_stored_quantity_of_one_item(self.stored_item_fk):
                raise forms.ValidationError(
                    "You can only destore what's there!"
                )
        return input_quantity
