import random
import string

from django.db import models
from django.utils.text import slugify


def rand_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits, 3))


# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=250, db_index=True)
    parent = models.ForeignKey(verbose_name='Родительская категория', to='self', on_delete=models.CASCADE,
                               related_name='children', blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + 'pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)
