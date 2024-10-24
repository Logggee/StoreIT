# forms.py
from django import forms

class Store_Item_Form(forms.Form):
    item_image_file = forms.FileField(label='Picture', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'item-image-file',
    }))
    
    item_name = forms.CharField(max_length=255, label='Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'item-name',
        'placeholder': 'Item name'
    }))
    
    item_quantity = forms.IntegerField(label='Quantity', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'item-quantity',
        'placeholder': 'Quantity to be stored'
    }))
    
    item_volume = forms.IntegerField(label='Volume', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'item-volume',
        'placeholder': 'Volume of the item/s'
    }))
    
    item_node = forms.CharField(label='Node', required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'item-node',
        'placeholder': 'Optional nodes',
        'rows': 1
    }))
    
    item_datasheet = forms.URLField(label='Datasheet', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'item-datasheet',
        'placeholder': 'Optional datasheet'
    }))
    
    item_purchase_place = forms.URLField(label='Purchase place', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'item-purchase-place',
        'placeholder': 'Optional link to purchase place'
    }))
