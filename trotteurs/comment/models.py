from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), default=1)

    content_type = models.ForeignKey(ContentType, verbose_name=_('Type'), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(verbose_name=_('Content'))
    timestamp =  models.DateTimeField(verbose_name=_('Timestamp'), auto_now_add=True)
    parent = models.ForeignKey("self", verbose_name=_('Parent'), null=True, blank=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(sef):
        if self.parent is not None:
            return False
        return True

    def get_username(self):
        return self.user.username
    get_username.short_description = _('Username')
    content_object.short_description = _('Object')

    # def get_content_name(self):
    #     return self.content_object
