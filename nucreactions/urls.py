from django.conf.urls import url
from . import views

app_name = 'nucreations'

urlpatterns = [
    url(r'^reactions/add_reactions/', views.add_reactions, name='add_reactions'),
    url(r'^reactions/(?P<pk>\d+)/$', views.ReactionDetailView.as_view(), name='reaction-detail'),
    url(r'^reactions/', views.ReactionListView.as_view(), name='reactions')
]