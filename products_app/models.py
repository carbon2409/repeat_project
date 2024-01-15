from django.db import models
from pytils.translit import slugify


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

    def __str__(self):
        return f'Товар {self.name}'
