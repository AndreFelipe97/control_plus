from django.db import models
from products.models import Product


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('debito', 'Cartão de Débito'),
        ('credito', 'Cartão de Crédito'),
        ('pix', 'Pix'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return f'Venda #{self.pk}'


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
