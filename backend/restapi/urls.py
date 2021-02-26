from django.conf.urls import url
from .views import user, client, scan

urlpatterns = [
    url(r'^user$', user),
    url(r'^client$', client),
    url(r'^scan$', scan)
]
