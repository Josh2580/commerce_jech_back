from django import forms
from django.core.exceptions import ValidationError
from .models import Category

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image', 'parent']

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent and parent.parent is not None:
            raise ValidationError("A subcategory cannot use another subcategory as its parent.")
        return parent
