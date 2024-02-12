from django.db import models
from django.conf import settings
from pytils.translit import slugify
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CategoryModel(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(null=False, blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.name)
        super().save()


class ProductsModel(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    stripe_price_id = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f'Товар {self.name}'

    def create_stripe_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price*100),
            currency='rub'
        )
        return stripe_product_price['id']

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.stripe_price_id:
            stripe_product_price_id = self.create_stripe_price()
            self.stripe_price_id = stripe_product_price_id
        super(ProductsModel, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

