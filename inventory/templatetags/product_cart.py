from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    print(keys)
    valu = cart.values()
    print(cart.get('1'))
    for id in keys:
        if int(id) == product.id:
            print(int(id), product.id)
            print(cart.get(id))
            return True
    return False


@register.filter(name='total_product_after_sale')
def total_product_after_sale(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return product.quantity - cart.get(id)


@register.filter(name='cart_count')
def cart_count(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


@register.filter(name='price_after_discount')
def price_after_discount(product, cart):
    return product.selling_price - (product.selling_price * product.discount_percent / 100)


@register.filter(name='product_total')
def product_total(product, cart):
    return price_after_discount(product, cart) * cart_count(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += product_total(p, cart)
    return sum
