from __future__ import unicode_literals
import datetime
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class Tag(models.Model):
    """
        A Tag is composed of :
            * a name
            * a slug
    """
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200
    )

    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

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
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=200
    )

    date = models.DateField(
        verbose_name=_('Date'),
        default=datetime.date.today
    )

    image = models.ImageField(
        upload_to='media/images',
        verbose_name=_('Image'),
        help_text=_('Size: height:300px, width:900px'),
        blank=True)

    abstract = models.CharField(
        verbose_name=_('Abstract'),
        max_length=1000,
        blank=True
    )

    text = RichTextUploadingField()

    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        blank=True
    )

    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

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
        super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
    article = models.ForeignKey('Article', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, related_name='replies')

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
