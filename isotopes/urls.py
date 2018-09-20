from django.conf.urls import url
from . import views

app_name = 'isotopes'

urlpatterns = [
    url(r'^iso/add_isotopes/', views.add_isotopes, name='add_isotopes'),
    url(r'^iso/(?P<pk>\d+)/$', views.IsotopeDetailView.as_view(), name='isotope-detail'),
    url(r'^iso/', views.IsotopeListView.as_view(), name='isotopes')
]

