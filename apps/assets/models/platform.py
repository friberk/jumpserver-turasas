from django.db import models
from django.utils.translation import gettext_lazy as _

from common.fields.model import JsonDictTextField

__all__ = ['Platform']


class Category(models.TextChoices):
    Host = 'host', _('Host')
    Network = 'network', _('Network device')
    Database = 'database', _('Database')
    RemoteApp = 'remote_app', _('Microsoft remote app')
    Cloud = 'cloud', _("Cloud")


class Platform(models.Model):
    CHARSET_CHOICES = (
        ('utf8', 'UTF-8'),
        ('gbk', 'GBK'),
    )
    BASE_CHOICES = (
        ('Linux', 'Linux'),
        ('Unix', 'Unix'),
        ('MacOS', 'MacOS'),
        ('BSD', 'BSD'),
        ('Windows', 'Windows'),
        ('Other', 'Other'),
    )
    name = models.SlugField(verbose_name=_("Name"), unique=True, allow_unicode=True)
    base = models.CharField(choices=BASE_CHOICES, max_length=16, default='Linux', verbose_name=_("Base"))
    charset = models.CharField(default='utf8', choices=CHARSET_CHOICES, max_length=8, verbose_name=_("Charset"))
    meta = JsonDictTextField(blank=True, null=True, verbose_name=_("Meta"))
    internal = models.BooleanField(default=False, verbose_name=_("Internal"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    @classmethod
    def default(cls):
        linux, created = cls.objects.get_or_create(
            defaults={'name': 'Linux'}, name='Linux'
        )
        return linux.id

    def is_windows(self):
        return self.base.lower() in ('windows',)

    def is_unixlike(self):
        return self.base.lower() in ("linux", "unix", "macos", "bsd")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Platform")
        # ordering = ('name',)
