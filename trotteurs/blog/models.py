from __future__ import unicode_literals

import datetime

from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Tag(models.Model):
    """
    """
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If the object is newly created, we set the slug
        if not self.id:
            self.slug = slugify(self.name)

        super(Tag, self).save(*args, **kwargs)

class Article(models.Model):
    """
        An article is composed of :
            * a title
            * a publication date
            * a text
            * a slug : to define the url of the article
            * [an image] : Corresponding to the main image
            * [a thumbnail] : Corresponding to the image in the result list
            * [a list of tags]
            * [an abstract]

    """
    title = models.CharField("Titre", max_length=200)
    date = models.DateField("Date de publication", default=datetime.date.today)
    image = models.ImageField(upload_to='media/images', blank=True)
    abstract = models.CharField("Résumé", max_length=1000, blank=True)
    text = RichTextUploadingField()
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If the object is newly created, we set the slug
        if not self.id:
            self.slug = slugify(self.title)

        super(Article, self).save(*args, **kwargs)
