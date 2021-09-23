from import_export import resources

from .models import AddProduct


class AddProductResource(resources.ModelResource):
    class Meta:
        model = AddProduct
