import urllib as ul

from django import db
from django.db import models

from common.data import BUZZWORDS


class URLpair(models.Model):
    original_url = models.URLField()
    buzzified_key = models.CharField(max_length=2000, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_redirected_at = models.DateTimeField(null=True)
    redirects_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'URL pair'
        verbose_name_plural = 'URL pair'

    def __str__(self):
        return '{0} / {1}'.format(self.original_url, self.buzzified_key)

    @classmethod
    def buzzify(cls, original_url: str):
        """
        Returns url pair object for the given original URL

        The algo here is deterministic, stateless and utilizes all buzzwords with equal probability.
        With buzzwords list of decent length (say more than 100 elements), number of DB queries is ok-ish for
        low-throughput service.
        """
        url = original_url
        buzzwords_to_use = []
        while True:
            # check if original URL is already been buzzified
            pair = cls.objects.filter(original_url=original_url).first()
            if pair is not None:
                return pair

            # add one more quoted buzzword to a list of buzzwords to use in url
            buzzword_ix = hash(url) % len(BUZZWORDS['en'])
            buzzwords_to_use.append(ul.parse.quote(BUZZWORDS['en'][buzzword_ix]))

            # construct buzzified key
            buzzified_key = '+'.join(buzzwords_to_use)

            try:
                # check if buzzified_key exists in DB
                cls.objects.get(buzzified_key=buzzified_key)
            except cls.DoesNotExist as e:

                # buzzified_key doesn't exist in DB yet. We can pair it with original_url
                pair = cls(original_url=original_url, buzzified_key=buzzified_key)
                try:
                    pair.save()
                    return pair
                except db.IntegrityError as e:
                    # Catched race condition. Just run the while loop one more time.
                    pass

            url += '_'
