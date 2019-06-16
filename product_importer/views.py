from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from product_importer.models import Product


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)



class ProductsView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.all()