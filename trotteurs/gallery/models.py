from django.db import models
import datetime
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile


class Country(models.Model):
    """
    """
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200
    )

    slug = models.SlugField(
        blank=True,
        unique=True
    )

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
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200
    )

    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        on_delete=models.CASCADE
    )

    latitude = models.DecimalField(
        verbose_name=_('Latitude'),
        decimal_places=10,
        max_digits=15
    )

    longitude = models.DecimalField(
        verbose_name=_('Longitude'),
        decimal_places=10,
        max_digits=15
    )

    slug = models.SlugField(blank=True, unique=True)

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
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=200
    )

    image = models.ImageField(
        upload_to='media/images',
        verbose_name=_('Cover image'),
        help_text=_('Size: width: 346px, height: 220px')
    )

    description = models.CharField(
        verbose_name=_('Description'),
        max_length=50,
        blank=True
    )

    city = models.ManyToManyField(
        City,
        verbose_name=_('City')
    )

    slug = models.SlugField(blank=True, unique=True)

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

    def get_cities(self):
        return [city.name for city in self.city.all()]
    get_cities.short_description = _('Cities')

def has_changed(instance, field, manager='objects'):
    """Returns true if a field has changed in a model

    May be used in a model.save() method.

    """
    if not instance.pk:
        return True
    manager = getattr(instance.__class__, manager)
    old = getattr(manager.get(pk=instance.pk), field)
    return not getattr(instance, field) == old

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
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=200
    )

    date = models.DateField(
        verbose_name=_('Publication date'),
        default=datetime.date.today
    )

    image = models.ImageField(
        upload_to='media/images',
        verbose_name=_('Image')
    )

    thumbnail = models.ImageField(
        upload_to='media/images/thumbs/',
        verbose_name=_('Thumbnail'),
        blank=True
    )

    legend = models.CharField(
        verbose_name=_('Legend'),
        max_length=1000,
        blank=True
    )

    album = models.ManyToManyField(
        Album,
        verbose_name=_('Album')
    )

    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __str__(self):
        """
            Return the string version of the object
        """
        return self.title

    def get_albums(self):
        return [album.title for album in self.album.all()]
    get_albums.short_description = _('Albums')

    def image_tag(self):
        return u'<img style="width: 200px; height: 150px;"src="%s" />' % self.image.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        """
            Create a slug when saved
            Create a thumbnail if the image is modificated
        """

        # If the object is newly created, we set the slug
        if not self.id:
            self.slug = slugify(self.title)

        # If the image has been change, create the thumbnail
        if has_changed(self, 'image'):
            size = 445, 800

            full_image = Image.open(self.image)
            full_image.thumbnail(size, Image.ANTIALIAS)

            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()

            thumb_filename = thumb_name + '_thumb' + thumb_extension

            if thumb_extension == '.gif':
                FTYPE = 'GIF'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                FTYPE = 'JPEG'

            # Save thumbnail to in-memory file as StringIO
            temp_thumb = BytesIO()
            full_image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            # set save=False, otherwise it will run in an infinite loop
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

        super(Photo, self).save(*args, **kwargs)
