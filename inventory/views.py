from django.contrib.auth.forms import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .decorators import allowed_user
from .forms import AddProductForm, DealerForm, SoldForm, ReOrderLevel, AddProductToShop, SearchForm
from .models import AddProduct, Sales, Order


# import for uploading excel file to database.


def dashboard(request):
    if request.user.is_superuser:
        product = AddProduct.objects.all()
        print('i am product')
        print(product)

        products = render(request, 'inventory/index.html', {'name': request.user, 'product': product})
        return products
    else:
        return redirect('/shop/')


@allowed_user(allowed_roles=['Staffs'])
def add_product(request):
    forms = SearchForm(request.POST)
    product = AddProduct.objects.order_by('total_product')
    amount = 0
    for products in product:
        amount += products.purchase_price
    print(amount)

    if request.method == 'POST':
        product = AddProduct.objects.filter(product_name__icontains=forms['product_name'].value())
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = AddProductForm()
            return redirect('/add_product/')
    else:
        form = AddProductForm()
        # print(request.session.get('total_product'))
    paginator = Paginator(product, 8, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory/add_product.html',
                  {'forms': form, 'product': page_obj, 'name': request.user, 'amount': amount})


@allowed_user(allowed_roles=['Staffs'])
def add_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            form.save()
            dealerform = DealerForm()
            return redirect('/add_product/')
    else:
        dealerform = DealerForm()
    return render(request, 'inventory/add_dealer.html', {'forms': dealerform})


def sell_product(request):
    if request.method == 'POST':
        form = AddProduct.object.get('total_product')


@allowed_user(allowed_roles=['Staffs'])
def update_product(request, id):
    if request.method == 'POST':
        get_instance_variable = AddProduct.objects.get(pk=id)
        fm = AddProductForm(request.POST, request.FILES, instance=get_instance_variable)
        print('update running')
        if fm.is_valid():
            print('update is valid')
            fm.save()
        return HttpResponseRedirect('/add_product/')
    else:
        # print(id)
        p = AddProduct.objects.get(pk=id)
        fm = AddProductForm(instance=p)
    return render(request, 'inventory/update_product.html', {'forms': fm})


@allowed_user(allowed_roles=['Staffs'])
def delete_product(request, id):
    fm = AddProduct.objects.get(pk=id)
    fm.delete()
    return HttpResponseRedirect('/add_product/')


@allowed_user(allowed_roles=['Staffs'])
def selling_product(request):
    sell = Sales.objects.all()
    product = AddProduct.objects.all()
    new_total = 0
    for sells in sell:
        new_total += sells.sold_product_price
    return render(request, 'inventory/sells.html', {'products': sell, 'product': product, 'new_total': new_total})


# class OnlineShop(View):
#     def get(self, request):
#         product = AddProduct.objects.all()
#
#         productID = request.GET.get('product')
#         if productID:


def onlineshop(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product = request.POST.get('product')
            remove = request.POST.get('remove')
            cart = request.session.get('cart')
            # print(request.session.get('selling_price'))
            if cart:
                quantity = cart.get(product)
                if quantity:
                    if remove:
                        if quantity == 1:
                            cart.pop(product)
                        else:
                            cart[product] = quantity - 1
                    else:
                        cart[product] = quantity + 1
                else:
                    cart[product] = 1
            else:
                cart = {}
                cart[product] = 1
            # print(cart)
            student = cart
            request.session['cart'] = cart
            # print(student.get('1'))
            return HttpResponseRedirect('/shop/')
        else:
            cart = request.session.get('cart')
            if not cart:
                request.session['cart'] = {}
                print('not')
        product = AddProduct.objects.all()
        in_group = request.user.groups.filter(name='Staffs').exists()
        return render(request, 'inventory/shop.html', {'product': product, 'is_group': in_group})
    else:
        return redirect('/user/login/')


def cart(request):
    if request.user.is_authenticated:
        id = list(request.session.get('cart').keys())
        value = request.session.get('cart')
        print(value)
        print(request.session.get('cart'))
        product = AddProduct.objects.filter(id__in=id)
        if request.method == 'POST':
            form = SoldForm(request.POST)
            if form.is_valid():
                for products in product:
                    sold_product_name = products.product_name
                    product_quantity = int(value.get(str(products.id)))
                    print('I am product quantity' + str(product_quantity))
                    products.total_product -= product_quantity
                    discount = products.discount_percent
                    selling_price_product = products.selling_price
                    price_after_discount = selling_price_product - discount / 100 * selling_price_product
                    actual_price_of_product = price_after_discount * product_quantity
                    sales = Sales(sold_product_name=sold_product_name, sold_product_quantity=product_quantity,
                                  sold_product_price_per_product=price_after_discount,
                                  sold_product_price=actual_price_of_product)

                    products.save()
                    sales.save()

                return redirect('/shop/')
        else:
            return render(request, 'inventory/cart.html', {'product': product})
    else:
        return redirect('/user/login/')


def invoice(request):
    if request.user.is_authenticated:
        id = list(request.session.get('cart').keys())
        value = request.session.get('cart')
        print(request.session.get('cart'))
        product = AddProduct.objects.filter(id__in=id)
        in_group = request.user.groups.filter(name='Staffs').exists()
        if request.method == 'POST':
            form = SoldForm(request.POST)
            if form.is_valid():
                for products in product:
                    sold_product_name = products.product_name
                    product_quantity = int(value.get(str(products.id)))
                    products.total_product -= product_quantity
                    discount = products.discount_percent
                    selling_price_product = products.selling_price
                    price_after_discount = selling_price_product - discount / 100 * selling_price_product
                    actual_price_of_product = price_after_discount * product_quantity
                    sales = Sales(sold_product_name=sold_product_name, sold_product_quantity=product_quantity,
                                  sold_product_price_per_product=price_after_discount,
                                  sold_product_price=actual_price_of_product)
                    products.save()
                    sales.save()

                return redirect('/shop/')
        else:
            return render(request, 'inventory/invoice.html', {'product': product, 'in_group': in_group})
    else:
        return redirect('/user/login/')


def reroder_level(request, id):
    queryset = AddProduct.objects.get(pk=id)
    form = ReOrderLevel(request.POST, instance=queryset)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/add_product/')
    else:

        return render(request, 'inventory/reorder_level.html', {'instance': queryset, 'form': form})


def receive_product(request, id):
    queryset = AddProduct.objects.get(pk=id)
    form = AddProductToShop(request.POST, instance=queryset)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.total_product += instance.issue_quantity
            instance.save()
            return redirect('/add_product/')
    else:
        return render(request, 'inventory/add_product_item.html', {'instance': queryset, 'form': form})


def reorder_detail(request, id):
    products = AddProduct.objects.get(pk=id)

    return render(request, 'inventory/product_scarce_detail.html', {'products': products})


def customer_order(request):
    id = list(request.session.get('cart').keys())
    value = request.session.get('cart')
    product = AddProduct.objects.all()
    for products in product:
        customer = request.user.username
        order_product_name = products.product_name
        product_quantity = int(value.get(str(products.id)))
        product_quantity = int(value.get(str(products.id)))
        discount = products.discount_percent
        selling_price_product = products.selling_price
        price_after_discount = selling_price_product - discount / 100 * selling_price_product
        actual_price_of_product = price_after_discount * product_quantity
        order = Order(order_customer_name=customer, order_product_name=order_product_name,
                      order_quantity=product_quantity,
                      order_per_product_price=price_after_discount
                      , order_total_product_price=actual_price_of_product)
        products.save()
        order.save()
    return redirect('/shop/')


def staffs_in_system(request):
    user = User.objects.filter(groups__name='Staffs')
    return render(request, 'inventory/staffs.html', {'staffs': user})


def order_detail(request):
    order = Order.objects.all()
    return render(request, 'inventory/orders.html', {'orders': order})
