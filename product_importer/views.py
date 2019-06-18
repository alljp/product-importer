import logging
import boto3
import json
import os
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from product_importer.models import Product
from product_importer.tasks import import_data


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
        file_url = request.POST.get('file_url')
        import_data(file_url)
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("product_importer:upload_csv"))




def sign_s3(request):
  # S3_BUCKET = os.environ.get('S3_BUCKET')
  S3_BUCKET = 'fulfilio-product-importer'
  file_name = request.GET.get('file_name')
  file_type = request.GET.get('file_type')

  s3 = boto3.client('s3', region_name='ap-south-1')
  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )
  return JsonResponse({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })