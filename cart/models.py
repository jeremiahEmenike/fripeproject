from django.db import models
from onlineshop.models import Product


class OrderItem(models.Model):
    item=models.ManyToManyField(Product)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} de {self.item.name} "
    
    
class Paiements(models.Model):
    idd=models.BigAutoField(primary_key=True)
    numero = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    adresse = models.CharField(max_length=200)
    # items=models.OneToOneField(OrderItem,on_delete=models.CASCADE,default=1)
    items = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # ordering = ('idd',)
        verbose_name_plural = 'paiements'

    def __str__(self):
        # return str(self.idd)
        return str(self.numero)
    
    def get_num(self):
        return self.numero
    
    def get_paymentid(self):
        return self.idd

    
    def get_adr(self):
        return self.adresse
    
    def set_ord(self, ordered):
        self.ordered=ordered
        return self.ordered
    