from math import sin

from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer

from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from common.data import BUZZWORDS
from .serializers.serializers import InputTextSerializer


class BuzzMeterView(TemplateView):
    template_name = 'buzz_meter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'page_name': 'Buzzmeter'})

        return context


class SentimentMeterView(TemplateView):
    template_name = 'sentiment_meter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'page_name': 'Sentiment meter'})

        return context


class BuzzMeter(GenericAPIView):
    """
    Returns buzz score of a text.

    Buzz score is a number from 0 to 1.
    The higher the worse.
    """
    serializer_class = InputTextSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            text = serializer.validated_data['text']
            language = serializer.validated_data['language']

            text = text[:10000]
            text_lowercase = text.lower()

            text_tokens = RegexpTokenizer(r'\w+').tokenize(text_lowercase)

            if language == 'en':
                stops = stopwords.words('english')

            normalized_text_tokens = [t for t in text_tokens if t not in stops]
            normalized_text_length = len(normalized_text_tokens)

            count_buzzwords = 0
            buzzwords_in_text = []
            for bw in BUZZWORDS[language]:
                c = text_lowercase.count(bw)
                text_lowercase = text_lowercase.replace(bw, '#')
                count_buzzwords += c
                if c:
                    buzzwords_in_text.append(bw)

            if normalized_text_length > 0:
                ratio = count_buzzwords / normalized_text_length
            else:
                ratio = 0

            if ratio > 0:
                # https://www.desmos.com/calculator/mzvo5mx1vd
                score = 1.5 * sin(4 * ratio - 1.624) / 2 + 0.75
                score = min([score, 1])
                score = max([score, 0])
            else:
                score = 0

            return Response({'score': score, 'buzz words': buzzwords_in_text})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Sentiment(GenericAPIView):
    """
    Performs sentiment analysis of a text.

    Uses VADER lexicon https://github.com/cjhutto/vaderSentiment
    """
    serializer_class = InputTextSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            text = serializer.validated_data['text']
            language = serializer.validated_data['language']

            if language == 'en':
                sid = SentimentIntensityAnalyzer(lexicon_file=settings.NLTK_DATA + 'sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt')
                scores = sid.polarity_scores(text)

                return Response(scores)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
