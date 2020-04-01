from django.db import models
import tldextract
# Create your models here.


class URLModel(models.Model):
    url = models.URLField(max_length=200)

    def __str__(self):
        url = self.url
        info = tldextract.extract(url)
        return str(info.domain)


class WordModel(models.Model):
    url = models.ForeignKey(
        URLModel, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=50)
    count = models.IntegerField()

    def __str__(self):
        return self.word
