from django.db import models
import datetime
from django.template.defaultfilters import slugify

class Album(models.Model):
    """
        An album is composed of :
            * a name
            * a slug
    """
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        """
            Return the string version of the object
        """
        return self.name

    def save(self, *args, **kwargs):
        """
            Create a slug when saved
        """
        # If the object is newly created, we set the slug
        if not self.id:
            self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

class Photo(models.Model):
    """
        An photo is composed of :
            * an image
            * a title
            * a date
            * [a legend]
            * a slug : to define the url
            * an album

    """
    title = models.CharField("Titre", max_length=200)
    date = models.DateField("Date de publication", default=datetime.date.today)
    image = models.ImageField(upload_to='media/images')
    legend = models.CharField("Légende", max_length=1000, blank=True)
    album = models.ManyToManyField(Album)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        """
            Return the string version of the object
        """
        return self.title

    def save(self, *args, **kwargs):
        """
            Create a slug when saved
        """
        # If the object is newly created, we set the slug
        if not self.id:
            self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)
