from django.shortcuts import render
from django.views.generic import ListView

from .models import CategoryModel, ProductsModel


def main_page(request):
    return render(request, 'index.html')


class ProductListView(ListView):
    model = ProductsModel
    template_name = 'product_app/products.html'
    context_object_name = 'product_objects'

    def get_queryset(self):
        queryset = ProductsModel.objects.all()
        category_slug = self.kwargs.get('category_slug')
        category_filtered = queryset.filter(category__slug=category_slug)
        return category_filtered if category_slug else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = CategoryModel.objects.all()
        return context
