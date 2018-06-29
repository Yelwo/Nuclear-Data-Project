from django.conf.urls import url
from . import views

app_name = 'radiations'

urlpatterns = [
    url(r'^radiations/', views.RadiationListView.as_view(), name = 'radiations'),
    url(r'^radiations/(?P<pk>\d+)/$', views.RadiationDetailView.as_view(), name = 'radiation-detail')
]