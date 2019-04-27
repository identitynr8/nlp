from django.conf.urls import url

from .views import URLsBuzzifierView, Buzzifier, Redirector


buzzifier_urlpatterns = [
    url(r'^buzzifier/', URLsBuzzifierView.as_view(), name='urls_buzzifier'),

    url(r'^r/(?P<url>.*)$', Redirector.as_view(), name='redirector'),

    url(r'^api/buzzifier/', Buzzifier.as_view(), name='api-buzzifier'),
]
