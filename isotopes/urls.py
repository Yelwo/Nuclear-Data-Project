from django.conf.urls import url
from . import views

app_name = 'isotopes'

urlpatterns = [
    url(r'^isotopes/addisotopes/', views.addisotopes, name= 'addisotopes'),
    url(r'^isotopes/(?P<pk>\d+)/$', views.IsotopeDetailView.as_view(), name = 'isotope-detail'),
    url(r'^isotopes/', views.IsotopeListView.as_view(), name= 'isotopes')
]

