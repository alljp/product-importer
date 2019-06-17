from django.conf.urls import url
from product_importer import views
 
app_name = 'product_importer'
urlpatterns = [
    # url(r'^$', views.HomePageView.as_view()),
    url(r'^$', views.upload_csv, name='upload_csv'),
    url(r'products', views.ProductsView.as_view())
]