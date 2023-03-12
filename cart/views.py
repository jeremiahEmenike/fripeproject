from django.shortcuts import render,redirect, get_object_or_404
from .cart import Cart
from django.views.decorators.http import require_POST
from onlineshop.models import Product
from .models import Paiements,OrderItem
from .forms import CartAddProductForm
from django.views.generic import View
from .forms import PaymForm
import requests
from django.contrib import messages
from django.contrib.auth.models import User
import json
from django.utils import timezone



@require_POST
def cart_add(request, product_id): 
    cart= Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form =CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product = product, quantity = cd['quantity'], overrride_quantity = cd['override']) 
        order_item, created= OrderItem.objects.get_or_create(request, ordered=False)
        # order_item, created= OrderItem.objects.add(item=product, ordered=False)
        order_item.item.add(product)
        order_item.save()
        # order_qs=Paiements.objects.create(items=order_item,ordered=False)
        # paiements, created = Paiements.objects.get_or_create(items=order_item, ordered=False)
        paiements = Paiements.objects.filter(items=order_item).first()
        paiements.save()
        return redirect('cart:cart_detail')
        # if order_qs.exists():
        #     order=order_qs[0]
        #     if order.items.filter(item__slug=product.slug).exists():
        #         order_item.quantity=1
        #         order_item.save()
        #         messages.success(request, f"{product.name}'s quantity was updated ")
        #         return redirect('cart:cart_detail')
        #     else:
        #         order.items.add(order_item)
        #         # order.items.set([order_item])
        #         # order.items.add()
        #         order.save()
        #         messages.success(request, f"{product.name} was added to your cart")
        #         return redirect('cart:cart_detail')
        # else:
        #     ordered_date=timezone.now()
        #     order=Paiements.objects.create(request, ordered=False,ordered_date=ordered_date)
        #     order.items.add(order_item)
        #     # order.items.set([order_item])
            
        #     # order.items.add()
        #     order.save()
        #     messages.success(request, f"{product.name} was added to your cart")
        #     return redirect('cart:cart_detail')
        
	# return redirect('cart:cart_detail')
	
def cart_remove(request, product_id):
	cart= Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')

def cart_detail(request):
	cart= Cart(request)
	for item in cart:
		item['update_quantity_form']= CartAddProductForm(initial=
                                                        {'quantity':item['quantity'], 'override':True})
	return render(request, 'cart/detail.html', {'cart': cart})


import random

def generate_id():
    """Generate a unique ID of at least 4 digits"""
    with open("used_ids.txt", "r") as f:
        used_ids = set(f.read().split("\n"))

    while True:
        # Generate a random integer between 1000 and 9999
        new_id = random.randint(1000, 9999)
        if new_id not in used_ids:
            break

    with open("used_ids.txt", "a") as f:
        f.write(str(new_id) + "\n")

    yield new_id
class CheckoutView(View):
    def get(self, *args, **kwargs):
        cart= Cart(self.request)
        for item in cart:
            item['update_quantity_form']= CartAddProductForm(initial=
                                                        {'quantity':item['quantity'], 'override':True})
            return render(self.request, 'cart/checkout.html', {'cart': cart}) 

    
    def post(self, *args, **kwargs):
        authentication_classes = []
        form = PaymForm(self.request.POST or None)
        order_item= OrderItem.objects.filter( ordered=False)
        
        payment=Paiements.objects.filter(ordered=False, items__in=order_item)
        if form.is_valid():  
            numero = form.cleaned_data.get('numero')
            adresse = form.cleaned_data.get('adresse')
            payment=payment.first()
            id_generator = generate_id()
            payment.idd= next(id_generator)
            
            payment.numero = numero
            payment.adresse = adresse
            payment.save()
            # pay = Paiements(
            #         numero=numero,
            #     	adresse=adresse,
            #     )
            # orderItems = OrderItem(
            #         numero =numero,	
            #     )
            
            # orderItems.save()
            
                
            return redirect('cart:confirmation')

        else:
            print('form is invalid')
            return redirect('cart:checkout')
        
def confirmation(request):
    
    cart= Cart(request)
    for item in cart:
            item['update_quantity_form']= CartAddProductForm(initial=
                                                        {'quantity':item['quantity'], 'override':True})
   
    paymentidd=Paiements.objects.latest('idd').get_paymentid()
    
    numero =Paiements.objects.last()
    context = {
                'cart': cart,
                'paymentidd':paymentidd,
                'numero':numero
            }
    return render(request,'cart/confirmation.html',context)
        
def status(status):
    types={'0': 'Paiement réussi avec succès', '2' : 'En cours', '4': 'Expiré', '6': 'Annulé'}
    return types[str(status)]
    

def paysuccess(request):
    url ='https://paygateglobal.com/api/v2/status'
    
    identifier=Paiements.objects.latest('idd').get_paymentid()  
    params = dict(
					auth_token='593bd3ea-c9ae-4bc3-bb7b-d92cfaba604b',
					identifier= identifier,
				)
    res = requests.post(url,params=params)
    ct =res.json()
    st=status(ct['status'])
    if st=='Paiement réussi avec succès':
        print(st)
        numero =Paiements.objects.last()
        numero.ordered=True
        numero.save() 
        return render(request,'cart/paysucess.html')
    elif st=='En cours':
         print(st)
         messages.info(request, " veuillez valider sur votre téléphone portable")
         return redirect('cart:checkout')
    elif st=='Expiré':
         print(st)
         messages.info(request, " Etat de votre paiement: Expiré; veuillez recommencer")
         return redirect('cart:checkout')
    elif st=='Annulé':
         print(st)
         messages.info(request, "Vous avez annulé votre commande")
         return redirect('cart:checkout')
    else:
        return redirect('index')