from django.contrib import admin

from .models import AddProduct, DealerInformation, Order, Sales


@admin.register(AddProduct)
class AdminAddProduct(admin.ModelAdmin):
    list_display = ['product_name', 'product_image', 'bar_code', 'total_product', 'purchase_price', 'selling_price',
                    'discount_percent'
                    ]

    search_fields = ['product_name']


@admin.register(DealerInformation)
class AdminDealerInformation(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['order_product_name']


@admin.register(Sales)
class AdminSales(admin.ModelAdmin):
    list_display = ['sold_product_name']
