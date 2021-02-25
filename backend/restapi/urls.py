from django.conf.urls import url
from .views import user, scan

urlpatterns = [
    url(r'^user$', user),
    url(r'^scan$', scan)
]
