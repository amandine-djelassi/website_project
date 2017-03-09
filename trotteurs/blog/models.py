from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
    """
    """
    tag_title = models.CharField("Titre", max_length=200)

    def __str__(self):
        return self.tag_title

class Article(models.Model):
    """
        An article is composed of :
            * a title
            * a publication date
            * a text
            * [an image]
            * [a list of tags]
            * [an abstract]

    """
    title = models.CharField("Titre", max_length=200)
    date = models.DateTimeField("Date de publication")
    image = models.ImageField(upload_to='media/images', blank=True)
    abstract = models.CharField("Résumé", max_length=1000, blank=True)
    text = models.TextField("Corps de l'article")
    # tags = models.ManyToManyFiled("Tag", Tag, blank=True)

    def __str__(self):
        return self.title
