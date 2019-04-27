from django.conf.urls import url

from .views import BuzzMeterView, SentimentMeterView, Sentiment, BuzzMeter


meter_urlpatterns = [
    url(r'^$', BuzzMeterView.as_view(), name='buzzmeter'),
    url(r'^sentiment/', SentimentMeterView.as_view(), name='sentiment_meter'),

    url(r'^api/sentiment/', Sentiment.as_view(), name='api-sentiment'),
    url(r'^api/buzzmeter/', BuzzMeter.as_view(), name='api-buzzmeter'),
]
