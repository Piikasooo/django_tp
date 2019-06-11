from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.urls import reverse
from pytz import unicode
from transliterate import translit
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})

def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(unicode(instance.name), reversed=True))
        instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)

class PetititonManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(PetititonManager, self).get_queryset().filter(isGood=True)

PETITION_STATUS_CHOICES = (
    ('Збираємо підписи', 'Збираємо підписи'),
    ('Підписи зібрані', 'Підписи зібрані'),
    ('Підписи не зібрані', 'Підписи не зібрані')
)

class Petition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    info = models.TextField()
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=(timezone.now() + timedelta(days=14)))
    status = models.CharField(max_length=100, choices=PETITION_STATUS_CHOICES, default='Збираємо підписи')
    #objects = PetititonManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('petition_detail', kwargs={'petition_slug': self.slug})

def pre_save_petition_slug(sender, instance, *args, **kwargs):
    try:
        if not instance.slug:
            slug = slugify(translit(unicode(instance.title), reversed=True))
            instance.slug = slug
    except BaseException:
        instance.slug = instance.title

pre_save.connect(pre_save_petition_slug, sender=Petition)

class voted(models.Model):
    vote = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    voteFor = models.CharField(max_length=100)