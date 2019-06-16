from django.conf.urls import url
from product_importer import views
 
urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]