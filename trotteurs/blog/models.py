from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
    """
    """
    tag_titlle = models.CharField("Titre", max_length=200)

    def __str__(self):
        return self.tag_title

class Article(models.Model):
    """
        An article is composed of : 
            * a title 
            * an image (facultative)
            * a list of tags (facultative)
            * a publication date 
            * an abstract (facultative)
            * a text
    """
    title = models.CharField("Titre", max_length=200)
    # image 
    # tags = models.ManyToManyFiled("Tag", Tag, blank=True)
    pub_date = models.DateTimeField("Date de publication")
    abstract = models.CharField("Résumé", max_length=200)
    text = models.TextField("Corps de l'article")

    def __str__(self):
        return self.title
