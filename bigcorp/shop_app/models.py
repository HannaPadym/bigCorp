import random
import string
from django.urls import reverse
from django.db import models
from django.utils.text import slugify


def rand_slug():
    """
    return slug for object
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


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

    # def get_absolute_url(self):
    #     return reverse('model_detail', kwargs={'pk': self.pk})


class Product(models.Model):
    """
    product unit description
    """
    category = models.ForeignKey(Category, related_name='Products', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=250)
    brand = models.CharField(verbose_name='Бренд', max_length=250)
    description = models.CharField(verbose_name='Описание', max_length=250)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField(verbose_name='Изображение', upload_to='products/products/%Y/%m/%d')
    slug = models.SlugField(verbose_name='URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now_add=True)
    available = models.BooleanField(verbose_name='Наличие', default=True)

    class Meta:
        unique_together = (['slug', ])
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('model_detail', kwargs={'pk': self.pk})


class ProductManager:
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(avaible=True)


class ProxyProduct:
    objects = ProductManager()

    class Meta:
        proxy = True
