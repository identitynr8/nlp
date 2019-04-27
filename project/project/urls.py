from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

from buzzifier.urls import buzzifier_urlpatterns
from meter.urls import meter_urlpatterns


schema_view = get_swagger_view(title='API documentation')

urlpatterns = [
    url(r'^', include(meter_urlpatterns)),
    url(r'^', include(buzzifier_urlpatterns)),
    url(r'^docs/$', schema_view),
]
