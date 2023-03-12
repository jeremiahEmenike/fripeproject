from django.urls import path
from . import views
app_name= 'cart'

urlpatterns= [
	path('', views.cart_detail, name='cart_detail'),
	path('add/<int:product_id>/', views.cart_add, name= 'cart_add'),
	path('remove/<int:product_id>/', views.cart_remove, name= 'cart_remove'),
 	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	# path('checkout/', views.checkout, name='checkout'),
	path('confirmation/', views.confirmation, name='confirmation'),
	path('paysuccess/', views.paysuccess, name='paysuccess'),
 
 
]
