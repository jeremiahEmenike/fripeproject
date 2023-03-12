from decimal import Decimal
from django.conf import settings
from onlineshop.models import Product
import locale


# locale.setlocale(locale.LC_ALL, 'USA')

class Cart(object):
	def __init__(self,request):
		"""Initializing Cart"""
		self.session=request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart= self.session[settings.CART_SESSION_ID]={}
		self.cart=cart

	def add(self, product, quantity=1, overrride_quantity=False):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id]={'quantity':0, 'price':str(product.price)}
		if overrride_quantity:
			self.cart[product_id]['quantiy']=quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()
  
	def save(self):
		self.session.modified = True
  
	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()
	def __iter__(self):
		product_ids= self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		for product in products:
			cart[str(product.id)]['product'] = product
		for item in cart.values():
			# item['price'] = locale.atoi(item['price'])
			item['price'] = Decimal(item['price'])
			# item['price'] = item['price']
			# item['total_price'] = item['price'] * item['quantity']
			item['total_price'] = item['price'] * 1
   
			yield item
	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())
	def get_total_price(self):
		# total=sum((item['price'] * item['quantity']) for item in self.cart.values())
		return sum(Decimal(item['price'] * 1) for item in self.cart.values())
		# return sum(int(item['price'] * item['quantity']) for item in self.cart.values())
		# return sum(locale.atoi(item['price'] * item['quantity']) for item in self.cart.values())
	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.save()