from django.db import models
from users_app.models import CustomUser, BasketModel


class OrderModel(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUS_CHOICES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    basket = models.JSONField(default=dict)
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=64, null=False, blank=False)
    address = models.CharField(max_length=256, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS_CHOICES)

    def __str__(self):
        return f'Заказ №{self.id} - {self.first_name}  {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.basket:
            basket_items = BasketModel.objects.filter(user=self.user)
            basket_history = {
                'product_items': [item.to_json() for item in basket_items],
                'totally': float(basket_items.totally())
            }
            self.basket = basket_history
            basket_items.delete()
        return super(OrderModel, self).save(*args, **kwargs)

    def actions_after_payment(self):
        self.status = self.PAID
        self.save()




