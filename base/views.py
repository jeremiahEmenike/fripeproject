from django.shortcuts import render,get_object_or_404, redirect
from onlineshop.models import Product
import random


# Create your views here.
def index(request):
    # items=Item.objects.filter(category='H')[:5]
    # items=Item.objects.all()[:10]
    # items=Item.objects.random.choice(items)
    items=Product.objects.all()

    ma_liste=list()
    for i in range(4):
        randnum=random.choice(items)
        
        if randnum not in ma_liste:
            ma_liste.append(randnum)

    # items=Item.objects.all()
    context={
        'items':items,
        'ma_liste':ma_liste
        # 'randnum':randnum

    }
    return render(request, 'base/index.html',context)

def hauts(request):
    # items=Item.objects.filter(category='H')[:5]
    # items=Item.objects.all()[:10]
    # items=Item.objects.random.choice(items)
    items=Product.objects.all()

    ma_liste=list()
    for i in range(4):
        randnum=random.choice(items)
        
        if randnum not in ma_liste:
            ma_liste.append(randnum)

    # items=Item.objects.all()
    context={
        'items':items,
        'ma_liste':ma_liste
        # 'randnum':randnum

    }
    return render(request, 'base/hauts.html',context)

def jupes(request):
    # items=Item.objects.filter(category='H')[:5]
    # items=Item.objects.all()[:10]
    # items=Item.objects.random.choice(items)
    items=Product.objects.all()

    ma_liste=list()
    for i in range(4):
        randnum=random.choice(items)
        
        if randnum not in ma_liste:
            ma_liste.append(randnum)

    # items=Item.objects.all()
    context={
        'items':items,
        'ma_liste':ma_liste
        # 'randnum':randnum

    }
    return render(request, 'base/jupes.html',context)

def pantalons(request):
    # items=Item.objects.filter(category='H')[:5]
    # items=Item.objects.all()[:10]
    # items=Item.objects.random.choice(items)
    items=Product.objects.all()

    ma_liste=list()
    for i in range(4):
        randnum=random.choice(items)
        
        if randnum not in ma_liste:
            ma_liste.append(randnum)

    # items=Item.objects.all()
    context={
        'items':items,
        'ma_liste':ma_liste
        # 'randnum':randnum

    }
    return render(request, 'base/pantalons.html',context)

def robes(request):
    # items=Item.objects.filter(category='H')[:5]
    # items=Item.objects.all()[:10]
    # items=Item.objects.random.choice(items)
    items=Product.objects.all()

    ma_liste=list()
    for i in range(4):
        randnum=random.choice(items)
        
        if randnum not in ma_liste:
            ma_liste.append(randnum)

    # items=Item.objects.all()
    context={
        'items':items,
        'ma_liste':ma_liste
        # 'randnum':randnum

    }
    return render(request, 'base/robes.html',context)


def contact(request):
    return render(request, 'base/contact.html')