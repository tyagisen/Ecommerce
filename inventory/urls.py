from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('add_product/', views.add_product, name='add_product'),
                  path('dealer/', views.add_dealer, name='dealer'),
                  path('update/<int:id>/', views.update_product, name='update_product'),
                  path('delete/<int:id>/', views.delete_product, name='delete_product'),
                  path('selling/', views.selling_product, name='sell'),
                  path('shop/', views.onlineshop, name='shop'),
                  path('cart/', views.cart, name='cart'),
                  path('invoice/', views.invoice, name='invoice'),
                  path('reorder/<int:id>/', views.reroder_level, name='reorder'),
                  path('receive_product/<int:id>/', views.receive_product, name='receive'),
                  path('reorder_detail/<int:id>/', views.reorder_detail, name='reorder_detail'),
                  path('customer_order/', views.customer_order, name='customer_order'),
                  path('staffs/', views.staffs_in_system, name='staffs'),
                  path('order/', views.order_detail, name='order'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
