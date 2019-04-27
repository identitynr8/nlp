import json

from django.core.validators import URLValidator
from django.test import TestCase, Client
from django.urls import reverse

from .models import URLpair


class BuzzifierTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_buzzifier_page_doesnt_crash(self):
        response = self.client.get(reverse('urls_buzzifier'))
        self.assertEqual(response.status_code, 200)

    def test_buzzifying_api(self):
        original_url = 'http://sdfsf.sfsf.sdff.wr'
        response = self.client.post(reverse('api-buzzifier'),
                                    data='{"url": "' + original_url + '"}',
                                    content_type='application/json',
                                    SERVER_NAME='gg.gg')

        resp_data = json.loads(response.content)

        self.assertIn('buzzified_url', resp_data)
        URLValidator()(resp_data['buzzified_url'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(URLpair.objects.filter(original_url=original_url,
                                               buzzified_key=resp_data['buzzified_url'].split('/')[-1]).exists())

    def test_redirecting(self):
        original_url = 'http://sdfsf.sfsf.sdff.wr'
        response = self.client.post(reverse('api-buzzifier'),
                                    data='{"url": "' + original_url + '"}',
                                    content_type='application/json')

        resp_data = json.loads(response.content)

        # check that redirect works
        response = self.client.get(resp_data['buzzified_url'])

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], original_url)
        self.assertEqual(URLpair.objects.get(original_url=original_url,
                                             last_redirected_at__isnull=False).redirects_count, 1)
