from django.db import models
import datetime
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    """
    """
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

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
        super(Country, self).save(*args, **kwargs)

class City(models.Model):
    """
    """
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.DecimalField(blank=True, decimal_places=5, max_digits=10)
    longitude = models.DecimalField(blank=True, decimal_places=5, max_digits=10)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

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
        super(City, self).save(*args, **kwargs)

class Album(models.Model):
    """
        An album is composed of :
            * a name
            * a slug
    """
    title = models.CharField("Nom", max_length=200)
    image = models.ImageField(upload_to='media/images')
    description = models.CharField("Description", max_length=1000, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    city = models.ManyToManyField(City)

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

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

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

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
