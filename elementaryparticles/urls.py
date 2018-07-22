from django.conf.urls import url
from . import views

app_name = 'elementaryparticles'

urlpatterns =[
    url(r'^elementary_particles/(?P<pk>\d+)/$', views.ElementaryParticleDetailView.as_view(),
        name='elementary-particle-detail'),
    url(r'^elementary_particles/', views.ElementaryParticleListView.as_view(), name='elementary_particles')
]

