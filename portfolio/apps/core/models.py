from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Project(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='portfolio/projects/', blank=True)
    github_url = models.URLField(max_length=200)
    view_url = models.URLField(max_length=200)
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='projects')
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
