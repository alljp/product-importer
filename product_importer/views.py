import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "index.html", data)
    # if not GET, then proceed
    try:
        print("PEYE")
        csv_file = request.FILES["csv_file"]
        print (csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("product_importer:home"))
        handle_uploaded_file(csv_file)
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("product_importer:upload_csv"))


def handle_uploaded_file(f):
    for chunk in f.chunks():
        pass