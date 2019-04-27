import urllib

from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import URLpair
from .serializers.serializers import URLSerializer


class URLsBuzzifierView(TemplateView):
    template_name = 'urls_buzzifier.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'page_name': 'URLs buzzifier'})

        return context


class Redirector(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        try:
            urlpair = URLpair.objects.get(buzzified_key=urllib.parse.quote(kwargs['url'], safe='/+'))
        except URLpair.DoesNotExist as e:
            return None
        urlpair.redirects_count += 1
        urlpair.last_redirected_at = timezone.now()
        urlpair.save()
        return urlpair.original_url


class Buzzifier(GenericAPIView):
    """
    Returns buzzified url which redirects to the original one.
    """
    serializer_class = URLSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            url = serializer.validated_data['url']

            buzzified_url = reverse('redirector', kwargs={'url': urllib.parse.unquote(URLpair.buzzify(original_url=url).buzzified_key)})

            return Response({'buzzified_url': {True: 'https://', False: 'http://'}[request.is_secure()] + request.get_host() + buzzified_url})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
