from django.conf.urls import url
from . import views

app_name = 'nucreations'

urlpatterns = [
    url(r'^reactions/addreactions/', views.addreactions, name = 'addreactions'),
    url(r'^reactions/(?P<pk>\d+)/$', views.ReactionDetailView.as_view(), name = 'reaction-detail'),
    url(r'^reactions/', views.ReactionListView.as_view(), name = 'reactions')
]