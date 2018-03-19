from django.db import models


# Create your models here.
class ActiveCategoryManager(models.Manager):
    """ Manager class to return only those categories where each instance is active """
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class Category(models.Model):    # sup  broski explain this class

    """ model class containing information about a category in the product catalog """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveCategoryManager()

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {'category_slug': self.slug})


class ActiveProductManager(models.Manager):
    """ Manager class to return only those products where each instance is active """

    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    """ Manager class to return only those products where each instance is featured """

    def get_query_set(self):
        return super(FeaturedProductManager, self).get_query_set().filter(is_active=True).filter(is_featured=True)


class Product(models.Model):
    """ model class containing information about a product; instances of this class are what the user
    adds to their shopping cart and can subsequently purchase

    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2,
                                    blank=True, default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords", max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    # image fields, added in Chapter 7
    # image fields require a varchar(100) in db
    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=200, default=False)


    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product', (), {'product_slug': self.slug})

    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
