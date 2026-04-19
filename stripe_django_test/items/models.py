from decimal import Decimal

from django.db import models




class Item(models.Model):
    CURRENCY_CHOICES = [
        ("usd", 'USD'),
        ("rub", 'RUB'),
    ]
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    currency = models.CharField(max_length=100, choices=CURRENCY_CHOICES, default="rub")


    class Meta:
        ordering = ['name']
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return self.name



class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"



class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = Decimal(0)
        for item in self.items.all():
            total += Decimal(str(item.price))

        if self.discount:
            percent = Decimal(str(self.discount.percent_off)) / 100
            total -= total * percent
        if self.tax:
            tax_percent = Decimal(str(self.tax.percent)) / 100
            total += total * tax_percent
        return total


    def get_currency(self):
        currencies =  self.items.values_list('currency', flat=True).distinct()
        if len(currencies) == 1:
            return currencies[0]
        else:
            raise ValueError("В заказе есть товары в разных валютах")





