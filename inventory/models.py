import datetime

from django.db import models


class DealerInformation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=14)
    phone2 = models.CharField(max_length=14)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AddProduct(models.Model):
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')
    bar_code = models.ImageField(upload_to='bar_code/', blank=True, null=True)
    total_product = models.IntegerField(default=0)
    issue_quantity = models.IntegerField(null=True, blank=True)
    purchase_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0, blank=True, null=True)
    dealer = models.ForeignKey(DealerInformation, on_delete=models.CASCADE)
    total_investment_made = models.IntegerField(default=0, null=True, blank=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    purchase_date = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return self.product_name


class Sales(models.Model):
    sold_product_name = models.CharField(max_length=100, blank=True, null=True)
    sold_product_image = models.ImageField(upload_to='sold_product_images/', blank=True, null=True)
    sold_product_quantity = models.IntegerField(default=0, blank=True, null=True)
    sold_product_price_per_product = models.FloatField(blank=True, null=True)
    sold_product_price = models.FloatField(blank=True, null=True)
    total_sales_done = models.FloatField(default=0, null=True, blank=True)


class Order(models.Model):
    order_customer_name = models.CharField(max_length=50)
    order_product_name = models.CharField(max_length=100)
    order_quantity = models.IntegerField()
    order_per_product_price = models.IntegerField()
    order_total_product_price = models.IntegerField()
    order_date = models.DateField(default=datetime.datetime.today)
