import json

from django.test import TestCase, Client
from django.urls import reverse


class MeterTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_buzzmeter_page_doesnt_crash(self):
        response = self.client.get(reverse('buzzmeter'))
        self.assertEqual(response.status_code, 200)

    def test_sentment_meter_page_doesnt_crash(self):
        response = self.client.get(reverse('sentiment_meter'))
        self.assertEqual(response.status_code, 200)

    def test_buzzmeter_api(self):
        response = self.client.post(reverse('api-buzzmeter'),
                                    data='{"language": "en", "text": "achieve breakout cost-effective lu-lu-lu"}',
                                    content_type='application/json')

        resp_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        # hardcoding ...
        self.assertEqual({'score': 0.8176223275870086, 'buzz words': ['achieve', 'breakout', 'cost-effective']}, resp_data)

    def test_sentiment_meter_api(self):
        response = self.client.post(reverse('api-sentiment'),
                                    data='{"language": "en", "text": "Super awesome delight here!"}',
                                    content_type='application/json')

        resp_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        # hardcoding ...
        self.assertEqual({'neg': 0.0, 'neu': 0.076, 'pos': 0.924, 'compound': 0.9215}, resp_data)

