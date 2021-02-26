from django.conf.urls import url
from .views import user, client, scan, exists

urlpatterns = [
    url(r'^user$', user),
    url(r'^client$', client),
    url(r'^scan$', scan),
    url(r'^exists/(?P<choice>[0-1]{1})$', exists)
]
