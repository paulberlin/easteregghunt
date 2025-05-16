import uuid
import urllib.parse
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


BASE_URL = "https://easter.uber.space/egg/"

class User(AbstractUser):
  pass


class EggHunt(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)
  description = models.TextField(blank=True)

  @property
  def encoded_link(self):
    return urllib.parse.quote(BASE_URL+self.slug)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = uuid.uuid4().hex[:16]    # can vary up to 32 chars in length
    super(EggHunt, self).save(*args, **kwargs)

  def __str__(self):
    return self.name


class Egg(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)
  description = models.TextField(blank=True)
  egghunt = models.ForeignKey(EggHunt, on_delete=models.CASCADE, related_name='eggs')

  @property
  def encoded_link(self):
    return urllib.parse.quote(BASE_URL+self.egghunt.slug+"/"+self.slug)
  
  @property
  def how_often(self):
    return EggCompletion.objects.filter(egg__exact=self).count()

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = uuid.uuid4().hex[:16]    # can vary up to 32 chars in length
    super(Egg, self).save(*args, **kwargs)

  def __str__(self):
    return self.name



class EggCompletion(models.Model):
  person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  egg = models.ForeignKey(Egg, on_delete=models.CASCADE, related_name='completions')
  timestamp = models.DateTimeField(auto_now_add=True)

  # Metadata
  class Meta:
    unique_together = ('person', 'egg')


