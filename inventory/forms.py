from django import forms

from .models import AddProduct, DealerInformation, Sales


class AddProductForm(forms.ModelForm):
    class Meta:
        model = AddProduct
        fields = ['dealer', 'product_name', 'reorder_level', 'total_product', 'purchase_price', 'selling_price',
                  'discount_percent',
                  'product_image', 'bar_code']
        label = {
            'product_name': 'Product Name'
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_product': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_percent': forms.TextInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.TextInput(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bar_code': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class DealerForm(forms.ModelForm):
    class Meta:
        model = DealerInformation
        fields = '__all__'
        label = {
            'name': 'Company Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SoldForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['sold_product_name', 'sold_product_quantity', 'sold_product_price_per_product',
                  'sold_product_price']


class IssueForm(forms.ModelForm):
    class Meta:
        model = AddProduct
        fields = ['total_product']


class ReOrderLevel(forms.ModelForm):
    class Meta:
        model = AddProduct
        fields = ['reorder_level']
        widgets = {
            'reorder_level': forms.TextInput(attrs={'class': 'form-control col-2'}),
        }


class AddProductToShop(forms.ModelForm):
    class Meta:
        model = AddProduct
        fields = ['issue_quantity']
        widgets = {
            'issue_quantity': forms.TextInput(attrs={'class': 'form-control col-2'}),
        }


class SearchForm(forms.ModelForm):
    # export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = AddProduct
        fields = ['product_name']
