from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     categories = cleaned_data.get('categories')
    #     if categories and categories.filter(parent=None).exists():
    #         raise ValidationError("Product cannot be associated with root categories. Assign valid subcategories.")
    #     return cleaned_data
    
    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')

        # Check if there are any root categories (categories with no parent)
        if categories and categories.filter(parent=None).exists():
            # Get the offending categories
            root_categories = categories.filter(parent=None)
            category_names = ", ".join([cat.name for cat in root_categories])  # Collect their names
            raise ValidationError(
                f"Product cannot be associated with root categories. "
                f"The following categories are root categories: {category_names}. "
                f"Please assign valid subcategories."
            )
        
        return cleaned_data
